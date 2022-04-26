import { test, expect, Page } from '@playwright/test';
import {uploadFile} from './helper';

test('Complete flow', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await page.locator('input:near(:text-is("PLC Path"),10)').fill('Main Oven');
  await page.locator('input:near(:text-is("PLC Set Point"),10)').fill('50');
  await page.locator('input:near(:text-is("P"),10)').fill('0.9');
  await page.locator('input:near(:text-is("I"),10)').fill('0.7');
  await page.locator('input:near(:text-is("D"),10)').fill('0.5');
  await page.locator('input:near(:text-is("Minutes"),10)').fill('1');
  await page.locator('input:near(:text-is("Seconds"),10)').fill('15');
  await uploadFile(page);
});