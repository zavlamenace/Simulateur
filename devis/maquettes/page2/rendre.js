const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: Number(process.argv[2] || 1) });
  for (const g of ['reference', 'design', 'prestige', 'lafuge']) {
    await p.goto('file://' + __dirname + '/page2-' + g + '.html');
    await p.evaluate(() => document.fonts.ready);
    const h = await p.evaluate(() => document.body.scrollHeight);
    console.log(g, 'hauteur', h);
    await p.screenshot({ path: __dirname + '/rendus/page2-' + g + '.png' });
  }
  await b.close();
})();
