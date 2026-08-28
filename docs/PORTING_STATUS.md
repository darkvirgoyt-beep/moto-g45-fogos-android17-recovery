# Android 17 porting status

## Target and evidence

This repository targets the Motorola Moto G45 5G, codename `fogos`, running the user-provided Evolution X 17.0 package `EvolutionX-17.0-20260812-fogos-12.1-Unofficial`. The ROM input record is maintained in [`ROM_INPUT.md`](ROM_INPUT.md). It records a version-2 `payload.bin`, `boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, and `vbmeta_system.img`; no `init_boot` image was found in that payload.

The checked-in recovery tree uses the inspected boot header and partition geometry: 4 KiB pages, header version 3, 100,663,296-byte boot and vendor-boot partitions, a 25,165,824-byte DTBO partition, A/B slots, recovery-as-boot, vendor-ramdisk support, metadata, and logical system partitions. The separate DTBO size is recorded from the payload, but this repository does not embed a recovery DTBO because no verified public prebuilt is available. The kernel and recovery module set are taken from the inspected fogos Android 17 payload record.

## Corrected source areas

| Area | Repository state |
| --- | --- |
| Dynamic partitions | Uses Motorola `mot_dp_group` with the verified logical partition list; the stale QTI group and nonexistent ODM target were removed. |
| `/data` | Uses the fogos userdata block device, F2FS, inline AES-256 encryption, wrapped-key v2 metadata, and the metadata key directory. |
| Emulated storage | `RECOVERY_SDCARD_ON_DATA := true` and TWRP `storage;settingsstorage` flags expose `/data/media/0` after successful decryption. |
| USB-OTG | Uses the concrete `/dev/block/sdg1` partition and `/dev/block/sdg` parent instead of wildcard removable-storage aliases. |
| Touchscreen | The Android 17 module files and generated dependency metadata are packaged by TeamWin under `/vendor/lib/modules/1.1`; the recovery init script inserts them from that canonical path in dependency-safe order. |
| Mouse/HID | Input event, mouse, and USB HID paths remain enabled; the touchscreen patch does not remove mouse fallback. |
| ADB/sideload | `adbd`, `minadbd`/sideload support, FunctionFS ADB, and the sideload gadget transition are retained and statically gated. |
| Runtime syntax | The malformed USB property expansion and stray ueventd comment token were removed. |
| Build environment | Unsupported product API/VNDK pins were removed; strict undefined-variable mode was removed because TWRP 12.1 reads unset helper variables during `mka`; the workflow verifies the local tree after lunch. |
| DTBO | The payload’s separate DTBO partition geometry is retained as metadata, but no recovery DTBO is fabricated or requested without a verified public prebuilt. |
| Signing | Fabricated security-patch overrides and AOSP test-key vbmeta synthesis were removed; stock signed vbmeta images remain outside this recovery build. |

## Release status

The current public artifact is an **unofficial Android 17 recovery candidate**, not a hardware-certified or permanently flashable image. GitHub Actions validates source invariants, image header, exact image size, checksum, module packaging, storage metadata, input permissions, and sideload wiring. CI cannot press the phone’s screen, decrypt the user’s installed `/data`, connect a real OTG mouse, or complete a host sideload session.

## Required physical acceptance

The target phone must be temporarily booted with the exact candidate. Finger touch, USB mouse/OTG, `/data` decryption using the existing credential, non-zero Internal Storage, `/data/media/0`, external OTG storage, normal ADB, ADB sideload, ZIP installation, clean reboot, and data preservation must all pass. If any check fails, remain on temporary boot, preserve recovery logs and the build tag, and do not permanently flash or erase user data.

## References

[1] [Android vendor boot partitions](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)

[2] [LineageOS fogos device tree](https://github.com/LineageOS/android_device_motorola_fogos)

[3] [TeamWin fogos device tree](https://github.com/TeamWin/android_device_motorola_fogos)

[4] [VirgoYT fogos recovery releases](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases)
