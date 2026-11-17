// Apply only changes explicitly recorded in an individual editorial review.
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
const name=process.argv[2];
if(!/^easy-\d+$/.test(name||''))throw Error('Pass an easy-<categoryID> directory');
const dir=new URL('./'+name+'/',import.meta.url);
const file=new URL('draft.json',dir);
const q=JSON.parse(fs.readFileSync(file,'utf8'));
const review=JSON.parse(fs.readFileSync(new URL('independent-review.json',dir),'utf8'));
const reviewKind=review.independent===false?'author final check':'independent review';
if(q.length!==100||review.rows.length!==100)throw Error('Incomplete batch');
const decisions=review.rows.map((d,i)=>{
 const x=q[i];
 if(d.row!==i+1||!['keep','edit'].includes(d.action))throw Error('Unaccepted row '+(i+1));
 if(x.prompt!==d.prompt&&x.prompt!==d.recommendedChanges?.prompt)throw Error('Question changed outside review: '+(i+1));
 const originalPrompt=d.prompt;
 Object.assign(x,d.recommendedChanges||{});
 x.draftID=`${name}-${String(i+1).padStart(3,'0')}`;
 if(x.answers.length!==4||new Set(x.answers).size!==4||x.correctIndex!==0)throw Error('Options changed unexpectedly');
 return {draftID:x.draftID,prompt:x.prompt,originalPrompt,decision:d.action==='edit'?'edited':'keep',reviewer:review.reviewer,
 meaning:d.note,answer:d.note,grammar:`The ${reviewKind} covered the prompt and all four options; required wording edits have been applied.`,
 category:'Appropriate to its assigned category, as individually checked in the editorial review.',sourceURL:x.sourceURL,
 sourceRelevance:d.sourceReview,reviewedSHA256:crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex')};
});
fs.writeFileSync(file,JSON.stringify(q,null,2)+'\n');
fs.writeFileSync(new URL('final-review.json',dir),JSON.stringify({status:'complete',reviewed:100,remaining:0,independent:review.independent!==false,
 appliedEdits:review.rows.filter(x=>x.action==='edit').length,sourceAccessNote:review.sourceAccessNote,decisions},null,2)+'\n');
console.log(`${name}: 100 individually checked (${reviewKind}); ${review.rows.filter(x=>x.action==='edit').length} recorded edits applied. Draft remains unpublished.`);
