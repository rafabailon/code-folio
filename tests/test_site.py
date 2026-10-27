import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ROOT / "index.html",
    ROOT / "en" / "index.html",
    ROOT / "en" / "projects.html",
    ROOT / "en" / "resume.html",
    ROOT / "es" / "index.html",
    ROOT / "es" / "projects.html",
    ROOT / "es" / "resume.html",
)


class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title_depth = 0
        self.title = []
        self.ids = set()
        self.links = []
        self.stylesheets = []
        self.scripts = []
        self.resources = []
        self.meta = []
        self.landmarks = set()
        self.tag_counts = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        if tag == "html":
            self.lang = attributes.get("lang")
        if tag == "title":
            self.title_depth += 1
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag == "link" and attributes.get("href"):
            self.resources.append(attributes["href"])
            if attributes.get("rel") == "stylesheet":
                self.stylesheets.append(attributes["href"])
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"])
            self.resources.append(attributes["src"])
        if tag == "meta":
            self.meta.append(attributes)
        if tag in {"header", "main", "nav", "footer"}:
            self.landmarks.add(tag)

    def handle_endtag(self, tag):
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data):
        if self.title_depth:
            self.title.append(data.strip())


def inspect_page(path):
    parser = PageInspector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class StaticSiteTests(unittest.TestCase):
    def test_every_page_has_language_title_viewport_and_description(self):
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                parser = inspect_page(page)
                self.assertIn(parser.lang, {"en", "es"})
                self.assertTrue("".join(parser.title))
                self.assertTrue(
                    any(
                        meta.get("name") == "viewport"
                        for meta in parser.meta
                    )
                )
                self.assertTrue(
                    any(
                        meta.get("name") == "description"
                        for meta in parser.meta
                    )
                )
                self.assertEqual(parser.tag_counts.get("main"), 1)

    def test_all_local_page_and_asset_links_resolve(self):
        for page in PAGES:
            parser = inspect_page(page)
            for reference in [*parser.links, *parser.resources]:
                with self.subTest(page=page.relative_to(ROOT), reference=reference):
                    parsed = urlsplit(reference)
                    if parsed.scheme or parsed.netloc or reference.startswith("data:"):
                        continue
                    target = page.parent / unquote(parsed.path)
                    if not parsed.path:
                        target = page
                    elif target.is_dir():
                        target = target / "index.html"
                    self.assertTrue(target.is_file(), f"Missing local target: {reference}")
                    if parsed.fragment and target.suffix == ".html":
                        self.assertIn(
                            unquote(parsed.fragment),
                            inspect_page(target).ids,
                            f"Missing anchor in {target}: {parsed.fragment}",
                        )

    def test_bilingual_pages_are_paired(self):
        for filename in ("index.html", "projects.html", "resume.html"):
            with self.subTest(page=filename):
                english = inspect_page(ROOT / "en" / filename)
                spanish = inspect_page(ROOT / "es" / filename)
                self.assertEqual(english.lang, "en")
                self.assertEqual(spanish.lang, "es")
                self.assertIn("EN", (ROOT / "en" / filename).read_text(encoding="utf-8"))
                self.assertIn("ES", (ROOT / "es" / filename).read_text(encoding="utf-8"))

    def test_pages_have_accessibility_landmarks_and_skip_link(self):
        for page in PAGES[1:]:
            with self.subTest(page=page.relative_to(ROOT)):
                parser = inspect_page(page)
                self.assertTrue({"header", "main", "nav", "footer"}.issubset(parser.landmarks))
                self.assertIn("main", parser.ids)
                source = page.read_text(encoding="utf-8")
                self.assertIn('class="skip-link"', source)
                self.assertIn("aria-label=", source)
                self.assertNotIn("style=", source)

    def test_styles_include_responsive_and_reduced_motion_rules(self):
        stylesheet = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 760px)", stylesheet)
        self.assertIn("@media (max-width: 540px)", stylesheet)
        self.assertIn("@media (prefers-reduced-motion: reduce)", stylesheet)
        self.assertIn("@media print", stylesheet)
        self.assertIn(".js-enabled .reveal", stylesheet)
        self.assertIn(".js-enabled .nav-links", stylesheet)

    def test_project_cards_have_categories_for_filtering(self):
        for language in ("en", "es"):
            with self.subTest(language=language):
                page = ROOT / language / "projects.html"
                parser = inspect_page(page)
                source = page.read_text(encoding="utf-8")
                self.assertIn('data-filter="all"', source)
                self.assertIn('data-filter="python"', source)
                self.assertIn('data-filter="web"', source)
                for project in ("path-quest", "prancing-pony", "valinor-reviews", "arkham-walker"):
                    self.assertIn(project, parser.ids)


if __name__ == "__main__":
    unittest.main()
