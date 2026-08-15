# Device input collection

Place only non-sensitive technical inputs in this directory. Do not add IMEI numbers, serial numbers, bootloader unlock tokens, personal account data, or private logs containing them.

## Required command output

Run these commands in Termux while Android is booted and paste the output into `device-props.txt`:

```sh
getprop ro.product.model
getprop ro.product.device
getprop ro.boot.hardware
getprop ro.boot.slot_suffix
getprop ro.build.version.release
getprop ro.build.version.incremental
getprop ro.build.version.security_patch
getprop ro.boot.verifiedbootstate
```

## Required ROM metadata

Record the full ROM filename, download URL, maintainer or source page, and the SHA-256 checksum if available. Record whether the payload was extracted from the exact ROM currently installed.

## Required images

Keep large images outside Git until their purpose and provenance are verified. Record their SHA-256 checksums and source paths for:

- `boot.img`
- `vendor_boot.img`
- `vbmeta.img`
- `dtbo.img`
- the recovery image or recovery partition image, if supplied by the ROM maintainer

## Test observations

Record whether the current recovery can boot, whether ADB is available, whether `/data` can be decrypted, and whether the recovery can sideload the original ROM package. Never test an experimental recovery by flashing it before a temporary-boot test has succeeded.
