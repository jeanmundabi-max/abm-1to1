const puppeteer=require('puppeteer-core'); const ffmpeg=require('ffmpeg-static');
const {execFileSync}=require('child_process'); const fs=require('fs'); const path=require('path');
const CHROME=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const SRC='file://'+process.argv[2]; const SLUG=process.argv[3];
const FPS=30, W=1920, H=1080;   // runtime comes from window.DURATION in the page
const FR=path.resolve(__dirname,'out/_vslframes');
(async()=>{
  const t0=Date.now();
  fs.rmSync(FR,{recursive:true,force:true}); fs.mkdirSync(FR,{recursive:true});
  const b=await puppeteer.launch({executablePath:CHROME,headless:'shell',args:['--no-sandbox','--hide-scrollbars']});
  const p=await b.newPage(); await p.setViewport({width:W,height:H,deviceScaleFactor:1});
  await p.goto(SRC,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,700));
  if(!(await p.evaluate(()=>typeof window.seek==='function'))) throw new Error('no seek()');
  const SECONDS=await p.evaluate(()=>window.DURATION||90), TOTAL=Math.round(FPS*SECONDS);
  console.log('  runtime',SECONDS+'s ->',TOTAL,'frames');
  for(let i=0;i<TOTAL;i++){
    await p.evaluate(x=>window.seek(x), i/(TOTAL-1));
    await p.screenshot({path:path.join(FR,'f'+String(i).padStart(5,'0')+'.png')});
    if(i%300===0) console.log('  frame',i,'/',TOTAL,((Date.now()-t0)/1000).toFixed(0)+'s');
  }
  await b.close();
  const out=path.resolve(__dirname,'out/'+SLUG+'.mp4');
  execFileSync(ffmpeg,['-y','-framerate',String(FPS),'-i',path.join(FR,'f%05d.png'),
    '-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',out],{stdio:'ignore'});
  fs.copyFileSync(path.join(FR,'f00000.png'),path.resolve(__dirname,'out/'+SLUG+'-poster.png'));
  fs.rmSync(FR,{recursive:true,force:true});
  const kb=(fs.statSync(out).size/1024).toFixed(0);
  console.log('OK ->',out,'|',kb,'KB |',((Date.now()-t0)/1000).toFixed(0)+'s total');
})().catch(e=>{console.error('RENDER FAILED:',e.message);process.exit(1);});
