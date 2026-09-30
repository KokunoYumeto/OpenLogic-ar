// Render only the exact corrected section, fonts and stylesheet. No network.
// Arguments: Puppeteer module directory, extracted render folder.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const puppeteer = require(path.resolve(process.argv[2]));
const root = path.resolve(process.argv[3]);

(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--disable-dev-shm-usage']});
  const rows = [];
  try {
    for (const profile of ['international', 'machrek']) {
      const page = await browser.newPage();
      await page.setViewport({width: 1100, height: 900});
      await page.setRequestInterception(true);
      page.on('request', r => r.url().startsWith('file:') || r.url().startsWith('data:') ? r.continue() : r.abort());
      await page.goto(pathToFileURL(path.join(root, profile, 'OEBPS', 'modern-reader-3-7-3.xhtml')).href,
                      {waitUntil: 'load', timeout: 30000});
      await page.evaluate(() => document.fonts.ready);
      const result = await page.evaluate(() => {
        const paragraphs = Array.from(document.querySelectorAll('p'));
        const corrected = ['يسمى الشرط', 'لا توجد قيود'].map(s => {
          const found = paragraphs.filter(p => p.textContent.trim().startsWith(s));
          if (found.length !== 1) throw new Error('Correction paragraph not unique');
          const rect = found[0].getBoundingClientRect();
          return {text: found[0].textContent.replace(/\s+/g, ' ').trim(), width: rect.width, height: rect.height};
        });
        const note = document.getElementById('modern-reader-3-7-3-note-2-ref');
        const footnote = document.getElementById('modern-reader-3-7-3-note-2');
        if (!note || !footnote) throw new Error('Corrective footnote absent');
        const target = note.getAttribute('href').slice(1);
        if (footnote.id !== target) throw new Error('Footnote target differs');
        return {corrected, note_target: target, footnote_text: footnote.textContent.trim(),
                fonts: Array.from(document.fonts).map(f => ({family:f.family,status:f.status})),
                math_count: document.querySelectorAll('math').length,
                proof_trees: document.querySelectorAll('[data-source-command="DisplayProof"]').length,
                page_width: document.documentElement.clientWidth,
                body_width: document.body.getBoundingClientRect().width,
                native_math_visible: Array.from(document.querySelectorAll('math')).every(m => {
                  const r = m.getBoundingClientRect(); return r.width > 0 && r.height > 0;
                })};
      });
      if (result.proof_trees !== 4 || !result.native_math_visible ||
          result.corrected.some(p => p.width <= 0 || p.height <= 0) ||
          result.fonts.some(f => f.status !== 'loaded')) throw new Error('Rendered layout/font check failed');
      await page.screenshot({path: path.join(root, profile + '-section.png'), fullPage: true});
      await page.click('#modern-reader-3-7-3-note-2-ref');
      const clicked = await page.evaluate(() => decodeURIComponent(location.hash.slice(1)));
      if (clicked !== result.note_target) throw new Error('Footnote navigation failed');
      await page.screenshot({path: path.join(root, profile + '-footnote.png')});
      rows.push({profile, ...result, footnote_click_pass: true});
      await page.close();
    }
    fs.writeFileSync(path.join(root, 'RENDER_CHECK.json'), JSON.stringify({profiles:rows}, null, 2)+'\n');
    process.stdout.write('PASS corrected section, native formulas, fonts and footnote in both profiles\n');
  } finally { await browser.close(); }
})().catch(error => { process.stderr.write(error.message+'\n'); process.exitCode = 1; });
