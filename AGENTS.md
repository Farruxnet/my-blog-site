# Agent Instructions

## Project Goal

This repository is a lightweight static personal blog site. Preserve the simple HTML/CSS/JavaScript setup and keep it easy to host on GitHub Pages or any static hosting provider.

## File Organization

- Keep deployable pages at the repository root, such as `index.html` and `post.html`.
- Store shared styles in `assets/css/style.css`.
- Store reusable scripts in `assets/js`.
- Do not introduce framework folders, package manifests, or generated build output unless the user explicitly asks for a build system.

## Coding Guidelines

- Use plain HTML, CSS, and JavaScript.
- Keep page links relative so the site works from a GitHub Pages subpath.
- Preserve Uzbek content and user-facing labels unless the user asks to rewrite them.
- Keep the visual style calm, readable, and suitable for a personal technical blog.
- Prefer small, focused JavaScript files over inline scripts when logic is shared.

## Verification

After changing HTML, CSS, or JavaScript:

- Check that `index.html` links to `post.html`.
- Check that `post.html` loads shared CSS and both JavaScript helpers.
- Check that mobile navigation still toggles.
- Check that code blocks on `post.html` still receive copy buttons.

## Deployment

The default branch is `master`. Commit only intentional source files and push to `origin/master` when the user asks to publish.
