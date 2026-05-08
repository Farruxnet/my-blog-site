# My Blog Site

Static personal blog prototype for `farruxnet.uz`.

The project contains a responsive blog index page, a post detail page, shared typography styles, PrismJS-powered code highlighting, and small JavaScript helpers for the mobile menu and code-copy buttons.

## Structure

```text
.
|-- index.html
|-- post.html
|-- assets
|   |-- css
|   |   `-- style.css
|   `-- js
|       |-- code-copy.js
|       `-- site.js
|-- AGENTS.md
`-- README.md
```

## Pages

- `index.html` is the blog list page.
- `post.html` is the article detail page.

## Local Usage

Open `index.html` directly in a browser, or serve the folder with any static file server.

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Dependencies

This project does not use a package manager or build step.

External browser dependencies are loaded through CDN:

- Tailwind CDN for utility classes.
- PrismJS CDN for code highlighting on post pages.
- Google Fonts for article typography.

## Development Notes

- Keep root HTML files deployable as plain static pages.
- Put shared CSS in `assets/css/style.css`.
- Put reusable JavaScript in `assets/js`.
- Avoid adding a build pipeline unless the project grows beyond a small static site.
