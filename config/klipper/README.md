# Exact working Klipper configuration

The three configuration files here are byte-for-byte copies of the owner's local files, independently matched by SHA256 to the running Pi on 18 October 2026. [SHA256SUMS](SHA256SUMS) records those copies. They are a reproducible machine snapshot, not universal S1 Plus calibration.

| File | Purpose |
|---|---|
| [printer.cfg](printer.cfg) | Board pins, mechanics, UART connection, heaters, probe, mesh, shaping, pressure advance and END_PRINT |
| [bedtime.cfg](bedtime.cfg) | BEDTIME_MODE toggles quiet limits and restores the prior active limits |
| [filament.cfg](filament.cfg) | Filament handling macro; inspect its temperature and retract distance for your material |
| [mcu-uart.cfg](mcu-uart.cfg) | Connection excerpt for reference; replace the existing MCU section rather than adding another |
| [observed-limits.json](observed-limits.json) | Saved defaults, separate runtime observation and quiet-mode limits |

Put the three working files together in the Pi's Klipper config folder, normally ~/printer_data/config. The [mainsail.cfg] include comes from the Mainsail installation and must be present there. This export does not replace the Mainsail-managed file.

Before another printer moves or heats, check board/MCU pin mapping, thermistors/heaters, probe geometry, travel and homing. Replace this owner's Z offset and mesh, and verify extrusion, PID, pressure advance and shaping. The saved probe offset is X=-48 / Y=0; confirm physical geometry even on an otherwise stock S1 Plus.

The exact printer.cfg retains upstream header comments mentioning the original USB build and firmware.bin. The final active connection is USART2 on /dev/serial0; use the [current firmware instructions](../../firmware/README.md), including a fresh SD filename. The comments are preserved to keep the working snapshot exact.

The saved defaults are **300 mm/s velocity, 500 mm/s² acceleration, 5 mm/s square corner velocity**. During the later webcam-mount print, the live limits were **800 mm/s² and 10 mm/s**, which are temporary runtime state and not saved here. See [limits and tuning](../../docs/limits-and-tuning.md).

The configuration includes an owner-specific SAVE_CONFIG block. Preserve your own calibration when adopting the structure. Cura start code requires a valid saved profile named pla_60, and Cura end code requires END_PRINT.
