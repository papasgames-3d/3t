import { chromium } from 'playwright';

const GAMES = [
  ['smash-the-ants', 'https://www.wgplayground.com/game/mapi-games/smash-the-ants'],
  ['cool-tuning-paint-the-car', 'https://www.wgplayground.com/game/welwise-studio/cool-tuning-paint-the-car'],
  ['dinosaurs-vs-asteroids', 'https://www.wgplayground.com/game/gamepush/dinosaurs-vs-asteroids'],
  ['merge-and-blast-2048', 'https://www.wgplayground.com/game/gamepush/merge-and-blast-2048'],
  ['hex-match', 'https://www.wgplayground.com/game/gmg-studios/hex-match'],
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

for (const [slug, url] of GAMES) {
  console.log(`\n=== ${slug} ===`);
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(8000);
    const html = await page.content();
    const ifrs = [...new Set(html.match(/play\.wgplayground\.com\/ifr\/[a-f0-9]+/g) || [])];
    const og = await page.locator('meta[property="og:image"]').getAttribute('content').catch(() => null);
    const embedBlocks = html.match(/<iframe[^>]+>/gi) || [];
    console.log('title:', await page.title());
    console.log('iframes:', ifrs);
    console.log('og:image:', og);
    const textareas = await page.locator('textarea').all();
    for (let i = 0; i < textareas.length; i++) {
      const val = await textareas[i].inputValue();
      if (val.includes('ifr') || val.includes('iframe')) {
        console.log(`textarea[${i}]:`, val.slice(0, 600));
      }
    }
    if (embedBlocks.length) console.log('iframe tags:', embedBlocks.slice(0, 3));
  } catch (e) {
    console.log('ERROR:', e.message);
  }
}

await browser.close();
