# Magisk root troubleshooting for fogos Android 17

## Verified evidence

| Check | Result |
| --- | --- |
| Device | Motorola Moto G45 5G, codename `fogos` |
| ROM | Evolution X 17.0, `EvolutionX-17.0-20260812-fogos-12.1-Unofficial` |
| Android | 17, SDK 37, build `CPRA.260605.016` |
| Active slot | `_b` |
| Magisk log device state | `ramdisk=true` |
| Payload images | `boot.img` and `vendor_boot.img`; no `init_boot.img` |
| Stock `boot.img` | 100,663,296 bytes; Android boot image containing a kernel and ramdisk |
| Stock `boot.img` SHA-256 | `9ced0522e6f5237c3fd86ad91bd753d79f5b26ab5443f5200b5940349af79b28` |
| Stock `vendor_boot.img` SHA-256 | `90d3aa8e5efeb77175818d4c29ecef10d1a264a8a2ae5d0f2e851e623dcad7dc` |
| Root test | `su -c id` returns `Permission denied` |

## What the evidence means

The current evidence points to `boot.img` as the first and primary Magisk target. The official Magisk guide lists `boot`, `init_boot`, or `recovery` as patch targets and says that the `Ramdisk` result determines whether the device has a boot ramdisk. The saved device log reports `ramdisk=true`, and the extracted stock `boot.img` contains a kernel and ramdisk. Therefore, the presence of a `vendor_boot.img` partition does **not** by itself prove that Magisk must be installed there.

The SM6375 recovery board configuration contains `BOARD_BUILD_VENDOR_RAMDISK_IMAGE := true` and `BOARD_USES_RECOVERY_AS_BOOT := true`. Those settings describe how a recovery build is assembled; they are not, on their own, proof that a Magisk-patched `vendor_boot.img` should replace the normal boot image. Vendor boot is an Android vendor-ramdisk container and may contain platform, recovery, or kernel-module ramdisk fragments.

The next test should change one variable at a time. Do not patch and flash boot and vendor_boot together as a blind experiment. If a `boot.img` patch still does not activate root, the next useful evidence is the exact Magisk install log plus fastboot slot and unlock-state output—not another random partition flash.

## Safe test sequence

### 1. Preserve the stock images

Keep the exact extracted `boot.img` and `vendor_boot.img` in a separate folder. Do not rename a patched image to `boot.img`, and do not overwrite the stock copy.

### 2. Confirm the bootloader state and active slot

From the computer with the phone in the bootloader, run:

```bash
fastboot devices
fastboot getvar current-slot
fastboot getvar unlocked
fastboot getvar is-userspace
```

Record the complete output. The phone should report the expected active slot, and the bootloader must accept custom images. If `fastboot getvar unlocked` reports that the bootloader is locked, stop before flashing anything.

### 3. Test the patched boot image without changing vendor_boot

Use Magisk 30.7 to patch the exact stock `boot.img` from this ROM. Pull the generated `magisk_patched-*.img` back to the computer and calculate its checksum:

```bash
sha256sum magisk_patched-*.img
```

First try a temporary boot if the Motorola bootloader supports it:

```bash
fastboot boot magisk_patched-*.img
```

After Android starts, verify the active slot and root directly:

```bash
adb shell getprop ro.boot.slot_suffix
adb shell su -c id
```

A working result must return a UID-0 identity, normally beginning with `uid=0(root)`. The Magisk application may need to be opened once after this test, but reinstalling the application cannot create root when `su` is denied.

### 4. Permanently flash only after the temporary test succeeds

If the temporary boot provides root, flash the same verified patched image to the currently active slot. For the recorded current slot `_b`, that is:

```bash
fastboot flash boot_b magisk_patched-*.img
fastboot set_active b
fastboot reboot
```

After booting normally, run `adb shell su -c id` again. Only after this succeeds should the second slot be considered, and it should be patched from the same ROM revision rather than copied from an unrelated build.

## If root still fails

Do not flash a patched `vendor_boot.img` yet. First collect the following information:

```bash
adb shell getprop ro.boot.slot_suffix
adb shell getprop ro.boot.verifiedbootstate
adb shell getprop ro.boot.vbmeta.device_state
adb shell getprop ro.build.version.sdk
adb shell su -c id
```

Also export the **Magisk installation log created immediately after patching**. The large uploaded `magisk_log_2026-08-15T20.23.41.log` is primarily an application/device bug-report log; it contains the useful `ramdisk=true` line but not the complete patch transcript. The missing patch transcript is needed to see whether Magisk injected its binaries and whether it warned about compression, AVB, or an unsupported image format.

If the temporary boot itself returns to fastboot, restore the exact stock `boot.img` to the affected slot and stop testing until the boot-image header and patch log are reviewed. If temporary boot starts normally but `su` remains denied, the likely problem is image selection, image replacement, slot selection, or a device/ROM-specific Magisk compatibility issue—not simply that `vendor_boot.img` exists.

## References

[1]: https://topjohnwu.github.io/Magisk/install.html "Official Magisk installation guide"

[2]: https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions "Android vendor boot partitions"

[3]: https://github.com/topjohnwu/Magisk/issues/9515 "Magisk still uninstalled after patched boot on Android 16"

[4]: https://github.com/topjohnwu/Magisk/issues/9928 "Magisk 30.7 on Android 17 SDK 37"

[1] [Official Magisk installation guide][1].

[2] [Android vendor boot partitions][2].

[3] [Related Android 16 Magisk issue][3].

[4] [Related Android 17 Magisk issue][4].
