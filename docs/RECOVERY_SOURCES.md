# Recovery source assessment

## Official references

TeamWin publishes an official `fogos` recovery based on the TWRP 12.1-era device tree. That image is a useful historical reference for the Moto G34/G45 family, but it is not evidence of Android 17 compatibility.[1]

The maintained LineageOS fogos tree and its SM6375-common board configuration provide the modern structural reference: boot header version 3, separated DTBO, DTB in boot, recovery-as-boot, vendor-ramdisk support, Motorola `mot_dp_group`, and the current boot/vendor-boot geometry. They do not certify the user’s unofficial Evolution X Android 17 build.[2] [3]

AOSP documents that header-v3 devices relocate vendor-specific information, including vendor ramdisk and DTB handling, into `vendor_boot`, and that recovery fstab belongs in the vendor-ramdisk first-stage location. The VirgoYT tree follows those packaging rules while using the user-provided fogos payload inputs.[4]

## VirgoYT adaptation

The repository’s current source adaptation includes the inspected fogos Android 17 kernel and recovery modules, Android 17 FBE/wrapped-key metadata, emulated-storage modeling, concrete OTG block-device mapping, early-boot touchscreen module insertion, USB HID/mouse permissions, and an explicit configfs sideload transition. The active workflow builds the image and runs static validation before any artifact can be released.

The audit also removed crossed configuration that had survived earlier builds: the stale QTI dynamic group and nonexistent ODM target, stale API/VNDK values, fabricated platform/security-patch overrides, AOSP test-key vbmeta synthesis, a malformed USB init property expansion, incomplete sideload function cleanup, a stray ueventd comment token, duplicate inactive baseline workflows, and obsolete pre-release documentation.

## Certification boundary

The public image remains an unofficial temporary-boot candidate. Static CI can verify source structure, image header/size, module packaging, partition metadata, and init configuration. It cannot press the target screen, connect an OTG mouse, decrypt the user’s existing `/data`, or prove a real host-to-phone ADB sideload. Those are physical acceptance tests and must pass before any permanent flash is considered.

## References

[1] [TeamWin fogos device tree](https://github.com/TeamWin/android_device_motorola_fogos)

[2] [LineageOS fogos device tree](https://github.com/LineageOS/android_device_motorola_fogos)

[3] [LineageOS SM6375-common board configuration](https://github.com/LineageOS/android_device_motorola_sm6375-common)

[4] [AOSP vendor boot partitions](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)
