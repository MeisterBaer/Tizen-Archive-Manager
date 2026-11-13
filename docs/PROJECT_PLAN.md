# Android app identity and language plan

This plan records product requirements and implementation status for the Tizen Archive Manager fork.

## 1. Give the fork its own Android identity

### Finding

The fork uses a separate Android application ID:

- `applicationId`: `de.meisterbaer.tizenarchivemanager`
- Android/Kotlin `namespace`: `dev.tizenarchive.companion`

Keeping the existing namespace and Kotlin package paths avoids an unnecessary source-wide rewrite. The distinct application ID permits the original app and fork to be installed side by side.

### Decision and implementation rules

- Use `de.meisterbaer.tizenarchivemanager` as the long-term `applicationId`; do not change it again after publishing.
- Keep the existing `namespace` and Kotlin package paths for now: they govern generated names such as `R` and `BuildConfig`.
- Keep the manifest action `dev.tizenarchive.companion.COMPANION` stable. It is the shared discovery contract used by helper apps.
- Before an independent release, point the in-app updater at the fork's own GitHub repository and confirm its expected APK asset name. The inherited updater default points to `Tizen-Archive/tizen-archive-android`; the fork's release setup must point it to `tizenarchivemanager-art/Tizen-Archive-Manager`.
- Update the F-Droid recipe and distribution metadata to the fork's final package ID and repository URLs before publishing independently.
- Treat the ID change as a new app installation: Android will not upgrade the old-ID installation or migrate its private data. Existing installs can remain beside it; both may appear as handlers for the same links or package files.

## 2. Use Android's automatic language selection with English fallback

### Binding language requirements

- **English is the complete default and fallback language.**
- The app automatically follows the Android system language whenever translations for that language are included.
- If Android's system language is not supported by the app, Android must display the English default resources automatically.
- Russian must be completely absent from the app's runtime user interface. Do not copy or retain Russian UI translations from the upstream project.
- The translation structure must make it straightforward to add more languages later.
- An optional manual language selector in the app settings is deferred to a later stage. Do not implement an app-specific language override or language picker now.

### Android localization implementation

Use Android's native resource-selection mechanism:

- Keep the complete English resource set in `app/src/main/res/values/strings.xml`.
- Add future translations in locale-qualified resource directories, for example `app/src/main/res/values-de/strings.xml`.
- Keep resource keys consistent across languages.
- Let Android select the matching locale resources based on the configured system language.
- Do not force English as the app locale. English is the fallback because it is the unqualified base resource set.
- Do not add Russian resource directories such as `values-ru` under either the main or debug app source sets.
- Put all user-visible app copy in Android resources, including labels, dialogs, notifications, accessibility descriptions, errors, plurals and formatted text. Dynamic values may remain data, but surrounding words and punctuation belong in resources.

### Verified repository state (2026-11-13)

Pull request #9, **Use English fallback for Android system locales**, has been merged into `main`.

The merged implementation:

- Removes `app/src/main/res/values-ru/strings.xml`.
- Removes `app/src/debug/res/values-ru/strings.xml`.
- Leaves the English base resources as the default and fallback.
- Moves the folder-summary separator into an Android string resource so that visible text remains localizable.
- Updates the UI test so an unsupported Russian system locale is expected to display the English fallback.
- Adds no app-language override and no manual language picker.

The repository's current resource layout was checked: the two Russian Android resource files no longer exist. The app therefore uses Android's native locale selection and falls back to English for unsupported locales.

### Remaining localization work

- Audit the complete UI for any visible text literals that are not yet Android string resources.
- Review Fastlane store-listing and changelog metadata separately. Russian distribution metadata is not an Android runtime translation, but it should not claim or imply that the app has a Russian UI.
- When another language is added, provide a complete matching resource set (for example, German in `values-de`) and test automatic system-locale selection plus English fallback.
- Consider a manual language selector only in a later, separately planned change.

### Completion checks

1. English is the complete default/fallback resource set. **Implemented.**
2. Android automatically selects translations matching the device's configured system language when those resources exist. **Native Android resource selection is retained; no app locale override is used.**
3. Unsupported system locales fall back to English. **Implemented and covered by a UI test.**
4. Russian UI resource overrides are absent from main and debug source sets. **Implemented and verified.**
5. Visible app copy is sourced from Android resources. **Audit still required.**
6. A later German translation can be added with locale resources only, without changing UI behavior or overriding the system language. **Structure prepared; German translation not yet implemented.**
7. Optional manual language selection remains deferred. **Not implemented by design.**

## 3. Overall publication follow-up

Before an independent public release, verify that:

- the in-app updater and release asset naming refer to this fork;
- F-Droid metadata and recipes refer to this fork and its final application ID;
- repository links and distribution metadata are correct;
- the README and store listings describe the actual supported UI languages accurately.
