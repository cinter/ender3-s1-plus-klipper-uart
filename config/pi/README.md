# Pi boot configuration excerpts

[uart-config.txt](uart-config.txt) contains the two UART settings used here. Merge them into the appropriate boot configuration section; do not replace the full file.

The observed boot path is /boot/firmware/config.txt. Confirm on your OS. Disable the serial login console/getty and release the PL011 UART from Bluetooth, then reboot while idle and verify /dev/serial0 resolves to /dev/ttyAMA0.

Follow the complete [UART guide](../../docs/uart.md#1-enable-the-pis-full-uart) for wiring and checks.

[usb-fiq-experiment.txt](usb-fiq-experiment.txt) preserves a historical USB diagnostic experiment. Those parameters are not required for UART and are not part of the recommended clean installation. They were still present on this Pi during the documented UART tests, so they are recorded for reproducibility.
