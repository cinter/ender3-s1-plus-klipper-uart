# Configuration snapshot and machine-specific values

`config/printer.cfg` is an example of the owner's working S1 Plus configuration after UART migration. It is derived from upstream Klipper's S1 Plus mapping, with local tuning and macros. It is not a universal commissioning file.

Only the MCU serial path and explicit baud are required for the UART transport change. Leave known-good mechanics and calibration alone when diagnosing communication.

Values which must be reviewed on another printer include:

| Setting | This machine's snapshot | Reason to check yours |
|---|---|---|
| Probe X/Y offset | -48 / 0 mm | Probe location/mount can differ from stock |
| Saved Z offset | 2.825 mm | Nozzle/probe/build-surface specific |
| Extruder rotation distance | 26.359 with 42:12 gear ratio | Extrusion calibration |
| Pressure advance | 0.0875 | Measured for this setup/material; not a generic TPU/PLA preset |
| Input shaper | MZV, X33.3 / Y36.4 Hz | Based on printed ringing measurement, not accelerometer data |
| Damping ratios | 0.15 / 0.15 | Imported provisional estimates |
| Acceleration | 500 mm/s² | Quiet working baseline, not printer capability limit |
| Heater PID | Values imported from prior Marlin configuration | Recalibrate when appropriate on your hardware |
| `pla_60` mesh | Saved owner-specific 4x4 map | Never substitute another printer's mesh for measuring yours |
| Axis/mesh limits | S1 Plus values with local probe geometry | Verify clearance before homing/probing/motion |

The snapshot includes `mainsail.cfg`, `bedtime.cfg` and `filament.cfg`. Use the normal `mainsail.cfg` supplied by your Mainsail installation; this repository does not replace it. The other two files are included alongside the snapshot.

- `BEDTIME_MODE` toggles runtime motion caps, with wrappers around `SET_VELOCITY_LIMIT` and `M204` to keep slicer commands from exceeding those caps. Check for conflicts with your own macros.
- `UNLOAD_FILAMENT` heats to 200 C and retracts 10 mm, then switches the hotend off. This is a local unloading helper, not a universal material-safe temperature or a full long-path filament ejection routine. Review before using it.
- `END_PRINT` retracts when hot, switches heaters/fan off, raises up to the available safe room, parks at X0/Y300 when homed and disables motors. Check the parking coordinates against your machine and any objects on the bed.

The saved configuration block is retained to document actual state, not as recommended values to copy. Calibrate your own Z offset and mesh, and check all heater/sensor/endstop mappings before any test print. Use Klipper's official [configuration checks](https://www.klipper3d.org/Config_checks.html) and [configuration reference](https://www.klipper3d.org/Config_Reference.html).

No model G-code, slicer projects or unverified third-party printable parts are included. The repository focuses on reproducible communication and the planned hardware integration.
