# Firmware, source and rebuild instructions

These images were built for the owner's **STM32F401 S1 Plus**, 64 KiB bootloader, 8 MHz reference, 84 MHz CPU and 250000 baud. They are not universal Creality firmware.

| File | Role |
|---|---|
| `firmware-uart1810.bin` | Successfully flashed USART2 PA3/PA2 image, 43,708 bytes |
| `firmware-usb1810.bin` | Previous USART1 PA10/PA9 image for USB/CH340 rollback, 43,676 bytes |
| `uart.config` / `uart.defconfig` | Full and minimal UART build settings |
| `usb.config` | Previous USB-bridge build settings |
| `manifest.json` / `SHA256SUMS` | Provenance and integrity |
| `source/klipper-9cb99754.tar.gz` | Exact corresponding upstream source archive |

Source commit: [`9cb99754c035b90206ef0a02660f674fc9517e9b`](https://github.com/Klipper3d/klipper/tree/9cb99754c035b90206ef0a02660f674fc9517e9b). Reported firmware version: `v0.13.0-800-g9cb99754c`. Build tools reported GCC `(15:14.2.rel1-1) 14.2.1 20241119` and binutils `(2.44-3+23+b2) 2.44`.

## Build in a separate checkout

Install build prerequisites following [Klipper's installation documentation](https://www.klipper3d.org/Installation.html). Do not overwrite an active printer's known-good build configuration just to follow this example.

```bash
git clone https://github.com/Klipper3d/klipper.git klipper-uart-build
cd klipper-uart-build
git checkout 9cb99754c035b90206ef0a02660f674fc9517e9b
# Set this to the location of this documentation repository:
UART_REPO=/path/to/ender3-s1-plus-klipper-uart
cp "$UART_REPO/firmware/uart.config" .config
make olddefconfig
make -j2
```

Inspect the resulting configuration: STM32F401, 64 KiB bootloader, 8 MHz reference, USART2 PA3/PA2, 250000 baud, empty initial GPIO list. The minimal defconfig relies on the defaults at this exact revision; prefer the full config for reproducing these settings. The included USB build uses USART1 PA10/PA9 instead.

An alternative is extracting the included source archive and building there. A non-Git archive or a different compiler can produce different embedded version/build metadata and hashes. The supplied hash identifies the tested binary; byte-for-byte reproducibility with arbitrary tooling is not claimed.

Check integrity from the firmware directory:

```bash
sha256sum -c SHA256SUMS
```

## Flashing and verification

Copy the selected image into `STM32F4_UPDATE/` on a suitable FAT32 SD card, using a filename **different from the previous flash**. `firmware-uart1810.bin` succeeded here after a reused `firmware.bin` was ignored. A later retry or rollback needs another fresh name if that name was last used.

Read the full power-off/USB-disconnect/mainboard-slot procedure in the [main guide](../docs/uart.md#3-flash-with-a-new-filename). Do not flash a running printer. USB enumeration is not MCU identity. Verify live `RESERVE_PINS_serial=PA3,PA2` over UART after the flash; USART1 firmware reports PA10/PA9.

## Source and licence

The prebuilt images are Klipper, licensed under GPLv3. The corresponding source is included in `source/` on the same repository, alongside both complete build configurations and these instructions. The archive is the unmodified upstream commit above; the transport selection is recorded in the configuration. No custom MCU source modifications were required.

The licence text is in [LICENSE](../LICENSE). Source can also be obtained directly from [the exact upstream archive](https://github.com/Klipper3d/klipper/archive/9cb99754c035b90206ef0a02660f674fc9517e9b.tar.gz). Do not redistribute these images without preserving the applicable licence and source availability.
