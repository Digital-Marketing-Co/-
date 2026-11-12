/**
 * Perfect v4: extra browser QA checks. Run:
 * npx playwright test skills/Perfect/tests/accessibility-v4.spec.mjs
 * Requires @playwright/test and installed Chromium.
 */
import { test, expect } from '@playwright/test';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { mkdir } from 'node:fs/promises';
const url=pathToFileURL(resolve('skills/Perfect/examples/holographic-lab-v4.html')).href;
test('keyboard toggles are operable and report state',async({page})=>{
 await page.goto(url);
 const control=page.locator('button[data-effect="glow"]');
 await control.focus();
 await expect(control).toBeFocused();
 const previous=await control.getAttribute('aria-pressed');
 await page.keyboard.press('Space');
 await expect(control).toHaveAttribute('aria-pressed',previous==='true'?'false':'true');
});
test('controls have accessible names and visible focus',async({page})=>{
 await page.goto(url);
 for(const button of await page.locator('button[data-effect]').all()){
  await expect(button).toHaveAttribute('aria-pressed',/^(true|false)$/);
  await expect(button).not.toHaveText('');
 }
 await page.keyboard.press('Tab');
 const focus=await page.evaluate(()=>document.activeElement?.tagName);
 expect(focus).not.toBe('BODY');
});
test('baseline size input clamps to valid range',async({page})=>{
 await page.goto(url);
 const field=page.locator('#sizeNumber');
 await field.fill('99');
 await field.dispatchEvent('change');
 await expect(field).toHaveValue('24');
});
test('screenshots captured for review',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 await page.goto(url);
 await expect(page.locator('#holo')).toBeVisible();
 await mkdir('skills/Perfect/test-results',{recursive:true});
 await page.screenshot({path:'skills/Perfect/test-results/accessibility-mobile.png',fullPage:true,animations:'disabled'});
});
