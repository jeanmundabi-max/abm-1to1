// Proves the film never holds still: steps every frame, signs the animated state, flags repeats.
const puppeteer=require('puppeteer-core');
const CHROME=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const SRC='file://'+process.argv[2];
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:'shell',args:['--no-sandbox','--hide-scrollbars']});
  const pg=await b.newPage(); await pg.setViewport({width:1920,height:1080,deviceScaleFactor:1});
  await pg.goto(SRC,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,900));
  const DUR=await pg.evaluate(()=>window.DURATION), FPS=30, N=Math.round(DUR*FPS);
  let prev=null, dead=[], sigs=[];
  for(let i=0;i<N;i++){
    const sig=await pg.evaluate(x=>{
      window.seek(x);
      const out=[];
      document.querySelectorAll('.stage *').forEach(function(e){
        const r=e.getBoundingClientRect(), cs=getComputedStyle(e);
        if(cs.opacity==='0') return;
        out.push(e.id||e.className, r.x.toFixed(1), r.y.toFixed(1), r.width.toFixed(1), r.height.toFixed(1),
                 (+cs.opacity).toFixed(3), cs.backgroundColor);
      });
      out.push('pg', getComputedStyle(document.getElementById('pg')).width);
      out.push('c1', document.getElementById('c1').textContent);
      return out.join('|');
    }, i/(N-1));
    if(sig===prev) dead.push(i);
    prev=sig; sigs.push(sig);
  }
  // longest run of identical consecutive frames
  let run=1,worst=1,at=0;
  for(let i=1;i<sigs.length;i++){ if(sigs[i]===sigs[i-1]){run++; if(run>worst){worst=run;at=i-run+1;}} else run=1; }
  console.log('frames',N,'| identical-to-previous:',dead.length,
    '| longest static run:',worst,'frames ('+(worst/FPS).toFixed(2)+'s) starting at',(at/FPS).toFixed(2)+'s');
  if(dead.length) console.log('  first 20 static frames (s):',dead.slice(0,20).map(f=>(f/FPS).toFixed(2)).join(' '));
  await b.close();
})().catch(e=>{console.error('QA FAILED:',e.message);process.exit(1);});
