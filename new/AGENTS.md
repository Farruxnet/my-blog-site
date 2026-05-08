# Agent Instructions For `new/`

## Purpose

`new/` is the maintainable prototype for the future farruxnet.uz static docs/blog generator. It should stay simple, static-host friendly, and close to the visual language of farruxnet.uz/MkDocs Material.

## Structure

- `index.html` is the docs/blog home page.
- `about.html` and `contact.html` are static pages.
- `post.html` is generated from Markdown and should not be hand-edited unless the user asks.
- `content/` stores Markdown source files.
- `templates/` stores generator HTML templates.
- `scripts/build_post.py` converts Markdown to HTML.
- `assets/css/style.css` stores shared styling.
- `assets/js/site.js` stores shared UI behavior.

## Design Rules

- Keep the UI single-column for article content unless the user asks for side navigation again.
- Keep colors, header, footer, fonts, and code blocks close to farruxnet.uz/MkDocs Material.
- Use Roboto for text and Roboto Mono for code.
- Use PrismJS for code highlighting.
- Do not add code block title bars or line numbers by default.
- Keep copy buttons on code blocks.
- Preserve dark/light mode.
- Keep `Home`, `About`, `Contact` as the main navigation.

## Markdown Generator Rules

- Source Markdown lives in `content/`.
- Use front matter keys: `title`, `date`, `description`, `tags`.
- Code fences should stay simple, for example:

~~~md
```python
print("hello")
```
~~~

- The generator should output semantic HTML with `language-*` classes for PrismJS.
- Templates should be edited in `templates/`, not inside generated output.
- Build with:

```powershell
python new\scripts\build_post.py new\content\test-post.md new\post.html
```

## Verification

After changing `new/`:

- Open `http://127.0.0.1:8000/new/index.html`.
- Open `http://127.0.0.1:8000/new/post.html`.
- Check search opens and returns results.
- Check dark/light mode toggles.
- Check mobile menu toggles.
- Check Prism tokens are present in code blocks.
- Check each code block has one copy button.
- Check browser console has no errors.
