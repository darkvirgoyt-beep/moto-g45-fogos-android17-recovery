#!/usr/bin/env python3
"""Static safety gates for the VirgoYT fogos Android 17 recovery tree."""
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
DEVICE = ROOT / "device/motorola/fogos"
EXPECTED_BOOT_SIZE = 100_663_296


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing file: {rel}")
    return path.read_text(errors="replace")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {needle!r} in {where}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        raise AssertionError(f"forbidden stale/crossed value {needle!r} in {where}")


def check_prop_expansions(text: str, where: str) -> None:
    for number, line in enumerate(text.splitlines(), 1):
        if "${" in line and line.count("${") != line.count("}"):
            raise AssertionError(f"unbalanced property expansion in {where}:{number}: {line}")


def check_no_stray_comment_tokens(text: str, where: str) -> None:
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip() in {"/*", "*/"}:
            raise AssertionError(f"stray comment token in {where}:{number}")


board = read("device/motorola/fogos/BoardConfig.mk")
fstab = read("device/motorola/fogos/recovery.fstab")
flags = read("device/motorola/fogos/recovery/root/system/etc/twrp.flags")
device_mk = read("device/motorola/fogos/device.mk")
init_qcom = read("device/motorola/fogos/recovery/root/init.recovery.qcom.rc")
init_usb = read("device/motorola/fogos/recovery/root/init.recovery.usb.rc")
ueventd = read("device/motorola/fogos/recovery/root/vendor/ueventd.rc")
workflow = read(".github/workflows/twrp-build-release.yml")
modules_load = read("device/motorola/fogos/modules.load.recovery")
modules_dep = read("device/motorola/fogos/prebuilt/modules/modules.dep")

# Android 17 device-layout and userdata invariants.
require(board, "BOARD_BOOT_HEADER_VERSION := 3", "BoardConfig.mk")
require(board, "BOARD_KERNEL_SEPARATED_DTBO := true", "BoardConfig.mk")
require(board, "BOARD_RAMDISK_USE_LZ4 := true", "BoardConfig.mk")
require(board, "BOARD_INCLUDE_RECOVERY_DTBO := true", "BoardConfig.mk")
require(board, "BOARD_INCLUDE_DTB_IN_BOOTIMG := true", "BoardConfig.mk")
require(board, "BOARD_BOOTIMAGE_PARTITION_SIZE := 100663296", "BoardConfig.mk")
require(board, "BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 100663296", "BoardConfig.mk")
require(board, "BOARD_DTBOIMG_PARTITION_SIZE := 25165824", "BoardConfig.mk")
require(board, "BOARD_USES_RECOVERY_AS_BOOT := true", "BoardConfig.mk")
require(board, "BOARD_BUILD_VENDOR_RAMDISK_IMAGE := true", "BoardConfig.mk")
require(board, "RECOVERY_SDCARD_ON_DATA := true", "BoardConfig.mk")
require(board, "BOARD_SUPER_PARTITION_GROUPS := mot_dp_group", "BoardConfig.mk")
require(board, "BOARD_MOT_DP_GROUP_PARTITION_LIST := product system system_ext vendor", "BoardConfig.mk")
for stale in ("qti_dynamic_partitions", "TARGET_COPY_OUT_ODM", "BOARD_ODMIMAGE_FILE_SYSTEM_TYPE", "testkey_rsa2048.pem", "PLATFORM_SECURITY_PATCH", "PLATFORM_VERSION :="):
    forbid(board, stale, "BoardConfig.mk")

require(fstab, "/dev/block/bootdevice/by-name/userdata", "recovery.fstab")
require(fstab, "/data", "recovery.fstab")
require(fstab, "fileencryption=aes-256-xts:aes-256-cts:v2+inlinecrypt_optimized+wrappedkey_v0", "recovery.fstab")
require(fstab, "keydirectory=/metadata/vold/metadata_encryption", "recovery.fstab")
require(fstab, "metadata_encryption=aes-256-xts:wrappedkey_v0", "recovery.fstab")
require(fstab, "/dev/block/sdg1", "recovery.fstab")
for stale in ("usbotg-*", "/storage/usbotg-"):
    forbid(fstab, stale, "recovery.fstab")

require(flags, "/data                  f2fs", "twrp.flags")
require(flags, "flags=storage;settingsstorage", "twrp.flags")
require(flags, "keydirectory=/metadata/vold/metadata_encryption", "twrp.flags")
require(flags, "/usb-otg               vfat", "twrp.flags")
require(flags, "/dev/block/sdg        ", "twrp.flags")

# Runtime/package invariants.
require(device_mk, "update_engine_sideload", "device.mk")
require(device_mk, "$(TARGET_COPY_OUT_RECOVERY)/root/lib/modules/", "device.mk")
require(device_mk, "PRODUCT_SHIPPING_API_LEVEL := 34", "device.mk")
require(device_mk, "PRODUCT_TARGET_VNDK_VERSION := 34", "device.mk")
for stale in ("TARGET_COPY_OUT_ODM", "PRODUCT_SHIPPING_API_LEVEL := 30", "PRODUCT_TARGET_VNDK_VERSION := 30", "    odm "):
    forbid(device_mk, stale, "device.mk")

require(init_usb, "sys.usb.config=sideload", "init.recovery.usb.rc")
require(init_usb, "ffs.adb", "init.recovery.usb.rc")
require(init_usb, "write /config/usb_gadget/g1/UDC \"none\"", "init.recovery.usb.rc")
require(init_usb, "rm /config/usb_gadget/g1/configs/b.1/f1", "init.recovery.usb.rc")
check_prop_expansions(init_usb, "init.recovery.usb.rc")
require(ueventd, "/dev/input/event*", "ueventd.rc")
require(ueventd, "/dev/input/mice", "ueventd.rc")
require(ueventd, "/dev/input/mouse*", "ueventd.rc")
check_no_stray_comment_tokens(ueventd, "ueventd.rc")
check_prop_expansions(init_qcom, "init.recovery.qcom.rc")
check_no_stray_comment_tokens(init_qcom, "init.recovery.qcom.rc")

# The metadata list is consumed by module loaders with dependency handling;
# the explicit raw insmod list must instead be dependency-first.
modules = [line.strip() for line in modules_load.splitlines() if line.strip() and not line.startswith("#")]
for module in modules:
    if not (DEVICE / "prebuilt/modules" / module).is_file():
        raise AssertionError(f"missing recovery module: {module}")
    require(init_qcom, f"insmod /lib/modules/{module}", "init.recovery.qcom.rc")
actual_order = [line.split("/lib/modules/", 1)[1].strip() for line in init_qcom.splitlines() if "insmod /lib/modules/" in line]
expected_raw_order = ["mmi_annotate.ko", "mmi_info.ko", "sensors_class.ko", "exfat.ko", "mmi-smbcharger-iio.ko", "chipone_tddi_v2_mmi.ko", "ilitek_v3_mmi.ko"]
if actual_order[: len(expected_raw_order)] != expected_raw_order:
    raise AssertionError(f"unexpected dependency-safe early-boot module order: {actual_order}")
expected_metadata_order = ["mmi_info.ko", "mmi_annotate.ko", "sensors_class.ko", "exfat.ko", "mmi-smbcharger-iio.ko", "chipone_tddi_v2_mmi.ko", "ilitek_v3_mmi.ko"]
if modules != expected_metadata_order:
    raise AssertionError(f"modules.load.recovery drifted: {modules}")
for module in ("chipone_tddi_v2_mmi.ko", "ilitek_v3_mmi.ko"):
    require(modules_load, module, "modules.load.recovery")
require(modules_dep, "mmi_info.ko: /lib/modules/mmi_annotate.ko", "modules.dep")
require(modules_dep, "chipone_tddi_v2_mmi.ko: /lib/modules/sensors_class.ko", "modules.dep")

# Workflow/release invariants.
require(workflow, "TWRP_MANIFEST_BRANCH: twrp-12.1", "workflow")
require(workflow, "validate_fogos_recovery.py", "workflow")
require(workflow, "timeout-minutes: 360", "workflow")
require(workflow, "inputs.publish_release == true", "workflow")
for stale in ("Build fogos recovery baseline", "TWRP_MANIFEST_BRANCH: twrp-14.1", "testkey_rsa2048.pem"):
    forbid(workflow, stale, "workflow")

if len(sys.argv) > 1:
    image = Path(sys.argv[1])
    data = image.read_bytes()
    if data[:8] != b"ANDROID!":
        raise AssertionError("image does not contain ANDROID! boot magic")
    if len(data) != EXPECTED_BOOT_SIZE:
        raise AssertionError(f"image size is {len(data)}; expected {EXPECTED_BOOT_SIZE} bytes")
    if len(data) < 44:
        raise AssertionError("image is too short for Android boot header")
    if struct.unpack_from("<I", data, 40)[0] < 3:
        raise AssertionError("image is not Android boot-header v3+")
    if struct.unpack_from("<I", data, 8)[0] == 0 or struct.unpack_from("<I", data, 16)[0] == 0:
        raise AssertionError("image has empty kernel or ramdisk payload")
    print(f"image={image}")
    print(f"image_size={len(data)}")

print("fogos recovery static validation: PASS")
print("NOTE: static validation cannot prove physical touchscreen, encryption, mouse, or sideload behavior")
