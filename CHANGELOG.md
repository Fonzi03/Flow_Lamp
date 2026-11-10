# Changelog

All notable changes to Flow Lamp are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-11-08

### Changed

- The card's Time Remaining now reads in hours and minutes: `11h 2min`, `1h 30min`, `2h`, `45min` (previously `11 h 2 min`).
- When there is nothing left to count down (the lamp is Off, or in the last seconds before a phase ends) the card shows a dash (`—`) instead of `0 min`.
- The Time remaining sensor's `formatted` attribute, and the message shown when turning the lamp on during cooldown, use the same style.

### Documentation

- The README now describes the current release only, with an "Updating" section and troubleshooting for an old cached copy of the card (a bare number such as `660`, or `—` while the lamp is running). After updating, restart Home Assistant and hard-refresh the browser once.

## [1.2.0] - 2026-11-08

First documented release.

### Added

- Lava lamp cycle management for a dimmable light, an on/off light, or a switch: warm up, flowing (a maintain hold, then a smooth taper), shut-off at the maximum runtime, then a cooldown during which any turn-on (wall switch, app, voice, power restore) is switched straight back off. A local turn-on starts a cycle too. Turning the lamp off before warm-up finishes just resets, with no cooldown. The cycle and cooldown survive restarts.
- Entities per lamp: State (Off, Warm Up, Flowing, Cool Down), Dimming level (only for lamps that can dim), Time remaining (minutes), Lamp Power, Cycle management, and Wax color and Liquid color selects.
- The Time remaining sensor is a number of minutes with a unit, so Home Assistant keeps it out of the activity log. It is recorded once a minute while the lamp runs, and not at all while the lamp is off. Its `formatted` attribute has a readable version.
- State sensor attributes: `light`, `dimmable`, `cycle_start`, `cooldown_until`, `ends_at`, `wax_color`, `liquid_color`, `liquid_clear`. They only change at phase changes, so they don't add to the activity log.
- Setup and Configure options for timings, brightness levels, wax and liquid colors, clear liquid, and dimming (detect automatically, dimmable, or on/off only). Color-only changes apply without a reload.
- The Flow Lamp dashboard card: an animated lamp (warm up lit with the wax resting, flowing with moving wax, cool down unlit with the wax still moving, off with the wax settled), glassmorphism styling, and State, Dimming Level and Time Remaining rows. The wax is seen through the liquid and lit from the bottom, clear liquid is supported, and tapping the animation turns the lamp on or off. The Dimming Level row is hidden for lamps that can't dim. Time Remaining is worked out from Home Assistant's own clock, so closing and reopening the page, or using another device, always shows the right time.
- The integration registers the card as a dashboard resource automatically and serves it so browsers re-check it on every load.
- A `flow_lamp/now` websocket command that returns Home Assistant's clock.
- Integration icon (Home Assistant 2026.3 or newer).

### Requirements

- Home Assistant 2026.10.1.
