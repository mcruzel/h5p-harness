// Headless smoke test: unzip a .h5p, play it with h5p-standalone in Chromium, report JS errors,
// missing files and the visible text. Usage: node tools/render.mjs <file.h5p> [screenshot.png]
// Needs: npm packages h5p-standalone and playwright resolvable from $H5P_RENDER_MODULES (see tools/qa.py).
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const modules = process.env.H5P_RENDER_MODULES;
const require = createRequire(path.join(modules, 'noop.js'));
const { chromium } = require('playwright');
const standalone = path.dirname(require.resolve('h5p-standalone/package.json'));

const [,, h5pFile, shot] = process.argv;
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'h5p-render-'));
const work = path.join(root, 'content');
fs.mkdirSync(work);
execFileSync('unzip', ['-q', path.resolve(h5pFile), '-d', work]);
fs.cpSync(path.join(standalone, 'dist'), path.join(root, 'player'), { recursive: true });
fs.writeFileSync(path.join(root, 'index.html'), `<!doctype html><meta charset="utf-8">
<div id="h5p-container"></div>
<script src="player/main.bundle.js"></script>
<script>
new H5PStandalone.H5P(document.getElementById('h5p-container'), {
  h5pJsonPath: '/content', frameJs: '/player/frame.bundle.js', frameCss: '/player/styles/h5p.css',
}).then(() => { window.__h5pReady = true; }).catch(e => { window.__h5pError = String(e); });
</script>`);
const types = { '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.html': 'text/html',
  '.svg': 'image/svg+xml', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.gif': 'image/gif', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4', '.webm': 'video/webm' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(p).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;
const launch = { args: ['--disable-background-networking', '--disable-component-update', '--no-first-run'] };
if (process.env.H5P_CHROMIUM) launch.executablePath = process.env.H5P_CHROMIUM;
const browser = await chromium.launch(launch);
const page = await browser.newPage({ viewport: { width: 1000, height: 800 } });
const errors = [], missing = [];
page.on('pageerror', e => errors.push('pageerror: ' + e.message.split('\n')[0]));
page.on('console', m => {
  // missing files are reported precisely by the response handler below
  if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) errors.push('console: ' + m.text().split('\n')[0]);
});
page.on('response', r => {
  const u = r.url().replace(/^http:\/\/[^/]+/, '');
  if (r.status() >= 400 && !u.endsWith('favicon.ico')) missing.push(r.status() + ' ' + u);
});
let initError = null, text = '', media = 0;
try {
  await page.goto(`http://127.0.0.1:${port}/index.html`);
  await page.waitForFunction(() => window.__h5pReady || window.__h5pError, null, { timeout: 30000 });
  initError = await page.evaluate(() => window.__h5pError || null);
  await page.waitForTimeout(2000);
  const frame = page.frames().find(f => f !== page.mainFrame());
  text = frame ? (await frame.locator('body').innerText()).replace(/\s+/g, ' ').trim().slice(0, 300) : '';
  media = frame ? await frame.evaluate(() => [...document.querySelectorAll('img, canvas, video, svg')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width > 20 && r.height > 20; }).length) : 0;
  if (shot) await page.screenshot({ path: shot, fullPage: true });
} catch (e) {
  initError = String(e).split('\n')[0];
}
console.log(JSON.stringify({ initError, errors: [...new Set(errors)], missing, text, media }));
await browser.close();
server.close();
fs.rmSync(root, { recursive: true, force: true });
