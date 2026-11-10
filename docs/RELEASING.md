# Releasing

HACS shows the **release notes of the GitHub release**, not the contents of `CHANGELOG.md`. So each release needs both:

1. Update `CHANGELOG.md` (Keep a Changelog format, newest version first).
2. Set `"version"` in `custom_components/flow_lamp/manifest.json` to the new version.
3. Commit and push.
4. Create a GitHub release with a tag that matches the version, for example `v1.3.0` (GitHub, Releases, Draft a new release).
5. Paste the notes from `RELEASE_NOTES.md` into the release description. HACS shows this text in its update dialog. Call out breaking changes at the top.

HACS offers an update when the latest release tag is newer than the installed version.
