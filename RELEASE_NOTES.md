## Flow Lamp 1.3.0

### Changed

- **Time Remaining on the card** now reads in hours and minutes: `11h 2min`, `1h 30min`, `2h`, `45min`.
- When there is nothing left to count down (the lamp is Off, or in the last seconds before a phase ends) the card shows a dash (`—`) instead of `0 min`.
- The Time remaining sensor's `formatted` attribute and the cooldown message use the same style.

### Upgrade

Replace `custom_components/flow_lamp`, restart Home Assistant fully, then **hard-refresh your browser** (Ctrl+Shift+R; in the mobile app, clear its frontend cache). If Time Remaining shows a bare number such as `660`, or `—` while the lamp is running, the browser is still running an old copy of the card: refresh once more.

Requires Home Assistant 2026.10.1. Full history: [CHANGELOG.md](https://github.com/your-name/flow-lamp/blob/main/CHANGELOG.md).
