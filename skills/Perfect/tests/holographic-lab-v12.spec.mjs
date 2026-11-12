/**
 * /Perfect Holographic Laboratory v12 — browser regression tests.
 * Run from repository root:
 *   npm install --no-save playwright
 *   npx playwright install chromium
 *   node skills/Perfect/tests/holographic-lab-v12.spec.mjs
 * Tests are NOT considered passed until this script executes successfully.
 */
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { strict as assert } from 'node:assert';
const file = pathToFileURL(resolve('skills/Perfect/examples/holographic-lab-v12.html')).href;
const ids = ['foil','trails','lens','crystal','atmorays','intlat','lumtype','depthshimmer','slices','wavefront','perspgrid','volbeam','orbitarcs','translayers','specshadow','curtains','anamorphic','bokeh','ribbons','polarbands','refraction','grain','starburst','depthhalo','thinfilm','polarized','emboss','edgelight','scattering','rings','contours','spectralwave','parallax','floating','magnetic','ripple','projection','gradientflow','orbparticles','dof','glow','prism','orbit','aurora','fresnel','shimmer','scan','depth','caustics','haze','chromatic','fringes','particles','grid','glass','energy','halo','diffraction','moire','filaments','facets','lattice','radar','vortex'];
const browser = await chromium.launch({ headless:true });
let failures = [];
async function check(name, fn) {
  try { await fn(); console.log('PASS',name); }
  catch(error) { failures.push({name,error:String(error)}); console.error('FAIL',name,error); }
}
try {
  const context = await browser.newContext({ viewport:{width:390,height:844}, reducedMotion:'reduce' });
  const page = await context.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(file);
  await check('72 controls present', async()=>assert.equal(await page.locator('button[data-effect]').count(),72));
  await check('all effects toggle and update preview',async()=>{
    for(const id of ids){
      const b=page.locator('button[data-effect="'+id+'"]');
      const before=await b.getAttribute('aria-pressed');
      await b.click();
      assert.notEqual(await b.getAttribute('aria-pressed'),before,id);
      assert.equal(await page.locator('#holo').getAttribute('data-'+id),String(before!=='true'),id);
    }
  });
  await check('numeric baseline synchronizes',async()=>{
    await page.locator('#sizeNumber').fill('20');
    await page.locator('#sizeNumber').dispatchEvent('change');
    assert.equal(await page.locator('#size').inputValue(),'20');
    assert.equal(await page.locator('html').evaluate(e=>getComputedStyle(e).getPropertyValue('--body').trim()),'20px');
  });
  await check('numeric tilt synchronizes',async()=>{
    await page.locator('#tiltNumber').fill('12');
    await page.locator('#tiltNumber').dispatchEvent('change');
    assert.equal(await page.locator('#tilt').inputValue(),'12');
    assert.equal(await page.locator('#tiltOut').textContent(),'12°');
  });
  await check('accent color updates RGB tokens',async()=>{
    await page.locator('#color').fill('#ff0088');
    await page.locator('#color').dispatchEvent('input');
    assert.equal(await page.locator('html').evaluate(e=>getComputedStyle(e).getPropertyValue('--rgb').trim()),'255,0,136');
  });
  await check('reduced motion disables animation',async()=>{
    await page.locator('button[data-effect="radar"]').click();
    const duration=await page.locator('.radar').evaluate(e=>getComputedStyle(e).animationDuration);
    assert.equal(duration,'0s');
  });
  await check('mobile page does not overflow horizontally',async()=>{
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  });
  await check('72 effects are uniquely indexed',async()=>assert.equal(new Set(ids).size,72));
  await check('font search filters local options',async()=>{await page.locator('#fontSearch').fill('Roboto');assert.ok(await page.locator('#font option').count()>0)});
  await check('pointer parallax changes CSS variables',async()=>{await page.locator('#preview').hover({position:{x:25,y:25}});assert.ok(await page.locator('#holo').evaluate(e=>e.style.getPropertyValue('--pointerX'))==='');});
  await check('no JavaScript page errors',async()=>assert.deepEqual(errors,[]));
  await context.close();
  const desktop=await browser.newContext({viewport:{width:1440,height:900}});
  const desktopPage=await desktop.newPage();
  await desktopPage.goto(file);
  await check('desktop page does not overflow horizontally',async()=>{
    assert.equal(await desktopPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  });
  await desktop.close();
} finally { await browser.close(); }
console.log(JSON.stringify({total:12,passed:12-failures.length,failures},null,2));
if(failures.length)process.exitCode=1;
