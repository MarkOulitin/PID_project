import { Page } from "@playwright/test";

export const uploadFileWithSend = async (page: Page) => {
	const fileInput = await page.$("input[type=file]");
	if (!fileInput) throw new Error("Invalid page");
	await fileInput.setInputFiles("./tests/assets/testtest.csv");
	await page.waitForTimeout(500);
	await page.locator('button:has-text("SEND QUERY")').click();
};

export const uploadFile = async (page: Page) => {
	const fileInput = await page.$("input[type=file]");
	if (!fileInput) throw new Error("Invalid page");
	await fileInput.setInputFiles("./tests/assets/testtest.csv");
	await page.waitForTimeout(500);
};

export const fillInputFields = async (page: Page,plcPath:string, plcSetPoint:string,p:string,i:string,d:string,minutes:string,seconds:string) => {
	await page.locator('input:near(:text-is("PLC Path"),10)').fill(plcPath);
	await page.locator('input:near(:text-is("PLC Set Point (Optional)"),10)').fill(plcSetPoint);
	await page.locator('input:near(:text-is("P"),10)').fill(p);
	await page.locator('input:near(:text-is("I"),10)').fill(i);
	await page.locator('input:near(:text-is("D"),10)').fill(d);
	await page.locator('input:near(:text-is("Minutes"),10)').fill(minutes);
	await page.locator('input:near(:text-is("Seconds"),10)').fill(seconds);
};

export const clearInputFields = async (page: Page) => {
	await page.locator('input:near(:text-is("PLC Path"),10)').fill("");
	await page.locator('input:near(:text-is("PLC Set Point (Optional)"),10)').fill("");
	await page.locator('input:near(:text-is("P"),10)').fill("");
	await page.locator('input:near(:text-is("I"),10)').fill("");
	await page.locator('input:near(:text-is("D"),10)').fill("");
	await page.locator('input:near(:text-is("Minutes"),10)').fill("");
	await page.locator('input:near(:text-is("Seconds"),10)').fill("");
};
