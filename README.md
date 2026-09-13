# Safeguard-Inc/.github

Organization-level profile and shared community health files for
[Safeguard Inc.](https://github.com/Safeguard-Inc).

## What is in here

| Path | Purpose |
| ---- | ------- |
| `profile/README.md` | The organization profile page GitHub renders at <https://github.com/Safeguard-Inc>. |
| `CODE_OF_CONDUCT.md` | Default code of conduct, inherited by repositories that do not define their own. |
| `LICENSE` | Default license, matching the repositories it covers. |
| `scripts/check-profile.py` | The checks that keep the profile honest (below). |
| `.github/workflows/ci.yml` | Runs those checks on every push, every pull request, and weekly. |

## Presentation

[![Five-minute Safeguard pitch: the problem, the architecture, the live decision engine and the contracts running on Testnet](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch-poster.jpg)](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch.mp4)

[![Pitch video](https://img.shields.io/badge/pitch_video-5_minutes-4ade9b)](https://safeguard-docs.vercel.app/assets/video/safeguard-pitch.mp4)

Five minutes on the problem, the architecture, the engine running live and the
contracts deployed to Stellar Testnet. The video is generated from
[`safeguard-docs`](https://github.com/Safeguard-Inc/safeguard-docs/tree/main/video)
rather than hand-edited, so the same pipeline that produced it re-checks the
numbers quoted on screen.

## What CI checks here

The profile is prose, so its tests have to be about being *current* rather than
about compiling. `scripts/check-profile.py` fails the build when:

- a link in any Markdown file has no text, points at a file that is not in the
  repository, or targets an anchor with no matching heading;
- the published pitch video or its poster frame stops answering with a video or
  image content type — a 404 behind a poster frame reads as a broken page, and
  nothing else in CI would notice;
- a repository is **public in the organization but not named in the profile**,
  which is the one way this page goes stale on its own. That check runs on a
  weekly schedule as well as on push, because the trigger is a change in
  another repository.

## Why this repository exists

GitHub reads organization-level community health files from a public
repository named `.github`. Keeping them here means a new repository in the
organization inherits a code of conduct without anyone having to remember to
copy one, and the organization's front page is version-controlled alongside the
projects it describes rather than edited in a web form.

## Editing the profile

`profile/README.md` is ordinary Markdown. Keep it accurate: every claim it
makes about a deployment, a contract address or a passing gate should be
checkable against the repository it describes, and a change that invalidates a
statement here should update it in the same pull request.
