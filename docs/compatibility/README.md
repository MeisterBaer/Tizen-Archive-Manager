# Compatibility

This directory records device and firmware compatibility evidence for Tizen Archive Manager.

## Evidence levels

- **Verified**: the stated operation completed on the exact device/firmware combination.
- **Partially verified**: only explicitly listed operations were tested; other behavior remains unknown.
- **Not tested**: no device evidence is available.
- **Known limitation**: a reproducible restriction or failure with a documented scope.

Do not infer general compatibility from one successful operation. Record model number, Tizen version, firmware, transfer path (Galaxy Wearable/Bluetooth or SDB/Wi-Fi), Android version where relevant, package type and exact watch response. Unknown errors must remain unknown; do not assign a cause without evidence.

## Device profiles

- [Samsung Gear S3 Frontier](gear-s3-frontier.md)

Compatibility is package- and signature-dependent. A device being connectable does not mean it accepts every `.wgt` or `.tpk` package.
