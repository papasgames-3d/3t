#!/usr/bin/env python3
"""Fetch WGPlayground embed iframe URLs via Playwright."""
from playwright.sync_api import sync_playwright

GAMES = [
    ("smash-the-ants", "https://www.wgplayground.com/game/mapi-games/smash-the-ants"),
    ("cool-tuning-paint-the-car", "https://www.wgplayground.com/game/welwise-studio/cool-tuning-paint-the-car"),
    ("dinosaurs-vs-asteroids", "https://www.wgplayground.com/game/gamepush/dinosaurs-vs-asteroids"),
    ("merge-and-blast-2048", "https://www.wgplayground.com/game/gamepush/merge-and-blast-2048"),
    ("hex-match", "https://www.wgplayground.com/game/gmg-studios/hex-match"),
]


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for slug, url in GAMES:
            print(f"\n=== {slug} ===")
            try:
                page.goto(url, wait_until="networkidle", timeout=90000)
                page.wait_for_timeout(3000)
                html = page.content()
                import re

                ifrs = re.findall(r"play\.wgplayground\.com/ifr/[a-f0-9]+", html)
                imgs = re.findall(r"https?://[^\"'\s]+(?:thumb|thumbnail|cover|icon)[^\"'\s]*\.(?:png|jpg|webp)", html, re.I)
                og = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
                title = page.title()
                print("title:", title)
                print("iframes:", list(dict.fromkeys(ifrs)))
                print("og:image:", og[:3])
                # try embed textarea
                embed = page.locator("textarea").all()
                for i, ta in enumerate(embed):
                    val = ta.input_value()
                    if "ifr" in val or "iframe" in val:
                        print(f"textarea[{i}]:", val[:500])
            except Exception as e:
                print("ERROR:", e)
        browser.close()


if __name__ == "__main__":
    main()
