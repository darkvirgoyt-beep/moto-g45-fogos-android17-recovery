#
# Copyright (C) 2022 The Android Open Source Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Enable project quotas and casefolding for emulated storage without sdcardfs
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)

# Installs gsi keys into ramdisk, to boot a GSI with verified boot.
$(call inherit-product, $(SRC_TARGET_DIR)/product/gsi_keys.mk)

# A/B
AB_OTA_UPDATER := true
TARGET_ENFORCE_AB_OTA_PARTITION_LIST := true

# Android 17 fogos uses a vendor-ramdisk boot path for A/B recovery.
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/launch_with_vendor_ramdisk.mk)


AB_OTA_PARTITIONS += \
    boot \
    dtbo \
    product \
    system \
    system_ext \
    vbmeta \
    vbmeta_system \
    vendor \
    vendor_boot

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=ext4 \
    POSTINSTALL_OPTIONAL_system=true

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_vendor=true \
    POSTINSTALL_PATH_vendor=bin/checkpoint_gc \
    FILESYSTEM_TYPE_vendor=ext4 \
    POSTINSTALL_OPTIONAL_vendor=true

PRODUCT_PACKAGES += \
    checkpoint_gc \
    otapreopt_script

# Boot control
PRODUCT_PACKAGES += \
    android.hardware.boot@1.1-impl-qti.recovery \
    bootctrl.holi.recovery

# Update engine
PRODUCT_PACKAGES += \
    update_engine \
    update_engine_sideload \
    update_verifier

# Display
TARGET_RECOVERY_DEVICE_MODULES += \
    libion \
    libxml2 \
    vendor.display.config@1.0 \
    vendor.display.config@2.0

# fastbootd
PRODUCT_PACKAGES += \
    android.hardware.fastboot@1.0-impl-mock \
    fastbootd

# Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# QCOM
PRODUCT_PACKAGES += \
    qcom_decrypt \
    qcom_decrypt_fbe

# Do not force PRODUCT_SHIPPING_API_LEVEL or PRODUCT_TARGET_VNDK_VERSION here.
# The selected TWRP 12.1 manifest defines BOARD_SYSTEMSDK_VERSIONS=32; forcing
# the Android 17 device input level (34) into this older framework branch causes
# build/make/core/config.mk to reject the product before local lunch completes.
# Android 17 compatibility is represented by the inspected kernel, modules,
# fstab, vendor ramdisk, and partition inputs—not by a false framework override.

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# First-stage recovery metadata for the Android 17 vendor-ramdisk layout.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery.fstab:$(TARGET_COPY_OUT_VENDOR_RAMDISK)/first_stage_ramdisk/fstab.qcom \
    $(LOCAL_PATH)/recovery.fstab:$(TARGET_COPY_OUT_VENDOR)/etc/fstab.qcom

# Force the audited device rules into the actual recovery staging tree. Direct
# recovery/root destinations are kept in addition to TARGET_RECOVERY_DEVICE_DIRS
# because some TWRP product configurations rebuild the generic root directory
# and can otherwise replace device-specific init files.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery/root/init.recovery.qcom.rc:recovery/root/init.recovery.qcom.rc \
    $(LOCAL_PATH)/recovery/root/init.recovery.usb.rc:recovery/root/init.recovery.usb.rc \
    $(LOCAL_PATH)/recovery/root/vendor/ueventd.rc:recovery/root/vendor/ueventd.rc

# The BoardConfig declares the exact Android 17 module source paths and the
# recovery load list. TeamWin then runs depmod and places the result in the
# canonical vendor-ramdisk/recovery module directories. USB HID and mouse input
# remain independent of this touchscreen module list.
