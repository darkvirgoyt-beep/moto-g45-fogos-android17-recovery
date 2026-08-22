#!/usr/bin/env python3
"""Static safety gates for the VirgoYT fogos Android 17 recovery tree."""
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
DEVICE = ROOT / "device/motorola/fogos"

def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing file: {rel}")
    return path.read_text(errors="replace")

def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {needle!r} in {where}")

board = read("device/motorola/fogos/BoardConfig.mk")
fstab = read("device/motorola/fogos/recovery.fstab")
flags = read("device/motorola/fogos/recovery/root/system/etc/twrp.flags")
device_mk = read("device/motorola/fogos/device.mk")
init_qcom = read("device/motorola/fogos/recovery/root/init.recovery.qcom.rc")
init_usb = read("device/motorola/fogos/recovery/root/init.recovery.usb.rc")
ueventd = read("device/motorola/fogos/recovery/root/vendor/ueventd.rc")
modules_load = read("device/motorola/fogos/modules.load.recovery")
modules_dep = read("device/motorola/fogos/prebuilt/modules/modules.dep")

require(board, "RECOVERY_SDCARD_ON_DATA := true", "BoardConfig.mk")
require(fstab, "/dev/block/bootdevice/by-name/userdata", "recovery.fstab")
require(fstab, "/data", "recovery.fstab")
require(fstab, "fileencryption=aes-256-xts:aes-256-cts:v2+inlinecrypt_optimized+wrappedkey_v0", "recovery.fstab")
require(fstab, "keydirectory=/metadata/vold/metadata_encryption", "recovery.fstab")
require(fstab, "metadata_encryption=aes-256-xts:wrappedkey_v0", "recovery.fstab")
require(fstab, "/dev/block/sdg1", "recovery.fstab")
if "usbotg-*" in fstab or "/storage/usbotg-" in fstab:
    raise AssertionError("legacy wildcard USB-OTG entries remain in recovery.fstab")
require(flags, "/data                  f2fs", "twrp.flags")
require(flags, "flags=storage;settingsstorage", "twrp.flags")
require(flags, "keydirectory=/metadata/vold/metadata_encryption", "twrp.flags")
require(flags, "/usb-otg               vfat", "twrp.flags")
require(flags, "/dev/block/sdg        ", "twrp.flags")
require(device_mk, "update_engine_sideload", "device.mk")
require(device_mk, "$(TARGET_COPY_OUT_RECOVERY)/root/lib/modules/", "device.mk")
require(init_usb, "sideload", "init.recovery.usb.rc")
require(init_usb, "ffs.adb", "init.recovery.usb.rc")
require(ueventd, "/dev/input/event*", "ueventd.rc")
require(ueventd, "/dev/input/mice", "ueventd.rc")
require(ueventd, "/dev/input/mouse*", "ueventd.rc")

modules = [line.strip() for line in modules_load.splitlines() if line.strip() and not line.startswith("#")]
for module in modules:
    if not (DEVICE / "prebuilt/modules" / module).is_file():
        raise AssertionError(f"missing recovery module: {module}")
    require(init_qcom, f"insmod /lib/modules/{module}", "init.recovery.qcom.rc")
for module in ("chipone_tddi_v2_mmi.ko", "ilitek_v3_mmi.ko"):
    require(modules_load, module, "modules.load.recovery")
for dependency in ("/lib/modules/sensors_class.ko",):
    require(modules_dep, dependency, "modules.dep")

if len(sys.argv) > 1:
    image = Path(sys.argv[1])
    data = image.read_bytes()
    if data[:8] != b"ANDROID!":
        raise AssertionError("image does not contain ANDROID! boot magic")
    if len(data) > 100663296:
        raise AssertionError(f"image exceeds 96 MiB limit: {len(data)}")
    if struct.unpack_from("<I", data, 40)[0] < 3:
        raise AssertionError("image is not Android boot-header v3+")
    if struct.unpack_from("<I", data, 8)[0] == 0 or struct.unpack_from("<I", data, 16)[0] == 0:
        raise AssertionError("image has empty kernel or ramdisk payload")
    print(f"image={image}")
    print(f"image_size={len(data)}")

print("fogos recovery static validation: PASS")
print("NOTE: static validation cannot prove physical touchscreen, encryption, mouse, or sideload behavior")
