# Evidence summary

All times are Europe/London (BST), 18 October 2026 unless noted. This document contains selected measurements, not an upload of private raw logs.

## Independent UART verification

| Check | Result |
|---|---|
| Pi loopback, 115200 baud | 8192 bytes compared successfully |
| Pi loopback, 250000 baud | 65536 bytes compared successfully; no corruption/errors reported |
| First printer UART attempt | TX 468, RX 0 |
| Swapped signal attempt | TX rose from 468 to 858, RX stayed 0 |
| USB identity after failed flash | USART1 PA10/PA9; old firmware still running |
| New-filename flash | Live UART identity now PA3/PA2 |
| Independent protocol queries | 22 replies: get_config, get_uptime, 20 get_clock |
| Live constants | STM32F401xc, 84 MHz, 250000 baud |
| Klipper transport | `/dev/serial0` -> `/dev/ttyAMA0`, USB disconnected |

The successful independent connection reported an unconfigured, non-shutdown MCU before Klipper was started. The later configured connection reached ready normally.

## Camera plus idle MCU stability

Test ended 15:07:21. Six samples spanned 50.414 seconds. An MJPEG stream consumer received 122,880,000 bytes. All samples were ready, with sensible room-temperature sensors and zero heater targets.

| Counter | Change over test |
|---|---:|
| MCU bytes written | +300 |
| MCU bytes read | +6294 |
| Retransmitted bytes | **0** |
| Invalid bytes | **0** |

The configured connection's retransmission total was 9 at the beginning and remained 9 at the end. Initial connection counters and sustained-link errors are different measurements. The independent probe also had startup bytes discarded; that was not presented as an entirely zero-error startup.

## Printing

The owner reports two successful prints after migrating and describes UART screen-connector communication as flawless. Another read-only check during preparation of this repository showed ready MCU state, PA3/PA2 identity, `/dev/serial0` and a webcam-mount job printing. A completion time and independent log audit for every owner-reported job are not claimed.

This is strong practical support for the UART workaround on this machine. It is not a long-duration certification of the power arrangement or proof of the exact original USB fault.

## Power warnings during heat-up

The new display-powered boot showed voltage warnings at 14:58:22, normalising at 14:58:28. Fresh warnings occurred around print startup, including 15:08:54. At 15:08:56 the flag was `0x50005`, meaning active undervoltage and throttling as well as history. At 15:09:52 it was `0x50000`, history retained but active warnings cleared.

UART remained clean at those checkpoints. The owner was informed and chose to keep the print running. Successful communication during a voltage warning does not make that warning spurious.

## Webcam removal comparison

The USB device described itself as NexiGo N60 FHD. With the webcam connected, the kernel recorded **69 undervoltage detections between 20:30 and its removal**.

| Event | Time |
|---|---|
| Last undervoltage detection | 20:45:50 |
| Camera USB disconnect | 20:45:51 |
| Voltage normalised | 20:45:54 |
| Follow-up check, no new detections | 20:54:19 |

That gave approximately **8.5 minutes without a new voltage event**, with `0x50000` showing retained history. No Wi-Fi power setting was changed for this comparison.

Removing the camera changes its USB electrical demand and may also reduce capture/streaming/CPU/network work. Therefore the test implicates webcam-associated load but does not prove defective hardware, a specific current draw, a cable fault or a particular regulator limit. A replacement-camera comparison and voltage/current measurements remain useful follow-up work.
