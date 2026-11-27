const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: Number(process.argv[2] || 1) });
  fs.mkdirSync(__dirname + '/rendus', { recursive: true });
  for (const f of fs.readdirSync(__dirname).filter((x) => x.endsWith('.html')).sort()) {
    await p.goto('file://' + __dirname + '/' + f);
    await p.evaluate(() => document.fonts.ready);
    const deborde = await p.evaluate(() => document.body.scrollHeight > 1123);
    console.log(f, deborde ? 'DÉBORDE' : 'ok');
    await p.screenshot({ path: __dirname + '/rendus/' + f.replace('.html', '.png') });
  }
  await b.close();
})();
