/* Render captioned marketing layouts around intact app screenshots.
 * Requires playwright + sharp (the Codex bundled runtime supplies both).
 * Usage: node render.cjs CAPTURE_ROOT OUTPUT_ROOT [--prototype]
 * CAPTURE_ROOT/device/ must contain the semantically named original PNGs.
 * No app screen is painted, rearranged or retouched by this renderer.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const sharp = require('sharp');
const root = path.resolve(__dirname, '../..');
const shots = require('./captions.json');
const captureRoot = path.resolve(process.argv[2]);
const outputRoot = path.resolve(process.argv[3]);
const prototype = process.argv.includes('--prototype');
const devices = [
  {key:'iphone-medium',folder:'iPhone-6.3-inch',name:'iPhone · 6.3-inch',w:1206,h:2622},
  {key:'iphone-large',folder:'iPhone-6.9-inch',name:'iPhone · 6.9-inch',w:1320,h:2868},
  {key:'ipad',folder:'iPad-13-inch',name:'iPad · 13-inch',w:2064,h:2752}
];
const palettes = {
 coral:{bg:'#E96959',ink:'#FFFFFF',muted:'#FFF3E9',accent:'#FFD79F',line:'#F6A594'},
 cream:{bg:'#F7F6F2',ink:'#243449',muted:'#526275',accent:'#E96959',line:'#E8E2D8'},
 navy:{bg:'#142D43',ink:'#FFFFFF',muted:'#D4E1EA',accent:'#FFD79F',line:'#2D526A'},
 lilac:{bg:'#DED3F0',ink:'#283448',muted:'#5D5370',accent:'#7753A1',line:'#C5B5DF'},
 teal:{bg:'#205867',ink:'#FFFFFF',muted:'#D1E8E9',accent:'#FFD79F',line:'#337382'},
 gold:{bg:'#F8D48B',ink:'#243449',muted:'#625239',accent:'#AC562D',line:'#E7BB6B'}
};
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function html(shot,device,rawFile) {
 const p=palettes[shot.theme],pad=device.key==='ipad';
 // A common logical artboard keeps typography identical across iPhone sizes.
 const W=pad?2064:1320,H=pad?2752:2868;
 const screenW=pad?1500:924;
 const screenH=screenW*device.h/device.w;
 const screenY=pad?650:730;
 const screenX=(W-screenW)/2;
 const scale=device.w/W;
 const maxTitle=Math.max(...shot.headline.map(s=>s.length));
 const titleSize=pad?114:(maxTitle>18?91:109);
 return `<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(shot.headline.join(' '))} — ${device.name}</title><style>
 @font-face{font-family:Nunito;font-weight:200 1000;font-style:normal;src:url('../assets/Nunito.ttf')}*{box-sizing:border-box}html,body{margin:0;width:${device.w}px;height:${device.h}px;overflow:hidden;background:${p.bg}}.art{position:relative;width:${W}px;height:${H}px;transform:scale(${scale});transform-origin:top left;background:${p.bg};font-family:Nunito,Arial,sans-serif;color:${p.ink};overflow:hidden}
 .brand{position:absolute;left:${pad?130:92}px;top:${pad?72:80}px;display:flex;align-items:center;gap:21px;font-size:${pad?47:43}px;font-weight:900;letter-spacing:-1.4px}.brand img{width:${pad?65:60}px;height:${pad?65:60}px;border-radius:18px}.sequence{position:absolute;right:${pad?130:92}px;top:${pad?92:100}px;font-size:24px;font-weight:800;letter-spacing:3px;opacity:.72}
 .copy{position:absolute;top:${pad?170:200}px;left:${pad?130:92}px;right:${pad?130:92}px}.eyebrow{font-size:${pad?29:24}px;line-height:1.2;letter-spacing:${pad?4:3}px;font-weight:900;color:${p.accent};margin:0 0 ${pad?23:26}px}h1{font-size:${titleSize}px;line-height:1.01;letter-spacing:${pad?-4.5:-3.4}px;font-weight:950;margin:0}h1 span{display:block}h1 span+span::before{content:''}.caption{font-size:${pad?43:39}px;line-height:1.28;font-weight:650;letter-spacing:-.55px;margin:${pad?27:29}px 0 0;color:${p.muted}}
 .ring{position:absolute;width:${pad?1870:1450}px;height:${pad?1870:1450}px;border:${pad?2:2}px solid ${p.line};border-radius:50%;left:${pad?760:640}px;top:${pad?1150:1570}px}.ring.two{transform:translate(-160px,160px)}
 .device{position:absolute;left:${screenX-14}px;top:${screenY-14}px;width:${screenW+28}px;height:${screenH+28}px;padding:14px;background:#172533;border:2px solid #485765;border-radius:${pad?48:72}px;box-shadow:0 32px 75px #10213030,0 3px 4px #FFFFFF25 inset;overflow:hidden}.device img{display:block;width:${screenW}px;height:${screenH}px;border-radius:${pad?32:56}px;object-fit:contain;background:#000}
 .footer{position:absolute;left:0;right:0;bottom:${pad?34:37}px;text-align:center;font-weight:800;font-size:${pad?23:21}px;letter-spacing:3px;opacity:.65}
 </style></head><body><main class="art"><div class="ring"></div><div class="ring two"></div><div class="brand"><img src="../assets/Quizfolk.png" alt="">quizfolk</div><div class="sequence">${shot.id.slice(0,2)} / 10</div><div class="copy"><p class="eyebrow">${esc(shot.eyebrow)}</p><h1>${shot.headline.map(s=>`<span>${esc(s)}</span>`).join('')}</h1><p class="caption">${esc(shot.caption).replaceAll('\n','<br>')}</p></div><div class="device"><img src="../../original-captures/${device.key}/${rawFile}" alt="Real Quizfolk ${esc(shot.capture)} screen"></div><div class="footer">A LITTLE KNOWLEDGE. A GREAT RIVALRY.</div></main></body></html>`;
}
async function main(){
 await fs.mkdir(path.join(outputRoot,'artwork/assets'),{recursive:true});
 await fs.copyFile(path.join(root,'android/app/src/main/res/font/nunito.ttf'),path.join(outputRoot,'artwork/assets/Nunito.ttf'));
 await fs.copyFile(path.join(root,'android/FONT-LICENSE.txt'),path.join(outputRoot,'artwork/assets/FONT-LICENSE.txt'));
 await fs.copyFile(path.join(root,'iOS/Assets.xcassets/AppIcon.appiconset/AppIcon.png'),path.join(outputRoot,'artwork/assets/Quizfolk.png'));
 const browser=await chromium.launch({channel:process.env.STORE_BROWSER_CHANNEL||'chrome',headless:true});
 const report=[];
 try {for(const device of devices){
  if(prototype && device.key!=='iphone-medium')continue;
  const dir=path.join(captureRoot,device.key);
  const names=await fs.readdir(dir);
  const out=path.join(outputRoot,device.folder), originals=path.join(outputRoot,'original-captures',device.key), artdir=path.join(outputRoot,'artwork',device.key);
  await Promise.all([out,originals,artdir].map(d=>fs.mkdir(d,{recursive:true})));
  const page=await browser.newPage({viewport:{width:device.w,height:device.h},deviceScaleFactor:1});
  for(const shot of shots){
   const name=names.find(n=>n.toLowerCase()===`${shot.capture}.png`.toLowerCase() || n.toLowerCase().includes(`-${shot.capture.toLowerCase()}.png`));
   if(!name)throw new Error(`Missing capture ${device.key}/${shot.capture}`);
   const raw=await fs.readFile(path.join(dir,name)), meta=await sharp(raw).metadata();
   if(meta.width!==device.w || meta.height!==device.h)throw new Error(`Wrong native size for ${device.key}/${name}: ${meta.width}x${meta.height}`);
   const rawName=`${shot.capture}.png`;
   await fs.writeFile(path.join(originals,rawName),raw);
   const htmlPath=path.join(artdir,`${shot.id}.html`);
   await fs.writeFile(htmlPath,html(shot,device,rawName),'utf8');
   await page.goto(pathToFileURL(htmlPath).href);
   await page.evaluate(()=>document.fonts.ready);
   await page.locator('.device img').evaluate(img=>img.decode());
   const overflow=await page.evaluate(()=>{const copy=document.querySelector('.copy').getBoundingClientRect(), dev=document.querySelector('.device').getBoundingClientRect();return {copyBottom:copy.bottom,deviceTop:dev.top,titleOverflows:document.querySelector('h1').scrollWidth>document.querySelector('h1').clientWidth};});
   if(overflow.copyBottom+15>overflow.deviceTop||overflow.titleOverflows)throw new Error(`Copy overflow ${device.key}/${shot.id}: ${JSON.stringify(overflow)}`);
   const pixels=await page.screenshot({type:'png',animations:'disabled'});
   const file=path.join(out,`${shot.id}.png`);
   await sharp(pixels).removeAlpha().withIccProfile('srgb').png().toFile(file);
   const result=await sharp(file).metadata();
   if(result.hasAlpha || result.width!==device.w || result.height!==device.h)throw new Error(`Export validation failed: ${file}`);
   report.push({device:device.name,file:path.relative(outputRoot,file).replaceAll('\\','/'),width:result.width,height:result.height,colourSpace:result.space,alpha:result.hasAlpha,sha256:crypto.createHash('sha256').update(await fs.readFile(file)).digest('hex'),source:path.relative(outputRoot,path.join(originals,rawName)).replaceAll('\\','/'),sourceSHA256:crypto.createHash('sha256').update(raw).digest('hex'),title:shot.headline.join(' '),caption:shot.caption.replaceAll('\n',' ')});
   console.log(`${device.key}: ${shot.id}`);
  }
  await page.close();
 }}finally{await browser.close()}
 await fs.writeFile(path.join(outputRoot,'artwork-verification.json'),JSON.stringify(report,null,2));
 await fs.writeFile(path.join(outputRoot,'captions.txt'),shots.map((s,i)=>`${i+1}. ${s.headline.join(' ')}\n${s.caption.replaceAll('\n',' ')}`).join('\n\n')+'\n');
 let gallery=`<!doctype html><html lang="en-GB"><meta charset="utf-8"><title>Quizfolk · App Store screenshots</title><style>body{margin:40px;background:#f7f6f2;color:#243449;font:17px system-ui}h1{font-size:38px;letter-spacing:-1px}p{line-height:1.55;max-width:850px}.grid{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:28px;max-width:1500px}figure{margin:0}img{width:100%;border-radius:12px;box-shadow:0 6px 20px #2434491c}figcaption{font-size:14px;margin:10px 0 24px}a{color:inherit}h2{margin-top:60px}@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}}</style><h1>Quizfolk · App Store screenshots</h1><p>Ten features, with captions and genuine app captures. Open any image for the full-resolution PNG. The iPad set shows the current iPhone app running in iPad compatibility mode; it does not imply a native iPad layout.</p>`;
 for(const d of devices){const items=report.filter(r=>r.device===d.name);if(!items.length)continue;gallery+=`<h2>${d.name} · ${d.w} × ${d.h}</h2><div class="grid">`+items.map(r=>`<figure><a href="${r.file}"><img src="${r.file}" alt="${esc(r.title)}"></a><figcaption>${esc(r.title)}</figcaption></figure>`).join('')+'</div>';}
 await fs.writeFile(path.join(outputRoot,'index.html'),gallery,'utf8');
 // Small contact sheets for quick visual review; full-resolution artwork stays separate.
 for(const d of devices){const items=report.filter(r=>r.device===d.name);if(!items.length)continue;const tw=d.key==='ipad'?320:245, th=Math.round(tw*d.h/d.w), gap=20, cols=5, rows=2;
  const layers=[];for(let i=0;i<items.length;i++){layers.push({input:await sharp(path.join(outputRoot,items[i].file)).resize({width:tw}).toBuffer(),left:gap+(i%cols)*(tw+gap),top:gap+Math.floor(i/cols)*(th+gap)});}
  await sharp({create:{width:cols*(tw+gap)+gap,height:rows*(th+gap)+gap,channels:3,background:'#f7f6f2'}}).composite(layers).png().toFile(path.join(outputRoot,`${d.key}-overview.png`));
 }
}
main().catch(e=>{console.error(e);process.exitCode=1});
