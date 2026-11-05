'use strict';
const statusText=document.getElementById('status');
const dashboard=document.getElementById('dashboard');
const actions=document.getElementById('actions');
const number=new Intl.NumberFormat('en-GB');
const time=new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeStyle:'medium',timeZone:'Europe/London'});
function cell(row,value){const td=document.createElement('td');td.textContent=value;row.append(td);return td;}
function render(data){
  for(const key of ['total','today','week'])document.getElementById(key).textContent=number.format(data.totals[key]);
  const days=document.getElementById('days');days.replaceChildren();
  const maximum=Math.max(1,...data.daily.map(day=>day.clicks));
  for(const day of [...data.daily].reverse()){
    const row=document.createElement('tr');cell(row,new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeZone:'UTC'}).format(new Date(day.day+'T12:00:00Z')));
    const count=cell(row,number.format(day.clicks));const bar=document.createElement('meter');bar.min=0;bar.max=maximum;bar.value=day.clicks;bar.setAttribute('aria-label',day.clicks+' requests');count.append(bar);days.append(row);
  }
  const recent=document.getElementById('recent');recent.replaceChildren();
  for(const request of data.recent){const row=document.createElement('tr');cell(row,time.format(new Date(request.requested_at)));cell(row,request.version);recent.append(row);}
  if(!data.recent.length){const row=document.createElement('tr');const empty=cell(row,'No download requests yet.');empty.colSpan=2;recent.append(row);}
  document.getElementById('since').textContent='Tracking started '+time.format(new Date(data.startedAt))+'. '+number.format(data.totals.checks)+' verification requests excluded. Detailed history keeps the latest 1,000 requests; daily totals are retained.';
  dashboard.hidden=false;actions.hidden=false;statusText.textContent='Updated '+time.format(new Date(data.generatedAt));
}
async function load(key){
  document.getElementById('refresh').disabled=true;
  try{
    const response=await fetch('stats.php?data=1',{method:key?'POST':'GET',credentials:'same-origin',cache:'no-store',headers:key?{'Content-Type':'application/json'}:{},body:key?JSON.stringify({action:'unlock',key}):undefined});
    const data=await response.json();if(!response.ok)throw new Error(data.error||'Could not load statistics.');
    if(key)history.replaceState(null,'',location.pathname);
    render(data);
  }catch(error){dashboard.hidden=true;actions.hidden=true;statusText.textContent=error.message;}
  finally{document.getElementById('refresh').disabled=false;}
}
document.getElementById('refresh').addEventListener('click',()=>load());
document.getElementById('signout').addEventListener('click',async()=>{
  try{const response=await fetch('stats.php?data=1',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'logout'})});if(!response.ok)throw new Error('Could not sign out.');dashboard.hidden=true;actions.hidden=true;statusText.textContent='Signed out. Reopen your private stats link to view this dashboard.';}
  catch(error){statusText.textContent=error.message;}
});
function openPrivateLink(){load(new URLSearchParams(location.hash.slice(1)).get('key')||undefined);}
window.addEventListener('hashchange',openPrivateLink);
openPrivateLink();
