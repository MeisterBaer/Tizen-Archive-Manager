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

## 2. Use Android's automatic language selection with English fallback

### Current state

- `app/src/main/res/values/strings.xml` is already the English default resource set.
- Russian overrides exist in both `app/src/main/res/values-ru/strings.xml` and `app/src/debug/res/values-ru/strings.xml`, so Android displays Russian when the device locale is Russian.
- The debug build's app name is already English in its default resources.
- Most UI copy is already read from Android string resources. The UI still needs a complete audit for visible literals and text assembled in code; for example, the folder summary combines a dynamic folder name, a hard-coded separator, and a plural resource.
- Fastlane also contains Russian store listing and changelog metadata. That content is separate from runtime UI and should be reviewed as part of the distribution cleanup.

### Requirements and implementation rules

- English is the complete default and fallback language. Keep every required resource in `app/src/main/res/values/strings.xml` (and the corresponding debug defaults where needed).
- Use Android's native resource selection: the system locale selects a matching `values-<language>` resource set when one exists; otherwise Android uses the English base resources. Do not force the app locale to English.
- Remove the Russian Android resource overrides and do not copy Russian UI translations from upstream. A Russian system locale must therefore display the English base strings.
- Put every user-visible app string in Android resources, including labels, dialogs, notifications, accessibility descriptions, errors, plurals, and formatted text. Dynamic values may remain data, but surrounding words and punctuation belong in resources.
- Keep resource keys stable and make the English resource set complete. Add later translations in separate locale-qualified resource directories, such as `values-de/strings.xml`, with the same keys.
- Do not add an in-app language picker or override the system language now. An optional manual language choice can be considered later using Android's app-language support.
- Review Russian Fastlane metadata separately so distribution pages do not imply Russian UI support.

### Completion checks

1. English is the complete default/fallback resource set.
2. A supported Android system locale selects its matching translations automatically; unsupported locales fall back to English.
3. A Russian-locale device shows English because no Russian UI resource overrides remain.
4. All visible app copy is sourced from Android resources.
5. Original and fork release APKs have different application IDs and install together.
6. The fork's updater, release asset naming, F-Droid recipe, and repository links all refer to the fork before independent publishing.
7. A later German translation can be added with locale resources only, without changing UI behavior or overriding the system language.
