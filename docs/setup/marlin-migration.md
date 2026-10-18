# Moving from stock / Thomas Toka Marlin

This S1 Plus ran Thomas Toka's Marlin firmware before Klipper. That was a working starting point, not an installation requirement. The conversion keeps the printer's mechanical hardware while changing the MCU firmware, adding a Pi host and using Mainsail.

| Previous setting or behaviour | Klipper counterpart / action |
|---|---|
| Marlin steps per mm | Express extrusion as rotation_distance plus the actual gear ratio; measure it rather than blindly transcribing steps |
| Probe X/Y offsets | Confirm against the physical nozzle/probe; owner's snapshot uses -48 / 0 |
| Z offset | Recalibrate with PROBE_CALIBRATE; owner's saved result is 2.825 mm |
| EEPROM bed mesh | Make and save a Klipper mesh; Cura start loads pla_60 |
| PID tuning | Owner initially imported hotend/bed values; recheck using Klipper calibration |
| Linear advance / slicer pressure control | Use Klipper pressure_advance; do not stack competing pressure-control features |
| Marlin display menus | Mainsail in a browser now; a replacement Pi display and KlipperScreen are planned |
| Slicer acceleration / jerk commands | Disabled in this machine export; Klipper owns the configured limits |
| Marlin end G-code | Replaced with END_PRINT, including safe lifting and parking |

See the exact [working configuration](../../config/klipper/README.md) and [commissioning sequence](commissioning.md). The stock DACAI screen does not become a KlipperScreen display by changing its firmware: it is disconnected, and the Pi uses its former serial connection.

Retain your own previous working Marlin firmware/config for rollback. The supplied USB rollback binary is still **Klipper**, not Marlin.
