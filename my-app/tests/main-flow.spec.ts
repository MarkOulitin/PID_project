import { test ,expect} from '@playwright/test';
import {uploadFile,uploadFileWithSend, fillInputFields, clearInputFields,uploadPythonFile} from './helper';

test('Complete Happy Flow', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
  await uploadFileWithSend(page);
  await page.waitForURL('**/output');
});

test('Complete Sad Flow', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await fillInputFields(page,"oven","50","0.5","0.5","0.5","0","45");
  await uploadFileWithSend(page);
  await page.locator('text="Server Error"').click();;
  await page.waitForURL('**/');
});

test('Insert Fields then delete fields', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","50","0.5","0.5","0.5","0","45");
  await uploadFile(page);
  await clearInputFields(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Insert Invalid field for PID', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","50","hey","how","are","0","45");
  await uploadFile(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Insert Invalid field time values', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","50","0.5","0.5","0.5","61","61");
  await uploadFile(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Insert negative field time values', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","50","0.5","0.5","0.5","-45","-45");
  await uploadFile(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Insert random invalid fields', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","test","hi","how","are","61","61");
  await uploadFile(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Insert valid fields, with file field empty', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","50","0.5","0.5","0.5","0","45");
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Set point optional', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"Oven","","0.5","0.5","0.5","0","45");
  await uploadFileWithSend(page);
  await page.waitForURL('**/');
});

test('PLC path empty', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"","5","0.5","0.5","0.5","0","45");
  await uploadFile(page);
  await page.locator('button:has-text("SEND QUERY")').isDisabled();
  await page.waitForURL('**/');
});

test('Info rendered correctly', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await page.locator('text="Info"').click();
  await page.locator('text=Fill the provided fields and upload a CSV file').click();
});

test('Complete Happy Flow with custom algo', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
  await uploadPythonFile(page);
  await uploadFileWithSend(page);
  await page.waitForURL('**/output');
});

test('Custom Algo name added', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
  await uploadPythonFile(page);
  await uploadFileWithSend(page);
  await page.waitForURL('**/output');
  await page.goto('http://localhost:3000/');
  await page.locator('text="NewAlgo.py"').click();
});

test.skip('10 users requesting calculations Happy Flow', async ({ page,browserName  }) => {
  let i = 0;
  if(browserName === 'chromium'){
    do {
      await page.goto('http://localhost:3000/');
      await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
      await uploadFileWithSend(page);
      await page.waitForURL('**/output');
      await page.waitForTimeout(100);
      i++;
      } while (i < 10);
  }
});

test('Only 1 checkbox can be checked', async ({ page  }) => {
    await page.goto('http://localhost:3000/');
    await page.waitForSelector("input[type=checkbox]");
    const checkBoxes = await page.$$("input[type=checkbox]");
    let counter = 0;
    for(let i = 0 ; i < checkBoxes.length; i++){
      const val = await checkBoxes[i].isChecked();
      if(val === true) {
        counter++;
      }
    }
    expect(counter).toBe(1);
    await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
    await uploadFileWithSend(page);
    await page.waitForURL('**/output');
});

test('Only 1 checkbox can be checked even after checking another one', async ({ page  }) => {
    await page.goto('http://localhost:3000/');
    await page.waitForSelector("input[type=checkbox]");
    const checkBoxes = await page.$$("input[type=checkbox]");
    let counter = 0;
    if(checkBoxes.length >= 2){
      await checkBoxes[checkBoxes.length-1].check();
      for(let i = 0 ; i < checkBoxes.length; i++){
        const val = await checkBoxes[i].isChecked();
        if(val === true) {
          counter++;
        }
      }
      await fillInputFields(page,"test","50","0.5","0.5","0.5","0","45");
      await uploadFileWithSend(page);
      await page.waitForURL('**/output');
    }
    expect(counter).toBe(1);
});
