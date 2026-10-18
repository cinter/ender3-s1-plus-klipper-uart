# One printer supply, one Pi/display harness

The aim is to go from the stock S1 Plus to a Pi and replacement touchscreen on the original screen mount, with power and MCU communication following one tidy harness from the printer.

## Working now

The original DACAI display is disconnected. Its four populated cable conductors carry USART2 TX/RX, common ground and stock display 5V to the Pi. The Pi uses physical pins **8 TX, 10 RX, 6 GND and 4 5V**, with micro-USB power disconnected. See the [photographed orientation and wiring](uart.md#wiring-understand-which-end-the-labels-describe) before making connections.

Communication has been flawless in the owner's subsequent use, including two reported successful prints. The **power arrangement still needs improvement**: with the webcam attached, stock display-cable power produced Pi undervoltage. Removing the webcam stopped new warnings during the observed comparison.

## Planned final arrangement

~~~text
Printer mains lead -> existing printer PSU
                       |-- 24V -> printer mainboard
                       '-- fused DC branch -> internal buck -> regulated 5V
                                                               |
Mainboard UART TX/RX ---- same external harness -----------------+-> Pi
Common GND -----------------------------------------------------+

Original mainboard display 5V: isolated from injected buck output
Pi -> local display ribbon -> BIGTREETECH Pi TFT43
Pi -> local camera connection -> mounted webcam
~~~

The external harness is intended to carry power and serial together. The display ribbon stays local to the Pi/screen assembly. Exact internal mounting, fuse, wire gauge, connectors and sustained load capability remain to be designed and measured.

The ordered [converter](https://www.amazon.co.uk/dp/B0CKZ54Z4P) will be installed inside the printer. **Disconnect/isolate the stock motherboard 5V feed before injecting the converter's 5V. Do not parallel the regulator outputs.** Verify voltage, polarity and isolation before attaching the Pi.

Reusing the cable route does not prove that the existing power wire and connector can carry Pi + screen + webcam load. A better converter may still require stronger power conductors in the same harness. Read the [power design and acceptance measurements](power.md).

The **BIGTREETECH PITFT43, CN** is ordered; the exact PCB revision is pending. KlipperScreen and the enclosure are planned after stable power. CAD/STL, dimensions and final photographs will be added after fitting to the original screen mounting points. The [models directory](../models/README.md) tracks this and the webcam mount.

Power the Pi down before switching off its printer supply. GPIO 5V power bypasses the Pi 3B's normal micro-USB input protection, so the finished DC branch needs appropriate protection.
