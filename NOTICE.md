# Provenance and publication notes

Firmware and board pin mappings originate from [Klipper](https://github.com/Klipper3d/klipper), GPLv3. Both firmware images were built from commit `9cb99754c035b90206ef0a02660f674fc9517e9b`. The matching upstream source archive, full build configurations, licence and build instructions are supplied together in this repository. No custom MCU source changes were required.

The printer configuration derives from upstream's S1 Plus configuration with owner-specific calibration and macros. Documentation and original contributions in this repository are supplied under GPLv3; the upstream licence text is in LICENSE. Existing upstream copyright notices remain applicable to the source archive and firmware.

Hardware photographs were supplied by the repository owner for this project. EXIF/XMP/IPTC metadata and JPEG comments were removed for publication without recompressing the image pixels.

Configuration examples were selected and inspected before publication. The private workspace README, passwords, network configuration, raw host logs, service credentials, OctoEverywhere settings, unrelated print projects and private diagnostic archives are not part of this repository. The Crowsnest device identifier is a placeholder. Diagnostic documents contain a deliberately rewritten subset of useful measurements.

The complete-build guide adds three exact working Klipper configuration files, verified by SHA256 against the Pi, and six selected native Cura machine containers. Cura inherits bundled upstream definitions rather than redistributing its resource library. The portable export normalises machine group metadata and replaces the owner's custom eSUN material reference with bundled generic 1.75 mm PLA. Original and published hashes and those changes are recorded in cura/export-manifest.json. No Cura account store, global preferences, plugin configuration or private project models are included.

Product links identify ordered hardware and technical references; no affiliate parameters are included. No unverified enclosure or webcam-mount STL is distributed. References to external projects or hardware do not imply endorsement.
