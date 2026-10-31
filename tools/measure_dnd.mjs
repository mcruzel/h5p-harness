// Hauteur d'un glisser-déposer H5P (H5P.DragQuestion) avant et après « Vérifier ».
// Usage: node tools/measure_dnd.mjs <file.h5p> '<requête JSON>' [préfixe-de-capture]
//   requête: {"widths": [400, 760], "plans": {"juste": [[rang, zone], ...], "faux": [...]}}
//   rang = ordre de l'étiquette dans la page (0 = première étiquette déplaçable), zone = ordre de la zone de dépôt (0 = première).
// Pour chaque largeur et chaque plan : joue le paquet dans une page de cette largeur, mesure la hauteur de l'iframe, dépose les étiquettes
// selon le plan, clique « Vérifier », mesure de nouveau. Une ligne JSON sur la sortie standard (voir tools/dnd_measure.py).
// Needs: npm packages h5p-standalone and playwright resolvable from $H5P_RENDER_MODULES (see tools/qa.py); $H5P_CHROMIUM optional.
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

const [,, h5pFile, requestJson, shotPrefix] = process.argv;
const request = JSON.parse(requestJson);
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'h5p-measure-'));
const work = path.join(root, 'content');
fs.mkdirSync(work);
execFileSync('unzip', ['-q', path.resolve(h5pFile), '-d', work]);
fs.cpSync(path.join(standalone, 'dist'), path.join(root, 'player'), { recursive: true });
fs.writeFileSync(path.join(root, 'index.html'), [
  '<!doctype html><meta charset="utf-8">',
  '<div id="h5p-container"></div>',
  '<script src="player/main.bundle.js"></script>',
  '<script>',
  "new H5PStandalone.H5P(document.getElementById('h5p-container'), {",
  "  h5pJsonPath: '/content', frameJs: '/player/frame.bundle.js', frameCss: '/player/styles/h5p.css',",
  '}).then(() => { window.__h5pReady = true; }).catch(e => { window.__h5pError = String(e); });',
  '</script>'].join('\n'));
const types = { '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.html': 'text/html',
  '.svg': 'image/svg+xml', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.gif': 'image/gif' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(p).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;
const launch = { args: ['--disable-background-networking', '--disable-component-update', '--no-first-run'] };
if (process.env.H5P_CHROMIUM) launch.executablePath = process.env.H5P_CHROMIUM;

// Hauteur de l'activité : celle de l'iframe (ce que la page de Moodle réserve) et celle du document qu'elle contient.
const heights = async (page, frame) => ({
  iframe: await page.evaluate(() => { const f = document.querySelector('iframe'); return f ? Math.round(f.getBoundingClientRect().height) : -1; }),
  doc: await frame.evaluate(() => document.documentElement.scrollHeight),
});
// Attend que la hauteur ne bouge plus (animations de dépôt, retours, redimensionnement de l'iframe).
async function settle(page, frame, min = 600, max = 8000) {
  const t0 = Date.now();
  let prev = null, same = 0;
  while (Date.now() - t0 < max) {
    await page.waitForTimeout(150);
    const h = await heights(page, frame);
    same = prev && h.iframe === prev.iframe && h.doc === prev.doc ? same + 1 : 0;
    prev = h;
    if (same >= 3 && Date.now() - t0 >= min) break;
  }
  return prev;
}

async function runOne(browser, width, name, plan) {
  const run = { largeur: width, plan: name, attendus: plan.length, deposes: 0, avant: null, apres: null, verifie: false, erreur: null };
  // la hauteur de la fenêtre n'intervient pas dans celle de l'activité : assez haute pour que tout soit atteignable à la souris
  const page = await browser.newPage({ viewport: { width, height: 3000 } });
  try {
    await page.goto('http://127.0.0.1:' + port + '/index.html');
    await page.waitForFunction(() => window.__h5pReady || window.__h5pError, null, { timeout: 30000 });
    const initError = await page.evaluate(() => window.__h5pError || null);
    if (initError) throw new Error(initError);
    const frame = page.frames().find(f => f !== page.mainFrame());
    await frame.waitForSelector('.h5p-dropzone', { timeout: 20000 });
    await frame.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 20000 });
    run.avant = await settle(page, frame, 1500);

    // chaque étiquette reçoit son rang d'après l'ordre du document ; la copie d'une étiquette « multiple » hérite du rang de l'originale
    const tag = rank => frame.evaluate(r => {
      const all = [...document.querySelectorAll('.h5p-draggable')];
      if (r === null) all.forEach((e, i) => e.setAttribute('data-hx', i));
      else all.filter(e => !e.hasAttribute('data-hx')).forEach(e => e.setAttribute('data-hx', r));
    }, rank);
    const dropped = () => frame.evaluate(() => document.querySelectorAll('.h5p-draggable.h5p-dropped').length);
    await tag(null);
    const zones = frame.locator('.h5p-dropzone');
    for (const [rank, zone] of plan) {
      const before = await dropped();
      const d = await frame.locator('.h5p-draggable[data-hx="' + rank + '"]:not(.h5p-dropped)').first().boundingBox({ timeout: 5000 });
      const t = await zones.nth(zone).boundingBox({ timeout: 5000 });
      if (!d || !t) continue;
      await page.mouse.move(d.x + d.width / 2, d.y + d.height / 2);
      await page.mouse.down();
      await page.mouse.move(t.x + t.width / 2, t.y + t.height / 2, { steps: 10 });
      await page.mouse.up();
      await page.waitForTimeout(400);
      await tag(rank);
      if (await dropped() > before) run.deposes++;
    }
    // H5P.Question 1.5 : .h5p-theme-check ; 1.4 : .h5p-question-check-answer ; sinon, le bouton nommé « Vérifier »
    let check = frame.locator('.h5p-theme-check, .h5p-question-check-answer').first();
    if (!await check.count()) check = frame.getByRole('button', { name: /Vérifier|Check/ }).first();
    if (await check.count()) {
      await check.click();
      run.verifie = true;
      run.apres = await settle(page, frame, 1000);
    }
    if (shotPrefix) await page.screenshot({ path: shotPrefix + '-' + width + '-' + name + '.png', fullPage: true });
  } catch (e) {
    run.erreur = String(e).split('\n')[0];
  }
  await page.close();
  return run;
}

let initError = null;
const runs = [];
const browser = await chromium.launch(launch);
try {
  for (const width of request.widths)
    for (const [name, plan] of Object.entries(request.plans)) runs.push(await runOne(browser, width, name, plan));
} catch (e) {
  initError = String(e).split('\n')[0];
}
console.log(JSON.stringify({ initError, runs }));
await browser.close();
server.close();
fs.rmSync(root, { recursive: true, force: true });
