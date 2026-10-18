# Limits, calibration and print settings

Snapshot: 18 October 2026. The authoritative saved values are in [printer.cfg](../config/klipper/printer.cfg), with a machine-readable distinction between saved and runtime settings in [observed-limits.json](../config/klipper/observed-limits.json).

## Saved machine limits

| Setting | Saved value | Meaning |
|---|---:|---|
| max_velocity | 300 mm/s | Ceiling; it does not make every sliced move run at 300 |
| max_accel | 500 mm/s² | Conservative saved acceleration |
| square_corner_velocity | 5 mm/s | Klipper default, not explicitly overridden in the file |
| minimum_cruise_ratio | 0.5 | Klipper default for the documented version |
| max_z_velocity / max_z_accel | 10 mm/s / 100 mm/s² | Z motion caps |
| max_extrude_only_velocity / accel | 50 mm/s / 1000 mm/s² | Extruder-only motion caps |
| X travel | -15 to 316 mm | Owner's configured nozzle travel, not nominal print size |
| Y travel | -15 to 304 mm | Same distinction |
| Z travel | -4 to 300 mm | Negative lower allowance requires particular care |
| Hotend / bed temperature ceiling | 260 / 100°C | Configured limits, not recommended material temperatures |

The nominal Cura build volume is **300 × 300 × 300 mm** with a front-left origin. Cura does not need the negative homing allowances or the extra nozzle travel as printable volume.

During a later webcam-mount print, live limits were **300 mm/s, 800 mm/s² acceleration and 10 mm/s corner velocity**, with minimum cruise ratio 0.5. These are runtime overrides. A config restart restores the saved baseline unless a macro or command changes it again.

The bedtime macros cap velocity at **40 mm/s**, acceleration at **250 mm/s²** and corner velocity at **2 mm/s**, remembering/restoring the previous active limits and intercepting later limit requests. Review [bedtime.cfg](../config/klipper/bedtime.cfg) before combining it with other wrappers.

## Extruder and pressure advance

The saved extruder rotation distance is **26.359**, with **42:12** gearing and 16 microsteps. Measure your own extrusion; do not copy both a pre-geared steps value and a gear ratio and accidentally apply gearing twice.

The pressure-advance tower used a 0.005 increment per mm of height. The owner's selected height was **17.5 mm**, giving **0.0875**, now saved as pressure_advance. The default smoothing time is 0.040 s. This result is specific to the filament, nozzle and extrusion setup used.

Follow [Klipper's pressure advance procedure](https://www.klipper3d.org/Pressure_Advance.html). Normal retraction remains in the slicer; coasting or competing pressure-control features should not be added on top without understanding their effect.

## Input shaping

The saved shaper is **MZV**, with **X 33.3 Hz / Y 36.4 Hz** and damping ratio 0.15 on both axes. These were estimated from a printed ringing tower, not measured with an accelerometer.

At 80 mm/s, five ringing intervals over approximately 12 mm gave X = 80×5/12 ≈ 33.3 Hz; five over approximately 11 mm gave Y ≈ 36.4 Hz. An EI comparison offered little visible benefit in this trial, so MZV was retained.

These are an initial tuning result, not a validated maximum-acceleration analysis. Use [Klipper resonance compensation](https://www.klipper3d.org/Resonance_Compensation.html) and preferably measure your own resonances, particularly after changing the bed load, camera mounting or frame.

## Probe, mesh and PID

The saved probe offsets are X=-48, Y=0 and Z=2.825 mm. A 4×4 mesh at a settled 60°C bed is stored as pla_60; configured probe sampling runs from 20,20 to 268,263. All of these must be checked against the actual geometry.

Hotend PID is Kp28.30 / Ki3.08 / Kd65.09, and bed PID is Kp55.97 / Ki9.55 / Kd218.8. They were initially imported from Marlin; a fresh Klipper PID tune remains deferred rather than claimed complete.

See [commissioning](setup/commissioning.md) and the [calibration status](calibration.md).

## Cura and the speed distinction

The exported native machine disables slicer acceleration and jerk control. Its 500 mm/s² machine acceleration fields are used for Cura's estimates; they do not synchronise runtime Klipper limits.

The actual exported containers have **no explicit print or travel speed override** and inherit the selected Cura quality/material settings. Earlier setup notes discussed 80 mm/s print / 150 mm/s travel as a moderate option. Those are optional manual settings, not the saved machine export or a tested universal speed recommendation.

Inspect Cura's Preview and the resulting G-code. Requested speed, motion caps, acceleration, cornering, extrusion flow and part geometry all affect actual speed. The supplied start sequence resets M220/M221 to 100% but does not reset Klipper pressure advance, shaping or motion limits.
