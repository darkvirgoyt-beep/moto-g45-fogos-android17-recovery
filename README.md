# Moto G45 5G (fogos) Android 17 Recovery Project

This repository is a research and build workspace for developing a recovery environment for the Motorola moto g45 5G, codename `fogos`, running an unofficial Evolution X Android 17 build. The project is intentionally conservative: no recovery image is considered flash-ready until it has been built from verified sources and tested by temporary boot on the target device.

## Current device context

The available evidence identifies the device as a Motorola moto g45 5G with Android 17, build `CPRA.260605.016`, kernel `5.4.302-moto-KAGE`, and an A/B partition layout. The user's ROM package is verified as `EvolutionX-17.0-20260812-fogos-12.1-Unofficial`. Its signed `payload.bin` contains `boot.img` and `vendor_boot.img`, but no `init_boot.img`; the exact sizes and archive checksum are recorded in [`docs/ROM_INPUT.md`](docs/ROM_INPUT.md).

## Project status

The existing public fogos TWRP device tree is based on TWRP 12.1 and is not assumed to be compatible with Android 17. The verified ROM layout now confirms that both `boot` and `vendor_boot` are present, so recovery placement and vendor ramdisk handling remain to be validated. No verified OrangeFox Android 17 build for this device has been identified. This repository documents the baseline and the porting gaps; it does not yet publish a flash-ready image.

## Safety policy

The original ROM package, stock/recovery images, and device backups must remain untouched. Experimental recovery images must be temporary-boot tested before any partition is flashed. Do not relock the bootloader while a custom ROM is installed. Do not flash an image from another Motorola model or variant.

## Required inputs

The following inputs are required before a build configuration can be finalized:

| Input | Purpose |
| --- | --- |
| Exact ROM filename and download URL | Confirms the Android 17 source and build revision |
| `getprop` device identifiers | Confirms model, hardware, codename, and variant |
| `boot.img`, `vendor_boot.img`, `vbmeta.img`, and `dtbo.img` from the exact ROM | Establishes the boot and recovery layout |
| Kernel source or ROM kernel configuration | Required if recovery needs kernel or driver changes |
| Current recovery behavior | Determines whether data can be mounted/decrypted and whether ADB works |
| Desired feature set | Defines whether the target is TWRP-style flashing, OrangeFox UI, or a minimal sideload recovery |

## References

- Official device information: https://wiki.lineageos.org/devices/fogos/variant2/
- Existing fogos TWRP device tree: https://github.com/TeamWin/android_device_motorola_fogos
- Magisk installation documentation: https://topjohnwu.github.io/Magisk/install.html
