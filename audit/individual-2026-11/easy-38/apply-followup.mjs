import fs from 'node:fs';
const file=new URL('./independent-review.json',import.meta.url);
const review=JSON.parse(fs.readFileSync(file,'utf8'));
const row=review.rows[96];
row.action='edit';
row.note='Independent follow-up review by botany_author: replace repeated sour-lemon fact with the savoury taste name. NIDCD explicitly gives broth, meat extracts and some cheeses as examples. Existing bank asks for glutamate, rather than naming this taste from foods.';
row.sourceReview='Verified primary NIDCD taste-disorders educational content; this is an identification question, not medical advice.';
row.recommendedChanges={prompt:'What is the name of the savoury basic taste associated with foods such as meat broth and aged cheese?',answers:['Umami','Sour','Sweet','Bitter'],correctIndex:0,rationale:'Umami names the savoury basic taste; broth and some cheeses supply glutamate, while sour, sweet and bitter are separate taste qualities.',sourceURL:'https://www.nidcd.nih.gov/health/taste-disorders'};
fs.writeFileSync(file,JSON.stringify(review,null,2)+'\n');
