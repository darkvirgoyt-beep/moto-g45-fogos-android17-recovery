# Android 17 porting status

## Baseline

The repository currently contains the public `fogos` TWRP device tree as a baseline under `device/motorola/fogos`. The baseline is derived from the TeamWin repository at commit `5851454778947504335184ef0559903acbd69e71`, dated 2024-05-09, and targets the TWRP 12.1 build system.

The baseline is not being represented as an Android 17 recovery. It is a starting point for comparison only. Its configuration includes a 96 MiB `boot` image, a 96 MiB `init_boot` size, a 96 MiB `vendor_boot` size, A/B partitions, QCOM FBE settings, and recovery-as-boot settings. These values must be checked against the user's exact Android 17 payload before they are reused.

## Current evidence from the user's device

The device reports Android 17 and build `CPRA.260605.016`. The extracted Evolution X payload contains `boot.img` and `vendor_boot.img`, and Magisk successfully patched `boot.img`. Fastboot reported `OKAY` for sending and writing the patched image to `boot_b`. Termux nevertheless reports that `su` cannot obtain root. This indicates that the recovery project and the Magisk investigation are related but not yet proven to have the same boot-image requirements.

## Required inputs before an Android 17 build

The following must be verified from the exact ROM package currently installed:

1. The complete ROM filename, download URL, maintainer, and checksum.
2. `ro.product.model`, `ro.product.device`, `ro.boot.hardware`, `ro.build.version.incremental`, and `ro.build.version.security_patch`.
3. The extracted `boot.img`, `vendor_boot.img`, `vbmeta.img`, and `dtbo.img` provenance and SHA-256 checksums.
4. The kernel source or a matching kernel configuration and module set.
5. Whether the ROM expects recovery-as-boot, a vendor-boot recovery ramdisk, or the stock/ROM recovery image.
6. Whether the current recovery can mount and decrypt `/data`, expose ADB, and sideload the original ROM ZIP.

## Safe test order

The first test for any new recovery artifact must be a temporary boot from the bootloader. The artifact must not be flashed to a permanent partition until it boots, the screen and touch work, ADB is available, and the recovery behavior is understood. Keep the original boot, vendor-boot, vbmeta, and dtbo images outside the repository as recovery material.

No experimental Android 17 image is currently flash-ready. No claim of OrangeFox compatibility is made by this repository.
