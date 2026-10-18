# Commissioning before the first print

These checks record the sequence used on this machine. Repeat the checks on your hardware; the exported offsets and mesh are measurements of this particular printer.

Follow [Klipper's configuration checks](https://www.klipper3d.org/Config_checks.html), with access to emergency stop and the power switch. Do not run unattended sequences while direction, endstops or probe operation are uncertain.

## Sensors, motors and homing

1. With all heater targets zero, confirm plausible room-temperature readings.
2. Use QUERY_ENDSTOPS and manually operate the X/Y switches; verify the correct state changes.
3. Check the CR Touch/BLTouch probe deploys, stows and reports triggered/open correctly using the upstream probe checks.
4. Use STEPPER_BUZZ for one motor at a time. Confirm each axis and direction before homing.
5. Home X/Y under supervision, then Z only after confirming probe function, geometry and the safe homing point. On this machine safe_z_home is nozzle X187 Y192 with a 10 mm hop.
6. Test the usable travel slowly and establish bounds that do not strike hardware. Negative coordinates in the snapshot are not a general instruction to extend another printer's travel.

Observed direction checks were X nozzle right, Y bed forward and Z up. X/Y/Z homing and the probe checks passed.

## Probe, bed and first layer

The bed was mechanically trammed before the migration. Verify the configured probe X/Y offsets first, then use [PROBE_CALIBRATE](https://www.klipper3d.org/Probe_Calibrate.html), TESTZ and ACCEPT to measure your own Z offset. SAVE_CONFIG restarts Klipper and belongs in an idle session.

The owner's saved Z offset is **2.825 mm**. It is not a setting to copy blindly.

For this PLA baseline the bed was heated to **60°C**, allowed about **five minutes** to settle, and measured with a 4×4 [bed mesh](https://www.klipper3d.org/Bed_Mesh.html). The profile was saved as **pla_60**. Cura's supplied start sequence explicitly loads that profile after homing.

Create your own profile with that name, or change the start G-code to match yours. Inspect and replace the included SAVE_CONFIG mesh before printing on another bed. Its approximately 0.578 mm peak-to-valley range describes the owner's bed at the time of measurement.

Check a small first-layer print and adjust by measurement. The owner reported a good central first layer. That does not establish every location on every bed.

## Heating and extrusion

Heater operation was checked. PID values were initially carried across from the previous Marlin setup; an independent Klipper PID calibration remains sensible before treating them as tuned for a changed hotend or enclosure.

A small PLA extrusion check at 210°C, 5 mm at F60, ran smoothly. This establishes basic extrusion, not a calibrated flow multiplier. Measure [rotation distance](https://www.klipper3d.org/Rotation_Distance.html) and material flow on your own setup. The snapshot's rotation distance is 26.359 with a 42:12 gear ratio.

Use suitable temperatures for the actual filament; this PLA check is not a material-independent procedure.

## First sliced print

Install the [Cura machine](../../cura/README.md), check the selected material and preview the toolpath and start/end code. Keep acceleration conservative for the first print. Observe homing, purge, adhesion, temperatures and final parking.

The END_PRINT macro parks at X0 Y300 when homed. An earlier Y310 end move was outside the usable configuration and was corrected. Keep both slicer and macro parking coordinates inside verified travel.

Once basic operation works, proceed to [limits and tuning](../limits-and-tuning.md). Save a known-good config before each change. The final UART connection has completed two owner-reported successful prints.
