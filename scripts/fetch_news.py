#!/usr/bin/env python3
"""Coletor de notícias da BragaTech.

- Lê data/feeds.json e busca os feeds RSS/Atom.
- Remove duplicatas (por URL) e gera um Markdown por notícia em src/content/noticias/.
- Extrai a imagem de destaque (media:content, enclosure, <img> no conteúdo ou og:image da página).
- Reclassifica para "ia" notícias claramente sobre Inteligência Artificial.
- Remove notícias mais antigas que MAX_AGE_DAYS.
"""
import hashlib
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = ROOT / "data" / "feeds.json"
OUT_DIR = ROOT / "src" / "content" / "noticias"
MAX_PER_FEED = 8          # novas notícias por fonte, por execução
MAX_AGE_DAYS = 45         # apaga notícias mais antigas que isso
SUMMARY_LEN = 280
MAX_OG_FETCH = 80         # buscas de og:image por execução (inclui notícias antigas sem imagem)
USER_AGENT = "Mozilla/5.0 (compatible; BragaTechNewsBot/1.1; +https://www.bragagnolo.tec.br)"

AI_RE_CS = re.compile(r"\b(IA|AI|IAs|LLMs?|GPT-?\d*|GenAI)\b")
AI_RE_CI = re.compile(
    r"intelig[eê]ncia artificial|artificial intelligence|chatgpt|openai|anthropic|claude|gemini|copilot|"
    r"machine learning|aprendizado de m[aá]quina|deepseek|llama|mistral|nvidia blackwell|agentes? de ia|"
    r"ai agents?|agentic|generative|generativa|chatbot",
    re.I,
)
IMG_EXT_RE = re.compile(r"\.(jpe?g|png|webp|gif|avif)(\?|$)", re.I)


def clean_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"The post .* appeared first on .*$", "", text).strip()
    text = re.sub(r"O post .* apareceu primeiro em .*$", "", text).strip()
    if len(text) > SUMMARY_LEN:
        text = text[:SUMMARY_LEN].rsplit(" ", 1)[0] + "…"
    return text


def yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def entry_date(e) -> datetime:
    for key in ("published_parsed", "updated_parsed"):
        t = e.get(key)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def norm_img(url: str | None) -> str | None:
    if not url:
        return None
    url = html.unescape(url.strip())
    if url.startswith("//"):
        url = "https:" + url
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    if not url.startswith("https://"):
        return None
    if re.search(r"(pixel|tracking|feedburner|gravatar|emoji|\.svg)", url, re.I):
        return None
    return url


def image_from_entry(e) -> str | None:
    for m in e.get("media_content", []) or []:
        url = m.get("url")
        if url and (m.get("medium") == "image" or "image" in (m.get("type") or "") or IMG_EXT_RE.search(url)):
            if norm_img(url):
                return norm_img(url)
    for m in e.get("media_thumbnail", []) or []:
        if norm_img(m.get("url")):
            return norm_img(m.get("url"))
    for l in e.get("links", []) or []:
        if l.get("rel") == "enclosure" and "image" in (l.get("type") or ""):
            if norm_img(l.get("href")):
                return norm_img(l.get("href"))
    blobs = [c.get("value", "") for c in e.get("content", []) or []] + [e.get("summary", "")]
    for b in blobs:
        m = re.search(r"<img[^>]+src=[\"']([^\"']+)[\"']", b or "", re.I)
        if m and norm_img(m.group(1)):
            return norm_img(m.group(1))
    return None


def og_image(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=8) as r:
            page = r.read(300_000).decode("utf-8", "ignore")
    except Exception:  # noqa: BLE001
        return None
    for pat in (
        r"<meta[^>]+property=[\"']og:image(?::secure_url)?[\"'][^>]+content=[\"']([^\"']+)",
        r"<meta[^>]+content=[\"']([^\"']+)[\"'][^>]+property=[\"']og:image",
        r"<meta[^>]+name=[\"']twitter:image(?::src)?[\"'][^>]+content=[\"']([^\"']+)",
    ):
        m = re.search(pat, page, re.I)
        if m and norm_img(m.group(1)):
            return norm_img(m.group(1))
    return None


def classify(title: str, base: str) -> str:
    if base == "ciberseguranca":
        return base
    if AI_RE_CS.search(title) or AI_RE_CI.search(title):
        return "ia"
    return base


def parse_front(text: str) -> dict:
    data = {}
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def unq(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def write_item(path: Path, d: dict) -> None:
    lines = [
        "---",
        f"title: {yaml_str(d['title'])}",
        f"summary: {yaml_str(d.get('summary', ''))}",
        f"pubDate: {d['pubDate']}",
        f"category: {d['category']}",
        f"source: {yaml_str(d['source'])}",
        f"sourceUrl: {yaml_str(d['sourceUrl'])}",
    ]
    if d.get("image"):
        lines.append(f"image: {yaml_str(d['image'])}")
    lines.append("---")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    feeds = json.loads(FEEDS_FILE.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=MAX_AGE_DAYS)
    existing = {p.stem for p in OUT_DIR.glob("*.md")}
    added = og_used = 0

    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"], agent=USER_AGENT)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERRO] {feed['name']}: {exc}")
            continue
        if parsed.bozo and not parsed.entries:
            print(f"[AVISO] {feed['name']}: feed indisponível ({parsed.get('bozo_exception')})")
            continue

        count = 0
        for e in parsed.entries:
            if count >= MAX_PER_FEED:
                break
            link = (e.get("link") or "").strip()
            title = clean_text(e.get("title", ""))
            if not link.startswith("http") or not title:
                continue
            published = entry_date(e)
            if published < cutoff:
                continue
            slug = hashlib.sha1(link.encode("utf-8")).hexdigest()[:16]
            if slug in existing:
                continue
            image = image_from_entry(e)
            if not image and og_used < MAX_OG_FETCH:
                og_used += 1
                image = og_image(link)
            write_item(OUT_DIR / f"{slug}.md", {
                "title": title,
                "summary": clean_text(e.get("summary", "") or e.get("description", "")),
                "pubDate": published.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "category": classify(title, feed["category"]),
                "source": feed["name"],
                "sourceUrl": link,
                "image": image,
            })
            existing.add(slug)
            count += 1
            added += 1
        print(f"[OK] {feed['name']}: {count} novas")

    # Manutenção: remove antigas, reclassifica IA e completa imagens que faltam
    removed = fixed = 0
    for p in sorted(OUT_DIR.glob("*.md"), reverse=True):
        d = {k: unq(v) for k, v in parse_front(p.read_text(encoding="utf-8")).items()}
        try:
            date = datetime.strptime(d.get("pubDate", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if date < cutoff:
            p.unlink()
            removed += 1
            continue
        changed = False
        new_cat = classify(d.get("title", ""), d.get("category", "tecnologia"))
        if new_cat != d.get("category"):
            d["category"] = new_cat
            changed = True
        if not d.get("image") and og_used < MAX_OG_FETCH and d.get("sourceUrl"):
            og_used += 1
            img = og_image(d["sourceUrl"])
            if img:
                d["image"] = img
                changed = True
        if changed:
            write_item(p, d)
            fixed += 1

    print(f"Total: {added} adicionadas, {fixed} atualizadas, {removed} removidas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
