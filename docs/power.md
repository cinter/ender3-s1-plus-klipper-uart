# Internal power: observations and planned buck-converter installation

## Present arrangement

The owner strongly prefers using the printer's existing supply and mains cable. The Pi currently receives 5V from the original display cable into physical pin 4, with ground on pin 6 and micro-USB power disconnected. UART also travels through the display cable. This works for communication, but repeated Pi undervoltage was observed with a USB webcam connected.

Unplugging the webcam at 20:45:51 on 18 October 2026 was followed by voltage normalisation at 20:45:54. There were no new warnings in the next 8.5 minutes, versus 69 warnings from 20:30 until removal. This implicates the webcam-associated load. It does not distinguish normal webcam current, a faulty camera, CPU/streaming/network load, voltage drop in the jumpers, or limited stock-regulator capacity.

## Planned parts and topology — not yet installed

Ordered converter: [Amazon ASIN B0CKZ54Z4P](https://www.amazon.co.uk/dp/B0CKZ54Z4P). Exact hardware markings and rating need checking on arrival. This link is a purchase record, not a recommendation based on a completed test. Marketplace search results associate the ASIN with an LM2596-type module, but the actual delivered module is not yet verified.

Ordered display: **BIGTREETECH Pi TFT43**, PCB revision to confirm. Its backlight and display load must be included in the power budget together with the Pi and camera.

The intended topology is:

```text
Existing printer 24V DC supply
  |-- existing mainboard supply, unchanged
  `-- appropriately fused branch -> regulated buck converter
                                    |-- 5V -> isolated power conductor(s)
                                    |         along display-cable route -> Pi/screen
                                    `-- GND -> common ground

Mainboard USART2 TX/RX/GND -> display-cable signal conductors -> Pi UART
Mainboard ORIGINAL display 5V -> DISCONNECTED from the injected-power conductor
```

**Do not join the buck's 5V output to the mainboard's existing display 5V output.** The original positive feed must be isolated at the source end of the reused conductor, with the loose contact insulated. Do not modify this based solely on a diagram: identify the actual plug contacts and verify isolation while unpowered. UART still needs a common ground reference.

The aim is to reuse the cable route and tidy mounting, not to assume the stock power wire and contacts can carry any desired current. If voltage drop or contact heating is excessive, replace the power conductors or harness with adequately rated wiring, even if it follows the same route.

## Checks before connecting the Pi

1. Work on the low-voltage DC side with the printer unplugged; do not alter the PSU's mains input. Inspect supply headroom, available terminals, wire sizes and the proposed mounting point.
2. Check the actual converter input rating against the printer's 24V supply. Creality specifies 24V for the S1 Plus; verify the machine's actual supply and label.
3. Identify the converter and determine its usable continuous current at 24V input, enclosure temperature and airflow. A chip's advertised 3A maximum does not validate a complete small module at that load. If it is LM2596-based, consult the [TI data](https://www.ti.com/product/LM2596), but do not assume the marketplace board duplicates TI's design or thermal performance.
4. Set and measure a stable Pi-appropriate output around 5.0–5.1V **before attaching the Pi**. Check polarity and the disconnected original 5V feed. Never feed 24V or an unadjusted converter output into the Pi.
5. Provide wiring protection/fusing matched to the branch and conductor ratings. GPIO power enters after the Pi 3B's normal input protection, so protection and regulation must be supplied by the installation.
6. Use secure, suitably rated terminals/connectors and insulated mounting. Temporary individual prototyping jumpers are not the proposed finished power harness.

## Acceptance tests after installation

- Measure at the converter and at the Pi with the Pi, screen and webcam operating together. A significant difference points to the harness rather than converter regulation.
- Check idle, boot, screen brightness changes, camera streaming, Wi-Fi activity and printer heat-up/motion. Monitor converter temperature and the cable/contact temperature as well as voltage.
- Run `watch -n 1 vcgencmd get_throttled` and review timestamped kernel warnings. Retained historical flags are not new events; record the test's start time and compare the journal.
- Establish a stable baseline over multiple prints before adding more changes. A short idle pass is insufficient.
- Publish measured voltages, current, temperature, fuse/wire details and final connector photographs here once verified.

Raspberry Pi recommends a 5V/2.5A supply for Pi 3 models. That is a supply design recommendation, not a claim that the Pi always draws 2.5A; extra peripherals and the new screen need appropriate margin. A larger rated converter only supplies what the load draws, but its thermal capability and output quality still matter.

## Monitoring commands

On the Pi, not in the Mainsail G-code console:

```bash
vcgencmd get_throttled
watch -n 1 vcgencmd get_throttled
journalctl -k -b -g '[Vv]oltage'
```

| Flag observed here | Meaning |
|---|---|
| `0x0` | None of the documented warnings recorded |
| `0x50000` | Undervoltage and throttling have occurred; neither is active in this sample |
| `0x50005` | Undervoltage and throttling active, with history also set |

`vcgencmd measure_volts` measures internal rails; it is not a measurement of the 5V input at the Pi. Use a meter for that. A meter may also miss very short transients.

At one checkpoint, Moonraker returned fallback `throttled_state` data (`bits=0`, `flags=["?"]`) while `vcgencmd` and the kernel journal showed real warnings. Therefore, absence of a Mainsail banner was not accepted as proof of good power. This UI discrepancy has not been fixed by restarting services during a print.

## Other experiments discussed, not applied

- A different, lower-current webcam or a CSI camera may help, but neither camera's actual power draw was measured here. CSI still uses Pi power and adds image-processing work.
- Wi-Fi transmit power can be limited with `sudo iw dev wlan0 set txpower limit 1500` (15 dBm requested) and restored with `sudo iw dev wlan0 set txpower auto`, if supported by the driver. Range/retries can worsen, and the Pi's total electrical savings are not the same as the RF power reduction. This setting was **not applied** in the recorded comparison. Idle Wi-Fi power saving is a different setting.
- Extra capacitance can address some transients, but it does not replace a supply with adequate continuous capability or repair a poor contact. No capacitor modification is claimed tested here.

Primary references: [Creality's S1 Plus supply specification](https://www.creality.com/blog/creality-launches-ender-3-s1-plus-the-sizeable-smart-3d-printer-for-prosumers), [Pi power recommendation](https://www.raspberrypi.com/documentation/computers/getting-started.html#power-supply), [GPIO power protection](https://magazine.raspberrypi.com/articles/power-supply), [power flag definitions](https://www.raspberrypi.com/documentation/computers/os.html#get_throttled), [Linux Wireless TX power](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw.html#setting-tx-power).
