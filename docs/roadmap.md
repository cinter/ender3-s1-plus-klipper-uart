# Roadmap and current build status

Last updated: 18 October 2026. The owner wants a tidy setup powered from the printer, with the Pi and replacement display using the original display mounting points.

## Completed baseline

- [x] Identify stock DACAI connector from actual PCB photographs.
- [x] Enable Pi PL011 UART and verify loopback at 250000 baud.
- [x] Build matching STM32F401 USART2 firmware and preserve USART1 rollback.
- [x] Discover the first flash had not applied; retry with a new filename.
- [x] Verify live MCU identity and status queries over display-cable UART.
- [x] Switch Klipper to `/dev/serial0` and verify ready.
- [x] Pass idle webcam/MCU stability check without growing invalid/retransmission counters.
- [x] Owner reports two successful UART prints; communication described as flawless.
- [x] Observe major power improvement when the USB webcam is unplugged.

## 1. Better power inside the printer — ordered

Purchased link: [buck converter, ASIN B0CKZ54Z4P](https://www.amazon.co.uk/dp/B0CKZ54Z4P). Actual delivered board markings and sustained output rating are pending inspection.

- [ ] Confirm converter type, input rating, output adjustment, thermal capability and protection.
- [ ] Plan a fused 24V DC branch and insulated internal mounting.
- [ ] Isolate the motherboard's existing 5V feed before injecting regulated 5V into the cable to the Pi.
- [ ] Verify whether the existing cable/contact system is adequate, or replace its power conductors along the same route.
- [ ] Measure voltage and temperature under Pi + screen + webcam loads.
- [ ] Record a stable full-print baseline without new undervoltage events.

See [power design](power.md). No completed converter installation is claimed.

## 2. BIGTREETECH Pi TFT43 and KlipperScreen — screen ordered

The owner specified **BIGTREETECH PITFT43, CN**. CN is retained as part of the supplied order description, not treated as proof of a PCB revision. Confirm the actual label on arrival.

- [ ] Identify revision, connector and cable from the delivered hardware.
- [ ] Verify the manufacturer's display setup for the installed Pi/OS.
- [ ] Install and configure [KlipperScreen](https://klipperscreen.readthedocs.io/en/latest/).
- [ ] Check touch alignment, rotation, boot behaviour, power and shutdown.
- [ ] Keep the known-working UART firmware and printer connection as the baseline.

Manufacturer resources: [BIGTREETECH TouchScreenHardware](https://github.com/bigtreetech/BIGTREETECH-TouchScreenHardware), including the Pi TFT43 V2.0 hardware/manual and STEP model. Match the model/revision before using those dimensions. The ordinary serial TFT43 firmware project is not interchangeable with the Pi TFT43 display.

## 3. Printed Pi + screen enclosure — planned

- [ ] Measure the original S1 Plus screen mounting points.
- [ ] Verify physical Pi, screen, connector, ribbon bend and cable-clearance dimensions.
- [ ] Design ventilation, service access and strain relief.
- [ ] Print and fit a prototype to the original mounting points.
- [ ] Publish source CAD and STL only after an actual fit check, with print settings and revision notes.

No enclosure CAD/STL is included yet; there is no claim that an untested model fits.

## 4. Webcam mount — printing

- [ ] Finish the current webcam-mount print and check fit.
- [ ] Confirm the camera's actual physical model, rather than relying only on its USB descriptor.
- [ ] Measure or compare camera load once the new supply is installed.
- [ ] Add mount source/link, creator attribution, licence and tested print settings before redistributing any third-party STL.

The current job is a webcam-mount print. A mount is not yet included because its source/licence and fit have not been established for publication.

## How to contribute a useful result

Include printer board/MCU markings, Pi model, cable orientation, firmware commit/settings, live serial identity, power source and warnings, camera model/settings, and actual print outcomes. Remove credentials, addresses, serial identifiers and unrelated log contents. Clearly distinguish a proposal, an idle check and a completed print.
