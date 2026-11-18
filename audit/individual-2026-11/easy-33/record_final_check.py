"""Individual second-pass solutions for original puzzles, not independent review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
7:{'prompt':'A door can be open only while its light is green. The door is open now. What must be true?'},
12:{'prompt':'Every ticket in this drawer is entirely blue. A ticket is entirely yellow. What can you conclude?','answers':['It is not in this drawer','It is definitely in this drawer','It must be blue too','The drawer is empty']},
15:{'prompt':'Some library volunteers are students. Every student has a locker. What must be true?'},
16:{'prompt':'Whenever a bell is ringing, a red lamp is lit. The lamp is dark right now. What must be true?','answers':['The bell is not ringing','The bell is ringing','A blue lamp is lit','The bell is broken'],'rationale':'Bell ringing implies red lamp lit at that time. The currently dark lamp excludes a currently ringing bell; it says nothing about earlier ringing or a fault.'},
18:{'prompt':'Exactly one of three doors, A, B and C, is unlocked. A and C are locked. Which is unlocked?'},
49:{'answers':['GFRO','GORF','ROGF','FGRO']},
52:{'prompt':'Cups A, B and C stand left to right. A marble stays under the leftmost cup. Swap only the labels A and C, keeping the cups still. Which label is above the marble?','answers':['C','A','B','None of them'],'rationale':'The marble and cup remain in the leftmost position. Only the labels move, so that cup now has label C.'},
53:{'prompt':'A book has consecutively numbered pages. Open, it shows pages 12 and 13. Turn one leaf forward. Which pages are now visible?'},
54:{'prompt':'Three boxes stand left to right in the order A, B, C. Exactly one holds a toy, after A but before C. Which box holds it?'},
68:{'prompt':'A map has roads A-B, B-C and A-D, with no others. Which town must be an intermediate stop when travelling from A to C?','answers':['B','D','A','None']},
72:{'prompt':'A dentist visit and a haircut occupy the 2 pm and 3 pm slots, one appointment per slot. The dentist is earlier. When is the haircut?'},
84:{'prompt':'A family has exactly three children, all with the same parents. Each would need exactly one sister and one brother. Which group is possible?','answers':['No such group is possible','Two girls and one boy','One girl and two boys','Three girls and no boys'],'rationale':'With three siblings, two girls and one boy gives the boy two sisters and no brother; one girl and two boys gives the girl two brothers and no sister. Three of the same sex also fails. No arrangement gives every child one sister and one brother.'},
89:{'prompt':'A photograph shows exactly two people: a mother and her daughter. What is the greatest number of these two who could be mothers?','answers':['Two','One','Zero','Three'],'rationale':'The daughter may also have her own child outside the photograph. Both pictured people could be mothers, so the maximum is two, not necessarily only one.'},
92:{'prompt':'A shelf has three complete pairs of shoes and one extra shoe. How many matching shoes must you add to make four complete pairs?'},
95:{'prompt':'In a game, every move to a higher-numbered square is allowed, and no other move is. You are on square 5. Which move is allowed?'},
}
notes='''1|Red before blue before green uniquely puts green last. Red/blue cannot be last and together contradicts before/after. Three-train scope clear.
2|Delete Ben from Ava,Ben,Cara,Dan: Ava,Cara,Dan. Cara second; Ben no longer in queue, Ava first and Dan third. Front/back direction explicit.
3|Moving P to front yields P,L,M,N. Third M, not L,N,P. Preserve remaining order is explicit; no reversal assumption.
4|Remove red from top-to-bottom red,blue,green: blue remains atop green. Not empty; red removed and green lower. Plate and colour referents clear.
5|Exactly one of two boxes holds coin; red empty forces other. Red/both/neither violate the stated constraints. Simple elimination, no hidden extra box.
6|Only one of silver/brass works; silver fails, so brass works. Both and neither contradict exactly one. No assumption about a third key.
7|Green is a necessary condition while the door is open. Tighten temporal wording so an earlier green light changing later cannot invalidate inference. Red/off/blue fail the explicit current-state rule.
8|On iff up makes down imply off. On, blinking and unknown do not satisfy the two-state equivalence. Input specifies down rather than a third switch setting.
9|Bridge/tunnel are exhaustive route alternatives, bridge excluded. Tunnel remains the possible choice; no claim it has been independently confirmed open. Both/neither/bridge fail available facts.
10|Exactly one rabbit or turtle, not turtle, leaves rabbit. Both and neither contradict one pet; no inference about biology required.
11|Red sticker implies fragile; named parcel has sticker, therefore fragile. Non-fragile contradicts rule; empty and no-sticker do not follow. Universal conditional correctly applied.
12|Make ticket colours entirely blue versus entirely yellow to exclude a multicoloured ticket. Yellow cannot be a drawer member; no conclusion drawer empty. Other options unsupported.
13|No wooden round blocks plus this block round implies not wooden. Colour and size unrestricted; wooden contradicts rule. Set membership explicitly included.
14|Team membership implies badge; Alex member implies badge. Hat/scarf/jacket unrequired. What must be worn is distinct from what could also be worn.
15|At least one volunteer is student and all students have lockers, so at least one volunteer has locker. Simplify ambiguous 'in that group'. All volunteers and ownership of every locker do not follow; none contradicts overlap.
16|Use simultaneous ringing/lit state rather than ambiguous past event. Dark lamp means bell not currently ringing; does not establish earlier events, blue lamp or broken bell. Contrapositive is valid.
17|Exactly tea or coffee, never both; tea excludes coffee. Temperature irrelevant and information sufficient. No follows from the explicit mutually exclusive breakfast rule.
18|Name the three doors A,B,C explicitly. A/C locked and exactly one unlocked selects B. All-three contradicts exactly-one; no unnamed door loophole.
19|Only apples/pears; apples all removed; nonempty remainder consists of pears. Other fruit types disallowed and apples excluded. At least one avoids empty-bowl ambiguity.
20|Only circles/squares and not circle forces square. Non-square rectangle explicitly excludes square; triangle and pentagon outside allowed types. Four options distinct.
21|Jo<Kim<Lee<Mo yields Kim second. Other names occupy positions1,3,4. No ties specified and no additional runners implied by four runners.
22|Ben,Ava,Cara follows immediate behind/ahead clues. Ava between both. Ben/Cara are endpoints; nobody contradicts placement. Spatial order is fully defined.
23|Exactly three books and Art<Music<Travel puts Travel rightmost. Art/Music have books to their right. No-book option contradicts three-book shelf.
24|Blue heavier than red heavier than yellow makes yellow lightest. Other colours heavier; all equal contradicts inequalities. Weights need no numerical assumption.
25|Pia before Nia before Omar makes Pia first among three. Together contradicts before; other people not relevant due among-these-three scope.
26|Green at position3 in five has two on each side. Blue has1/3, yellow3/1, white4/0. Order and equal bead-count condition checked.
27|Four already queued plus Sam at back puts Sam fifth. Other positions imply departure/insertion not stated. Nobody leaves closes that loophole.
28|Two ahead plus self plus one behind equals4. Three double-counts incorrectly, five/six too large. From-front and from-back rankings include the same person.
29|Swap B,D in A,B,C,D,E gives A,D,C,B,E. Immediately right of C is B; A/D/E are elsewhere. Swap is simultaneous, not overwrite.
30|Red below blue below green gives blue middle. Red/green are extremes and none conflicts with three-cube relation. Scope only these three.
31|Left quarter-turn from east is north. South is right, west half-turn and east no turn. Compass orientation and turn size clear.
32|Half-turn south to north regardless of clockwise/anticlockwise choice. East/west are quarter-turns and south unchanged. No rotation ambiguity.
33|Two right quarter-turns west->north->east. North is one turn, south is left turn and west unchanged. Each turn explicitly quarter.
34|Equal steps north and south on same line cancel. Net position start; other displacement options wrong. Equal-length premise avoids stride-length assumption.
35|If library east of school, school west of library. East reverses incorrectly; north/south perpendicular. Map directional relationship is explicit.
36|North->east->south through two clockwise quarter-turns. East intermediate only, north initial and west not on route. Toy rotation defined.
37|Up/right/down/left forms closed unit square; starting square. Other displacements fail cancellation. No boundary or obstruction is stated for grid moves.
38|Clock minute hand 12 plus clockwise quarter-circle lands3. Six half-circle, nine anticlockwise quarter and12 full/no turn. Ordinary numbered clock implied by prompt.
39|Behind a north-facing person is south. North ahead and east/west sides. Directly removes diagonal position possibilities.
40|Second arrow starts right; half-turn makes left. Up/down quarter-turns; right unchanged. Transform each separately, not reorder list.
41|252 alone has same end digits and different middle, drawn only from2/5. 225 ends differ,255 ends differ,522 ends differ. Fully stated code rule replaces plain addition draft.
42|Double3 then add1 gives7. Six omits addition,8 reverses operations and9 neither. Ordered machine rule prevents guessed-pattern ambiguity.
43|BCA maps2,3,1 ->231. Other permutations wrong. All mapping entries needed are supplied; numeric string does not lose leading zero.
44|Specified alternating red/blue rule makes seventh red. Blue even positions; green/yellow excluded. Explicit forever rule avoids underdetermined sequence complaint.
45|Specified add2 rule yields5,7,9. Seven second,11fourth,10not generated. Third includes initial term as first, normal sequence convention.
46|Specified subtract4 gives12,8,4,0. Four third,eight second,16not generated. Fourth is zero; not a free pattern guess.
47|Simultaneous substitutions yieldBAAB. ABAB,BBAA,AABB differ at some positions. Wording swaps every letter, not a sequential destructive replace operation.
48|Reverse word order only: mice chase cats. Reversed letters and other permutations fail instructions. All supplied words remain intact and lower-case as source.
49|FROG last letterG moved beforeFRO givesGFRO. GORF reverses,ROGF rotates wrong,FGRO different. Fix distractor 'FGR O' accidental space; arbitrary code strings need not form English words.
50|Input/2=6 gives12. Three reverses operation wrongly,6unchanged,18would output9. Inverse reasoning and explicit halves rule checked.
51|Right/up moves allow net two right/one up. Every other option requires net left/down, impossible without such allowed moves. Empty infinite grid implicit; no obstacles asserted.
52|Replace ambiguous cup-motion scenario. Cups and marble stay still; only A/C labels swap, leaving C over marble on left. A moves to rightmost label; B middle; none wrong. Correct option changed to C with explanatory rationale.
53|Normal consecutive book pages12/13 become14/15 after one leaf.13/14 overlap,15/16 shifted oddly,16/17 skips leaf. Explicit consecutive numbering added to exclude inserts/skipped pagination.
54|Add explicit left-to-right A,B,C. Strictly afterA beforeC selectsB; endpoints fail. None wrong because B valid. Removes unstated shelf-order assumption.
55|Three pairs each two gloves gives6;3counts pairs,4/9incorrect. Handedness explicitly one left/right each; no missing gloves or wearer assumption.
56|Ana,Bea,Cy sole offered order with Bea between. Other options put Ana or Cy in middle. Reverse valid order exists generally but is not a second offered answer; options uniqueness checked.
57|LISTEN exactly permutes SILENT. SILVER containsV/R notN/T; LITTER repeatsT and hasR; LISTED substitutesD forN. Each letter occurrence counted, not just membership.
58|EARTH is multiset HEART. THERE has twoEs/noA; HEARD hasD/noT; EARNS hasN/S insteadH/T. All answer strings standard words and exactly one anagram.
59|Budget8, unitprice3: two cost6, three cost9, so max2. Four/eight farther over budget. Whole notebooks explicit to exclude fractions.
60|A key uses key; B notring and cannotduplicatekey means Bcoin, Cring. Key/coin/all-three inC violate one-each constraints. Distinct objects and one per box clear.
61|64 distinct even digits descending.46ascending,66notdistinct,63odd digit. All three constraints stated; solely correct code no inferred pattern.
62|Starting1 with +2 repeatedly reaches odd3,5,7, nevereven6. All distractor odd targets reachable. Forward moves intended; even if backwards allowed parity still excludes6.
63|Exactly oneA and oneB yields AB,BA, two ordered strings. One omits arrangement,3/4include illegal codes. Either-order phrase makes order relevant.
64|Explicit reflection maps right to left and holds up/down. Right unchanged violates rule; up/downnotmapping. Avoid relying on unspecified physical mirror placement.
65|OPEN10:00,CLOSED10:01,OPEN10:02,CLOSED10:03. Both/neither not allowed display states. Alternates once per minute; endpoints and three changes checked.
66|One ball inside contradicts EMPTY label. No-contents/secondball/outside statements contradict or are unsupported. Label can be false without requiring all real-world labels truthful.
67|Coin remains in unopened small box, carried outside large box. Other containment alternatives fail one part. No dropping/moving coin separately allowed by stated actions.
68|C's sole road is B-C, so B must be intermediate. D dead-end, A start rather than necessary intermediate, none false. Tighten prompt/options to distinguish passing through from starting town.
69|Ring1..6 then back1; from5 steps6,1,2. Other numeric options one/two/four steps away. Explicit ring order supplies wrap rule.
70|B,C lacks compulsoryA. A,B/A,C/A,D each satisfy two distinct cards withA. Pair order irrelevant but all offered pairs distinct.
71|False 'notinC' means inC; false 'inA' is consistent. A/B conflict with second clue; no-possible false becauseCworks. Two false claims can both hold without liar-paradox assumptions.
72|Explicit one appointment per2/3pm slot; dentist earlier2, haircut3. Both/neither invalid and2belongsdentist. Adds assignment constraint rather than assuming bookings are one per slot.
73|Two different fruits one each: Lia pear leaves Max apple. Pear duplicates, both/neither violate one-each. Names and pronouns unambiguous.
74|Ada red,Bo green leaves Cy blue from all-different three colours. Red/greenused,yellowoutside supply. Each has exactly one hat.
75|BellA and bookB leave ballC. Book/bellrepeat and all-threeviolates one-per-bag. Distinct spelling book/ball/bell increases attention but remains readable.
76|Among1..6 even and >4 only6.2/4fail inequality,5odd. Both clues needed and all options in range.
77|Units4 and tens one less=>3, so34.14/24differences3/2,44difference0. Digit relation clear, not numeric value difference.
78|First/last4,middle3=>434.343wrongends,444middlewrong,443lastwrong. Full length and positions stated.
79|UsingX,Yonce givesXY,YX; onlyYXcomesafterXY. XX/YYillegal andXYnotafteritself. Ordinary alphabet ordering of supplied uppercaseletters sufficient.
80|262 palindrome withmiddle6.226and266notpalindromes;626palindrome butmiddle2. Both constraints used; all options three digits.
81|Anna mother of Bella, Bella mother of Chris=>grandmother. Sister/aunt/daughter are not stated relation. Direct line of descent explicit.
82|Same two parents makes Leo/Mina siblings; Mina girl=>sister. Mother/aunt/daughter not the relation established. No adoption/half-sibling caveats needed under given premises.
83|Pia girl and Omar's child=>daughter. Mother/sister/grandmother reverse or change relation. Prompt direction 'Pia related to Omar' checked.
84|Original candidate had wrong keyed answer; correct to no-such-group. Two girls/oneboy fails forboy, onegirl/twoboys fails forgirl, threegirlsfailsbrother condition. Threeboys also fails, so no three-child sex-count assignment works for every sibling. Exact one sister/brother reading retained.
85|Both age byfive, difference remains30.25/35mistakenly age only one;60doublesdifference. Same birthday handles integer-age-boundary ambiguity.
86|Each brother's single sister is Mina. Different girls/twoothergirls would add sisters and nobody contradicts Mina. Same parents plus exact-one-sister rules exclude separate half-sibling families.
87|FatherSam's sisterRosa is Tom's aunt. Sister/mother/daughternotthisrelation. No need Tom's sex to identify an aunt.
88|Finn sonofGia,Eli sonofFinn gives Gia's grandson. Father/brother/uncle wronggenerationaldirection. Son explicitly specifiesmale.
89|Mother and daughter can both be mothers because daughter's child can be off-camera. Change to greatest number and numeric options: max2.1mayactuallyoccur but is notmaximum;0contradictsmother;3exceedspicturedpeople.
90|Kai brotherofLee andJune daughterofKai=>Lee's niece. Nephewwrongsex,mother/grandmotherwronggeneration. Lee's sex irrelevant.
91|Only2,3empty andadjacent.1,2and3,4includeoccupiedend;1,4bothoccupiedandnonadjacent. Fourconsecutive seatnumbers explicit.
92|Threepairs+extra=seven shoes; one matching shoe completesfourthpair. Add matching wording rather than allowing arbitrary nonmatching purchase. Two/three/fourmore exceed minimum required.
93|Tuesdayforward1Wednesday,back2Monday. Otherweekdaysnotnetminus1. Calendar marker statesdaysteps, not dates/monthboundaries.
94|YesterdaySunday=>todayMonday=>tomorrowTuesday. Mondaytoday,Sundayyesterday,Wednesdaydayaftertomorrow. Similar old relative-day puzzle asks a different relationship and result, not exact duplicate.
95|Make sufficiency explicit: everyhigherdestinationallowed and no others.8>5;4/2lower,5equalnotallowed. Original only-if wording alone could permit extra unstated restrictions.
96|CATlength3distinctletters. CAArepeatsA,CATSlength4,CC length2/repeats. Both conditions necessary; lowercase/uppercase consistent.
97|Pair2+single1=3validtickets for3guests. Noneextra; otheranswersovercount. Each requiresone; pairnotoneitemforticketcount.
98|Total8balls invariant; fivein eachrequires10. Everyyesoptionredistributesbutcannotcreate2missing. At-mostcapacitynotinvoked; simpleconservationpuzzle.
99|Exceptblue means red/greenlent, bluekept. Red/greenwrong,nonewrong. Scope threepens exactlylisted, no hiddenoriginalpensneeded.
100|Onefinisheraheadmeanssecond; twobehindwithfourtotalconsistent. Firsthasnoneahead,thirdhastwoahead,fourthhasthreeahead. Completefinishingandnotiesexplicit.
'''
rows=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 changes=dict(edits.get(n,{}))
 changes['sourceURL']='https://github.com/krabople/Quizfolk-iOS/blob/main/audit/individual-2026-11/easy-33/draft.json'
 rows.append({'row':n,'action':'edit','prompt':draft[n-1]['prompt'],'note':note,'recommendedChanges':changes,
 'sourceReview':'Original self-contained puzzle, checked by solving its stated premises and comparing all four options. No external factual assertion is required; the source link identifies the final original problem specification. Author second pass, not independent review.'})
assert [x['row'] for x in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'These are newly authored, self-contained reasoning problems. Every problem and four options were checked individually by working through the supplied rules; this is not a retrieval-based or independent approval. Weak first drafts were rewritten, the ambiguous cup puzzle replaced, temporal implications made simultaneous, book/slot/order premises specified, a mistyped code fixed and the impossible sibling puzzle answer corrected. The exact final specification is linked as original provenance; no external fact source is invented.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit second-pass solutions recorded; apply corrections before publication.')
