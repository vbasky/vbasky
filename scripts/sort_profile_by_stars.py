#!/usr/bin/env python3
"""Reorder Featured Projects inside each section by GitHub stars.

The profile README is static Markdown. This script rewrites the order of the
project blocks under Media, Data, and Desktop. A tie keeps the existing order.
Prose stays attached to its heading. Nothing outside Featured Projects moves.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"
REPO = re.compile(r"https://github\.com/vbasky/([A-Za-z0-9._-]+)")
TRAILING_RULE = re.compile(r"\n---\n(?:\n)?\Z")


@dataclass
class Project:
    repo: str
    text: str
    index: int


@dataclass
class Section:
    header: str
    projects: list[Project]


def is_h2(line: str) -> bool:
    return line.startswith("## ") and not line.startswith("###")


def split_featured(text: str) -> tuple[str, str, str]:
    lines = text.splitlines(keepends=True)
    start = next(
        (i for i, line in enumerate(lines) if is_h2(line) and "Featured Projects" in line),
        None,
    )
    if start is None:
        raise SystemExit("Featured Projects heading not found")
    end = next((j for j in range(start + 1, len(lines)) if is_h2(lines[j])), None)
    if end is None:
        raise SystemExit("No heading after Featured Projects")
    prefix = "".join(lines[: start + 1])
    body = "".join(lines[start + 1 : end])
    rest = "".join(lines[end:])
    return prefix, body, rest


def peel_trailing_rule(body: str) -> tuple[str, str]:
    match = TRAILING_RULE.search(body)
    if match is None:
        return body, ""
    return body[: match.start() + 1], body[match.start() + 1 :]


def parse_body(body: str) -> tuple[str, list[Section], str]:
    body, trailing = peel_trailing_rule(body)
    lines = body.splitlines(keepends=True)
    preamble: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    project_lines: list[str] | None = None
    index = 0

    def close_project() -> None:
        nonlocal project_lines, index
        if project_lines is None:
            return
        if current is None:
            raise SystemExit("Project heading appeared before a section")
        text = "".join(project_lines)
        match = REPO.search(text)
        if match is None:
            raise SystemExit("A project block has no https://github.com/vbasky/ link")
        current.projects.append(Project(match.group(1), text, index))
        index += 1
        project_lines = None

    i = 0
    while i < len(lines) and not lines[i].startswith("### "):
        preamble.append(lines[i])
        i += 1

    while i < len(lines):
        line = lines[i]
        if line.startswith("#### "):
            close_project()
            project_lines = [line]
            i += 1
            continue
        if line.startswith("### "):
            close_project()
            current = Section(header=line, projects=[])
            sections.append(current)
            i += 1
            while i < len(lines) and not lines[i].startswith("### ") and not lines[i].startswith("#### "):
                current.header += lines[i]
                i += 1
            continue
        if project_lines is not None:
            project_lines.append(line)
        elif current is not None:
            current.header += line
        else:
            preamble.append(line)
        i += 1
    close_project()
    if not sections:
        raise SystemExit("Featured Projects has no sections")
    return "".join(preamble), sections, trailing


def sort_sections(sections: list[Section], stars: dict[str, int]) -> None:
    for section in sections:
        missing = [project.repo for project in section.projects if project.repo not in stars]
        if missing:
            raise SystemExit("Missing star counts for: " + ", ".join(missing))
        section.projects.sort(key=lambda project: (-stars[project.repo], project.index))


def render(prefix: str, preamble: str, sections: list[Section], trailing: str, rest: str) -> str:
    parts = [prefix, preamble]
    for section in sections:
        parts.append(section.header)
        for project in section.projects:
            parts.append(project.text)
    parts.append(trailing)
    parts.append(rest)
    return "".join(parts)


def sort_readme(text: str, stars: dict[str, int]) -> str:
    prefix, body, rest = split_featured(text)
    preamble, sections, trailing = parse_body(body)
    sort_sections(sections, stars)
    return render(prefix, preamble, sections, trailing, rest)


def featured_repos(text: str) -> list[str]:
    _, body, _ = split_featured(text)
    _, sections, _ = parse_body(body)
    return [project.repo for section in sections for project in section.projects]


def fetch_stars(repo: str) -> int:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return fetch_stars_http(repo, token)
    if shutil.which("gh"):
        output = subprocess.check_output(
            ["gh", "api", f"repos/vbasky/{repo}", "--jq", ".stargazers_count"],
            text=True,
        )
        return int(output.strip())
    return fetch_stars_http(repo, None)


def fetch_stars_http(repo: str, token: str | None) -> int:
    request = urllib.request.Request(
        f"https://api.github.com/repos/vbasky/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "vbasky-profile-sort",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"GitHub star lookup failed for {repo}: HTTP {error.code}") from error
    if "stargazers_count" not in payload:
        raise SystemExit(f"GitHub star lookup failed for {repo}: no stargazers_count")
    return int(payload["stargazers_count"])


def main() -> None:
    text = README.read_text(encoding="utf-8")
    repos = featured_repos(text)
    stars = {repo: fetch_stars(repo) for repo in dict.fromkeys(repos)}
    updated = sort_readme(text, stars)
    _, body, _ = split_featured(updated)
    _, sections, _ = parse_body(body)
    for section in sections:
        title = section.header.strip().lstrip("#").strip()
        order = ", ".join(f"{project.repo} ({stars[project.repo]})" for project in section.projects)
        print(f"{title}: {order}")
    if updated == text:
        print("Order unchanged.")
        return
    README.write_text(updated, encoding="utf-8")
    print("README updated.")


if __name__ == "__main__":
    main()
