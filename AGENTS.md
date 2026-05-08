# Agent Instructions

## Project Vision

This repository is evolving into a lightweight static site generator for developers, inspired by MkDocs Material, but kept simple and easy to host. The long-term goal is:

- Write posts and documentation in Markdown (`.md`).
- Generate static HTML pages from Markdown.
- Keep the generated site fast, readable, responsive, and suitable for technical content.
- Deploy easily to GitHub Pages or any static hosting provider.

Agents should treat this project as a developer-focused static documentation/blog platform, not as a marketing site or a framework app.

## Core Principles

- Prefer plain HTML, CSS, and JavaScript for the published site.
- Keep the architecture understandable for one person to maintain.
- Optimize for readable technical articles, code blocks, navigation, and search/discovery.
- Preserve Uzbek user-facing content unless the user explicitly asks to rewrite it.
- Keep links relative so the site works from GitHub Pages subpaths.
- Avoid unnecessary dependencies, generated clutter, or framework lock-in.
- Make changes incrementally and verify behavior after each meaningful frontend change.

## File Organization

Current deployable pages live at the repository root:

- `index.html`
- `post.html`

Shared assets:

- `assets/css/style.css` for site-wide styles.
- `assets/js/site.js` for shared UI behavior.
- `assets/js/code-copy.js` for code block copy buttons.

Future generator-friendly organization should prefer:

- `content/` for source Markdown files.
- `templates/` for reusable HTML templates.
- `assets/` for deployable CSS, JavaScript, images, icons, and fonts.
- `dist/` or `site/` only when the user explicitly asks for generated output to be committed.

Do not introduce framework folders, package manifests, or generated build output unless the user asks to build the generator or add a build system.

## Generator Direction

When asked to add Markdown-to-HTML generation:

- Keep source posts as `.md` files.
- Preserve front matter support if introduced, using simple metadata such as `title`, `date`, `description`, `tags`, `slug`, and `draft`.
- Generate clean, semantic HTML.
- Keep generated page links relative.
- Prefer a small, transparent generator script over a large framework.
- If dependencies become necessary, choose minimal, well-known libraries and explain why.
- Do not overwrite hand-written content or generated files without checking existing structure first.

Expected Markdown features for technical content:

- Headings with stable anchor links.
- Code fences with language classes for Prism or another chosen highlighter.
- Tables.
- Blockquotes.
- Lists and task lists.
- Inline code.
- Article metadata.

## Design And UX

- The site should feel calm, readable, and developer-focused.
- Do not create a landing page unless the user asks for one.
- The first screen should expose useful content, navigation, or documentation structure.
- Keep typography comfortable for long technical reading.
- Keep layout responsive on mobile and desktop.
- Avoid decorative clutter, heavy gradients, or oversized marketing sections.
- Use icons where they improve scanning, such as footer social links or navigation affordances.
- Keep footer and header consistent across pages.

## HTML Guidelines

- Use semantic HTML: `header`, `nav`, `main`, `article`, `section`, `footer`.
- Each page should have a meaningful `<title>`.
- Add a concise `<meta name="description">` when useful.
- Keep accessible labels for icon-only controls and links.
- Menu buttons should use `type="button"`, `aria-controls`, and correctly updated `aria-expanded`.
- External links should be intentional. Add `rel="noopener"` with `target="_blank"` when opening new tabs.
- Avoid inline scripts when logic is shared across pages.

## CSS Guidelines

- Keep shared styles in `assets/css/style.css`.
- Prefer stable, reusable classes over one-off styling.
- Keep styles readable and grouped by feature.
- Do not let text overlap or overflow awkwardly on mobile.
- Keep code blocks horizontally scrollable.
- Preserve dark mode behavior when touching colors.
- Avoid unused selectors. Remove obsolete CSS when markup changes.

## JavaScript Guidelines

- Keep JavaScript small, focused, and framework-free unless the user asks otherwise.
- Put reusable behavior in `assets/js`.
- Scope selectors narrowly to the feature they control.
- Make scripts resilient when optional elements are missing.
- Avoid duplicate event handlers or duplicate generated buttons.
- Defer non-critical scripts where possible.
- Keep copy-button behavior working for all article code blocks.

## External Resources

- Avoid unused third-party scripts, stylesheets, fonts, and trackers.
- Only add CDN resources when they are clearly needed.
- If a local asset would be more reliable than a CDN resource, prefer local assets when practical.
- Keep Font Awesome usage limited to icons that are actually displayed.
- Keep syntax highlighting resources limited to pages that need code highlighting.

## Content Rules

- Preserve Uzbek text and labels unless asked to rewrite them.
- Keep technical terms accurate.
- Do not silently translate content.
- Do not replace real article content with placeholders unless the user requests sample content.
- When generating docs/posts from Markdown, preserve code exactly unless formatting is explicitly requested.

## Verification Checklist

After changing HTML, CSS, JavaScript, templates, or generator behavior:

- Check that `index.html` links to `post.html` or to the generated post route expected by the current structure.
- Check that article pages load shared CSS.
- Check that article pages load shared JavaScript helpers.
- Check that mobile navigation toggles correctly.
- Check that icon-only links/buttons have accessible labels.
- Check that code blocks receive copy buttons.
- Check that code block language classes match the displayed code.
- Check that browser console errors were not introduced.
- Check that relative links still work from a subpath-friendly static host.
- If using a local static server for verification, stop it after testing.

For generator changes:

- Run the generator on at least one Markdown file.
- Inspect the generated HTML structure.
- Confirm front matter is parsed correctly if front matter exists.
- Confirm generated slugs and links are stable.
- Confirm code fences keep their language classes.
- Confirm generated files do not overwrite source files unexpectedly.

## Git And Deployment

- The default branch is `master`.
- Commit only intentional source files.
- Do not commit IDE metadata such as `.idea/` unless the user explicitly asks.
- Do not commit generated output unless the user asks for generated files to be versioned.
- Push to `origin/master` only when the user asks to publish.
- Never revert user changes unless the user explicitly asks.

## How Agents Should Work

Before editing:

- Inspect the current file structure.
- Read the relevant HTML, CSS, JavaScript, Markdown, templates, or generator files.
- Check `git status --short` and avoid touching unrelated changes.

While editing:

- Keep changes focused on the user's request.
- Prefer small patches over broad rewrites.
- Preserve the current static-hosting friendliness.
- Explain important architectural choices briefly.

Before finishing:

- Run the relevant verification checklist.
- Summarize what changed.
- Mention any checks that could not be run.
- Mention unrelated untracked files only if they matter.
