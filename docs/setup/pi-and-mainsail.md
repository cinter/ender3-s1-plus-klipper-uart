# From the stock printer to a Klipper host

This is the route to reproduce the build, followed by the UART conversion. It is not a claim that every S1 Plus board uses the same MCU. This machine has a stock **STM32F401** mainboard, a DACAI display and a **Raspberry Pi 3B**. Thomas Toka's Marlin firmware was used before Klipper; it is not a prerequisite.

## 1. Preserve the working starting point

Save your Marlin settings and any existing printer configuration, slicer start/end G-code, probe offsets and calibration notes. Photograph board and MCU markings and the display connector before disconnecting anything. Prepare a known-good rollback firmware for your actual board.

The supplied Klipper configuration contains this owner's calibration. In particular, its probe offset of X=-48 / Y=0 must be checked against your physical probe/nozzle geometry. Do not infer stock geometry from the printer model name. Keep your own Z offset, bed mesh and verified travel limits.

## 2. Install MainsailOS on the Pi

Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and the image/instructions linked by [MainsailOS](https://github.com/mainsail-crew/MainsailOS). Select an image compatible with your Pi; the observed installation here is 64-bit MainsailOS on Debian 13/Trixie. This snapshot does not require another owner to install that exact OS release.

1. Use a suitable microSD card. Set your own hostname, user, SSH access and Wi-Fi details in Imager.
2. Boot the Pi on an adequate supply and find its address on your network.
3. Open Mainsail in a browser. Confirm Moonraker and Klipper are installed, then apply updates while the printer is idle.
4. Check disk space, cooling and power health before commissioning. Save backups of working configuration as you go.

Mainsail is the browser interface; Moonraker provides its API; Klipper on the Pi plans motion and communicates with the printer's flashed MCU. Crowsnest handles the optional camera. OctoEverywhere was used for remote access, but is optional and its account configuration is not included.

## 3. Choose the initial printer connection

The original commissioning used USB with an MCU image configured for **USART1 PA10/PA9** through the board's CH340 bridge. The final working build uses **USART2 PA3/PA2** through the display cable.

You can commission over USB before moving to UART, or use the UART guide from the outset. Both firmware configurations and exact source are in [firmware](../../firmware/README.md). A host-side serial-path change alone cannot switch the MCU's UART.

For the final build, follow the complete [UART wiring, Pi configuration, build, SD flash and identity test](../uart.md). For USB, use the supplied USB build configuration and your own persistent device path from:

~~~bash
ls -l /dev/serial/by-id/
~~~

Use that actual path in your single MCU section, with baud 250000 and restart_method command for the documented bridge build. Do not invent a device ID or assume the USB bridge enumerating proves the MCU was flashed. The F401 update uses a FAT32 card, STM32F4_UPDATE directory and a **fresh firmware filename**, as detailed in the UART guide.

## 4. Install the printer configuration

Download the selected files in [config/klipper](../../config/klipper/README.md). Back up the Pi's configuration first. The normal destination is ~/printer_data/config, available through Mainsail's Machine page.

Review printer.cfg against your board, physical geometry and calibrations before installing it. Put printer.cfg, bedtime.cfg and filament.cfg together. Keep the Mainsail-provided mainsail.cfg installed; it is an external include, not a file missing from this export. Do not append the MCU example as a duplicate section.

Historical comments in the exact printer.cfg describe the original upstream USB build. The active MCU section is UART, and the current [firmware guide](../../firmware/README.md) gives the correct final connection.

Restart Klipper only with the machine idle and then follow [commissioning](commissioning.md). Do not start by running a sliced print.

## 5. Camera and remote access

Use the [Crowsnest example](../../config/crowsnest/README.md) with your own camera device path. Check a stream in Mainsail before enabling remote viewing. The observed webcam identifies as NexiGo N60 FHD, and its load coincided with Pi undervoltage on display-cable power. Work up to the full load only after validating the supply.

Configure optional OctoEverywhere using its own installation/account flow. Never publish API keys, network credentials or your complete host configuration with a build guide.

Next: [commission the printer](commissioning.md), [configure Cura](../../cura/README.md), then [finish the single-cable power design](../single-cable.md).
