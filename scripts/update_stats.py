#!/usr/bin/env python3
"""
EUR-UN Organization Stats Generator

Scans all public repositories in the EUR-UN GitHub organization via the
GitHub REST API and dynamically updates the profile README with live
statistics (repo count, forks, stars, language distribution, licenses, etc.).

Usage:
    python3 scripts/update_stats.py          # uses GITHUB_TOKEN env var
    python3 scripts/update_stats.py --dry-run # print to stdout only

Designed to run in GitHub Actions on a cron schedule (see .github/workflows/update-stats.yml).
Zero external dependencies — stdlib only.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────
ORG = "EUR-UN"
API_BASE = "https://api.github.com"
README_PATH = Path(__file__).resolve().parent.parent / "profile" / "README.md"
BAR_WIDTH = 20  # chars for the ASCII progress bar
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Languages to exclude from the stats (noise / non-code / inflated byte counts)
EXCLUDED_LANGUAGES = {
    "HTML", "CSS", "LESS", "SCSS", "Roff", "Makefile",
    "Dockerfile", "Batchfile", "Procfile",
    "Jupyter Notebook",  # .ipynb are bloated JSON; distorts real language ratios
}

# ──────────────────────────────────────────────────────────────────────
# GitHub API helpers
# ──────────────────────────────────────────────────────────────────────

def _api_get(url: str) -> any:
    """GET a GitHub API endpoint with optional auth. Returns parsed JSON."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "EUR-UN-Stats-Bot/1.0",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[WARN] HTTP {e.code} for {url}", file=sys.stderr)
        return None


def fetch_all_pages(endpoint: str) -> list:
    """Paginate through a GitHub API list endpoint."""
    results = []
    page = 1
    while True:
        sep = "&" if "?" in endpoint else "?"
        url = f"{API_BASE}{endpoint}{sep}per_page=100&page={page}"
        data = _api_get(url)
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


# ──────────────────────────────────────────────────────────────────────
# Data collection
# ──────────────────────────────────────────────────────────────────────

def collect_org_stats() -> dict:
    """Collect all stats for the organization."""
    repos = fetch_all_pages(f"/orgs/{ORG}/repos?type=public")

    total_repos = len(repos)
    total_forks = 0
    total_stars = 0
    total_open_issues = 0
    license_set: set[str] = set()
    language_bytes: dict[str, int] = {}
    source_count = 0
    fork_count = 0

    for repo in repos:
        total_forks += repo.get("forks_count", 0)
        total_stars += repo.get("stargazers_count", 0)
        total_open_issues += repo.get("open_issues_count", 0)

        if repo.get("fork"):
            fork_count += 1
        else:
            source_count += 1

        # License
        lic = repo.get("license")
        if lic and lic.get("spdx_id") and lic["spdx_id"] != "NOASSERTION":
            license_set.add(lic["spdx_id"])

        # Languages (per-repo)
        lang_url = repo.get("languages_url", "")
        if lang_url:
            lang_data = _api_get(lang_url)
            if lang_data:
                for lang, nbytes in lang_data.items():
                    language_bytes[lang] = language_bytes.get(lang, 0) + nbytes

    # Filter excluded languages
    filtered_langs = {
        k: v for k, v in language_bytes.items() if k not in EXCLUDED_LANGUAGES
    }
    total_bytes = sum(filtered_langs.values()) or 1

    # Sort and calculate percentages
    lang_sorted = sorted(filtered_langs.items(), key=lambda x: x[1], reverse=True)
    lang_pcts = []
    for lang, nbytes in lang_sorted:
        pct = nbytes / total_bytes * 100
        if pct >= 1.0:  # only show >= 1%
            lang_pcts.append((lang, round(pct, 1)))

    # Top N for summary
    top_languages = [lp[0] for lp in lang_pcts[:6]]

    # Licenses as sorted list
    licenses = sorted(license_set) if license_set else ["MIT"]

    return {
        "total_repos": total_repos,
        "source_repos": source_count,
        "forked_repos": fork_count,
        "total_forks": total_forks,
        "total_stars": total_stars,
        "total_open_issues": total_open_issues,
        "licenses": licenses,
        "top_languages": top_languages,
        "lang_pcts": lang_pcts,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


# ──────────────────────────────────────────────────────────────────────
# Markdown generation
# ──────────────────────────────────────────────────────────────────────

def _bar(pct: float, width: int = BAR_WIDTH) -> str:
    """Generate an ASCII bar: ████████░░░░░░░░░░░░"""
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def generate_hero_badges(stats: dict) -> str:
    """Generate the HERO badge row."""
    repo_count = stats["total_repos"]
    licenses_label = "_|_".join(stats["licenses"]).replace("-", "--")
    return f"""\
[![Base](https://img.shields.io/badge/Base-Europe_🇪🇺-003399?style=flat-square)](https://eurun.eu.org)
[![Website](https://img.shields.io/badge/Web-eurun.eu.org-0969da?style=flat-square&logo=google-chrome&logoColor=white)](https://eurun.eu.org)
[![Email](https://img.shields.io/badge/Contact-info%40eurun.eu.org-ea4335?style=flat-square&logo=gmail&logoColor=white)](mailto:info@eurun.eu.org)
[![Repos](https://img.shields.io/badge/Repos-{repo_count}-181717?style=flat-square&logo=github)](https://github.com/orgs/EUR-UN/repositories)
[![License](https://img.shields.io/badge/Open_Source-{licenses_label}-3da639?style=flat-square&logo=open-source-initiative&logoColor=white)](#-engineering-principles)"""


def generate_about_stats(stats: dict) -> str:
    """Generate the quick-stats table in the About section."""
    top_langs = " · ".join(f"<b>{l}</b>" for l in stats["top_languages"][:5])
    licenses_str = " / ".join(stats["licenses"])
    return f"""\
<table>
<tr>
<td><b>🔧 {stats['total_repos']}</b> Public Repositories</td>
<td><b>🐍</b> {top_langs}</td>
<td><b>🌍 {stats['total_forks']}</b> Community Forks</td>
<td><b>📜 {licenses_str}</b> Licensed</td>
</tr>
</table>"""


def generate_tech_stack(stats: dict) -> str:
    """Generate the Tech Stack at a Glance section."""
    lines = []

    # Language bars
    for i, (lang, pct) in enumerate(stats["lang_pcts"][:8]):
        bar = _bar(pct)
        label = f"{lang} ({pct}%)"
        prefix = "Languages" if i == 0 else "        "
        lines.append(f"  {prefix:18s}{bar}  {label}")

    # Static domain info
    lines.append("")
    lines.append("  Domains           Network Infra · Cybersecurity · Automation · IoT · Data Science")
    lines.append("  Protocols         MQTT · SSH · TLS/SSL · HTTP/CDN · REST API")
    lines.append("  Platforms         Linux · macOS · Home Assistant · ERPNext · Jupyter")

    body = "\n".join(lines)
    return f"```text\n{body}\n```"


def generate_org_stats_table(stats: dict) -> str:
    """Generate the Organization Statistics table."""
    licenses_str = " · ".join(stats["licenses"])
    top_langs_str = " · ".join(stats["top_languages"][:5])
    return f"""\
<div align="center">

| Metric | Value |
|:-------|:------|
| Public Repositories | **{stats['total_repos']}** ({stats['source_repos']} source · {stats['forked_repos']} forked) |
| Total Stars | **{stats['total_stars']}** |
| Community Forks | **{stats['total_forks']}** |
| Open Issues | **{stats['total_open_issues']}** |
| Primary Languages | {top_langs_str} |
| Licenses | {licenses_str} |
| Base | Europe 🇪🇺 · Globally Distributed |
| Website | [eurun.eu.org](https://eurun.eu.org) |

<sub>Auto-updated by CI · Last run: {stats['updated_at']}</sub>

</div>"""


# ──────────────────────────────────────────────────────────────────────
# README update logic
# ──────────────────────────────────────────────────────────────────────

def replace_section(content: str, tag: str, replacement: str) -> str:
    """Replace content between <!-- {tag}_START --> and <!-- {tag}_END -->."""
    pattern = re.compile(
        rf"(<!-- {tag}_START -->)\n.*?\n(<!-- {tag}_END -->)",
        re.DOTALL,
    )
    new_content = f"\\1\n{replacement}\n\\2"
    result, count = pattern.subn(new_content, content)
    if count == 0:
        print(f"[WARN] Marker <!-- {tag}_START/END --> not found in README", file=sys.stderr)
    return result


def update_readme(stats: dict, dry_run: bool = False) -> bool:
    """Read the README, replace all dynamic sections, write back.
    Returns True if content changed."""

    if not README_PATH.exists():
        print(f"[ERROR] README not found at {README_PATH}", file=sys.stderr)
        return False

    content = README_PATH.read_text(encoding="utf-8")
    original = content

    content = replace_section(content, "HERO_BADGES", generate_hero_badges(stats))
    content = replace_section(content, "ABOUT_STATS", generate_about_stats(stats))
    content = replace_section(content, "TECH_STACK", generate_tech_stack(stats))
    content = replace_section(content, "ORG_STATS", generate_org_stats_table(stats))

    changed = content != original

    if dry_run:
        print(content)
        print(f"\n--- {'CHANGED' if changed else 'NO CHANGE'} ---", file=sys.stderr)
    else:
        README_PATH.write_text(content, encoding="utf-8")
        status = "updated" if changed else "unchanged"
        print(f"[OK] README {status} at {README_PATH}")

    return changed


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv

    print(f"[INFO] Collecting stats for {ORG}...")
    stats = collect_org_stats()

    print(f"[INFO] Repos: {stats['total_repos']}  Stars: {stats['total_stars']}  Forks: {stats['total_forks']}")
    print(f"[INFO] Top languages: {', '.join(f'{l} ({p}%)' for l, p in stats['lang_pcts'][:6])}")
    print(f"[INFO] Licenses: {', '.join(stats['licenses'])}")

    # Safety: refuse to write zeros (likely API rate-limit or auth failure)
    if stats["total_repos"] == 0:
        print("[ERROR] API returned 0 repos — likely rate-limited or auth failure. Skipping update.", file=sys.stderr)
        gh_output = os.environ.get("GITHUB_OUTPUT", "")
        if gh_output:
            with open(gh_output, "a") as f:
                f.write("changed=false\n")
        return 1

    changed = update_readme(stats, dry_run=dry_run)

    # Write output for GitHub Actions
    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
