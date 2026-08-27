# Android 17 port notes

## Reference inputs

The target is the Motorola Moto G45 5G (`fogos`) with the user-provided Evolution X 17.0 package. The payload record is documented in [`ROM_INPUT.md`](ROM_INPUT.md). Its relevant images are `boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, and `vbmeta_system.img`; no `init_boot` image is present in the recorded payload.

The maintained LineageOS fogos and SM6375-common sources provide the structural reference for the board: boot header version 3, 4 KiB pages, separated DTBO, DTB in boot, recovery-as-boot, vendor-ramdisk support, Motorola `mot_dp_group`, and the 100,663,296-byte boot/vendor-boot geometry. The TeamWin fogos tree remains a historical TWRP 12.1 reference and is not treated as Android 17 proof.[1] [2] [3]

## Current device-tree adaptation

The VirgoYT tree contains the following device-specific work:

| Area | Implementation |
| --- | --- |
| Kernel | Prebuilt kernel extracted from the inspected Evolution X fogos payload. |
| Boot packaging | Header v3, LZ4 ramdisk, DTB/DTBO integration matching the maintained fogos board conventions, recovery-as-boot, and vendor-ramdisk support. |
| Dynamic partitions | Motorola `mot_dp_group` with `product`, `system`, `system_ext`, and `vendor`; the old QTI group and ODM target were removed. |
| First-stage fstab | `recovery.fstab` is copied into the vendor-ramdisk first-stage location and the vendor fstab location. |
| Encryption | F2FS userdata with inline AES-256, wrapped-key v2, metadata encryption, and `/metadata/vold/metadata_encryption`. |
| Emulated storage | `RECOVERY_SDCARD_ON_DATA := true`, TWRP storage flags, and `/data/media/0` modeling. |
| OTG | Concrete `/dev/block/sdg1` plus `/dev/block/sdg` parent mapping; no wildcard `usbotg-*` aliases. |
| Touch | Android 17 fogos touchscreen modules and dependency metadata under `/lib/modules`, with early-boot insertion in dependency order. |
| Mouse/HID | USB HID, `/dev/input/event*`, `/dev/input/mice`, and `/dev/input/mouse*` support preserved. |
| ADB/sideload | FunctionFS ADB, `update_engine_sideload`, `adbd`, and a clean configfs sideload transition. |

## Important corrections in this audit

The previous tree contained several crossed or stale values. `BOARD_SUPER_PARTITION_GROUPS` used a QTI group instead of the maintained Motorola group; an ODM image target was declared even though the verified payload inventory did not list an ODM partition; the product API/VNDK values were stale; the tree overrode platform/security-patch values; and the AVB section pointed to an AOSP test key. Those overrides were removed or aligned with the maintained fogos source.

The USB init file also contained an unbalanced `${sys.usb.config` expansion at its tail and the sideload transition did not detach existing configfs functions before reusing `f1`. Both were corrected. A stray standalone `*/` token in `ueventd.rc` was removed. Early touch module insertion now follows the same dependency order as `modules.load.recovery`.

## Validation boundary

The repository validator checks the corrected paths, partition group, encryption flags, input rules, module files and order, init property expansions, USB sideload transition, absence of test-key overrides, and the exact boot image size/header. A successful CI run remains a static result. It cannot certify hardware touch, mouse/OTG, user-data decryption, or host-side sideloading. Those must be tested on the exact phone by temporary boot before any permanent operation.

## References

[1] [AOSP vendor boot partitions](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)

[2] [LineageOS fogos device tree](https://github.com/LineageOS/android_device_motorola_fogos)

[3] [LineageOS SM6375-common board configuration](https://github.com/LineageOS/android_device_motorola_sm6375-common)

[4] [TeamWin fogos device tree](https://github.com/TeamWin/android_device_motorola_fogos)
