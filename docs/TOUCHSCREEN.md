# fogos touchscreen and mouse input

The recovery keeps both input paths enabled. Touchscreen event nodes are granted to the `input` group, while `/dev/input/mice`, `/dev/input/mouse*`, USB HID nodes, and OTG mouse support remain present. The TWRP configuration explicitly sets `TW_INPUT_BLACKLIST := ""` so a generic framework blacklist cannot discard the fogos touch device.

The recovery still loads the fogos panel modules in dependency order and packages the corresponding firmware. No coordinate rotation or calibration values are fabricated; those values must come from the phone's actual event capabilities.

## Test procedure

Boot the image temporarily first. If touch wakes the display but does not activate controls, connect the mouse and run:

```sh
/system/bin/touch-diagnostics /tmp/touch.txt
```

Pull the report with ADB:

```bash
adb pull /tmp/touch.txt
```

Then test raw touch events:

```bash
adb shell getevent -lt
```

A working touchscreen should appear as an input device in `/proc/bus/input/devices` and produce `ABS_MT_POSITION_X`, `ABS_MT_POSITION_Y`, and touch press/release events. If events exist but TWRP still ignores them, the remaining problem is TWRP input interpretation or coordinate mapping. If no touchscreen event device exists, the kernel module, firmware, panel variant, or IRQ setup is still wrong and the diagnostic log is required before choosing another module.

The mouse fallback is intentionally preserved and must continue to work while touch is being diagnosed.
