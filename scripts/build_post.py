from __future__ import annotations

import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_front_matter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown

    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, markdown

    meta: dict[str, str] = {}
    for line in markdown[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()

    return meta, markdown[end + 5 :].lstrip()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def inline_markdown(text: str) -> str:
    code_parts: list[str] = []

    def keep_code(match: re.Match[str]) -> str:
        code_parts.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"@@CODE{len(code_parts) - 1}@@"

    text = re.sub(r"`([^`]+)`", keep_code, html.escape(text))
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    for index, code in enumerate(code_parts):
        text = text.replace(f"@@CODE{index}@@", code)

    return text


def parse_table(lines: list[str], start: int) -> tuple[str, int] | None:
    if start + 1 >= len(lines):
        return None

    header = lines[start]
    separator = lines[start + 1]
    if "|" not in header or not re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", separator):
        return None

    def cells(row: str) -> list[str]:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    headers = cells(header)
    rows: list[list[str]] = []
    index = start + 2

    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        rows.append(cells(lines[index]))
        index += 1

    head_html = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in headers)
    body_html = "\n".join(
        "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )

    return f"<table>\n<thead><tr>{head_html}</tr></thead>\n<tbody>\n{body_html}\n</tbody>\n</table>", index


def parse_list(lines: list[str], start: int) -> tuple[str, int] | None:
    first = lines[start]
    unordered = re.match(r"^\s*[-*]\s+(.+)$", first)
    ordered = re.match(r"^\s*\d+\.\s+(.+)$", first)
    if not unordered and not ordered:
        return None

    tag = "ul" if unordered else "ol"
    items: list[str] = []
    index = start

    while index < len(lines):
        line = lines[index]
        match = re.match(r"^\s*[-*]\s+(.+)$", line) if tag == "ul" else re.match(r"^\s*\d+\.\s+(.+)$", line)
        if not match:
            break

        value = match.group(1)
        task = re.match(r"^\[(x|X| )\]\s+(.+)$", value)
        if task:
            checked = " checked" if task.group(1).lower() == "x" else ""
            value = f'<input type="checkbox"{checked} disabled> {inline_markdown(task.group(2))}'
        else:
            value = inline_markdown(value)

        items.append(f"<li>{value}</li>")
        index += 1

    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", index


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            index += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip() or "text"
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            escaped_code = html.escape("\n".join(code))
            output.append(f'<pre class="language-{language}"><code class="language-{language}">{escaped_code}</code></pre>')
            continue

        table = parse_table(lines, index)
        if table:
            flush_paragraph()
            output.append(table[0])
            index = table[1]
            continue

        listed = parse_list(lines, index)
        if listed:
            flush_paragraph()
            output.append(listed[0])
            index = listed[1]
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quotes: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quotes.append(lines[index].strip()[1:].strip())
                index += 1
            quote_html = "\n".join(f"<p>{inline_markdown(line)}</p>" for line in quotes if line)
            output.append(f"<blockquote>\n{quote_html}\n</blockquote>")
            continue

        if re.match(r"^---+$", stripped):
            flush_paragraph()
            output.append("<hr>")
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            title = heading.group(2).strip()
            output.append(f'<h{level} id="{slugify(title)}">{inline_markdown(title)}</h{level}>')
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    return "\n".join(output)


def render_page(meta: dict[str, str], article_html: str) -> str:
    title = meta.get("title", "Post")
    description = meta.get("description", title)
    date = meta.get("date", "")

    return f"""<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content="{html.escape(description)}">
    <title>{html.escape(title)} - farruxnet.uz</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        accent: '#3f51b5'
                    }}
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="bg-white text-slate-800 dark:bg-slate-900 dark:text-white transition-colors duration-300">

<header class="border-b border-slate-200 dark:border-slate-700 sticky top-0 bg-white/90 dark:bg-slate-900/90 backdrop-blur z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="h-16 flex items-center justify-between">
            <div class="font-bold text-lg">
                <a href="index.html" class="hover:text-accent transition">farruxnet.uz</a>
            </div>

            <nav
                id="siteMenu"
                class="hidden md:flex md:items-center md:gap-8 text-sm font-medium
                       absolute md:static top-16 left-0 w-full md:w-auto
                       bg-white dark:bg-slate-900
                       md:bg-transparent
                       border-t md:border-0 border-slate-200 dark:border-slate-700
                       px-4 py-4 md:p-0
                       flex-col md:flex-row gap-4 md:gap-8"
            >
                <a href="index.html" class="hover:text-accent transition">Home</a>
                <a href="about.html" class="hover:text-accent transition">About</a>
                <a href="contact.html" class="hover:text-accent transition">Contact</a>
            </nav>

            <div class="flex items-center gap-3">
                <input
                    type="text"
                    placeholder="Search blog..."
                    class="hidden lg:block px-4 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 outline-none focus:border-accent"
                />
                <button
                    id="menuToggle"
                    class="md:hidden text-2xl leading-none"
                    type="button"
                    aria-label="Toggle menu"
                    aria-controls="siteMenu"
                    aria-expanded="false"
                >
                    ☰
                </button>
            </div>
        </div>
    </div>
</header>

<main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-8">
    <article class="post-content border-b border-slate-200 dark:border-slate-700 pb-6">
{article_html}
    </article>
    <p class="text-sm text-slate-500 mt-6">{html.escape(date)}</p>
</main>

<footer class="border-t border-slate-200 dark:border-slate-700">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-sm text-slate-500">© 2026 Blog Clone</p>

        <div class="social-links flex flex-wrap justify-center items-center gap-3">
            <a href="#" aria-label="Telegram">
                <i class="fa-brands fa-telegram" aria-hidden="true"></i>
            </a>
            <a href="#" aria-label="YouTube">
                <i class="fa-brands fa-youtube" aria-hidden="true"></i>
            </a>
            <a href="https://www.linkedin.com/in/farruxnet/" aria-label="LinkedIn">
                <i class="fa-brands fa-linkedin-in" aria-hidden="true"></i>
            </a>
        </div>
    </div>
</footer>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script defer src="assets/js/code-copy.js"></script>
<script defer src="assets/js/site.js"></script>
</body>
</html>
"""


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "content" / "programming-markdown-test.md"
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "post.html"

    markdown = source.read_text(encoding="utf-8")
    meta, body = parse_front_matter(markdown)
    article_html = markdown_to_html(body)
    target.write_text(render_page(meta, article_html), encoding="utf-8", newline="\n")
    print(f"Generated {target} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
