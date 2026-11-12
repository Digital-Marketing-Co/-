import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const url=pathToFileURL(resolve('skills/Perfect/examples/holographic-lab-v4.html')).href;
const dir=resolve('skills/Perfect/test-results');
await mkdir(dir,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
 for(const item of [
  {name:'mobile',width:390,height:844,reducedMotion:'reduce'},
  {name:'desktop',width:1440,height:900,reducedMotion:'no-preference'}
 ]){
  const context=await browser.newContext({viewport:{width:item.width,height:item.height},reducedMotion:item.reducedMotion,deviceScaleFactor:1});
  const page=await context.newPage();
  await page.goto(url);
  await page.screenshot({path:resolve(dir,item.name+'.png'),fullPage:true,animations:'disabled'});
  await context.close();
 }
}finally{await browser.close()}
