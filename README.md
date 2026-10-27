# Code Folio

A responsive, bilingual portfolio starter for GitHub Pages. It uses static HTML, shared CSS and vanilla JavaScript, and the Tailwind CSS CDN. No build step or backend is required. Clean, accessible, and easy to personalize.

## Preview locally

From the project root, start a static server:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. Choose English or Spanish, then browse the home, projects, and résumé pages.

## Personalize before publishing

Replace the sample content throughout `en/` and `es/`:

- Update `Your Name` / `Tu nombre`, role, biography, skills, and experience.
- Change the `hello@example.com` email and the GitHub and LinkedIn profile links.
- Add repository and live-demo URLs to the project cards. This starter intentionally does not invent public links.
- Review project summaries and replace them with your own work as needed.
- Update page titles, descriptions, and Open Graph metadata for your identity.
- The résumé is a printable HTML page. Use **Print / Save PDF** and choose **Save as PDF** in the browser; replace every bracketed prompt first.

English pages live in `en/`; Spanish pages live in `es/`. The root `index.html` is a language chooser. Each language switch links to its equivalent page in the other language. Shared assets are in `assets/`.

### Choose English or Spanish

Start at `/` (the root `index.html`) and choose **English** or **Español**. To bypass the chooser, open `en/index.html` or `es/index.html`; use `en/projects.html` / `es/projects.html` and `en/resume.html` / `es/resume.html` for the corresponding inner pages. Each page's language switch links directly to its equivalent in the other language.

## Publish with GitHub Pages

1. Push the contents of this folder to a GitHub repository.
2. In the repository, open **Settings → Pages**.
3. Choose **Deploy from a branch**, select the branch and `/ (root)`, then save.
4. Open the published URL and check both language paths.

The Tailwind CDN and Google Fonts import need an internet connection. The layout and content remain readable with the system-font fallbacks if remote fonts are unavailable. For production-scale sites, consider compiling Tailwind locally to avoid loading the full CDN runtime.

## Features

- Bilingual (English / Español) with a simple language chooser
- Responsive design with mobile navigation and reduced-motion support
- Accessible markup with skip links, landmarks, and ARIA attributes
- Project filtering on the projects page
- Print-friendly résumé
- SEO-friendly metadata, sitemap, robots.txt, and a custom 404 page

## Tests

Run the built-in static-site checks with Python 3.10 or later:

```sh
make test
```

The checks validate page language metadata, local page and asset links, bilingual page pairs, accessibility landmarks, and responsive CSS breakpoints. The equivalent direct command is `python3 -m unittest discover -s tests -v`.

## Structure

```text
assets/
  css/site.css
  js/site.js
  js/projects.js
  favicon.svg
en/
  index.html
  projects.html
  resume.html
es/
  index.html
  projects.html
  resume.html
tests/
  test_site.py
404.html
index.html
Makefile
README.md
robots.txt
sitemap.xml
```
