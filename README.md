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

> **Project identity:** This is an **unofficial VirgoYT custom TWRP project** for the Motorola Moto G45 5G, codename `fogos`. The long-term target is a genuinely tested 2026 Android 17 recovery—not an Android 15 build and not a relabeled older image. The currently downloadable file is clearly marked as an older TeamWin baseline, not as a finished VirgoYT Android 17 build.

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

The repository contains an **unofficial custom TWRP development tree** for `fogos`, modern SM6375 board-layout notes, Android 17 porting documentation, a build workflow template, and verified ROM metadata. The downloadable recovery image is an older official TeamWin baseline used as a device reference and temporary-boot test; it is not yet a VirgoYT-built Android 17 image.

| Component | Status |
| --- | --- |
| Device identity | Verified for Moto G45 5G / `fogos` |
| Evolution X Android 17 payload | Inspected and documented |
| VirgoYT branding | Added to this project |
| TWRP device-tree baseline | Included for adaptation |
| Android 17 configuration port | Experimental / in progress |
| Genuine Android 17 recovery image | **Not released yet** |
| Temporary-boot validation | Required before any permanent flash |
| OrangeFox Android 17 build | No verified build identified |

The project deliberately does not call the old 2024 image “Android 17.” A recovery image is considered ready only after it builds from the updated source, passes image validation, and is temporarily boot-tested on the target phone.

## Downloadable unofficial custom-TWRP baseline

The public release below is labeled **VirgoYT Unofficial Custom TWRP 3.7.1 Baseline** for Moto G45 5G (`fogos`). The image itself is the verified 2024 TeamWin fogos build supplied as a baseline for this unofficial project. It is not a newly compiled VirgoYT Android 17 recovery, and compatibility with the user’s Android 17 ROM is not guaranteed.

### [Download VirgoYT Unofficial Custom TWRP 3.7.1 Baseline for fogos](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/tag/virgoyt-unofficial-custom-twrp-3.7.1-baseline)

| Asset | Link |
| --- | --- |
| Recovery image | [twrp-3.7.1_12-0-fogos.img](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/download/virgoyt-unofficial-custom-twrp-3.7.1-baseline/twrp-3.7.1_12-0-fogos.img) |
| SHA-256 file | [twrp-3.7.1_12-0-fogos.img.sha256](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/download/virgoyt-unofficial-custom-twrp-3.7.1-baseline/twrp-3.7.1_12-0-fogos.img.sha256) |
| Temporary-boot guide | [TEMPORARY_BOOT.md](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/download/virgoyt-unofficial-custom-twrp-3.7.1-baseline/TEMPORARY_BOOT.md) |
| Release notes | [VIRGOYT_UNOFFICIAL_CUSTOM_TWRP_RELEASE_NOTES.md](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/download/virgoyt-unofficial-custom-twrp-3.7.1-baseline/VIRGOYT_UNOFFICIAL_CUSTOM_TWRP_RELEASE_NOTES.md) |

Verified SHA-256:

```text
498690b6c4b510deefd94b054a731f977f159aab17952106cd45f80ce0bcc373
```

This is an `.img` file, not an APK. For a temporary test from the bootloader, use `fastboot boot`; do not permanently flash this baseline to `boot`, `boot_a`, `boot_b`, or `vendor_boot`.

```bash
fastboot devices
fastboot boot twrp-3.7.1_12-0-fogos.img
```

## Build direction

The Android 17 port is being aligned with the modern SM6375 configuration used by the current `fogos` device sources. The relevant board settings include a 100,663,296-byte boot partition, a 100,663,296-byte vendor-boot partition, recovery-as-boot, recovery DTBO, DTB in boot, vendor ramdisk support, A/B partitions, metadata, and logical `system`, `system_ext`, `product`, and `vendor` partitions.

The old TWRP tree cannot be treated as complete Android 17 support. It must be adapted to the current vendor ramdisk, kernel modules, fstab, encryption behavior, SELinux policy, and recovery boot header. The detailed worklist is in [`docs/ANDROID17_PORT_NOTES.md`](docs/ANDROID17_PORT_NOTES.md), while the safe build and temporary-boot policy is in [`docs/BUILD_AND_TEST.md`](docs/BUILD_AND_TEST.md).

## Automation

The corrected **custom-TWRP build workflow template** is stored at [`ci/twrp-build-release.yml`](ci/twrp-build-release.yml). GitHub only executes workflow files located under `.github/workflows/`, so this template must be copied to:

```text
.github/workflows/twrp-build-release.yml
```

The intended automation builds on pushes and pull requests, records build metadata, validates the generated Android boot image, uploads artifacts, and keeps release creation separately gated. A release must never be created merely because a file exists; it should be published only after a successful build and validation pass.

## Safe testing policy

Recovery development can make a phone fail to boot or fail to decrypt data. Keep the original ROM archive, stock images, and current working boot image untouched. Test an experimental image with `fastboot boot` before considering any permanent flash. Do not flash `vendor_boot.img` merely because it exists in the payload, and do not modify or sideload an edited `payload.bin`.

Do not relock the bootloader while a custom ROM is installed. Do not use an image from another Motorola model, variant, or build. If a temporary recovery fails to boot, return to the bootloader and reboot normally; do not keep flashing random partitions.

## Repository map

| Path | Purpose |
| --- | --- |
| `device/motorola/fogos/` | Unofficial fogos custom-TWRP baseline and device configuration |
| `docs/ROM_INPUT.md` | Verified Evolution X payload details and image sizes |
| `docs/RECOVERY_SOURCES.md` | Official TWRP and LineageOS source assessment |
| `docs/ANDROID17_PORT_NOTES.md` | Android 17 board and recovery porting worklist |
| `docs/BUILD_AND_TEST.md` | Reproducible build and temporary-boot procedure |
| `docs/MAGISK_ROOT_TROUBLESHOOTING.md` | Verified Magisk findings and safe root test sequence |
| `docs/assets/virgoyt-banner.jpg` | VirgoYT project branding image |
| `ci/twrp-build-release.yml` | Workflow template for manual activation |

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
