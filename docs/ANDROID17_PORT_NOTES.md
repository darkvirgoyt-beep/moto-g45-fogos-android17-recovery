# Android 17 port notes

## Confirmed from the current fogos reference tree

The current official LineageOS fogos tree (commit `eb605967825f23f9f649b1f05b3b3d4f2fbc5fcc`) inherits `device/motorola/sm6375-common/BoardConfigCommon.mk`. The shared common board configuration contains values that match the user-provided Evolution X payload:

| Configuration | Current Lineage/common value | User payload |
|---|---:|---:|
| Boot header | Version 3 | `boot.img` begins with Android boot magic and is 100,663,296 bytes |
| Boot partition | 100,663,296 bytes | 100,663,296 bytes |
| DTBO partition | 25,165,824 bytes | 25,165,824 bytes |
| Vendor boot partition | 100,663,296 bytes | 100,663,296 bytes |
| Recovery model | `BOARD_USES_RECOVERY_AS_BOOT := true` | Payload has `boot` and `vendor_boot`, no `init_boot` |
| Vendor ramdisk | `BOARD_BUILD_VENDOR_RAMDISK_IMAGE := true` | `vendor_boot.img` is present |
| Recovery fstab | Shared `fstab.qcom` | Must be compared with Evolution X vendor layout |
| Recovery DTB/DTBO | Includes recovery DTBO and DTB in boot image | `dtbo.img` is present |

These matches strongly suggest that the current Lineage common tree is a better structural reference for an Android 17 port than the old standalone TWRP BoardConfig. However, it is an Android 16 reference and does not prove that the current Evolution X vendor ramdisk, kernel modules, encryption metadata, or SELinux policy are compatible.

## Required port work

1. Use the exact Evolution X vendor/kernel sources or device configuration where available, rather than assuming the LineageOS Android 16 vendor tree is interchangeable.
2. Reconcile `vendor_boot` ramdisk contents and recovery kernel-module loading with the Evolution X package.
3. Reconcile the recovery fstab with the current dynamic partitions and F2FS metadata encryption.
4. Reconcile VINTF manifests and SELinux policy before attempting a build.
5. Build a recovery image only after the source tree is complete; temporary-boot test it first for display, touch, ADB, fastbootd, partition access, and data decryption.

## Important limitation

No public Evolution X Android 17 `fogos` recovery/device source was located in the supplied package or public references. The payload provides compiled images, not the source tree needed to reproduce a fully compatible recovery. The repository therefore records a buildable direction and verified inputs, but does not claim that an Android 17 recovery image can be safely produced from the old TWRP tree alone.
