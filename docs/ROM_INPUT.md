# Verified ROM input

## Package identity

The ROM provided by the user is the unofficial Evolution X package for the Motorola Moto G45 5G (`fogos`):

```text
EvolutionX-17.0-20260812-fogos-12.1-Unofficial
```

The package is presented as a `.jar` on Google Drive and DevUploads and as a `.zip` on Pixeldrain. The archive is a ZIP-compatible Android OTA package containing `payload.bin` and `payload_properties.txt`.

The Google Drive file metadata is:

| Field | Value |
|---|---|
| Drive file ID | `1sFaZx6dqdWbmKyK6MxObTOpwV5iv_Oe2` |
| Size | `2,910,003,709` bytes |
| MIME type | `application/java-archive` |
| Modified time | `2026-08-15T13:18:46.614Z` |
| Archive SHA-256 | `00a4c74ea803508071d15e5bb692d81c6b448d0057cf75d5f7bdbf055dc56b43` |

## Payload layout

The `payload.bin` is version 2 and contains the following partitions:

```text
abl bluetooth boot devcfg dsp dtbo fsg hyp keymaster logo modem product
prov qupfw rpm storsec system system_ext tz uefisecapp vbmeta
vbmeta_system vendor vendor_boot vendor_dlkm xbl xbl_config
```

The relevant extracted image sizes are:

| Image | Size |
|---|---:|
| `boot.img` | 100,663,296 bytes |
| `vendor_boot.img` | 100,663,296 bytes |
| `dtbo.img` | 25,165,824 bytes |
| `vbmeta.img` | 8,192 bytes |
| `vbmeta_system.img` | 4,096 bytes |

There is **no `init_boot` partition** in this payload. The payload includes both `boot` and `vendor_boot`, so Android 17 recovery work must explicitly determine whether recovery is packaged in `vendor_boot`, a recovery-as-boot layout, or another ROM-specific arrangement. The presence of both images is not sufficient evidence that either one is safe to flash as a recovery image.

## Current device evidence

The user’s device reports Android 17, build `CPRA.260605.016`, and the active slot is `_b`. Magisk 30.7 successfully patches the extracted `boot.img`. Fastboot reports successful sending and writing of the generated image to `boot_b`, but `su -c id` still cannot obtain root. This project therefore treats the current boot/root behavior as unresolved and does not publish a flash-ready recovery or root image.

## Source links

- [DevUploads ROM page](https://devuploads.com/c0uhg7xj44yg)
- [Pixeldrain ROM page](https://pixeldrain.com/u/oVyv9zBK)
- [Google Drive ROM file](https://drive.google.com/file/d/1sFaZx6dqdWbmKyK6MxObTOpwV5iv_Oe2/view)
