#
# Copyright (C) 2022 The Android Open Source Project
#
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/motorola/fogos

# Architecture
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-2a-dotprod
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_ABI2 :=
TARGET_CPU_VARIANT := generic
TARGET_CPU_VARIANT_RUNTIME := kryo385

TARGET_2ND_ARCH := arm
TARGET_2ND_ARCH_VARIANT := armv8-a
TARGET_2ND_CPU_ABI := armeabi-v7a
TARGET_2ND_CPU_ABI2 := armeabi
TARGET_2ND_CPU_VARIANT := generic
TARGET_2ND_CPU_VARIANT_RUNTIME := kryo385

# Bootloader
TARGET_BOOTLOADER_BOARD_NAME := fogos
TARGET_NO_BOOTLOADER := true

# Assert
TARGET_OTA_ASSERT_DEVICE := fogos,fogos_retcn

# Kernel / Android 17 boot image
# The prebuilt is the exact kernel extracted from the Evolution X 17.0 fogos payload.
TARGET_NO_KERNEL := false
TARGET_KERNEL_ARCH := arm64
BOARD_KERNEL_BASE := 0x00000000
BOARD_KERNEL_IMAGE_NAME := Image
BOARD_KERNEL_PAGESIZE := 4096
BOARD_KERNEL_SEPARATED_DTBO := true
BOARD_BOOT_HEADER_VERSION := 3
BOARD_RAMDISK_USE_LZ4 := true
TARGET_KERNEL_NO_GCC := true
BOARD_MKBOOTIMG_ARGS += --header_version $(BOARD_BOOT_HEADER_VERSION)
BOARD_KERNEL_CMDLINE += androidboot.hab.product=fogos
TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/Image

# Platform
TARGET_BOARD_PLATFORM := holi
TARGET_BOARD_PLATFORM_GPU := qcom-adreno619
QCOM_BOARD_PLATFORMS +=holi

# Metadata
BOARD_USES_METADATA_PARTITION := true

# Partition Info
BOARD_FLASH_BLOCK_SIZE := 262144 # (BOARD_KERNEL_PAGESIZE * 64)
BOARD_USES_PRODUCTIMAGE := true

BOARD_BOOTIMAGE_PARTITION_SIZE := 100663296
# fogos has no init_boot partition in the verified Android 17 payload.
BOARD_DTBOIMG_PARTITION_SIZE := 25165824
BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 100663296
BOARD_BUILD_VENDOR_RAMDISK_IMAGE := true
BOARD_SYSTEMIMAGE_JOURNAL_SIZE := 0
BOARD_SYSTEMIMAGE_EXTFS_INODE_COUNT := 4096
TARGET_USERIMAGES_USE_EXT4 := true
TARGET_USERIMAGES_USE_F2FS := true

BOARD_BUILD_SYSTEM_ROOT_IMAGE := false

BOARD_SUPER_PARTITION_SIZE := 5905580032
# Motorola SM6375 uses one logical super group named mot_dp_group. The
# payload inventory contains product, system, system_ext, and vendor; it does
# not contain an ODM logical partition.
BOARD_MOT_DP_GROUP_SIZE := 5901385728 # BOARD_SUPER_PARTITION_SIZE - 4MB
BOARD_SUPER_PARTITION_GROUPS := mot_dp_group
BOARD_MOT_DP_GROUP_PARTITION_LIST := product system system_ext vendor

BOARD_PRODUCTIMAGE_FILE_SYSTEM_TYPE := ext4
BOARD_SYSTEM_EXTIMAGE_FILE_SYSTEM_TYPE := ext4
BOARD_SYSTEMIMAGE_FILE_SYSTEM_TYPE := ext4
BOARD_VENDORIMAGE_FILE_SYSTEM_TYPE := ext4
TARGET_COPY_OUT_PRODUCT := product
TARGET_COPY_OUT_SYSTEM_EXT := system_ext
TARGET_COPY_OUT_VENDOR := vendor

# Props
TARGET_SYSTEM_PROP += $(DEVICE_PATH)/system.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# Vendor-ramdisk recovery modules
# These variables match the current official fogos/SM6375 layout. Only the
# seven modules extracted from the Android 17 vendor_boot are packaged; the
# remaining checked-in modules belong to the older baseline kernel.
FOGOS_RECOVERY_MODULE_NAMES := $(strip $(shell cat $(DEVICE_PATH)/modules.load.recovery))
FOGOS_RECOVERY_MODULE_FILES := $(foreach module,$(FOGOS_RECOVERY_MODULE_NAMES),$(DEVICE_PATH)/prebuilt/modules/$(module))
# Module filenames are the load list; the corresponding absolute paths are the
# module sources. This is the TeamWin build-system contract and avoids sending
# raw .ko filenames into compiler flags.
BOARD_VENDOR_RAMDISK_KERNEL_MODULES := $(FOGOS_RECOVERY_MODULE_FILES)
BOARD_VENDOR_RAMDISK_RECOVERY_KERNEL_MODULES_LOAD := $(FOGOS_RECOVERY_MODULE_NAMES)
BOOT_KERNEL_MODULES := $(FOGOS_RECOVERY_MODULE_NAMES)

# QCOM encryption and decryption
BOARD_USES_QCOM_FBE_DECRYPTION := true
# The kernel, vendor-ramdisk modules, fstab, and partition inputs follow the
# inspected Android 17 / Evolution X 17.0 payload. The TWRP framework version
# is supplied by the selected manifest and is not relabeled here.

# Recovery
# TeamWin copies this directory into TARGET_RECOVERY_OUT. Without this hook,
# files under recovery/root are silently absent from the booted image.
TARGET_RECOVERY_DEVICE_DIRS += $(DEVICE_PATH)
BUILD_BROKEN_ELF_PREBUILT_PRODUCT_COPY_FILES := true
BOARD_HAS_LARGE_FILESYSTEM := true
BOARD_HAS_NO_SELECT_BUTTON := true
BOARD_SUPPRESS_SECURE_ERASE := true
BOARD_USES_RECOVERY_AS_BOOT := true
# Match the maintained fogos recovery packaging. The DTB is carried in the
# boot image and the recovery DTBO is included using the board convention.
BOARD_INCLUDE_RECOVERY_DTBO := true
BOARD_INCLUDE_DTB_IN_BOOTIMG := true
TARGET_NO_RECOVERY := true
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/recovery.fstab
TARGET_RECOVERY_DENSITY := hdpi
TARGET_RECOVERY_UI_MARGIN_HEIGHT := 90
TARGET_USES_MKE2FS := true

RECOVERY_LIBRARY_SOURCE_FILES += \
    $(TARGET_OUT_SHARED_LIBRARIES)/libion.so \
    $(TARGET_OUT_SHARED_LIBRARIES)/libxml2.so \
    $(TARGET_OUT_SYSTEM_EXT_SHARED_LIBRARIES)/vendor.display.config@1.0.so \
    $(TARGET_OUT_SYSTEM_EXT_SHARED_LIBRARIES)/vendor.display.config@2.0.so

# TWRP

# Battery
TW_USE_LEGACY_BATTERY_SERVICES := true

TARGET_RECOVERY_QCOM_RTC_FIX := true
TARGET_RECOVERY_PIXEL_FORMAT := RGBX_8888
TARGET_USE_CUSTOM_LUN_FILE_PATH := /config/usb_gadget/g1/functions/mass_storage.0/lun.%d/file
TW_CUSTOM_CPU_TEMP_PATH := "/sys/devices/virtual/thermal/thermal_zone53/temp"
TW_THEME := portrait_hdpi
TW_BRIGHTNESS_PATH := "/sys/class/backlight/panel0-backlight/brightness"
TW_QCOM_ATS_OFFSET := 1621580431500
TW_DEFAULT_BRIGHTNESS := 150
TW_MAX_BRIGHTNESS := 2047
TW_EXCLUDE_DEFAULT_USB_INIT := true
TW_EXTRA_LANGUAGES := true
TW_INCLUDE_CRYPTO := true
# Android stores user media under /data/media/0. This enables TWRP's
# emulated-storage setup without formatting or wiping userdata.
RECOVERY_SDCARD_ON_DATA := true
TW_NO_EXFAT_FUSE := true
TW_INCLUDE_REPACKTOOLS := true
TW_INCLUDE_RESETPROP := true

# Statusbar icons flags
TW_STATUS_ICONS_ALIGN := center
TW_CUSTOM_CLOCK_POS := 50
TW_CUSTOM_CPU_POS := 280
TW_CUSTOM_BATTERY_POS := 790


# Add TW_DEVICE_VERSION
TW_DEVICE_VERSION := Fogos

# TWRP-debug
TARGET_USES_LOGD := true
TWRP_INCLUDE_LOGCAT := true
TARGET_RECOVERY_DEVICE_MODULES += debuggerd
RECOVERY_BINARY_SOURCE_FILES += $(TARGET_OUT_EXECUTABLES)/debuggerd
TARGET_RECOVERY_DEVICE_MODULES += strace
RECOVERY_BINARY_SOURCE_FILES += $(TARGET_OUT_EXECUTABLES)/strace

# Verified Boot
# The stock ROM supplies the signed vbmeta/vbmeta_system images. This recovery
# target must not synthesize a system vbmeta with AOSP test keys or fabricated
# rollback/security-patch values.
