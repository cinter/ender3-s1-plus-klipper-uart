"""Install the selected Cura machine without overwriting user configuration."""
from pathlib import Path
import argparse
import configparser
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EXTERNAL = {
    "empty_quality_changes", "empty_intent", "base_global_standard",
    "empty_material", "empty_variant", "creality_ender3s1plus",
    "base_0.4_PLA_standard", "generic_pla_175", "creality_ender3s1plus_0.4",
    "creality_base_extruder_0",
}


def validate(resources=None):
    manifest = json.loads((HERE / "export-manifest.json").read_text(encoding="utf-8"))
    parsed = {}
    import hashlib
    for name, info in manifest["files"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe package path")
        source = HERE / "machine" / relative
        if hashlib.sha256(source.read_bytes()).hexdigest() != info["published_sha256"]:
            raise ValueError("Package checksum mismatch: " + name)
        config = configparser.ConfigParser(interpolation=None)
        config.read(source, encoding="utf-8")
        if config["metadata"]["setting_version"] != "27":
            raise ValueError("Unexpected Cura setting version: " + name)
        container_id = relative.name.split(".", 1)[0]
        if container_id in parsed:
            raise ValueError("Duplicate container ID")
        parsed[container_id] = config
    if len(parsed) != 6:
        raise ValueError("Expected exactly six native machine files")
    for container in parsed.values():
        for reference in container["containers"].values() if container.has_section("containers") else []:
            if reference not in parsed and reference not in EXTERNAL:
                raise ValueError("Unresolved container: " + reference)
        for key in ("machine", "extruder"):
            reference = container["metadata"].get(key)
            if reference and reference not in parsed:
                raise ValueError("Unresolved parent: " + reference)
    if resources:
        if not resources.is_dir():
            raise ValueError("Cura resources folder does not exist")
        # Preserve dots in container IDs (e.g. nozzle size 0.4).
        available = set()
        for path in resources.rglob("*"):
            for suffix in (".def.json", ".inst.cfg", ".xml.fdm_material"):
                if path.name.endswith(suffix):
                    available.add(path.name[:-len(suffix)])
        # These empty containers are supplied by Cura at runtime, not files.
        builtin_empty = {"empty_quality_changes", "empty_intent", "empty_material", "empty_variant"}
        missing = EXTERNAL - available - builtin_empty
        if missing:
            raise ValueError("Missing bundled Cura resources: " + ", ".join(sorted(missing)))
    return list(manifest["files"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", required=True, type=Path,
                        help="Existing Cura 5.13 configuration folder (Help > Show Configuration Folder)")
    parser.add_argument("--resources-dir", type=Path, help="Optional Cura share/cura/resources dependency check")
    parser.add_argument("--install", action="store_true", help="Write new files; default is dry run")
    args = parser.parse_args()
    try:
        names = validate(args.resources_dir)
        target = args.config_dir.expanduser().resolve()
        if not target.is_dir():
            raise ValueError("Configuration folder does not exist: " + str(target))
        collisions = [name for name in names if (target / name).exists()]
        if collisions:
            raise ValueError("Refusing to overwrite existing files:\n" + "\n".join(collisions))
        if args.install and sys.platform == "win32":
            tasks = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq UltiMaker-Cura.exe", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, check=True,
            ).stdout.lower()
            if "ultimaker-cura.exe" in tasks:
                raise ValueError("Close Cura before installing.")
        # Close Cura on all platforms. Never edit its global cura.cfg or activate a printer.
        for name in names:
            print(("INSTALL " if args.install else "DRY RUN ") + name)
            if args.install:
                destination = target / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("xb") as stream:
                    stream.write((HERE / "machine" / name).read_bytes())
        print("Installed. Reopen Cura and select Ender 3 S1 Plus - Klipper."
              if args.install else "Validated six files; no configuration was changed. Add --install to write.")
    except (OSError, ValueError, KeyError, configparser.Error, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
