# The two node scripts

`vsl_render.js` and `vsl_motion_qa.js` render the hero film and measure whether it actually
moves. **They are optional.** The account pages and the ad cards do not need them.

## Install

```bash
cd scripts
npm install          # puppeteer-core and ffmpeg-static, from package.json
```

You also need a headless Chrome. Either point at one you have:

```bash
export CHROME_PATH=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
```

or install Playwright's, which is what this was built against:

```bash
npx playwright install chromium
```

## Run

```bash
node vsl_motion_qa.js <run>/04-pages/vsl/<slug>-vsl.html
node vsl_render.js    <run>/04-pages/vsl/<slug>-vsl.html <slug>
```

Rendering is roughly 70ms a frame at 1920x1080, so a 32 second film takes about 55 seconds.
