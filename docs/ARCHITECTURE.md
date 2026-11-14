# Technical architecture

## Product boundary

Tizen Archive Manager is an Android client for discovering, validating, transferring and managing Tizen application packages and watch faces. The Tizen Archive website/catalog is an external content source, not the application's identity or owner. Catalog links cannot select arbitrary update or service endpoints.

## Modules

- `app`: Android application, Jetpack Compose UI, lifecycle and foreground queue service, Storage Access Framework, Android PackageInstaller, Android Keystore, preferences and device networking.
- `core`: JVM-only domain and protocol layer: Tizen package parsing, companion APK construction, signing support, catalog access and install-link parsing, delivery pacing, SDB transport/protocol, watch discovery, package installation and delivery capture.

The core module remains independent of Android APIs. Android-specific capabilities are exposed through narrow interfaces implemented by `app`.

## Transfer paths

### Galaxy Wearable / Bluetooth

The app creates a minimal companion APK containing the selected Tizen package. Android PackageInstaller installs the companion; Samsung Galaxy Wearable and Gear Plugin deliver the package to the watch. The app can confirm companion installation, but cannot reliably confirm watch-side acceptance or installation.

### SDB / Wi-Fi

The app connects to the watch's SDB daemon over the local network (TCP port 26101), authenticates using an Android Keystore-backed key, then uses SDB shell/sync services and `pkgcmd -w` for installation and inventory operations. This path requires watch-side debugging authorization. The watch's response is surfaced without reinterpreting unknown error codes.

## Catalog and trust boundaries

- The catalog base URL is fixed by app build configuration; an install deep link supplies only package identity/version.
- Downloads are checked against catalog-provided SHA-256 and size before use.
- Package signatures are not modified. The watch package manager remains authoritative for acceptance.
- Certificate-chain inspection is advisory compatibility prediction, not a substitute for watch signature validation.
- SDB communication is limited to the explicitly selected or discovered local watch endpoint.

## UI, localization and identity

- Compose UI is in `app`; user-visible strings belong in Android resources.
- English base resources are complete and provide fallback. Android selects translated resources from the system locale when available; unsupported locales use English.
- Release application ID: `de.meisterbaer.tizenarchivemanager`. The Kotlin namespace remains `dev.tizenarchive.companion` to avoid a needless source/package migration.
- The shared companion discovery action `dev.tizenarchive.companion.COMPANION` remains stable for existing helper apps.

## Verification

`make check` runs JVM unit tests and Robolectric UI/view-model tests. GitHub Actions additionally runs Android instrumentation tests and reproducible-release checks. Device compatibility claims require physical-device evidence and must be recorded separately from protocol-level test coverage.
