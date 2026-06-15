const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Set viewport large enough so cards don't collapse into a column
  await page.setViewport({ width: 1440, height: 1080, deviceScaleFactor: 2 });
  
  const filePath = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(filePath, { waitUntil: 'networkidle0' });
  
  const cards = await page.$$('.card');
  console.log(`Found ${cards.length} cards in index.html`);
  
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    await card.screenshot({ path: path.resolve(__dirname, `slide_${i + 1}.png`) });
    console.log(`Saved slide_${i + 1}.png`);
  }
  
  await browser.close();
})();
