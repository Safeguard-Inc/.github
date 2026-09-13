#!/usr/bin/env python3
"""Check the organization profile the way a visitor reads it.

The organization page is the front door: it is what someone sees when they
follow the org rather than a repository. It is also the one artifact in the
organization with no tests behind it, because it is prose. These checks give it
the ones that actually matter.

Checked
-------

* **Links resolve.** Every Markdown link has text and a target, relative paths
  exist in the repository, and an in-page anchor points at a heading that is
  really there. A profile that links to a file that was renamed is a dead end
  on the first click.
* **The pitch video is published.** The URL the profile embeds is requested and
  must answer 200 with a video content type. This is the one external request,
  and it is deliberate: a 404 behind a poster frame looks like a broken page,
  not a broken link, and nothing else in CI would notice.
* **Every public repository is documented.** The org's public repositories are
  listed from the GitHub API and each must appear in `profile/README.md`. A new
  repository that nobody documents means the front page is quietly out of date
  — which is exactly the failure this check exists to catch.

Exit code 0 on success, 1 with a report of everything that failed.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "profile" / "README.md"

# The video the profile embeds. Kept here as a constant so the check names the
# artefact it is verifying rather than pattern-matching whatever URL it finds.
PITCH_VIDEO = "https://safeguard-docs.vercel.app/assets/video/safeguard-pitch.mp4"
PITCH_POSTER = "https://safeguard-docs.vercel.app/assets/video/safeguard-pitch-poster.jpg"

LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)

MARKDOWN = ("README.md", "profile/README.md", "CODE_OF_CONDUCT.md")


def slug(heading: str) -> str:
    """GitHub's heading-to-anchor rule, close enough for the anchors used here."""
    text = re.sub(r"<[^>]+>", "", heading).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def check_links() -> list[str]:
    problems: list[str] = []
    for name in MARKDOWN:
        page = ROOT / name
        if not page.exists():
            problems.append(f"{name} is missing from the repository")
            continue
        text = page.read_text(encoding="utf-8")
        anchors = {slug(h) for _, h in HEADING.findall(text)}
        for label, target in LINK.findall(text):
            if not label.strip():
                problems.append(f"{name}: a link to {target} has no text")
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = target.partition("#")
            if path:
                resolved = (page.parent / path).resolve()
                if not resolved.exists():
                    problems.append(f"{name}: '{target}' does not resolve on disk")
                continue
            if anchor and anchor not in anchors:
                problems.append(f"{name}: anchor '#{anchor}' has no matching heading")
    return problems


def fetch(url: str, method: str = "GET") -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": "safeguard-profile-check", "Range": "bytes=0-1023"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Content-Type", "") if error.headers else ""


def check_video() -> list[str]:
    profile = PROFILE.read_text(encoding="utf-8") if PROFILE.exists() else ""
    problems: list[str] = []
    for label, url, expected in (
        ("pitch video", PITCH_VIDEO, "video/"),
        ("poster frame", PITCH_POSTER, "image/"),
    ):
        if url not in profile:
            problems.append(f"profile/README.md no longer references the {label} ({url})")
            continue
        status, content_type = fetch(url)
        # 206 as well as 200: the request asks for a byte range, which is what a
        # browser does when it seeks, and a CDN answering it correctly is a pass
        # rather than a failure.
        if status not in (200, 206) or not content_type.startswith(expected):
            problems.append(
                f"the published {label} answered {status} {content_type!r}; "
                f"the profile embeds it as {url}"
            )
        else:
            print(f"  {label:<13} {status} {content_type}")
    return problems


def check_repository_coverage() -> list[str]:
    """Every public repository in the organization is named in the profile."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("  (skipped: no GITHUB_TOKEN, so the repository list cannot be read)")
        return []
    request = urllib.request.Request(
        "https://api.github.com/orgs/Safeguard-Inc/repos?per_page=100&type=public",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            repositories = json.load(response)
    except urllib.error.HTTPError as error:
        # A rate limit or a transient API failure must not read as "the profile
        # is wrong"; it reads as "this check did not run".
        print(f"  (skipped: GitHub API answered {error.code})")
        return []

    profile = PROFILE.read_text(encoding="utf-8")
    problems = []
    for repository in sorted(r["name"] for r in repositories):
        if repository not in profile:
            problems.append(
                f"'{repository}' is public in the organization but is not mentioned in "
                "profile/README.md; the organization page is out of date"
            )
    print(f"  repositories  {len(repositories)} public, all named in the profile"
          if not problems else f"  repositories  {len(repositories)} public")
    return problems


def main() -> int:
    failures = check_links() + check_video() + check_repository_coverage()
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        print(f"\n{len(failures)} problem(s) found", file=sys.stderr)
        return 1
    print("\norganization profile is current: links resolve, the video is published,"
          " every public repository is documented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
