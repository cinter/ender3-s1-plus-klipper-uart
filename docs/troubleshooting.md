# Troubleshooting the migration

## No UART response: check what is actually running

Our initial test sent 468 bytes and received zero. Swapping the two signal wires sent another 390 bytes and still received zero. Both wire orientations were tested while the old USART1 firmware was still active, so those failures did not establish which orientation was correct.

After reconnecting USB, Klipper reached ready and the MCU's live constants reported PA10/PA9, with `CONFIG_STM32_SERIAL_USART1=y`. This proved the UART flash had not been applied. The CH340 USB bridge enumerating by itself would not have proved that: it is a separate chip.

The SD card had reused the previous `firmware.bin` name. A fresh name, `STM32F4_UPDATE/firmware-uart1810.bin`, with the same verified binary, then worked. The original documented signal orientation produced PA3/PA2 identity and all 22 status replies.

Check, in order:

1. MCU marking, firmware build, bootloader offset, clock and flash procedure.
2. Shared ground, correct physical Pi pin numbers, removed loopback, secure contacts, and plug orientation.
3. `/dev/serial0` alias, full PL011 UART selection, no serial console/getty, and no other owner of the serial port.
4. The live MCU dictionary after connecting; do not rely on a saved build dictionary to prove what is flashed.

Kernel TX/RX counters were useful on this Pi:

```bash
sudo cat /proc/tty/driver/ttyAMA
```

Zero RX bytes differs from receiving bytes that fail protocol checks. The counter path is driver-specific. A prior successful loopback checks the Pi, not the printer cable or firmware.

Do not move live wires. If a signal swap is needed, remove power from both sides first. Never swap a signal with the cable's 5V supply.

## Earlier USB failure

The printer used a CH340/CH341 bridge and USART1 PA10/PA9 at 250000 baud. Failures persisted after a new short USB cable and moving to another Pi port. Kernel receive-URB `-32`/EPIPE errors preceded lost MCU replies and Klipper shutdown.

The investigation did not find CPU overheating, memory exhaustion, storage errors, a competing serial-port process, or evidence that USB autosuspend explained the event. These checks narrowed the investigation; they did not prove a particular component was at fault.

A printer power cycle seemed necessary at first. Later, two bounded `FIRMWARE_RESTART` attempts recovered the stopped system without power-cycling the printer: the first reopened transport, and the second reset the still-shutdown MCU after communication returned. This was a recovery observation for an already stopped job, **not** a failed-print-resume method. Never automate a reset loop during printing.

## Historical Pi USB/FIQ experiment

Before the UART conversion, the Pi boot command line was backed up and this reversible experiment was applied:

```text
dwc_otg.fiq_enable=0 dwc_otg.fiq_fsm_enable=0
```

Both parameters were verified disabled after reboot. This tested a USB-controller/FIQ hypothesis, not a proven root-cause repair. Under this setting, an old saved 1080p camera request produced no frames, while 720p worked. The saved Crowsnest resolution was changed to 1280x720.

These flags are part of the machine's troubleshooting history, **not a required step for UART**, and are not automatically installed by anything in this repository. They can affect USB performance. Back up and understand the existing single-line boot command line before any separate experiment.

Related references: [MainsailOS discussion](https://github.com/mainsail-crew/MainsailOS/issues/369), [Pi kernel USB serial handling](https://github.com/raspberrypi/linux/blob/rpi-6.18.y/drivers/usb/serial/generic.c), [Pi USB driver](https://github.com/raspberrypi/linux/blob/rpi-6.18.y/drivers/usb/host/dwc_otg/dwc_otg_driver.c).

## Power and webcam warnings

USB receive failures and undervoltage should not be conflated. There was no matching undervoltage journal event at one investigated USB failure. Later, repeated voltage dips were clearly associated with webcam-connected operation on display-cable power. Direct UART bypasses the USB communication path; it cannot increase the available 5V power.

See [diagnostics](diagnostics.md) for the timing and [power](power.md) for the planned internal converter. Configuration changes that merely hide the Pi's voltage warning are not a power fix.
