# Safe Magisk installation on fogos

## Important limitation

This recovery tree does not contain a Magisk binary, and a recovery build cannot safely invent one. Magisk must be obtained from the official project or supplied by the user. The repository includes a helper that downloads the official APK-as-ZIP and copies it to the phone; the actual installation is performed by TWRP's existing **Install ZIP** flow.

The supplied `Magisk-v30.7.zip` is bundled at `device/motorola/fogos/prebuilt/magisk/Magisk-v30.7.zip` and is checksum-verified by the source validator (`e0d32d2123532860f97123d927b1bb86c4e08e6fd8a48bfc6b5bee0afae9ebd5`).

## Recommended flow

1. Boot this recovery temporarily with `fastboot boot <recovery-image>`. Do not use `fastboot flash recovery`: the inspected fogos layout has **no standalone recovery partition**. It uses recovery-as-boot with A/B `boot` and `vendor_boot` partitions.
2. Unlock the phone and decrypt `/data` in TWRP using the existing lock-screen credential. Do not format or wipe Data.
3. From a computer with `adb` available, run:

   ```bash
   tools/install_magisk_fogos.sh
   ```

   To use a package already downloaded:

   ```bash
   tools/install_magisk_fogos.sh --zip /path/to/Magisk-v30.7.zip
   ```

   The helper validates that the APK is a ZIP, waits for ADB, and stages it at `/sdcard/Download/Magisk-*.zip`.
4. In TWRP select **Install**, choose the staged Magisk ZIP, and swipe to confirm. This is the same installer path as any ZIP selected from any mounted directory.
5. Reboot Android and open Magisk once. Verify root with `adb shell su -c id`.

## Why this does not delete old Magisk data

The request to remove Magisk data “stored anywhere” is unsafe. Blindly deleting `/data/adb`, module directories, caches, or files found by a broad search can remove modules, user data, app data, and recovery logs, and it cannot repair an incorrectly patched boot image. This feature therefore performs **no arbitrary deletion**. If a clean removal is needed, use Magisk's own uninstall option or remove a specifically identified module from Magisk/TWRP after making a backup.

## If root is still missing

Magisk installation through recovery is not equivalent to flashing a patched boot image on this device. The verified payload reports a boot ramdisk and no `init_boot.img`; the primary Magisk target is the exact stock `boot.img` for the active ROM slot. Patch that image in the Magisk app, preserve the stock image, and test it with:

```bash
fastboot getvar current-slot
fastboot boot magisk_patched-*.img
adb shell su -c id
```

Only after a successful temporary test should an active-slot `boot_<slot>` flash be considered. Never flash `recovery`, and do not patch `boot` and `vendor_boot` together as an experiment.

## ADB startup diagnosis

The recovery USB configuration now keeps the normal ADB and sideload paths separate and waits for FunctionFS readiness before connecting the gadget. If the host waits, collect:

```bash
adb kill-server
adb start-server
adb wait-for-device
adb shell getprop sys.usb.config
adb shell getprop sys.usb.state
adb shell getprop sys.usb.ffs.ready
```

A host-side timeout is not a reason to erase userdata or flash another partition. Save `recovery.log` and the exact USB properties first.
