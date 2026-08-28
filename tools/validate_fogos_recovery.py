#!/usr/bin/env python3
"""Safety gates for the VirgoYT fogos Android 17 recovery tree and image."""
from pathlib import Path
import gzip
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEVICE = ROOT / "device/motorola/fogos"
MAX_BOOT_SIZE = 100_663_296
EXPECTED_MODULES = [
    "mmi_annotate.ko",
    "mmi_info.ko",
    "sensors_class.ko",
    "exfat.ko",
    "mmi-smbcharger-iio.ko",
    "chipone_tddi_v2_mmi.ko",
    "ilitek_v3_mmi.ko",
]
EXPECTED_RAW_MODULE_ORDER = [
    "mmi_annotate.ko",
    "mmi_info.ko",
    "sensors_class.ko",
    "exfat.ko",
    "mmi-smbcharger-iio.ko",
    "chipone_tddi_v2_mmi.ko",
    "ilitek_v3_mmi.ko",
]


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


def round_up(value: int, alignment: int) -> int:
    return (value + alignment - 1) // alignment * alignment


def parse_newc(data: bytes) -> dict[str, bytes]:
    """Parse a newc/crc cpio stream into path-to-payload entries."""
    entries: dict[str, bytes] = {}
    pos = 0
    while pos + 110 <= len(data):
        magic = data[pos:pos + 6]
        if magic not in (b"070701", b"070702"):
            raise AssertionError(f"invalid cpio magic at offset {pos}: {magic!r}")
        fields = [int(data[pos + 6 + i * 8:pos + 14 + i * 8], 16) for i in range(13)]
        mode, filesize, namesize = fields[1], fields[6], fields[11]
        name_start = pos + 110
        name_end = name_start + namesize
        if name_end > len(data) or namesize == 0:
            raise AssertionError("invalid cpio pathname")
        name = data[name_start:name_end - 1].decode("utf-8", errors="replace")
        file_start = round_up(name_end, 4)
        file_end = file_start + filesize
        if file_end > len(data):
            raise AssertionError(f"cpio entry exceeds stream: {name}")
        payload = data[file_start:file_end]
        entries[name] = payload
        pos = round_up(file_end, 4)
        if name == "TRAILER!!!":
            break
    if "TRAILER!!!" not in entries:
        raise AssertionError("cpio stream has no TRAILER!!!")
    return entries


def decompress_ramdisk(blob: bytes) -> bytes:
    if blob.startswith(b"\x1f\x8b"):
        return gzip.decompress(blob)
    try:
        result = subprocess.run(["lz4", "-d", "-c"], input=blob, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", b"").decode(errors="replace")
        raise AssertionError(f"unable to decode non-gzip ramdisk as legacy LZ4: {detail}") from exc
    return result.stdout


def validate_image(image: Path) -> None:
    data = image.read_bytes()
    if data[:8] != b"ANDROID!":
        raise AssertionError("image does not contain ANDROID! boot magic")
    if len(data) == 0:
        raise AssertionError("image is empty")
    if len(data) > MAX_BOOT_SIZE:
        raise AssertionError(f"image size is {len(data)}; exceeds {MAX_BOOT_SIZE}-byte boot partition")
    if len(data) < 44:
        raise AssertionError("image is too short for Android boot header")
    kernel_size, ramdisk_size = struct.unpack_from("<2I", data, 8)
    header_version = struct.unpack_from("<I", data, 40)[0]
    if header_version < 3:
        raise AssertionError(f"image header version is {header_version}; expected v3+")
    if kernel_size == 0 or ramdisk_size == 0:
        raise AssertionError("image has empty kernel or ramdisk payload")
    ramdisk_offset = round_up(4096 + kernel_size, 4096)
    ramdisk_end = ramdisk_offset + ramdisk_size
    if ramdisk_end > len(data):
        raise AssertionError("ramdisk range exceeds image")
    entries = parse_newc(decompress_ramdisk(data[ramdisk_offset:ramdisk_end]))

    required = [
        "init.recovery.qcom.rc",
        "init.recovery.usb.rc",
        "vendor/ueventd.rc",
        "system/etc/recovery.fstab",
        "system/etc/twrp.flags",
    ]
    for path in required:
        if path not in entries:
            raise AssertionError(f"image ramdisk is missing {path}")

    qcom = entries["init.recovery.qcom.rc"].decode(errors="replace")
    usb = entries["init.recovery.usb.rc"].decode(errors="replace")
    ueventd = entries["vendor/ueventd.rc"].decode(errors="replace")
    fstab = entries["system/etc/recovery.fstab"].decode(errors="replace")
    flags = entries["system/etc/twrp.flags"].decode(errors="replace")
    if "system/bin/minadbd" not in entries:
        raise AssertionError("image ramdisk is missing system/bin/minadbd")
    for module in EXPECTED_MODULES:
        path = f"vendor/lib/modules/1.1/{module}"
        if path not in entries:
            raise AssertionError(f"image ramdisk is missing {path}")
        require(qcom, f"insmod /vendor/lib/modules/1.1/{module}", "packaged init.recovery.qcom.rc")
    require(qcom, "insmod /vendor/lib/modules/1.1/mmi_annotate.ko\n    insmod /vendor/lib/modules/1.1/mmi_info.ko", "packaged init.recovery.qcom.rc")
    require(usb, "stop adbd\n    write /config/usb_gadget/g1/UDC \"none\"", "packaged init.recovery.usb.rc")
    require(usb, "rm /config/usb_gadget/g1/configs/b.1/f1", "packaged init.recovery.usb.rc")
    require(usb, "rm /config/usb_gadget/g1/configs/b.1/f2", "packaged init.recovery.usb.rc")
    require(usb, "rm /config/usb_gadget/g1/configs/b.1/f3", "packaged init.recovery.usb.rc")
    check_prop_expansions(usb, "packaged init.recovery.usb.rc")
    check_no_stray_comment_tokens(ueventd, "packaged vendor/ueventd.rc")
    require(ueventd, "/dev/input/event*", "packaged vendor/ueventd.rc")
    require(ueventd, "/dev/input/mice", "packaged vendor/ueventd.rc")
    require(ueventd, "/dev/input/mouse*", "packaged vendor/ueventd.rc")
    require(fstab, "fileencryption=aes-256-xts:aes-256-cts:v2+inlinecrypt_optimized+wrappedkey_v0", "packaged recovery.fstab")
    require(fstab, "/dev/block/sdg1", "packaged recovery.fstab")
    require(flags, "flags=storage;settingsstorage", "packaged twrp.flags")
    require(flags, "keydirectory=/metadata/vold/metadata_encryption", "packaged twrp.flags")
    require(flags, "/usb-otg               vfat", "packaged twrp.flags")
    print(f"image={image}")
    print(f"image_size={len(data)}")
    compression = "gzip" if data[ramdisk_offset:ramdisk_offset + 2] == bytes((0x1F, 0x8B)) else "lz4"
    print(f"ramdisk_compression={compression}")
    print(f"packaged_entries={len(entries)}")


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

# Boot, recovery, and Android 17 payload invariants.
for needle in (
    "BOARD_BOOT_HEADER_VERSION := 3",
    "BOARD_KERNEL_SEPARATED_DTBO := true",
    "BOARD_RAMDISK_USE_LZ4 := true",
    "BOARD_BOOTIMAGE_PARTITION_SIZE := 100663296",
    "BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 100663296",
    "BOARD_DTBOIMG_PARTITION_SIZE := 25165824",
    "BOARD_USES_RECOVERY_AS_BOOT := true",
    "BOARD_BUILD_VENDOR_RAMDISK_IMAGE := true",
    "TARGET_RECOVERY_DEVICE_DIRS += $(DEVICE_PATH)",
    "BOARD_VENDOR_RAMDISK_KERNEL_MODULES := $(FOGOS_RECOVERY_MODULE_FILES)",
):
    require(board, needle, "BoardConfig.mk")
require(board, "BOARD_SUPER_PARTITION_GROUPS := mot_dp_group", "BoardConfig.mk")
require(board, "BOARD_MOT_DP_GROUP_PARTITION_LIST := product system system_ext vendor", "BoardConfig.mk")
for stale in ("qti_dynamic_partitions", "TARGET_COPY_OUT_ODM", "BOARD_ODMIMAGE_FILE_SYSTEM_TYPE", "testkey_rsa2048.pem", "PLATFORM_SECURITY_PATCH", "PLATFORM_VERSION :="):
    forbid(board, stale, "BoardConfig.mk")

# Userdata, metadata, emulated storage, and concrete OTG mapping.
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

# Product and runtime packaging invariants.
require(device_mk, "minadbd", "device.mk")
require(device_mk, "update_engine_sideload", "device.mk")
require(device_mk, "$(TARGET_COPY_OUT_VENDOR_RAMDISK)/first_stage_ramdisk/fstab.qcom", "device.mk")
require(device_mk, "$(TARGET_COPY_OUT_VENDOR)/etc/fstab.qcom", "device.mk")
require(device_mk, "recovery/root/init.recovery.qcom.rc:recovery/root/init.recovery.qcom.rc", "device.mk")
require(device_mk, "recovery/root/init.recovery.usb.rc:recovery/root/init.recovery.usb.rc", "device.mk")
require(device_mk, "recovery/root/vendor/ueventd.rc:recovery/root/vendor/ueventd.rc", "device.mk")
for module in EXPECTED_MODULES:
    require(device_mk, f"prebuilt/modules/{module}:recovery/root/vendor/lib/modules/1.1/{module}", "device.mk")
for metadata in ("modules.dep", "modules.alias", "modules.softdep", "modules.load.recovery"):
    require(device_mk, f"prebuilt/modules/{metadata}:recovery/root/vendor/lib/modules/1.1/{metadata}", "device.mk")
for stale in ("TARGET_COPY_OUT_ODM", "    odm "):
    forbid(device_mk, stale, "device.mk")
for number, line in enumerate(device_mk.splitlines(), 1):
    if line.strip().startswith(("PRODUCT_SHIPPING_API_LEVEL :=", "PRODUCT_TARGET_VNDK_VERSION :=")):
        raise AssertionError(f"unsupported product API/VNDK assignment in device.mk:{number}: {line}")

# Init/ueventd syntax and user-requested input/USB behavior.
require(init_usb, "sys.usb.config=sideload", "init.recovery.usb.rc")
require(init_usb, "stop adbd", "init.recovery.usb.rc")
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

# Module files, metadata order, and dependency-safe raw insmod order.
modules = [line.strip() for line in modules_load.splitlines() if line.strip() and not line.startswith("#")]
if modules != EXPECTED_MODULES:
    raise AssertionError(f"modules.load.recovery drifted: {modules}")
for module in modules:
    if not (DEVICE / "prebuilt/modules" / module).is_file():
        raise AssertionError(f"missing recovery module: {module}")
    require(init_qcom, f"insmod /vendor/lib/modules/1.1/{module}", "init.recovery.qcom.rc")
actual_order = [line.split("/vendor/lib/modules/1.1/", 1)[1].strip() for line in init_qcom.splitlines() if "insmod /vendor/lib/modules/1.1/" in line]
if actual_order[: len(EXPECTED_RAW_MODULE_ORDER)] != EXPECTED_RAW_MODULE_ORDER:
    raise AssertionError(f"unexpected dependency-safe early-boot module order: {actual_order}")
require(modules_dep, "/lib/modules/mmi_info.ko: /lib/modules/mmi_annotate.ko", "modules.dep")
require(modules_dep, "/lib/modules/chipone_tddi_v2_mmi.ko: /lib/modules/sensors_class.ko", "modules.dep")

# Workflow/release invariants.
require(workflow, "TWRP_MANIFEST_BRANCH: twrp-12.1", "workflow")
require(workflow, "validate_fogos_recovery.py", "workflow")
require(workflow, "timeout-minutes: 360", "workflow")
require(workflow, "inputs.publish_release == true", "workflow")
for stale in ("Build fogos recovery baseline", "TWRP_MANIFEST_BRANCH: twrp-14.1", "testkey_rsa2048.pem"):
    forbid(workflow, stale, "workflow")

if len(sys.argv) > 1:
    validate_image(Path(sys.argv[1]))

print("fogos recovery source/image validation: PASS")
print("NOTE: static and image-content validation cannot prove physical touchscreen, encryption, mouse, or sideload behavior")
