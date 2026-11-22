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
DELIMITER_CELL = re.compile(r":?-{3,}:?")


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


def is_delimiter(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return bool(cells) and all(DELIMITER_CELL.fullmatch(cell) for cell in cells)


def sort_one_table(block: list[str], stars: dict[str, int]) -> list[str]:
    if len(block) < 3 or not is_delimiter(block[1]):
        return block
    rows = block[2:]
    if not rows or any(REPO.search(row) is None for row in rows):
        return block
    missing = []
    for row in rows:
        match = REPO.search(row)
        assert match is not None
        if match.group(1) not in stars:
            missing.append(match.group(1))
    if missing:
        raise SystemExit("Missing star counts for: " + ", ".join(missing))

    def row_key(item: tuple[int, str]) -> tuple[int, int]:
        match = REPO.search(item[1])
        assert match is not None
        return (-stars[match.group(1)], item[0])

    ranked = sorted(enumerate(rows), key=row_key)
    return [block[0], block[1], *[row for _, row in ranked]]


def sort_table_rows(body: str, stars: dict[str, int]) -> str:
    lines = body.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            output.append(lines[index])
            index += 1
            continue
        block: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            block.append(lines[index])
            index += 1
        output.extend(sort_one_table(block, stars))
    return "".join(output)


def section_report(body: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    title: str | None = None
    repos: list[str] = []

    def flush() -> None:
        if title is not None:
            sections.append((title, list(repos)))

    for line in body.splitlines():
        if line.startswith("### "):
            flush()
            title = line.strip().lstrip("#").strip()
            repos = []
            continue
        if title is None:
            continue
        if line.startswith("#### ") or (line.lstrip().startswith("|") and not is_delimiter(line)):
            match = REPO.search(line)
            if match:
                repos.append(match.group(1))
    flush()
    return sections


def sort_readme(text: str, stars: dict[str, int]) -> str:
    prefix, body, rest = split_featured(text)
    body = sort_table_rows(body, stars)
    preamble, sections, trailing = parse_body(body)
    sort_sections(sections, stars)
    return render(prefix, preamble, sections, trailing, rest)


def featured_repos(text: str) -> list[str]:
    _, body, _ = split_featured(text)
    return [repo for _, repos in section_report(body) for repo in repos]


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
    for title, repos in section_report(body):
        order = ", ".join(f"{repo} ({stars[repo]})" for repo in repos)
        print(f"{title}: {order}")
    if updated == text:
        print("Order unchanged.")
        return
    README.write_text(updated, encoding="utf-8")
    print("README updated.")


if __name__ == "__main__":
    main()
