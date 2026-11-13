# Android app identity and language plan

This plan records two product requirements for the MeisterBaer fork.

## 1. Give the fork its own Android identity

### Finding

On `main`, the fork and upstream both currently set:

- `applicationId`: `dev.tizenarchive.companion`
- Android/Kotlin `namespace`: `dev.tizenarchive.companion`

The open release PR #7 currently proposes `de.meisterbaer.tizenarchivemanager` as the new `applicationId`. This is a suitable distinct identifier for the fork and permits the original and fork APKs to be installed side by side once that change is merged.

### Decision and implementation rules

- Use `de.meisterbaer.tizenarchivemanager` as the proposed long-term `applicationId`; do not change it again after publishing.
- Change only the installed application ID. Keep the existing `namespace` and Kotlin package paths for now: they govern generated names such as `R` and `BuildConfig`, and changing them would add a broad source rewrite without helping parallel installation.
- Keep the manifest action `dev.tizenarchive.companion.COMPANION` stable. It is the shared discovery contract used by helper apps. Do not rename it as part of the application-ID change.
- Before an independent release, point the in-app updater at the fork's own GitHub repository and confirm its expected APK asset name. The current updater defaults to `Tizen-Archive/tizen-archive-android`.
- Update the F-Droid recipe and distribution metadata to the fork's final package ID and repository URLs before resubmitting or publishing the fork independently.
- Treat the ID change as a new app installation: Android will not upgrade the old-ID installation or migrate its private data. Existing installs can remain beside it; both may appear as handlers for the same links or package files.

## 2. Develop the app UI in English first

### Current state

- `app/src/main/res/values/strings.xml` is already the English default resource set.
- Russian overrides exist in both `app/src/main/res/values-ru/strings.xml` and `app/src/debug/res/values-ru/strings.xml`, so Android displays Russian when the device locale is Russian.
- The debug build's app name is already English in its default resources.
- Most UI copy is already read from Android string resources. The UI still needs a complete audit for visible literals and text assembled in code; for example, the folder summary combines a dynamic folder name, a hard-coded separator, and a plural resource.
- Fastlane also contains Russian store listing and changelog metadata. That content is separate from runtime UI and should be reviewed as part of the distribution cleanup.

### Requirements and implementation rules

- English is the only UI language initially and the base resource set remains the source of truth.
- Remove the Russian Android resource overrides so Russian device settings fall back to the English base strings. Replace any Russian UI copy with English.
- Put every user-visible app string in Android resources, including labels, dialogs, notifications, accessibility descriptions, errors, and formatted/plural text. Dynamic values may remain data, but surrounding words and punctuation belong in resources.
- Keep resource keys stable and make the default English resource complete. Avoid adding a language picker until there is a product need; Android resource selection already handles device locale.
- Add German later as `values-de/strings.xml` using the same resource keys. This should not require language-specific UI logic.
- Review Russian Fastlane metadata separately so store descriptions do not imply Russian UI support.

### Completion checks

1. No Russian text is rendered by the app on a Russian-locale device; it falls back to English.
2. All visible app copy is sourced from Android resources and the default English set is complete.
3. Original and fork release APKs have different application IDs and install together.
4. The fork's updater, release asset naming, F-Droid recipe, and repository links all refer to the fork before independent publishing.
5. A later German translation can be added with resource files only, without changing UI behavior.
