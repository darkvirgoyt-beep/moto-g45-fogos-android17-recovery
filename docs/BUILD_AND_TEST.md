# Build and validation plan

## Current build status

The repository currently contains a verified ROM-input record, a historical TWRP `fogos` baseline, and Android 16 Lineage/Motorola source references. It does **not** yet contain enough verified Android 17 source to produce a flash-ready recovery image. The public Motorola source branches stop at `sixteen`, and the provided Evolution X package contains compiled payload images but not the vendor/kernel source needed to reproduce its recovery ramdisk.

A GitHub Actions workflow may be enabled later, but it must not publish or flash an artifact automatically. The first successful artifact must be treated as an experimental candidate only.

## Build prerequisites

Before enabling a build, the project needs:

| Requirement | Why it is required |
|---|---|
| Android 17-compatible recovery base | The historical TWRP 12.1 tree is not enough by itself |
| Exact `fogos` device and SM6375-common sources | Supplies board, fstab, init, module, and SELinux configuration |
| Compatible vendor files or a reproducible extraction source | Recovery needs vendor HALs, libraries, firmware interfaces, and encryption support |
| Kernel source/configuration and recovery modules | Required for display, touch, USB, storage, and vendor ramdisk behavior |
| Exact ROM payload images | Used for header, partition, DTB/DTBO, and AVB comparison |
| A GitHub Actions runner with sufficient storage | A full Android recovery/ROM source build is far larger than the repository itself |

## Safe test sequence

1. Build the candidate without signing or publishing it as a release.
2. Verify the output image’s Android boot header, size, and SHA-256 against the intended target partition.
3. Keep the original ROM `boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, and `vbmeta_system.img` unchanged and backed up.
4. Use a bootloader command that temporarily boots the candidate, if the device accepts temporary boot for that image type. Do not flash a new recovery partition during the first test.
5. Test whether the recovery display, touch, USB ADB, MTP, fastbootd, slot switching, dynamic-partition access, and `/data` decryption work.
6. Capture recovery logs and the output of `getprop`, `ls -l /dev/block/by-name`, and `mount` from recovery.
7. If any core test fails, return to the original boot/recovery images and stop. Do not attempt to fix a failed recovery by disabling verified boot or formatting data.
8. Only after a successful temporary-boot test should a maintainer decide whether a permanent installation method is appropriate.

## Root troubleshooting boundary

A recovery image and Magisk root image are separate artifacts. A successful Magisk patch and a successful `fastboot flash boot_b` do not establish that a custom recovery image will fix root. The user’s root issue remains a boot-image activation problem and should be diagnosed independently.

## References

- [Official TeamWin fogos page](https://dl.twrp.me/fogos/)
- [Official LineageOS fogos device page](https://wiki.lineageos.org/devices/fogos/variant2/)
- [Official LineageOS fogos build guide](https://wiki.lineageos.org/devices/fogos/build/variant2/)
- [Official Magisk installation guide](https://topjohnwu.github.io/Magisk/install.html)
