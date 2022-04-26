import { test, expect, Page } from '@playwright/test';

export const uploadFile = async (page:Page) => {
    const fileInput = await page.$('input[type=file]');
    if(!fileInput) throw new Error('Invalid page');
    await fileInput.setInputFiles('./tests/assets/testtest.csv');
    await page.waitForTimeout(500); 
    await page.locator('button:has-text("SEND QUERY")').click();
}