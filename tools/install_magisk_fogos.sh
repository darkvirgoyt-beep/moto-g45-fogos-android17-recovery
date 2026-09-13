#!/usr/bin/env bash
# Stage the official Magisk APK-as-ZIP for installation from TWRP on fogos.
# This helper never flashes a partition and never deletes Magisk/user data.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  install_magisk_fogos.sh [--zip /path/to/Magisk.zip] [--remote URL]

The APK is intentionally staged as an APK. Magisk's official custom-recovery
workflow accepts the APK renamed to .zip; TWRP then performs the ZIP install.
The helper does not patch or flash boot images itself.
EOF
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
bundled_zip="$script_dir/../device/motorola/fogos/prebuilt/magisk/Magisk-v30.7.zip"
zip_path=""
remote="https://github.com/topjohnwu/Magisk/releases/latest/download/Magisk.apk"
use_remote=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --zip) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; zip_path="$2"; shift 2 ;;
    --remote) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; remote="$2"; use_remote=1; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$zip_path" && "$use_remote" -eq 0 && -s "$bundled_zip" ]]; then
  zip_path="$bundled_zip"
fi

command -v adb >/dev/null || { echo "adb is required" >&2; exit 1; }
if [[ -z "$zip_path" ]]; then
  command -v curl >/dev/null || { echo "curl is required when --zip is omitted" >&2; exit 1; }
  tmp="$(mktemp --suffix=.apk)"
  trap 'rm -f "$tmp"' EXIT
  echo "Downloading official Magisk APK: $remote"
  curl --fail --location --retry 3 --connect-timeout 15 --output "$tmp" "$remote"
  zip_path="$tmp"
fi

[[ -s "$zip_path" ]] || { echo "Magisk package is missing or empty: $zip_path" >&2; exit 1; }
# An APK is a ZIP container. Check it before touching the phone.
unzip -tqq "$zip_path" || { echo "The supplied Magisk package is not a valid ZIP/APK" >&2; exit 1; }

serial="${ANDROID_SERIAL:-}"
adb_cmd=(adb); [[ -n "$serial" ]] && adb_cmd+=( -s "$serial" )
"${adb_cmd[@]}" wait-for-device
name="Magisk-$(basename "$zip_path")"
name="${name%.apk}.zip"
remote_path="/sdcard/Download/$name"
"${adb_cmd[@]}" push "$zip_path" "$remote_path"
cat <<EOF

Staged: $remote_path

In TWRP:
  1. Install -> $remote_path
  2. Swipe to confirm the ZIP install.
  3. Reboot System.

This flow deliberately does NOT erase /data, /data/adb, modules, or arbitrary
Magisk files. If Magisk is already installed, use Magisk's own uninstall or
module management flow; deleting those paths can remove modules and user data.
For this fogos layout, do not flash a standalone recovery target; there is no
standalone recovery partition. If a boot image must be flashed, use the active
slot's boot partition only after a verified Magisk patch and backup.
EOF
