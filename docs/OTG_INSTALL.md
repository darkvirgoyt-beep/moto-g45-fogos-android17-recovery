# OTG detection and ZIP installation on fogos

The recovery exposes the audited Moto G45 OTG block mapping as `/dev/block/sdg1` and the TWRP storage mount as `/usb-otg`. The fstab entry is non-blocking (`nofail`), so recovery startup does not wait indefinitely when no USB drive is attached.

## TWRP interface

1. Connect a FAT32 USB drive through a compatible USB-C OTG adapter.
2. In TWRP open **Mount** and select **USB-OTG**.
3. Open **Install**, choose `/usb-otg/`, select the ZIP, and swipe to confirm.

## Command helper

The recovery image also includes `/system/bin/otg-install`. With a USB drive connected, running it without an argument detects and mounts OTG and lists ZIP files:

```sh
/system/bin/otg-install
```

To pass one specific ZIP to TWRP's installer:

```sh
/system/bin/otg-install /usb-otg/Magisk-v30.7.zip
```

The helper never formats, wipes, or automatically selects a package. It validates that the selected file is a ZIP, then delegates the actual installation to TWRP's confirmation flow.

If OTG is not detected, test the adapter and drive first. The drive should be FAT32 and the phone must be in recovery with USB host/OTG power available. A USB mouse can be used as a fallback if the touchscreen is not working.
