#!/usr/bin/env python3
import re
import sys
import urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else "https://www.wgplayground.com/game/mapi-games/smash-the-ants"
req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
    },
)
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="ignore")
print("len", len(html))
ifrs = re.findall(r"play\.wgplayground\.com/ifr/[a-f0-9]+", html)
print("iframes:", list(dict.fromkeys(ifrs)))
og = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
print("og:image:", og)
thumbs = re.findall(r'https?://[^"\s]+\.(?:png|jpg|webp)(?:\?[^"\s]*)?', html, re.I)
thumb_candidates = [u for u in thumbs if "wgplay" in u.lower() or "wee" in u.lower() or "thumb" in u.lower()]
print("thumbs:", thumb_candidates[:8])
desc = re.search(r'DESCRIPTION:\s*\n\s*\n(.+?)\n\s*INSTRUCTIONS:', html, re.S)
if desc:
    print("description:", desc.group(1).strip()[:200])
for m in re.finditer(r"<textarea[^>]*>(.*?)</textarea>", html, re.S | re.I):
    t = m.group(1).strip()
    if "ifr" in t or "iframe" in t:
        print("TEXTAREA:", t[:1000])
