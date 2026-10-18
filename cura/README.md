# Cura 5.13: Ender 3 S1 Plus - Klipper

This is the custom machine selected in the owner's Cura **5.13.0** installation, exported from its six native machine containers on 18 October 2026. It inherits Cura's bundled S1 Plus definition and standard quality presets; it is a machine configuration, not a complete collection of material/quality profiles.

## Files and provenance

- [machine/](machine/) contains the six readable native configuration files, in Cura's folder layout.
- [s1plus-klipper-cura-5.13.zip](s1plus-klipper-cura-5.13.zip) contains exactly those six files.
- [install_machine.py](install_machine.py) validates the containers and installs only new files, with dry-run as the default.
- [start.gcode](start.gcode) and [end.gcode](end.gcode) are readable copies of the machine's embedded sequences.
- [export-manifest.json](export-manifest.json) records source/published hashes and portability changes.

The custom **eSUN PLA PRO Black** material reference was replaced with bundled **generic 1.75 mm PLA** so the export does not depend on a personal material file. Machine group metadata was normalised; the export has no online connection or post-processing scripts. Choose your own material temperatures, flow and quality settings after installing.

## Installation

Close Cura first. Use **Help → Show Configuration Folder** to locate the correct version's user folder. On Windows this is normally %APPDATA%/cura/5.13. Back up that folder before making changes.

Download/clone this repository or extract its GitHub source ZIP. Run the installer from the repository root:

~~~powershell
python cura/install_machine.py --config-dir "$env:APPDATA\cura\5.13"
~~~

That is a **dry run**. It must report valid containers and six new destinations. To write them:

~~~powershell
python cura/install_machine.py --config-dir "$env:APPDATA\cura\5.13" --install
~~~

The installer refuses to overwrite any of its six destination filenames. If you already have a machine with these IDs, use a separate Cura configuration environment or resolve the conflict manually after backing up; do not blindly replace an existing machine. It does not edit the global cura.cfg, activate the machine or configure a printer connection.

Alternatively, extract the ZIP into the version's configuration folder, merging its four folders only if none of the six files already exists. This ZIP is not a .curaprofile quality profile; Cura's ordinary profile-import dialog is not the installation route.

Reopen Cura and select **Ender 3 S1 Plus - Klipper** from its printer menu. Review Machine Settings and material/quality settings before slicing. The package was validated by parsing, dependency checks and a temporary-folder installation test; a fresh GUI import on another computer has not been tested.

For optional dependency validation against a local Cura installation, append:

~~~powershell
--resources-dir "C:\Program Files\UltiMaker Cura 5.13.0\share\cura\resources"
~~~

Other Cura versions may migrate these files differently. This export uses setting_version **27** and is supplied for 5.13, not promised compatible with every release.

## Machine settings

| Setting | Value |
|---|---|
| Width / depth / height | 300 / 300 / 300 mm |
| Origin at centre | Off |
| Heated bed | On |
| G-code flavour | Marlin, stored as RepRap (Marlin/Sprinter) |
| Extrusion mode | Absolute; relative_extrusion=False |
| Firmware retraction | Off |
| Extruders / nozzle / filament | One / 0.4 mm / 1.75 mm |
| Cura acceleration / jerk control | Off |
| Machine acceleration estimate / X / Y | 500 / 500 / 500 mm/s² |
| Start / end | Included start sequence / END_PRINT |

The nominal print volume differs from Klipper's extra travel/homing allowance. Keep Cura at the nominal volume.

The quality/material containers remain inherited. **No explicit speed_print or speed_travel override is present in this export.** An earlier 80 mm/s print and 150 mm/s travel setup option can be entered manually in Custom settings, but is not baked into these files. Wall/first-layer/material speeds can still differ.

Disable coasting or competing pressure-control features when using Klipper pressure advance, following [Klipper's slicer guidance](https://www.klipper3d.org/Slicers.html). Those compatibility settings are not all explicit overrides in this native machine; inspect your selected quality profile. Keep the slicer's acceleration/jerk controls off unless intentionally changing how limits are managed.

## Start G-code

The embedded [start sequence](start.gcode):

1. Resets speed and flow factors to 100%, uses absolute motion/extrusion, and switches the part fan off.
2. Clears the active mesh, starts bed heating and holds the nozzle at 150°C while the bed settles.
3. Waits for the bed, homes, then loads the owner's saved **pla_60** mesh.
4. Moves clear, heats to the selected first-layer nozzle temperature, and purges along X30 from Y30 to Y180 at Z0.28.
5. Resets E and lifts before the sliced toolpath.

You must create your own valid pla_60 profile or change the load command. The name does not dynamically select a mesh based on the material; this baseline assumes the appropriate settled PLA bed. Check purge coordinates and quantities against your machine and material.

Start code does not set pressure advance, shaping or motion limits. They come from Klipper's saved configuration and current runtime state. It intentionally clears any previous M220/M221 multiplier.

## End G-code and macros

The end field is **END_PRINT**, defined in the supplied [printer.cfg](../config/klipper/printer.cfg). That macro waits, retracts if hot, stops heaters/fan, lifts within available Z clearance, parks X0 Y300 when homed, and disables motors. Without that macro the end command will not work.

Other supplied helpers are **BEDTIME_MODE** and **UNLOAD_FILAMENT**; see [configuration notes](../config/klipper/README.md). Select an appropriate unloading temperature and distance for your filament.

## Sending a print

Slice, inspect Preview and inspect the generated start/end G-code. Save the G-code and upload it through Mainsail. A Moonraker Cura integration can be configured separately with your own address/authentication; no connection credentials are exported.

These files do not include model projects, support choices, a complete TPU profile or a universal flow/temperature calibration. See [commissioning](../docs/setup/commissioning.md) and [limits/tuning](../docs/limits-and-tuning.md).

For native container concepts, see [Cura's machine-profile documentation](https://github.com/Ultimaker/Cura/wiki/Adding-new-machine-profiles-to-Cura).
