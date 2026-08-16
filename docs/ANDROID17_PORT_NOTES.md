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

## Current VirgoYT adaptation

The working branch now contains a first compatibility pass based on the verified Evolution X payload and the current fogos reference configuration:

| Change | Evidence or purpose |
|---|---|
| Replaced the old prebuilt kernel | `device/motorola/fogos/prebuilt/Image` now matches the extracted Evolution X Android 17 `boot.img` kernel, SHA-256 `f0496203702eca73edf1bdf8d9a4e39d96409d4c8e134946f34fbeb2c90abbca` |
| Enabled Android boot-image settings | Header version 3, 4 KiB pages, LZ4 ramdisk, recovery DTBO, DTB-in-boot, and the `fogos` HAB command-line property |
| Enabled vendor-ramdisk recovery packaging | Uses `launch_with_vendor_ramdisk.mk` and copies `recovery.fstab` into the first-stage vendor ramdisk location |
| Added recovery module ordering | Added `modules.load.recovery` with the seven official fogos recovery modules available in the checked-in prebuilt set |

This is an **experimental source adaptation, not a finished recovery**. It has not yet produced a validated image and has not been tested on the user’s phone. The old TeamWin baseline already demonstrated that a recovery image can stop at the Hello Moto splash when its kernel and ramdisk are not compatible with the Android 17 boot environment.

## Required port work

1. Use the exact Evolution X vendor/kernel sources or device configuration where available, rather than assuming the LineageOS Android 16 vendor tree is interchangeable.
2. Reconcile `vendor_boot` ramdisk contents and recovery kernel-module loading with the Evolution X package.
3. Reconcile the recovery fstab with the current dynamic partitions and F2FS metadata encryption.
4. Reconcile VINTF manifests and SELinux policy before attempting a build.
5. Build the adapted image and inspect its boot/vendor-ramdisk contents before temporary-boot testing it for display, touch, ADB, fastbootd, partition access, and data decryption.

## Important limitation

No public Evolution X Android 17 `fogos` recovery/device source was located in the supplied package or public references. The payload provides compiled images, not the source tree needed to reproduce a fully compatible recovery. The repository therefore records a buildable direction and verified inputs, but does not claim that an Android 17 recovery image can be safely produced from the old TWRP tree alone.
