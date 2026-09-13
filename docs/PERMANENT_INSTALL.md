# Permanent installation on Moto G45 5G (`fogos`)

## Important layout warning

This device tree uses **recovery-as-boot**. It declares `BOARD_USES_RECOVERY_AS_BOOT := true` and `TARGET_NO_RECOVERY := true`, so this build does **not** target a standalone `recovery` partition. The recovery image is an Android boot image and the permanent target, when the device-specific procedure is confirmed, is a slot-specific `boot` partition.

Do **not** run `fastboot flash recovery ...` for this build. Do **not** flash this recovery image to `vendor_boot`, `dtbo`, `vbmeta`, or `bootloader`. A wrong-partition flash can make the phone fail to boot or prevent normal recovery access.

> Permanent flashing is reversible only if the matching stock images and the active slot are preserved first. The procedure below is for the exact Moto G45 5G (`fogos`) and the tested image from the corresponding release; do not reuse it on another Motorola model or ROM layout.

## Required files and checks

Download the recovery image, checksum, and build-info files from the [storage/sideload release][1]. Confirm that the image hash matches the checksum before connecting the phone.

| Item | Requirement |
| --- | --- |
| Device | Motorola Moto G45 5G, codename `fogos` |
| Bootloader | Unlocked, with fastboot working |
| Image | `virgoyt-fogos-twrp-80efbc0378fa7745d6af4f5bf079d601d06894ba.img` |
| Current commit | `80efbc0378fa7745d6af4f5bf079d601d06894ba` |
| Target layout | A/B `boot_a` or `boot_b`; no standalone `recovery` partition |
| Safety state | The image has already been temporarily boot-tested on this phone |

Verify the checksum on a computer:

```bash
sha256sum virgoyt-fogos-twrp-80efbc0378fa7745d6af4f5bf079d601d06894ba.img
cat fogos-twrp-boot.sha256
```

The two SHA-256 values must be identical. If they differ, stop and download the image again.

## 1. Preserve stock recovery and boot images

Before flashing, keep the original ROM package and stock `boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, and `vbmeta_system.img` in a separate directory. Do not overwrite or delete those backups.

If the stock `boot.img` came from the installed ROM, record its SHA-256:

```bash
sha256sum stock/boot.img stock/vendor_boot.img stock/dtbo.img
```

The recovery image is not a replacement for `vendor_boot.img`. Keep the stock `vendor_boot.img` available for restoration.

## 2. Confirm the phone and active slot

Reboot to the bootloader and verify the device is detected:

```bash
adb reboot bootloader
fastboot devices
fastboot getvar product 2>&1
fastboot getvar current-slot 2>&1
fastboot getvar has-slot:boot 2>&1
```

Continue only if `product` identifies `fogos` and `has-slot:boot` reports `yes`. Record whether the active slot is `a` or `b`.

The phone must remain bootloader-unlocked. Never relock the bootloader after installing a custom recovery or custom ROM.

## 3. Flash only the active boot slot

Use the slot reported by `fastboot getvar current-slot`. Replace `<slot>` with `a` or `b`; do not guess the slot.

```bash
fastboot flash boot_<slot> virgoyt-fogos-twrp-80efbc0378fa7745d6af4f5bf079d601d06894ba.img
fastboot getvar current-slot 2>&1
fastboot reboot recovery
```

For example, if the command reported `current-slot: b`, the target command is:

```bash
fastboot flash boot_b virgoyt-fogos-twrp-80efbc0378fa7745d6af4f5bf079d601d06894ba.img
```

Do **not** flash both slots unless you have a matching, tested recovery image and a tested slot-switch recovery plan. Keeping the other slot stock provides a rollback path.

## 4. Verify recovery after flashing

After `fastboot reboot recovery`, verify the following before changing any other partition:

1. Finger touch operates across menus, sliders, the file browser, and the keyboard.
2. `/data` mounts and decrypts with the existing device credential.
3. Internal Storage reports a nonzero size and `/data/media/0` is visible.
4. `/data` can be unmounted and mounted again without a reboot.
5. USB-OTG storage mounts and unmounts correctly.
6. ADB starts normally after recovery boot.
7. A current desktop `adb sideload` can send a known-good, non-destructive ZIP.
8. Cancelling sideload returns to normal recovery USB mode.
9. Rebooting to Android preserves the existing files.

Do not format data, wipe data, erase userdata, or disable verified boot as a troubleshooting step.

## Rollback

If the phone does not boot normally or recovery is unusable, return to the bootloader and restore the stock boot image to the same slot:

```bash
adb reboot bootloader
fastboot getvar current-slot 2>&1
fastboot flash boot_<slot> stock/boot.img
fastboot reboot
```

If the active slot changed, restore the stock image to the slot that is actually selected. Keep the stock `vendor_boot.img`, `dtbo.img`, and signed verification images unchanged unless a device-specific restoration procedure proves that another partition is damaged.

## Why there is no `recovery` command

The checked-in board configuration uses recovery-as-boot and disables a separate recovery image target. Therefore, a command such as `fastboot flash recovery recovery.img` is not the correct installation method for this project. The exact partition name must always be confirmed with fastboot before flashing.

## References

[1]: https://github.com/darkvirgoyt-beep/moto-g45-fogos-android17-recovery/releases/tag/virgoyt-fogos-twrp-storage-sideload-80efbc0 "VirgoYT Fogos TWRP storage and sideload release"

[2]: https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions "Android vendor boot partitions"

[3]: https://source.android.com/docs/core/architecture/bootloader/boot-image-header "Android boot image header"
