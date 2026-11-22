import unittest
from pathlib import Path

from sort_profile_by_stars import featured_repos, sort_readme

README = Path(__file__).resolve().parents[1] / "README.md"

SAMPLE = """# Intro

## 🚀 Featured Projects

### Media

#### [low](https://github.com/vbasky/low) — Low
Low body.

#### [high](https://github.com/vbasky/high) — High
High body.

#### [tied](https://github.com/vbasky/tied-a) — Tied A
Tied A stays ahead of an equal count.

#### [tied b](https://github.com/vbasky/tied-b) — Tied B
Tied B follows.

### Data

#### [only](https://github.com/vbasky/only) — Only
Only body.

---

## 💼 Career

Leave this [link](https://github.com/vbasky/ignored) where it is.
"""


class SortReadmeTest(unittest.TestCase):
    def test_sorts_within_sections_and_keeps_ties(self) -> None:
        stars = {"low": 1, "high": 9, "tied-a": 4, "tied-b": 4, "only": 2, "ignored": 100}
        updated = sort_readme(SAMPLE, stars)
        self.assertEqual(
            featured_repos(updated),
            ["high", "tied-a", "tied-b", "low", "only"],
        )
        self.assertIn("## 💼 Career", updated)
        self.assertLess(updated.index("Career"), updated.index("vbasky/ignored"))
        self.assertLess(updated.index("---"), updated.index("## 💼 Career"))
        self.assertTrue(updated.endswith("where it is.\n"))

    def test_real_readme_round_trips_when_order_is_already_correct(self) -> None:
        text = README.read_text(encoding="utf-8")
        repos = featured_repos(text)
        stars = {repo: len(repos) - index for index, repo in enumerate(repos)}
        self.assertEqual(sort_readme(text, stars), text)

    def test_missing_star_count_fails(self) -> None:
        with self.assertRaises(SystemExit):
            sort_readme(SAMPLE, {"low": 1})

    def test_sorts_table_rows_inside_each_section(self) -> None:
        text = """## Featured Projects

### Media

| Before | After |
| --- | --- |
| old-low | [low](https://github.com/vbasky/low) stays the sentence. |
| old-high | [high](https://github.com/vbasky/high) moves up. |

### Desk

| Before | After |
| --- | --- |
| tied first | [aa](https://github.com/vbasky/aa) keeps its place. |
| tied second | [bb](https://github.com/vbasky/bb) follows. |

---

## Elsewhere

| Leave | [ignored](https://github.com/vbasky/ignored) alone. |
| --- | --- |
| this | row |
"""
        stars = {"low": 1, "high": 8, "aa": 3, "bb": 3, "ignored": 100}
        updated = sort_readme(text, stars)
        self.assertEqual(featured_repos(updated), ["high", "low", "aa", "bb"])
        self.assertLess(updated.index("high"), updated.index("low"))
        self.assertLess(updated.index("aa"), updated.index("bb"))
        self.assertLess(updated.index("## Elsewhere"), updated.index("vbasky/ignored"))
        self.assertEqual(sort_readme(updated, stars), updated)


if __name__ == "__main__":
    unittest.main()
