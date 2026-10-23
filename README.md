# 🌿Leaf

An offline daily study journal — track subjects, daily targets, progress charts, and back up your data locally.

**Author:** Fatemehsadat Mortazavi

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Platform](https://img.shields.io/badge/platform-Web%20%7C%20Android-3DDC84?logo=android&logoColor=white)](#build-for-android)
[![Offline](https://img.shields.io/badge/offline-100%25-success)](#privacy)
[![No Tracking](https://img.shields.io/badge/tracking-none-blue)](#privacy)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Run in the Browser](#run-in-the-browser)
  - [Build for Android](#build-for-android)
- [Project Structure](#project-structure)
- [Data and Storage](#data-and-storage)
- [Privacy](#privacy)
- [Backup and Restore](#backup-and-restore)
- [Internationalization](#internationalization)
- [Calendars](#calendars)
- [Weekly Goal and Friday Reminder](#weekly-goal-and-friday-reminder)
- [Accessibility](#accessibility)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## About

Leaf is a private, offline-first study tracker designed for students who wish to record their daily study time, monitor their progress, and retain full ownership of their data. The application is distributed as a single HTML file, runs in any modern web browser, and can be packaged as a native Android application using [Capacitor](https://capacitorjs.com/).

The application does not require an account, does not contact any server, and does not perform analytics or tracking. All data is stored in the `localStorage` of the user's device.

The design philosophy is stated in the application itself: every day a new leaf, every leaf a trace of effort.

---

## Features

### Study Tracking
- A quick-log interface with one-tap buttons for 15, 30, 45, and 60 minutes.
- A manual entry form with separate hour and minute fields and full validation.
- A unified subject picker shared by both the quick-log and manual-entry paths, preventing accidental logging to an incorrect subject.
- Per-subject default targets and per-day overrides through the Target modal.
- An automatically computed daily target, defined as the sum of subject targets, with an optional manual override.
- A strict 24-hour daily cap enforced across all logging paths.

### Session Management
- Editing of any session, allowing the subject, hours, and minutes to be changed through a modal.
- Deletion of any session through a custom confirmation modal, without reliance on the native `confirm()` dialog.
- An undo action for the most recently added session, exposed through a toast notification.
- A History screen presenting a day-by-day breakdown of the last 90 days, with inline editing.

### Subject Progress
- A progress panel for each subject, showing a doughnut chart, the logged total, the target percentage, and a completion indicator.
- An "Edit session" button within the progress panel that opens the session the user selected, rather than always the first session of the subject.

### Statistics
- Totals for today, the current week, and the current month.
- A 7-day average and a day-streak counter.
- A 7-day trend line chart.
- A monthly subject-share doughnut chart with a corresponding legend.

### Weekly Goal
- A weekly goal expressed in hours, with a live progress bar.
- Weeks defined as starting on Saturday and ending on Friday, in accordance with the Persian and Islamic convention.
- A weekly-goal title that displays the exact date range in the active language, for example: `Week: 2 Nov to 8 Nov`, `هفته: ۲ آبان تا ۸ آبان`, or `الأسبوع: ٢ نوفمبر إلى ٨ نوفمبر`.
- A Friday reminder that displays an in-app banner and, if permission is granted, a browser notification when it is Friday and the current week's goal has not yet been set.

### Personalization
- Three languages: English, Persian (فارسی), and Arabic (العربية), with full right-to-left support.
- Three calendars: Gregorian, Jalali (شمسی), and Hijri (هجری قمری).
- Light and dark themes.
- Eight accent palettes: Neutral, Blue, Green, Red, Purple, Orange, Teal, and Pink.
- Use of system-default fonts, with no external font loading.
- Animated number transitions and restrained micro-interactions.

### Data Safety
- Automatic daily backups, retaining the last seven versions, stored in a separate `localStorage` key.
- Manual JSON backup and restore.
- CSV export of all sessions, compatible with Excel and Google Sheets, encoded as UTF-8 with a byte-order mark.
- Cross-tab synchronization through the `storage` event.
- A defensive `sanitizeState()` function applied on load and import, ensuring that malformed JSON cannot crash the application.
- A reset-all-data flow guarded through `sessionStorage`, preventing backups from being restored after a deliberate wipe.

### Accessibility and Robustness
- All event handlers are bound using `addEventListener`; no inline `onclick` attributes are used, which keeps the application compatible with strict Content Security Policies.
- ARIA roles are applied to all dialogs, including `role="dialog"`, `aria-modal`, and `aria-labelledby`.
- Keyboard navigation is fully supported: Enter and Space activate cards and rows, and Escape closes modals.
- Toast notifications use `aria-live` to announce changes to screen readers.
- If Chart.js fails to load, the application remains functional and charts display a placeholder.
- Date handling is safe across multiple languages, calendars, and time zones.

---

## Screenshots

Screenshots will be added to `docs/screenshots/` in a future release. The recommended layout is a three-column grid presenting the onboarding flow, the Today screen, and the progress panel, followed by a second row presenting the statistics, history, and settings screens.

---

## Tech Stack

| Layer | Technology |
|---|---|
| User interface | Vanilla HTML5, CSS3, and JavaScript (ES2020, without a framework) |
| Charts | [Chart.js](https://www.chartjs.org/), optional and gracefully degraded |
| Storage | `localStorage`, using a single JSON blob and rolling backups |
| Android shell | [Capacitor](https://capacitorjs.com/) 6.x |
| Build tooling | Node.js 18 or higher, npm 9 or higher, Android Studio with the SDK and JDK 17 |

There is no bundler, no transpiler, and no build step for the web application. The entire web client is contained in a single `index.html` file.

---

## Requirements

### To Run the Web Application
- Any modern browser on desktop or mobile, including Chrome, Firefox, Safari, or Edge.

### To Build the Android APK
- Node.js 18 or higher.
- npm 9 or higher.
- Android Studio with the Android SDK, API level 34 or higher recommended, and JDK 17.
- A USB-connected Android device or an emulator, optional and required only for running the application.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/leaf.git
cd leaf

# 2. Install Capacitor dependencies
npm install

# 3. Add the Android platform (first time only)
npx cap add android

# 4. Sync web assets into the Android project
npx cap sync
```

---

## Usage

### Run in the Browser

Open `index.html` directly in any modern browser. No server and no build step are required.

To use the browser-notification Friday reminder, serve the file over `http://localhost` or `https://`. Most browsers block the `Notification` API on `file://` origins.

### Build for Android

```bash
# Sync web assets into the native project
npx cap sync

# Open Android Studio
npx cap open android
```

In Android Studio:

1. Navigate to **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
2. Wait for the build to complete, then locate the generated APK.

Alternatively, from the command line:

```bash
cd android
./gradlew assembleDebug
```

The debug APK will be located at:

```
android/app/build/outputs/apk/debug/app-debug.apk
```

For a release build, refer to the [Capacitor Android deployment guide](https://capacitorjs.com/docs/android/deploying-to-google-play).

---

## Project Structure

```
leaf/
├── index.html                 # The entire web application (HTML, CSS, and JavaScript)
├── chart.umd.min.js           # Chart.js bundle, optional and used for charts
├── logo.png                   # Application logo
├── package.json               # Capacitor dependencies and scripts
├── capacitor.config.json      # Capacitor configuration
├── README.md                  # This file
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT License
└── android/                   # Generated by `npx cap add android`
    ├── app/
    │   ├── src/main/
    │   │   ├── assets/public/ # Web assets copied by `npx cap sync`
    │   │   └── AndroidManifest.xml
    │   └── build.gradle
    └── gradlew
```

The web application does not require a build step. `index.html`, `chart.umd.min.js`, and `logo.png` are the only runtime assets.

---

## Data and Storage

Leaf does not include any preloaded data. All sessions, subjects, targets, and settings are created by the user and stored exclusively in the device's `localStorage`.

| Key | Contents | Lifetime |
|---|---|---|
| `leaf_v8` | Full application state: user, subjects, sessions, targets, goals, and settings | Until reset |
| `leaf_backup_v8` | Rolling daily backups, retaining the last seven days | Automatically pruned |
| `leaf_resetting` | A transient flag in `sessionStorage` that prevents backup restoration during a reset | Cleared on the next load |

### Migration

On the first launch after an update, Leaf checks `leaf_v8`, then `leaf_v7`, then `leaf_v6`, and migrates the data automatically. Existing users retain their full history.

### Manual Backup

Navigate to **Settings → Data → Backup** to download a file named `leaf-YYYY-MM-DD.json` containing the full application state. The file can be restored from **Settings → Data → Restore**.

### CSV Export

Navigate to **Settings → Data → Export sessions (CSV / Excel)** to produce a UTF-8 CSV file with a byte-order mark, ready to open in Excel or Google Sheets.

---

## Privacy

- The application requires no account, contacts no server, performs no tracking, performs no analytics, and displays no advertisements.
- The application makes zero network requests at runtime. The only external asset is `chart.umd.min.js`, which is bundled locally in this repository so that the application is fully self-contained.
- All data remains on the user's device. Uninstalling the application or clearing site data removes everything permanently.
- If the Friday reminder is enabled, notifications are generated locally by the browser. No push server is involved.

---

## Backup and Restore

| Action | Location | Result |
|---|---|---|
| Daily automatic backup | Automatic on the first launch each day | Saved to `leaf_backup_v8`; the last seven are retained |
| Manual JSON backup | Settings → Data → Backup | Downloads `leaf-YYYY-MM-DD.json` |
| Restore from JSON | Settings → Data → Restore | Replaces the current state, subject to confirmation |
| CSV export | Settings → Data → Export sessions | Downloads `leaf-sessions-YYYY-MM-DD.csv` |
| Reset all data | Settings → Data → Reset all data | Wipes `leaf_v8`, backups, and all `leaf_*` keys |

Users are strongly advised to keep a manual JSON backup in a secure location, such as a cloud drive or an email archive, before resetting or reinstalling the application.

---

## Internationalization

Leaf provides complete translations for three languages.

| Language | Code | Direction | Default Calendar |
|---|---|---|---|
| English | `en` | LTR | Gregorian |
| Persian (فارسی) | `fa` | RTL | Jalali (شمسی) |
| Arabic (العربية) | `ar` | RTL | Hijri (هجری) |

All user-facing strings are defined in the `I18N` object inside `index.html`. To add a new language:

1. Copy the `en` block in `I18N`.
2. Translate every string while preserving the function signatures, for example `remainingHint:(r)=>...`.
3. Add a new `<button class="lang-card" data-lang="xx">` inside `#ob-langGrid`.
4. Add a matching `<option value="xx">` inside `#setLangSel`.

For Persian, the translation uses half-spaces (ZWNJ) everywhere except in "می" verbs, where the half-space is intentionally removed. This convention should be preserved when editing.

---

## Calendars

Three calendars are supported.

- Gregorian: the standard Western calendar.
- Jalali (شمسی): the Solar Hijri calendar used in Iran and Afghanistan.
- Hijri (هجری قمری): the Lunar Hijri calendar used across the Islamic world.

The active calendar is stored per user in `state.user.cal` and is applied to the main date line, the alternate date line, the labels of the 7-day trend chart, the History screen headers, and the weekly-goal date range.

Weeks always start on Saturday and end on Friday, regardless of the active calendar. This matches the Persian and Islamic convention.

---

## Weekly Goal and Friday Reminder

### Weekly Goal

- Enter a target in hours on the Statistics screen.
- The progress bar displays the percentage complete, the hours completed, and the hours remaining.
- The title displays the exact date range, for example `Week: 2 Nov to 8 Nov`, `هفته: ۲ آبان تا ۸ آبان`, or `الأسبوع: ٢ نوفمبر إلى ٨ نوفمبر`.
- The week key is the date of the Saturday that begins the current week, for example `2026-10-24`.

### Friday Reminder

Every Friday, if the current week's goal has not been set, Leaf displays the following.

1. An in-app banner at the top of the Today screen, offering two actions:
   - **Set goal**, which navigates to the Statistics screen and focuses the goal input.
   - **Later**, which dismisses the banner for the remainder of the day.
2. A browser notification, only if the user has granted permission. It fires at most once per Friday.

The reminder can be enabled or disabled in **Settings → Reminders → Friday weekly-goal reminder**.

Browser notifications require the `Notification` permission. If the application is opened directly from `file://`, most browsers will block such notifications. Serve the application over `http://localhost` or `https://`, or install the Android build, to enable them.

---

## Accessibility

- All interactive elements are accessible by keyboard.
- Dialogs use `role="dialog"`, `aria-modal="true"`, and `aria-labelledby`.
- Toasts use `aria-live="polite"`.
- Text color contrast meets the WCAG AA requirements.
- Animations are disabled when the `prefers-reduced-motion` media query is set.
- Focus rings remain visible through `:focus-visible`.

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---|---|---|
| Data disappears after a reload | `localStorage` is blocked, for example in private browsing or due to a storage quota | Use a normal browser window and verify that storage is permitted for the origin |
| Charts do not appear | `chart.umd.min.js` failed to load | Ensure the file resides next to `index.html`, or re-run `npx cap sync` after adding it to `assets/public/` |
| The Friday notification never appears | Notification permission was denied, or the application is running from `file://` | Grant permission in the browser settings, serve over `http://localhost`, or install the Android application |
| The weekly goal resets unexpectedly | The current date crossed a Saturday boundary | This is expected behavior: each week has its own goal keyed by its Saturday |
| A "storage blocked" toast appears | `localStorage.setItem` threw an exception due to quota or private mode | Free disk space, exit private mode, or export a backup immediately |
| Restored data is outdated | An older backup was restored | Verify the date in the JSON filename before restoring |

---

## Roadmap

The following items are candidates for future releases.

- An optional reminder at a custom time on Fridays, for example at 9:00 AM.
- Session notes, allowing a short free-text annotation per session.
- Per-subject weekly goals in addition to daily targets.
- A monthly heatmap view, similar to a contribution grid.
- Import from CSV, in addition to JSON.
- PWA installation through a manifest and a service worker, enabling offline installation from the browser.
- Export of the full history to PDF.
- Additional languages, such as Turkish and French.

Feedback and feature requests are welcome through GitHub Issues.

---

## Contributing

Contributions, bug reports, and translations are welcome.

1. Fork the repository.
2. Create a branch: `git checkout -b feature/my-feature`.
3. Make the changes.
4. Test in at least Chrome and Firefox, in both LTR and RTL modes, and with all three calendars.
5. Open a pull request describing what changed and why.

The following guidelines must be respected.

- The application must remain a single file (`index.html`). No bundlers and no transpilers.
- All handlers must use `addEventListener`; inline `onclick` attributes are not permitted.
- All user data must be escaped with `esc()` before being inserted into HTML.
- New user-facing strings must be added to all three language blocks in `I18N`.
- Persian half-space rules must be preserved.

---

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**Fatemehsadat Mortazavi**

Leaf was developed as a personal, offline-first study journal. Feedback and suggestions are welcome through GitHub Issues.