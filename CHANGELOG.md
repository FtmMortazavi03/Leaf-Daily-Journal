# Changelog

All notable changes to Leaf are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Native Android icons matching the Leaf logo.
- Optional cloud-free sync via export/import between devices.

## [1.0.0] — Nov 2026

### Added

- Initial release.
- Offline single-file study journal wrapped in Capacitor for Android.
- Daily study log with quick-add (15/30/45/60 min) and manual entry.
- Per-subject default targets + per-day overrides via the target modal.
- Auto-computed daily target (sum of subject targets) with manual override.
- Subject progress panel with doughnut chart and completion checkmark.
- Stats: today, week, month, 7-day average, day streak.
- 7-day trend line chart and monthly subject-share doughnut chart.
- Weekly goal with progress bar.
- Three languages: English, Persian, Arabic (full RTL support).
- Three calendars: Gregorian, Jalali, Hijri.
- Light/dark themes, 8 accent palettes, 3 Persian fonts.
- Automatic daily backups (last 7 versions) stored locally.
- Manual JSON backup and restore.
- Onboarding flow: language → story → name → appearance.
- Reset-all-data flow guarded against accidental backup restore.

### Fixed

- Half-spaces in Persian UI: only "می" verbs are joined; all other half-spaces are preserved.
- Default subject names follow the selected language.
- Reset now correctly clears all data and does not re-restore from backup.
- Onboarding no longer shows double blank lines in the story text.