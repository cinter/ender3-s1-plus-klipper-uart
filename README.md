# Ender 3 S1 Plus: stock printer to Klipper + Mainsail

The complete build log and reproducible configuration for a **Creality Ender 3 S1 Plus**, **Raspberry Pi 3B**, Klipper and Mainsail: initial setup, commissioning, tuning, a custom Cura machine, and UART communication through the stock DACAI display cable.

**Current state — 18 October 2026:** printing over the display-cable UART has been flawless in the owner's subsequent use, including **two reported successful prints**. The Pi currently takes power through that cable too, but webcam load exposed undervoltage. An internal buck converter is ordered to finish the power arrangement. A replacement Pi TFT43 touchscreen and printed enclosure are planned.

This documents one working machine and its remaining work. Calibration and power observations are labelled separately from finished, repeatable steps.

## Follow the build

| Stage | Guide | Files |
|---|---|---|
| Stock / previous Marlin setup | [Migration and what to preserve](docs/setup/marlin-migration.md) | Your own board identification and rollback firmware |
| Pi, MainsailOS, Moonraker and Klipper | [Host installation and first connection](docs/setup/pi-and-mainsail.md) | [Pi configuration](config/pi/README.md), [firmware](firmware/README.md) |
| Configure and commission the printer | [Sensors, homing, probe, mesh and first layer](docs/setup/commissioning.md) | [Exact working Klipper files](config/klipper/README.md) |
| Set limits and tune printing | [Saved limits, runtime overrides, PA and shaping](docs/limits-and-tuning.md) | [Machine-readable limits](config/klipper/observed-limits.json) |
| Set up Cura | [Custom machine installation and start/end G-code](cura/README.md) | [Native machine ZIP](cura/s1plus-klipper-cura-5.13.zip), [installer](cura/install_machine.py) |
| Replace USB with display-cable UART | [Wiring, Pi UART, build, SD flash and serial test](docs/uart.md) | [Connector photos](docs/hardware.md), [firmware/source/hashes](firmware/README.md) |
| Finish the single-cable build | [Architecture and current versus planned state](docs/single-cable.md) | [Power measurements and design](docs/power.md), [printed parts](models/README.md) |
| Diagnose problems | [USB/UART troubleshooting](docs/troubleshooting.md) | [Measured evidence](docs/diagnostics.md) |

## Hardware and software

- Ender 3 S1 Plus with its stock **STM32F401** mainboard and original DACAI display cable.
- Raspberry Pi 3 Model B Rev 1.2; observed host is 64-bit MainsailOS / Debian 13 Trixie.
- Klipper **v0.13.0-800-g9cb99754c**, Mainsail and Moonraker. [Exact source and build settings](firmware/README.md) accompany the MCU binaries.
- Cura **5.13.0**, with a separate **Ender 3 S1 Plus - Klipper** custom machine based on Cura's bundled S1 Plus definition.
- Optional Crowsnest USB camera, identifying as NexiGo N60 FHD, and OctoEverywhere for remote access.
- Previously used Thomas Toka Marlin. Its configuration informed parts of the migration; using it first is optional.

Check the physical MCU marking before flashing. The supplied firmware is **F401, 64 KiB bootloader, 8 MHz clock reference**; the printer name alone is insufficient.

## The working printer configuration

[config/klipper/printer.cfg](config/klipper/printer.cfg), [bedtime.cfg](config/klipper/bedtime.cfg) and [filament.cfg](config/klipper/filament.cfg) are exact working copies, verified against the Pi by SHA256. They include the saved calibration block, END_PRINT, bedtime mode and the filament helper. The Mainsail installation supplies the external mainsail.cfg include.

| Setting | Saved baseline |
|---|---|
| XY velocity / acceleration | 300 mm/s / 500 mm/s² |
| Square corner velocity | 5 mm/s, default |
| Z velocity / acceleration | 10 mm/s / 100 mm/s² |
| Pressure advance | 0.0875 |
| Input shaping | MZV: X33.3 Hz, Y36.4 Hz; printed-tower estimates |
| Nominal Cura build volume | 300 × 300 × 300 mm |
| Mesh | 4×4, owner's pla_60 profile |
| Probe X/Y / saved Z offset | -48 / 0 mm; Z2.825 mm, owner-specific |

A later print was running at **800 mm/s² acceleration and 10 mm/s corner velocity**. Those are temporary runtime values, not the saved defaults. See [limits and tuning](docs/limits-and-tuning.md) for full travel/extrusion/temperature limits and calibration status.

Verify probe geometry, travel, sensors and heaters; calibrate your own Z offset, mesh and extrusion before using these files on another machine. PID was imported from Marlin, and shaping was estimated from a print rather than an accelerometer.

## Cura machine and slicing

The [Cura folder](cura/README.md) includes six native configuration containers, a portable ZIP, a conflict-checking installer, and separate [start](cura/start.gcode) / [end](cura/end.gcode) G-code.

The machine uses Marlin flavour and absolute extrusion, disables Cura acceleration/jerk control, loads the saved pla_60 mesh after homing, and finishes through END_PRINT. The export inherits Cura quality/material presets and has **no explicit print/travel speed override**. Earlier 80/150 mm/s suggestions are documented as an optional manual choice.

For portability, the custom eSUN material reference is changed to bundled generic PLA; select and tune your own material. The [manifest](cura/export-manifest.json) records provenance and export changes. Personal Cura accounts, network settings, project models and complete material libraries are excluded.

## One harness from the printer

The working UART route uses the stock screen cable with the DACAI disconnected:

| Contact identified at the original screen | Pi physical pin | Function |
|---|---:|---|
| GND | 6 | Common ground |
| Screen TX / DOUT | 8 | Pi TX → mainboard PA3 RX |
| Screen RX / DIN | 10 | Mainboard PA2 TX → Pi RX |
| Display 5V | 4, current setup only | Pi power; stock rail has shown undervoltage |

These are **physical pin numbers**. The screen labels describe the device being replaced, explaining the apparently same-name TX/TX wiring. Follow the [actual PCB photos and orientation guide](docs/uart.md#wiring-understand-which-end-the-labels-describe); wire colour or a reversed plug drawing is insufficient. Pi UART is 3.3V logic.

The final plan is an internal 24V-to-5V converter, with regulated power and UART in one external harness to the Pi/screen enclosure. **Isolate the original motherboard 5V before injecting buck power.** Cable current capacity and voltage drop still need testing. See the [single-cable guide](docs/single-cable.md).

## What is complete and what comes next

| Area | Status |
|---|---|
| Klipper + Mainsail printing | Working; first layer, motion, probe and heating checked |
| UART screen connector | Working; independent serial identity/status tests and two reported successful prints |
| Saved config and Cura machine | Included, with calibration and portability notes |
| Pi power via stock display rail | Working with limited margin; undervoltage observed with webcam |
| Internal buck converter | [ASIN B0CKZ54Z4P](https://www.amazon.co.uk/dp/B0CKZ54Z4P) ordered; markings/rating and installation pending |
| BIGTREETECH PITFT43, CN | Ordered; PCB revision to confirm, KlipperScreen pending |
| Pi + screen enclosure on stock mounts | Planned; CAD/STL after measurements and fit check |
| Webcam mount | Printing; source/licence and fit to confirm before publishing files |

The [roadmap](docs/roadmap.md) tracks the remaining work.

## Lessons from this build

USB repeatedly lost its receive path despite a shorter cable and another port. A CH341 receive URB -32/EPIPE preceded the MCU timeout, but the initiating cause was never conclusively isolated. UART bypasses that data path; it does not cure inadequate Pi power.

The first UART flash silently left the old USART1 firmware running. A **fresh filename in STM32F4_UPDATE** made the verified image apply. The live MCU then identified PA3/PA2 and answered all 22 status queries. During a later 50.4-second camera/MCU check there were no new retransmitted or invalid bytes.

Unplugging the webcam stopped new undervoltage warnings during the next 8.5 minutes after 69 earlier warnings. That comparison supports improving the supply, without proving the camera itself is faulty or the stock rail permanently adequate.

## Repository layout

~~~text
config/
  klipper/     exact printer config, macros, limits and hashes
  pi/          UART boot excerpt and historical USB experiment
  crowsnest/   optional camera example
cura/
  machine/     native Cura machine/extruder/definition/user containers
  *.gcode      readable start/end sequences
  *.zip        portable native configuration package
docs/
  setup/       host installation, migration and commissioning
  uart.md      full wiring/flash/communication guide
  *.md         tuning, power, diagnostics, hardware and roadmap
firmware/      USB/UART images, build configs, hashes and exact source
photos/        owner's connector photographs, metadata removed
models/        mount/enclosure status; printable files when validated
scripts/       independent read-only UART identity test
~~~

## Sources and licence

Use the primary instructions linked throughout: [Klipper installation](https://www.klipper3d.org/Installation.html), [configuration checks](https://www.klipper3d.org/Config_checks.html), [slicer guidance](https://www.klipper3d.org/Slicers.html), [MainsailOS](https://github.com/mainsail-crew/MainsailOS), and [Raspberry Pi UART documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-uarts).

The [GPLv3 licence](LICENSE) and [provenance notes](NOTICE.md) cover the supplied contributions and upstream-derived firmware/configuration. Binaries include exact corresponding source. Raw private logs, credentials and unrelated projects are not published.
