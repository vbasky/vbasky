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


if __name__ == "__main__":
    unittest.main()
