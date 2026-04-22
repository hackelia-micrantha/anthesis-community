const { test, expect } = require('@playwright/test');
const http = require('http');
const fs = require('fs');
const path = require('path');

const webRoot = path.resolve(__dirname, '../../web');
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
    await expect(h1).toContainText('Build with accountable agents.');
  });

  test('health page responds with 200', async ({ request }) => {
    const r = await request.get(`http://localhost:${port}/health.html`);
    expect(r.status()).toBe(200);
  });
});
