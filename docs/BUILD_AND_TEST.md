# Build and validation guide

## Scope

This repository builds an unofficial Motorola Moto G45 5G (`fogos`) recovery candidate using the inspected Android 17 / Evolution X 17.0 kernel, vendor-ramdisk module set, partition geometry, fstab, and encryption metadata. The recovery framework comes from the current TWRP manifest selected by the active workflow. The image is not called hardware-certified until it has been tested on the exact phone.

## Reproducible build

The active workflow is `.github/workflows/twrp-build-release.yml`. It checks out the device tree, initializes the pinned TWRP `twrp-12.1` manifest branch, copies the fogos tree, builds `bootimage` and `adbd`, runs `tools/validate_fogos_recovery.py`, records SHA-256 metadata, and uploads the image as an artifact. To create a direct-download release, open **Actions → VirgoYT fogos TWRP build → Run workflow**, leave **Publish a direct-download GitHub Release** enabled, and choose a unique release tag. After the build passes, open the repository’s **Releases** page and download the `.img`, `.sha256`, and build-info files from that release; the release asset is not the temporary Actions artifact ZIP. The workflow never flashes a phone or erases userdata.

For a local build, use the same manifest and product target as the workflow, then run the validator against the generated image:

```bash
repo init --depth=1 \
  -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git \
  -b twrp-12.1
repo sync -c --no-clone-bundle --no-tags --optimized-fetch -j2
source build/envsetup.sh
lunch twrp_fogos-eng
mka bootimage adbd -j"$(nproc)"
python3 tools/validate_fogos_recovery.py out/target/product/fogos/boot.img
```

## Static checks

The validator checks Android boot-header magic/version and requires the generated image to be non-empty and no larger than the verified 100,663,296-byte boot partition when an image is supplied. It also checks the Motorola dynamic-partition group, `/data` and wrapped-key encryption flags, emulated-storage setup, concrete OTG mapping, touchscreen module files and dependency order, input permissions, ADB/sideload FunctionFS wiring, balanced init property expansions, removal of stale test-key and version overrides, and absence of duplicate baseline workflow references.

## Safe physical test order

First preserve the original ROM archive and the stock `boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, and `vbmeta_system.img` outside the repository. Verify the candidate SHA-256. From the bootloader, use `fastboot boot` with the candidate; do not flash it at this stage.

In recovery, test finger touch across menus and sliders, then test a USB mouse through OTG. Mount Data using the existing lock-screen credential. Confirm that Internal Storage is not zero megabytes and that `/data/media/0` is visible. Test external OTG storage, normal ADB, ADB sideload with a known-good non-destructive ZIP, successful ZIP verification/install, and a clean reboot back into Android. Confirm that existing user files remain present.

If any test fails, remain on temporary boot, save `recovery.log`, record the exact build tag and error text, and reboot normally. Never use Format Data, Wipe Data, erase userdata, disable verified boot, or flash a random partition to fix a failed test.

## Permanent-flash gate

Permanent flashing is not certified by the build system. It is considered only after every physical test passes on the target phone and the exact recovery-as-boot/slot procedure has been confirmed from the installed ROM’s partition map. Do not copy commands from another Motorola model or assume that a `boot`, `vendor_boot`, or slot name is interchangeable.

## Root boundary

Magisk root and recovery are separate artifacts. A recovery build cannot prove that a Magisk-patched boot image will activate `su`. Diagnose Magisk independently with a temporary `fastboot boot` test and preserve the original boot image.

## References

- [AOSP vendor boot partitions](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)
- [LineageOS fogos device tree](https://github.com/LineageOS/android_device_motorola_fogos)
- [LineageOS SM6375-common board configuration](https://github.com/LineageOS/android_device_motorola_sm6375-common)
- [TeamWin fogos device tree](https://github.com/TeamWin/android_device_motorola_fogos)
- [Official Magisk installation guide](https://topjohnwu.github.io/Magisk/install.html)
