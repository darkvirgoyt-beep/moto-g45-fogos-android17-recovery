# VirgoYT fogos TWRP storage and sideload fix

This note records the source-level fixes for the Android 17 fogos recovery candidate. No format-data, wipe-data, or metadata erase is part of this patch.

## Root causes found

The successful recovery image booted, but the device tree did not enable TWRP's data-media setup. Without `RECOVERY_SDCARD_ON_DATA := true`, TWRP can mount `/data` without creating its emulated-storage model, so the UI reports 0 MB and does not switch to `/data/media/0` after decryption.

The `/data` overlay also omitted TWRP's `storage` and `settingsstorage` flags and did not repeat the Android 17 metadata-encryption key directory and wrapped-key attributes. The actual Evolution Android 17 fstab uses FBE with inline encryption, wrapped keys, and `/metadata/vold/metadata_encryption`; those values are now preserved in the TWRP metadata.

The recovery fstab imported an Android-only wildcard `voldmanaged=usbotg:auto` entry at `/storage/usbotg`. TWRP's legacy partition parser expanded that entry into removable child paths while no corresponding TWRP parent partition existed, producing `Unable to locate parent partition '/storage/usbotg-*'`. The patch replaces it with the verified fogos block-device pair used by the existing TeamWin tree: `/dev/block/sdg1` with `/dev/block/sdg` as the alternate device and mount point `/usb-otg`.

The TWRP source already contains the modern `minadbd` sideload implementation and calls `SetUsbConfig("none")` before switching to `sideload`; the fogos product also includes `update_engine_sideload`. Therefore, the Bugjaeger message `trying pre-KitKat sideload method` is not evidence that data must be wiped. The build must retain `/system/bin/minadbd` and `/system/bin/update_engine_sideload`; testing with a current desktop `adb sideload` is the clean way to separate a Bugjaeger host-protocol limitation from a recovery packaging problem.

## Files changed

- `device/motorola/fogos/BoardConfig.mk`: enabled `RECOVERY_SDCARD_ON_DATA`.
- `device/motorola/fogos/recovery.fstab`: replaced the wildcard Android vold-managed OTG entry with the verified fogos block mapping.
- `device/motorola/fogos/recovery/root/system/etc/twrp.flags`: marked `/data` as internal/settings storage with the real Android 17 FBE metadata and removed the fabricated wildcard parent model; added the verified `/usb-otg` mapping.

## Validation policy

The next image must boot temporarily first. The storage test is: decrypt with the device credential if TWRP supports it, confirm `/data/media/0` and internal storage appear, and verify that no `/storage/usbotg-*` parent errors recur. The sideload test should use a current `adb` client and a non-destructive test ZIP. No format-data or wipe-data action is required for this diagnosis.

The image must remain at or below the fogos `boot`/`vendor_boot` partition limit of 100,663,296 bytes, and it must not be published until the workflow confirms the image header, checksum, `minadbd`, and `update_engine_sideload` packaging.

> The 46.91 MB file shown in Chrome is the compressed workflow artifact ZIP. The recovery image inside is a separate approximately 96 MiB file; the ZIP size is not the boot partition size.

## Source references

- [AOSP vendor boot partitions](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)
- [Android boot image header](https://source.android.com/docs/core/architecture/bootloader/boot-image-header)
- [TWRP fogos source baseline](https://github.com/TeamWin/android_device_motorola_fogos)
- [VirgoYT fogos Android 17 recovery project](https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery)

This is an unofficial VirgoYT project and is not an official TeamWin Android 17 release.

