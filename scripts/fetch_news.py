#!/usr/bin/env python3
"""Coletor de notícias da BragaTech.

Lê data/feeds.json, busca os feeds RSS/Atom, remove duplicatas (por URL)
e gera um arquivo Markdown por notícia em src/content/noticias/.
Notícias mais antigas que MAX_AGE_DAYS são removidas para manter o repositório leve.
"""
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = ROOT / "data" / "feeds.json"
OUT_DIR = ROOT / "src" / "content" / "noticias"
MAX_PER_FEED = 8        # novas notícias por fonte, por execução
MAX_AGE_DAYS = 45       # apaga notícias mais antigas que isso
SUMMARY_LEN = 280
USER_AGENT = "BragaTechNewsBot/1.0 (+https://www.bragagnolo.tec.br)"


def clean_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    # remove rodapés típicos de feeds WordPress
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


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    feeds = json.loads(FEEDS_FILE.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=MAX_AGE_DAYS)
    existing = {p.stem for p in OUT_DIR.glob("*.md")}
    added = 0

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
            summary = clean_text(e.get("summary", "") or e.get("description", ""))
            md = (
                "---\n"
                f"title: {yaml_str(title)}\n"
                f"summary: {yaml_str(summary)}\n"
                f"pubDate: {published.strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
                f"category: {feed['category']}\n"
                f"source: {yaml_str(feed['name'])}\n"
                f"sourceUrl: {yaml_str(link)}\n"
                "---\n"
            )
            (OUT_DIR / f"{slug}.md").write_text(md, encoding="utf-8")
            existing.add(slug)
            count += 1
            added += 1
        print(f"[OK] {feed['name']}: {count} novas")

    # limpeza de notícias antigas
    removed = 0
    for p in OUT_DIR.glob("*.md"):
        m = re.search(r"^pubDate:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            try:
                d = datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if d < cutoff:
                    p.unlink()
                    removed += 1
            except ValueError:
                pass

    print(f"Total: {added} adicionadas, {removed} removidas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
