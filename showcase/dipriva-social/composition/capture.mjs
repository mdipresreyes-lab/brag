// Renders every frame of index.html to PNG at 30 fps, or chosen stills.
// Usage: node capture.mjs <outDir> [t1,t2,...]
// Needs Playwright (npm i playwright). Set CHROMIUM_PATH to use a local Chromium.
import {mkdirSync} from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const [outDir, times] = process.argv.slice(2);
mkdirSync(outDir, {recursive: true});
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? {executablePath: process.env.CHROMIUM_PATH} : {});
const page = await browser.newPage({viewport: {width: 1080, height: 1920}});
await page.goto('file://' + path.resolve(import.meta.dirname, 'index.html'));
await page.evaluate(() => window.assetsReady());
const duration = await page.evaluate(() => window.DURATION);
const list = times ? times.split(',').map(Number) : Array.from({length: Math.round(duration * 30)}, (_, i) => i / 30);
for (let i = 0; i < list.length; i++) {
  await page.evaluate((t) => window.render(t), list[i]);
  const name = times ? `t${list[i].toFixed(2)}.png` : `f${String(i).padStart(4, '0')}.png`;
  await page.screenshot({path: path.join(outDir, name), type: 'png'});
}
await browser.close();
console.log(`${list.length} frames`);
