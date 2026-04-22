const { test, expect } = require('@playwright/test');

test.describe('Public website', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('homepage has expected title and heading', async ({ page }) => {
    await expect(page).toHaveTitle(/Anthesis/);
    const h1 = page.locator('h1').first();
    await expect(h1).toContainText('Anthesis');
  });

  test('health page responds with 200', async ({ request }) => {
    const r = await request.get('/health.html');
    expect(r.status()).toBe(200);
  });
});
