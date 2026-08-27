<div align="center">

# VirgoYT Unofficial Custom TWRP

### Moto G45 5G • `fogos` • Android 17 custom-recovery porting project

<img src="docs/assets/virgoyt-banner.jpg" alt="VirgoYT Prince branding" width="640" />

<p>
  <strong>Built different.</strong><br />
  A transparent recovery-development workspace for the Motorola Moto G45 5G.
</p>

<p>
  <a href="https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases">Releases</a> •
  <a href="https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/actions">Actions</a> •
  <a href="docs/ROM_INPUT.md">ROM input</a> •
  <a href="docs/BUILD_AND_TEST.md">Build and test guide</a> •
  <a href="docs/MAGISK_ROOT_TROUBLESHOOTING.md">Root troubleshooting</a>
</p>

</div>

> **Project identity:** This is an **unofficial VirgoYT custom TWRP project** for the Motorola Moto G45 5G, codename `fogos`. The repository contains an Android 17-oriented recovery candidate built from the checked-in device tree. It is statically validated, but it remains a temporary-boot candidate until the target phone passes the physical touch, mouse, storage, decryption, ADB, and sideload checks.

## Device profile

| Property | Verified value |
| --- | --- |
| Project type | Unofficial custom TWRP / Android 17 porting project |
| Device | Motorola Moto G45 5G |
| Codename | `fogos` |
| ROM | Evolution X 17.0, unofficial fogos build |
| ROM package | `EvolutionX-17.0-20260812-fogos-12.1-Unofficial` |
| Android | 17 |
| Build number | `CPRA.260605.016` |
| Kernel evidence | `5.4.302-moto-KAGE` |
| Boot layout | A/B, `boot` and `vendor_boot`, no `init_boot` |
| Boot image size | 100,663,296 bytes |
| Vendor boot size | 100,663,296 bytes |
| DTBO size | 25,165,824 bytes |

The ROM package was inspected from its signed `payload.bin`; the verified partition inventory and checksum are recorded in [`docs/ROM_INPUT.md`](docs/ROM_INPUT.md). The current board-layout comparison is documented in [`docs/ANDROID17_PORT_NOTES.md`](docs/ANDROID17_PORT_NOTES.md).

## Current status

The repository contains the unofficial `fogos` custom-TWRP tree, Android 17 port notes, storage/encryption configuration, touchscreen-module loading, USB mouse/OTG support, ADB/sideload wiring, and a gated GitHub Actions build. The current public artifact is a VirgoYT Android 17 candidate that passed static source and image checks. It is **not hardware-certified or approved for permanent flashing** until the exact Moto G45 passes the physical acceptance checklist.

| Component | Status |
| --- | --- |
| Device identity | Verified for Moto G45 5G / `fogos` |
| Evolution X Android 17 payload | Inspected and documented |
| VirgoYT branding | Added to this project |
| `/data` and emulated storage configuration | Patched and statically gated |
| Touchscreen module packaging/loading | Patched and statically gated |
| USB mouse/OTG configuration | Preserved and statically gated |
| ADB/sideload wiring | Present and statically gated; host/device test required |
| Android 17 recovery image | Built and released as a temporary-boot candidate |
| Permanent flash | **Blocked until every physical gate passes** |
| OrangeFox Android 17 build | No verified build identified |

A successful CI build proves source and image invariants only. It cannot certify touchscreen, encryption, mouse, or sideload behavior on a physical phone.

## Download the Android 17 all-checks candidate

The previously published artifact is **VirgoYT fogos Android 17 TWRP — All Checks**. It predates the current repository audit and is not the repaired candidate. Download only a release explicitly identified as an audit candidate after its CI run passes; every image remains unofficial and must be temporarily boot-tested before any permanent-flash decision.

### [Download VirgoYT fogos Android 17 All-Checks Recovery](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/tag/virgoyt-fogos-twrp-android17-all-checks-0ae4ebe)

```bash
fastboot devices
fastboot boot virgoyt-fogos-twrp-0ae4ebe455b511cda30aff7709d6514710b64b9d.img
```

This is an `.img` file, not an APK. Verify its SHA-256 from the release asset before booting. Do not permanently flash it until the physical checklist passes. Never use Format Data or Wipe Data as a troubleshooting shortcut.

## Build and validation direction

The Android 17 tree is aligned with the maintained SM6375/fogos layout and the inspected Evolution X payload: 100,663,296-byte boot and vendor-boot partitions, header version 3, recovery-as-boot, A/B slots, metadata, logical dynamic partitions, FBE/wrapped-key userdata, Android 17 vendor-ramdisk modules, and concrete OTG storage mapping.

The active workflow is [`.github/workflows/twrp-build-release.yml`](.github/workflows/twrp-build-release.yml). It runs the repository validator before artifact upload and keeps release creation behind an explicit manual input. Static gates cannot certify a physical phone, so the release remains temporary-boot only until the target-device checklist passes.

## Automation

GitHub Actions builds the checked-in device tree, packages the Android 17 recovery image and modules, validates the boot header and size, checks storage/input/ADB invariants, writes SHA-256 metadata, and optionally publishes a public candidate. It must never flash a device or erase user data.

## Safe testing policy

Recovery development can make a phone fail to boot or fail to decrypt data. Keep the original ROM archive, stock images, and current working boot image untouched. Test an experimental image with `fastboot boot` before considering any permanent flash. Do not flash `vendor_boot.img` merely because it exists in the payload, and do not modify or sideload an edited `payload.bin`.

Do not relock the bootloader while a custom ROM is installed. Do not use an image from another Motorola model, variant, or build. If a temporary recovery fails to boot, return to the bootloader and reboot normally; do not keep flashing random partitions.

## Repository map

| Path | Purpose |
| --- | --- |
| `device/motorola/fogos/` | VirgoYT fogos Android 17 recovery device tree |
| `.github/workflows/twrp-build-release.yml` | Active build, validation, and manually gated release workflow |
| `tools/validate_fogos_recovery.py` | Static storage, input, OTG, sideload, and image validator |
| `docs/ROM_INPUT.md` | Verified Evolution X payload details and image sizes |
| `docs/RECOVERY_SOURCES.md` | Official TWRP and LineageOS source assessment |
| `docs/ANDROID17_PORT_NOTES.md` | Android 17 board and recovery porting notes |
| `docs/BUILD_AND_TEST.md` | Reproducible build and no-wipe temporary-boot procedure |
| `docs/MAGISK_ROOT_TROUBLESHOOTING.md` | Separate Magisk root investigation |
| `docs/TWRP_STORAGE_SIDELOAD_FIX.md` | Data-media, encryption, OTG, and sideload fixes |
| `docs/assets/virgoyt-banner.jpg` | VirgoYT project branding image |

## References

[1]: https://wiki.lineageos.org/devices/fogos/variant2/ "LineageOS fogos device information"

[2]: https://dl.twrp.me/fogos/ "Official TeamWin fogos downloads"

[3]: https://github.com/TeamWin/android_device_motorola_fogos "TeamWin fogos device tree"

[4]: https://topjohnwu.github.io/Magisk/install.html "Official Magisk installation guide"

[5]: https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases "VirgoYT fogos recovery releases"

## References used in this project

[1] [LineageOS fogos device information][1].
[2] [Official TeamWin fogos downloads][2].
[3] [TeamWin fogos device tree][3].
[4] [Official Magisk installation guide][4].
[5] [VirgoYT fogos recovery releases][5].

<div align="center">

### VirgoYT • Moto G45 5G • `fogos`

**Built different.**

</div>
