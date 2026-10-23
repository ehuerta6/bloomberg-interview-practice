// Playwright CLI run-code function; see accessibility-review.md for prerequisites.
async (page) => {
  const base = page.url(); // Start on the locally served catalog.
  const links = await page.locator(".problem-card h3 a").evaluateAll(nodes => nodes.map(node => node.href));
  if (links.length !== 65 || new Set(links).size !== 65) throw new Error("Expected 65 distinct catalog links");
  const failures = [], incomplete = [];
  let checked = 0, disclosures = 0;
  for (const width of [1280, 390]) {
    await page.setViewportSize({width, height: 900});
    for (const url of [base, ...links]) {
      const response = await page.goto(url);
      if (response.status() !== 200) failures.push({url, width, error: "HTTP " + response.status()});
      await page.addScriptTag({path: "/tmp/bloomberg-axe.min.js"});
      const result = await page.evaluate(async () => {
        const a11y = await axe.run();
        const headings = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].filter(x => x.getClientRects().length);
        return {
          violations: a11y.violations.map(v => ({id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target)})),
          incomplete: a11y.incomplete.map(v => v.id),
          overflow: document.documentElement.scrollWidth > innerWidth,
          h1: document.querySelectorAll("h1").length,
          main: document.querySelectorAll("main").length,
          headingJump: headings.some((x, i) => i && Number(x.tagName[1]) > Number(headings[i-1].tagName[1]) + 1),
          brokenImages: [...document.images].filter(x => !x.complete || !x.naturalWidth || !x.alt).map(x => x.src),
          disclosure: document.querySelector("details.solution-reveal")?.open,
        };
      });
      if (result.violations.length || result.overflow || result.h1 !== 1 || result.main !== 1 || result.headingJump || result.brokenImages.length || result.disclosure === true) {
        failures.push({url, width, ...result});
      }
      if (result.incomplete.length) incomplete.push({url, width, rules: result.incomplete});
      if (url !== base) {
        const summary = page.locator(".solution-reveal > summary");
        await summary.focus();
        await page.keyboard.press("Space");
        if (!await page.locator(".solution-reveal").evaluate(x => x.open)) failures.push({url, width, error: "Space did not reveal"});
        if (!await page.locator(".solution-reveal a").isVisible()) failures.push({url, width, error: "Reference link hidden after reveal"});
        await page.keyboard.press("Space");
        if (await page.locator(".solution-reveal").evaluate(x => x.open)) failures.push({url, width, error: "Space did not close"});
        disclosures++;
      }
      checked++;
    }
  }
  return {browser: page.context().browser().version(), axe: "4.10.3", checked, disclosures, failures, incomplete};
}
