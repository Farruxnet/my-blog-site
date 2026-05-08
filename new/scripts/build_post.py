from __future__ import annotations

import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    return meta, text[end + 5 :].lstrip()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value)
    return value.strip("-")


def parse_code_fence(line: str) -> tuple[str, str]:
    info = line.strip()[3:].strip()
    if not info:
        return "text", "code.txt"

    language = info.split()[0]
    title_match = re.search(r'title="([^"]+)"', info)
    title = title_match.group(1) if title_match else f"code.{language}"
    return language, title


def inline(text: str) -> str:
    placeholders: list[str] = []

    def keep_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"@@CODE{len(placeholders) - 1}@@"

    text = re.sub(r"`([^`]+)`", keep_code, html.escape(text))
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    for index, value in enumerate(placeholders):
        text = text.replace(f"@@CODE{index}@@", value)

    return text


def render_code(language: str, title: str, code: list[str]) -> str:
    escaped = html.escape("\n".join(code))
    language = html.escape(language)
    return f'<pre class="language-{language}"><code class="language-{language}">{escaped}</code></pre>'


def parse_table(lines: list[str], index: int) -> tuple[str, int] | None:
    if index + 1 >= len(lines):
        return None

    if "|" not in lines[index] or not re.match(r"^\s*\|?\s*-{3,}.*\|\s*$", lines[index + 1]):
        return None

    def cells(row: str) -> list[str]:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    headers = cells(lines[index])
    rows: list[list[str]] = []
    index += 2

    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        rows.append(cells(lines[index]))
        index += 1

    head = "".join(f"<th>{inline(cell)}</th>" for cell in headers)
    body = "\n".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>", index


def parse_list(lines: list[str], index: int) -> tuple[str, int] | None:
    ordered = re.match(r"^\d+\.\s+(.+)$", lines[index].strip())
    unordered = re.match(r"^[-*]\s+(.+)$", lines[index].strip())
    if not ordered and not unordered:
        return None

    tag = "ol" if ordered else "ul"
    items: list[str] = []

    while index < len(lines):
        line = lines[index].strip()
        match = re.match(r"^\d+\.\s+(.+)$", line) if tag == "ol" else re.match(r"^[-*]\s+(.+)$", line)
        if not match:
            break

        value = match.group(1)
        task = re.match(r"^\[(x|X| )\]\s+(.+)$", value)
        if task:
            checked = " checked" if task.group(1).lower() == "x" else ""
            value = f'<input type="checkbox"{checked} disabled> {inline(task.group(2))}'
        else:
            value = inline(value)

        items.append(f"<li>{value}</li>")
        index += 1

    return f"<{tag}>" + "".join(items) + f"</{tag}>", index


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    output: list[str] = []
    headings: list[tuple[int, str, str]] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
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
            language, title = parse_code_fence(stripped)
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            output.append(render_code(language, title, code))
            continue

        admonition = re.match(r'^!!!\s+(\w+)\s+"([^"]+)"$', stripped)
        if admonition:
            flush_paragraph()
            kind, title = admonition.groups()
            body: list[str] = []
            index += 1
            while index < len(lines) and (lines[index].startswith("    ") or not lines[index].strip()):
                if lines[index].strip():
                    body.append(lines[index].strip())
                index += 1
            output.append(
                f'<div class="admonition admonition-{kind}">'
                f'<p class="admonition-title">{html.escape(title)}</p>'
                f"<p>{inline(' '.join(body))}</p>"
                "</div>"
            )
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
            output.append("<blockquote>" + "".join(f"<p>{inline(q)}</p>" for q in quotes if q) + "</blockquote>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            title = heading.group(2)
            slug = slugify(title)
            headings.append((level, title, slug))
            output.append(f'<h{level} id="{slug}">{inline(title)}</h{level}>')
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    return "\n".join(output), headings


def render_page(meta: dict[str, str], article: str, headings: list[tuple[int, str, str]]) -> str:
    title = meta.get("title", "Generated post")
    description = meta.get("description", title)
    date = meta.get("date", "")
    tags = [tag.strip() for tag in meta.get("tags", "").split(",") if tag.strip()]
    tag_html = "\n".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)

    template = (ROOT / "templates" / "post.html").read_text(encoding="utf-8")
    return (
        template.replace("{{title}}", html.escape(title))
        .replace("{{description}}", html.escape(description))
        .replace("{{date}}", html.escape(date))
        .replace("{{tags}}", tag_html)
        .replace("{{content}}", article)
    )


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "content" / "test-post.md"
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "post.html"
    meta, body = parse_front_matter(source.read_text(encoding="utf-8"))
    article, headings = markdown_to_html(body)
    target.write_text(render_page(meta, article, headings), encoding="utf-8", newline="\n")
    print(f"Generated {target} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
