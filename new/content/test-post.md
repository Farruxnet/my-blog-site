---
title: Markdown Converter Style Test
date: 2026-05-09
description: farruxnet.uz Material style uchun Markdown convert testi.
tags: markdown, python, docs
---

# Markdown Converter Style Test

Bu sahifa `new/test-post.md` faylidan generate qilindi. Maqsad: Markdown elementlari
farruxnet.uz uslubiga yaqin test UI ichida qanday ko'rinishini tekshirish.

> Documentation UI kontentni bezamasligi kerak. U kontentni o'qish, topish va nusxalashni osonlashtirishi kerak.

## Markdown syntax

Matn ichida **bold**, *italic*, ***bold italic***, ~~deleted text~~ va `inline code` ishlatiladi.
Ichki link ham bor: [Code blocks](#code-blocks).

- Oddiy ro'yxat elementi
- Ikkinchi element
- `inline code` ishlatilgan element

1. Birinchi qadam
2. Ikkinchi qadam
3. Uchinchi qadam

## Checklist

- [x] Markdown fayl yozildi
- [x] Python converter ishladi
- [x] HTML generate qilindi
- [ ] Search index avtomatik generate qilinadi
- [ ] Multiple post build qilinadi

## Table

| Qism | Markdown | HTML natija |
| --- | --- | --- |
| Sarlavha | `# Title` | `h1` |
| Code | fence block | code card |
| Quote | `>` | blockquote |
| Checklist | `- [x]` | disabled checkbox |

## Admonition

!!! note "Muhim eslatma"
    Converter code fence metadata, TOC va front matter kabi qismlarni bosqichma-bosqich qo'llab-quvvatlashi kerak.

!!! warning "Ehtiyot bo'ling"
    Generated HTML source Markdownni almashtirib yubormasligi kerak.

## Code blocks

```python
from pathlib import Path


def build(source: Path, target: Path) -> None:
    markdown = source.read_text(encoding="utf-8")
    html = render(markdown)
    target.write_text(html, encoding="utf-8")
```

```go
package main

import "fmt"

func main() {
    fmt.Println("farruxnet.uz")
}
```

```bash
#!/usr/bin/env bash
set -euo pipefail

python new/scripts/build_post.py new/content/test-post.md new/post.html
python -m http.server 8000 --bind 127.0.0.1
```

```sql
select title, slug, published_at
from posts
where draft = false
order by published_at desc;
```

## Deploy

Generated HTML oddiy static file bo'lgani uchun GitHub Pages, Netlify yoki istalgan static hostingda
ishlay oladi.
