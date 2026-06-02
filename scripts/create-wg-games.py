#!/usr/bin/env python3
"""Create WGPlayground game pages from kingdom-match template."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "game"
IMG_DIR = ROOT / "assets" / "img" / "img-up"
TEMPLATE = GAME_DIR / "kingdom-match.html"
GAMES_JSON = GAME_DIR / "games.json"
INDEX = ROOT / "index.html"
BASE = "https://monkeymart.one"

GAMES = [
    {
        "slug": "smash-the-ants",
        "name": "Smash the Ants",
        "wg_url": "https://www.wgplayground.com/game/mapi-games/smash-the-ants",
        "frame_url": "https://play.wgplayground.com/ifr/01fb0ec289031fdf65e4f4d4ad6ff0b9",
        "genre": ["Casual", "Clicker", "Arcade"],
        "keywords": "smash the ants, ant smasher, clicker game, casual arcade, free browser game",
        "description": "Play Smash the Ants online for free. Stop the ant invasion before they reach your candy—tap fast, avoid bees, and chase a high score in this reflex arcade game.",
        "instructions": "Click or tap to smash ants before they reach your candy. Avoid bees—they cost you points and break your streak.",
        "about": "The relentless tide of ants is spreading rapidly, and you are the last line of defense. With quick reflexes, smash every ant that marches toward your treats while steering clear of buzzing bees.",
    },
    {
        "slug": "cool-tuning-paint-the-car",
        "name": "Cool Tuning - Paint the Car",
        "wg_url": "https://www.wgplayground.com/game/welwise-studio/cool-tuning-paint-the-car",
        "frame_url": "https://play.wgplayground.com/ifr/ff0e2a67ade09a519cbad31249a6254d",
        "genre": ["Simulation", "Casual"],
        "keywords": "cool tuning paint the car, car tuning game, paint car game, auto customization, browser simulation",
        "description": "Play Cool Tuning: Paint the Car online for free. Buy cars, spray paint, add stickers and film, then sell your custom rides at auction in this creative tuning sim.",
        "instructions": "Buy your first car and start customizing with the brush, spray can, stickers, and film. Send finished builds to auction to earn money and unlock new cars.",
        "about": "Cool Tuning: Paint the Car is a creative auto customization game. Buy vehicles, paint and wrap them, apply decals, and sell your masterpieces at auction to grow your garage and unlock new styles.",
    },
    {
        "slug": "dinosaurs-vs-asteroids",
        "name": "Dinosaurs vs Asteroids",
        "wg_url": "https://www.wgplayground.com/game/gamepush/dinosaurs-vs-asteroids",
        "frame_url": "https://play.wgplayground.com/ifr/b7608d4ff6af54ee0c143b4ca79fa8ea",
        "genre": ["Casual", "Action", "Arcade"],
        "keywords": "dinosaurs vs asteroids, dinosaur shooter, asteroid game, arcade defense, free browser game",
        "description": "Play Dinosaurs vs Asteroids online for free. Defend the prehistoric world with dinosaur weapons, upgrade species, and blast falling asteroids before they hit Earth.",
        "instructions": "Aim at asteroids and shoot with the left mouse button. Activate dinosaur support abilities with the right click or by tapping the dinosaur. Earn leaves to upgrade your squad.",
        "about": "Imagine defending Earth from asteroids in a dinosaur world. Use unique species abilities, upgrade your dinosaurs, and survive wave after wave of falling rocks in this action arcade shooter.",
    },
    {
        "slug": "merge-and-blast-2048",
        "name": "Merge and Blast 2048",
        "wg_url": "https://www.wgplayground.com/game/gamepush/merge-and-blast-2048",
        "frame_url": "https://play.wgplayground.com/ifr/09ab20f115e3a08725e4d0a5edec94d2",
        "genre": ["Puzzle", "Casual"],
        "keywords": "merge and blast 2048, 2048 puzzle, merge blocks, number puzzle, free browser game",
        "description": "Play Merge and Blast 2048 online for free. Tap matching blocks to merge numbers, trigger chain reactions, and push toward the 2048 tile in this addictive puzzle game.",
        "instructions": "Tap adjacent blocks with the same number to merge them into higher values. Clear space and build combos to reach 2048 and beyond.",
        "about": "Merge and Blast 2048 combines classic 2048 number merging with satisfying blast combos. Plan your taps, merge smartly, and climb toward ever-higher tiles on a crowded board.",
    },
    {
        "slug": "hex-match",
        "name": "Hex Match",
        "wg_url": "https://www.wgplayground.com/game/gmg-studios/hex-match",
        "frame_url": "https://play.wgplayground.com/ifr/b1df5d28867e3ec22bb6a6913c11d037",
        "genre": ["Puzzle", "Casual"],
        "keywords": "hex match, hex puzzle, match 3 hex, puzzle game online, free browser game",
        "description": "Play Hex Match online for free. Swap hex tiles, match colors in six directions, trigger combos, and clear handcrafted puzzle levels—no download required.",
        "instructions": "Drag and drop hex tiles to make matches, clear lines, and score high. Use boosters and chain reactions to beat level goals.",
        "about": "Hex Match is a browser hex match puzzle with hundreds of levels, boss stages, and endless mode. Swap tiles on a six-sided grid, unlock boosters, and chase high scores on mobile or desktop.",
    },
]


def fetch_thumb(wg_url: str, ifr_hash: str) -> str | None:
    req = urllib.request.Request(
        wg_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="ignore")
    prefix = f"static.wgplayground.com/{ifr_hash.split('/')[-1] if '/' in ifr_hash else ifr_hash}/wgplayground/"
    ifr_id = ifr_hash.rsplit("/", 1)[-1]
    prefix = f"static.wgplayground.com/{ifr_id}/wgplayground/"
    for url in re.findall(r"https://static\.wgplayground\.com/[^\"\s]+\.png", html):
        if f"/{ifr_id}/" in url and "wgplayground" in url:
            return url
    for url in re.findall(r"https://static\.wgplayground\.com/[^\"\s]+\.jpg", html):
        if f"/{ifr_id}/" in url:
            return url
    return None


def download_image(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=30).read()
    dest.write_bytes(data)


def build_page(game: dict, template: str) -> str:
    name = game["name"]
    slug = game["slug"]

    text = template
    text = re.sub(
        r'<h1>Kingdom Match - Match 3 Strategy Game</h1>\s*<p>Welcome to Monkey Mart[^<]*</p>\s*<h2>Key Features:</h2>',
        f'<h1>{name} - Play Online Free</h1>\n<p>{game["about"]}</p>\n<h2>How to Play</h2>\n<p>{game["instructions"]}</p>\n<h2>Key Features</h2>\n<ul>\n<li>Free to play in your browser—no download</li>\n<li>Works on desktop and mobile</li>\n<li>Instant play with one click</li>\n</ul>',
        text,
        count=1,
    )
    text = text.replace("Kingdom match", name)
    text = text.replace("Kingdom Match", name)
    text = text.replace("kingdom-match", slug)
    text = text.replace("kingdom match.png", f"{slug}.png")
    text = text.replace(
        "https://play.wgplayground.com/ifr/2916009ed073d17ae49a64371ee96e10",
        game["frame_url"],
    )
    text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{game["description"]}" name="description"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta content="online games, free games, browser games, web games, fun games" name="keywords"/>',
        f'<meta content="{game["keywords"]}" name="keywords"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'"name": "Kingdom match"',
        f'"name": "{name}"',
        text,
    )
    text = re.sub(
        r'"description": "[^"]*Kingdom Match[^"]*"',
        f'"description": "{game["description"]}"',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta content="[^"]*" property="og:description"/>',
        f'<meta content="{game["description"]}" property="og:description"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'"genre": \[\s*"Casual"\s*\]',
        f'"genre": {json.dumps(game["genre"], indent=2)}',
        text,
        count=1,
    )
    return text


def update_games_json(games: list[dict]) -> None:
    data = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
    slugs = {g["slug"] for g in games}
    data = [e for e in data if not any(slugs & {e.get("title", "").lower().replace(" ", "-")})]
    for g in games:
        data.append(
            {
                "title": g["name"],
                "frame_url": g["frame_url"],
                "image_path": f"/assets/img/img-up/{g['slug']}.png",
            }
        )
    data.sort(key=lambda x: x["title"].lower())
    GAMES_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def add_index_snippets(games: list[dict]) -> None:
    html = INDEX.read_text(encoding="utf-8")
    anchor = "./game/blocks-merge-puzzle-2048.html"
    if anchor not in html:
        return
    snippets = []
    for g in games:
        slug = g["slug"]
        name = g["name"]
        if f"./game/{slug}.html" in html or f'game/{slug}.html' in html:
            continue
        snippets.append(
            f'            <a class="game-item" href="./game/{slug}.html">\n'
            f'              <img loading="lazy" alt="{slug}" src="/assets/img/img-up/{slug}.png"/>\n'
            f"              <span>{name}</span>\n"
            f"            </a>\n"
        )
    if not snippets:
        return
    block = re.search(
        rf'(<a class="game-item" href="{re.escape(anchor)}">.*?</a>\s*)',
        html,
        re.S,
    )
    if block:
        pos = block.end()
        html = html[:pos] + "".join(snippets) + html[pos:]
        INDEX.write_text(html, encoding="utf-8")


def main() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    for game in GAMES:
        slug = game["slug"]
        ifr_id = game["frame_url"].rsplit("/", 1)[-1]
        thumb_url = fetch_thumb(game["wg_url"], ifr_id)
        dest = IMG_DIR / f"{slug}.png"
        if thumb_url:
            print(f"Download thumb {slug}: {thumb_url}")
            try:
                download_image(thumb_url, dest)
            except Exception as e:
                print(f"  thumb failed: {e}")
        elif not dest.exists():
            fallback = IMG_DIR / "block-blast.png"
            if fallback.exists():
                dest.write_bytes(fallback.read_bytes())
                print(f"Using fallback image for {slug}")

        page = build_page(game, template)
        out = GAME_DIR / f"{slug}.html"
        out.write_text(page, encoding="utf-8")
        print(f"Wrote {out.name}")

    update_games_json(GAMES)
    add_index_snippets(GAMES)
    print("Updated games.json and index.html")


if __name__ == "__main__":
    main()
