const { test, expect } = require('@playwright/test');
const http = require('http');
const fs = require('fs');
const path = require('path');

const webRoot = path.resolve(__dirname, '../../../web');
let server, port;

function contentTypeFor(file) {
  const ext = path.extname(file).toLowerCase();
  const map = { '.html': 'text/html', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.pdf': 'application/pdf', '.json': 'application/json', '.txt': 'text/plain' };
  return map[ext] || 'application/octet-stream';
}

async function startServer() {
  server = http.createServer((req, res) => {
    try {
      let reqPath = decodeURIComponent(req.url.split('?')[0]);
      if (reqPath === '/') reqPath = '/index.html';
      const filePath = path.join(webRoot, reqPath);
      if (!filePath.startsWith(webRoot)) {
        res.statusCode = 403; res.end('forbidden'); return;
      }
      if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        res.statusCode = 404; res.end('not found'); return;
      }
      const data = fs.readFileSync(filePath);
      res.setHeader('Content-Type', contentTypeFor(filePath));
      res.statusCode = 200;
      res.end(data);
    } catch (err) {
      res.statusCode = 500; res.end('error');
    }
  });
  await new Promise((resolve) => server.listen(0, resolve));
  port = server.address().port;
}

async function stopServer() {
  if (server) await new Promise((resolve) => server.close(resolve));
}

test.beforeAll(async () => {
  await startServer();
  console.log('Started local static server on port', port);
});

test.afterAll(async () => {
  await stopServer();
});

test.describe('Public website', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`http://localhost:${port}/`);
  });

  test('homepage has expected title and heading', async ({ page }) => {
    await expect(page).toHaveTitle(/Anthesis/);
    const brand = page.locator('.brand');
    await expect(brand).toContainText('Anthesis');
    const h1 = page.locator('h1').first();
    await expect(h1).toContainText('Let agents act without giving them invisible authority.');
  });

  test('homepage leads to the constrained reference trial and public community', async ({ page }) => {
    const trial = page.locator('#trial');
    await expect(trial.getByRole('heading', { name: 'Run an authorized write. Attempt a bypass.' })).toBeVisible();
    await expect(trial.getByRole('link', { name: /complete Try Anthesis walkthrough/ }))
      .toHaveAttribute('href', 'https://github.com/hackelia-micrantha/anthesis-community/blob/main/docs/product/try-anthesis.md');
    await expect(page.locator('.nav-community'))
      .toHaveAttribute('href', 'https://github.com/hackelia-micrantha/anthesis-community');
    await expect(page.locator('.hero-actions .btn').first()).toHaveAttribute('href', '#trial');
  });

  test('mobile navigation closes on Escape and on internal link activation', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    const toggle = page.getByRole('button', { name: 'Menu' });
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await page.keyboard.press('Escape');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(toggle).toBeFocused();
    await toggle.click();
    await page.locator('.nav-links a[href="#trial"]').click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(page).toHaveURL(/#trial$/);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  });

  test('project brief explains gateway, enforcement, and reference trial', async ({ page }) => {
    await page.goto(`http://localhost:${port}/project-brief.html`);
    await expect(page.getByRole('heading', { level: 1 })).toHaveText('Anthesis');
    await expect(page.getByText('A deterministic policy gateway for AI agent actions.')).toBeVisible();
    await expect(page.getByRole('link', { name: /Follow the reference trial/ }))
      .toHaveAttribute('href', 'https://github.com/hackelia-micrantha/anthesis-community/blob/main/docs/product/try-anthesis.md');
    await expect(page.getByText(/does not make an AI model's reasoning deterministic/)).toBeVisible();
    await expect(page.locator('.nav-community'))
      .toHaveAttribute('href', 'https://github.com/hackelia-micrantha/anthesis-community');
    await page.setViewportSize({ width: 390, height: 844 });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  });

  test('health page responds with 200', async ({ request }) => {
    const r = await request.get(`http://localhost:${port}/health.html`);
    expect(r.status()).toBe(200);
  });
});
