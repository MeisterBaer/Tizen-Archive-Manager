# Android app identity

Tizen Archive uses `de.meisterbaer.tizenarchivemanager` as its Android `applicationId`. This identifies the installed app and its Play Store listing, and lets it be installed alongside the original app, which uses `dev.tizenarchive.companion`.

The Kotlin and Android resource `namespace` remains `dev.tizenarchive.companion`. It controls generated source names such as `R` and `BuildConfig`; keeping it avoids a broad source-code and package-path rewrite. The SDB implementation and Android permissions do not depend on the installed app ID.

Changing the application ID creates a distinct Android app. Android will not treat an installation made with the old ID as an update, and app-private data is not migrated. Back up anything needed before installing the new app. Both apps may be offered as handlers for the same Tizen Archive links or package files.

The manifest's `dev.tizenarchive.companion.COMPANION` intent action remains unchanged because it is a discovery contract shared with existing companion apps.
