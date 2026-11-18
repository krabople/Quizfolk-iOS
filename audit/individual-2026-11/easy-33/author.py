"""Original fully specified easy puzzles. Drafts are not approved by this script."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
rows='''1|A red train leaves before a blue train. A green train leaves after the blue train. Which leaves last?|The green train|The red train|The blue train|They all leave together|Red precedes blue, which precedes green; green is last.
2|A queue is Ava, Ben, Cara, Dan, from front to back. Ben leaves. Who is now second?|Cara|Ava|Ben|Dan|Removing Ben leaves Ava, Cara, Dan; Cara is second.
3|Four cards read L, M, N, P from left to right. Move P to the left end without changing the others' order. What is now third?|M|L|N|P|The new order is P,L,M,N; M is third.
4|A stack has a red plate on top of a blue plate, above a green plate. Remove the top plate. Which colour is now on top?|Blue|Red|Green|The stack is empty|Only red is removed; blue becomes top.
5|A coin is in exactly one of two boxes. The red box is empty. Where is the coin?|In the other box|In the red box|In both boxes|In neither box|Exactly one box holds the coin and red is excluded, so the other must contain it.
6|I have exactly two keys: silver and brass. Only one opens a lock. The silver key does not open it. Which key does?|Brass|Silver|Both|Neither|Exactly one works and silver fails, leaving brass.
7|A door opens only if its light is green. The door is open. What must be true?|The light is green|The light is red|The light is off|The light is flashing blue|Only-if makes green necessary for an open door, so it must be green.
8|A lamp is on if and only if a switch is up. The switch is down. What is the lamp's state?|Off|On|It must flash|It cannot be determined|The equivalence makes lamp on exactly when switch up; down means off.
9|A route must use either the bridge or the tunnel. The bridge is closed. Which route remains possible?|The tunnel|The bridge|Both routes|Neither route|Of the two specified alternatives, excluding bridge leaves tunnel.
10|Maya owns exactly one pet, either a rabbit or a turtle. It is not a turtle. What is it?|A rabbit|A turtle|Both animals|Neither animal|The stated two-way choice and exclusion force rabbit.
11|Every package with a red sticker is fragile. This package has a red sticker. What follows?|It is fragile|It is not fragile|It has no sticker|It must be empty|Universal implication applied to the named package establishes fragile only.
12|All tickets in this drawer are blue. A ticket is yellow. What can you conclude?|It is not from this drawer|It is definitely in this drawer|It must be blue too|The drawer is empty|A yellow ticket cannot belong to the all-blue drawer; the drawer need not be empty.
13|No wooden blocks in a set are round. This block from the set is round. What follows?|It is not wooden|It is wooden|It must be red|It must be the largest block|Round excludes wooden under the stated rule; colour and size are unknown.
14|Every member of a team wears a badge. Alex is a member. What must Alex wear?|A badge|A hat|A scarf|A uniform jacket|The rule requires a badge, without implying the other clothing items.
15|Some library volunteers are students. Every student in that group has a locker. What must be true?|At least one volunteer has a locker|Every volunteer has a locker|No volunteer has a locker|Every locker belongs to a volunteer|The student-volunteer overlap is nonempty and those students have lockers; no universal claim about all volunteers follows.
16|The rule is: if a bell rings, a red lamp lights. The red lamp is dark. What must be true?|The bell has not rung|The bell has rung|A blue lamp is lit|The bell is broken|Contrapositive of bell implies red light: dark red light excludes the bell ringing under this rule.
17|A café serves tea or coffee with each breakfast, never both. Pat's breakfast includes tea. Does it also include coffee?|No|Yes, always|Only if the tea is hot|There is not enough information|The explicit never-both rule excludes coffee when tea is included.
18|Exactly one of three doors is unlocked. Door A and door C are locked. Which is unlocked?|B|A|C|All three|Two exclusions and exactly one unlocked force B.
19|There are only apples and pears in a bowl. Every apple has been removed. At least one fruit remains. What must remain?|Pears|Apples|Oranges|Bananas|The remaining fruit cannot be apples and only pears are otherwise allowed.
20|A bag holds only circles and squares. You take out a shape that is not a circle. What is it?|A square|A triangle|A rectangle that is not a square|A pentagon|The two allowed types and exclusion force square.
21|Four runners finish without ties: Jo ahead of Kim, Kim ahead of Lee, and Lee ahead of Mo. Who finishes second?|Kim|Jo|Lee|Mo|The complete order Jo,Kim,Lee,Mo places Kim second.
22|Ava stands immediately behind Ben and immediately ahead of Cara. Who stands between the other two?|Ava|Ben|Cara|Nobody|Both immediate-position clues place Ben,Ava,Cara in that order.
23|A shelf has exactly three books. Art is left of Music; Music is left of Travel. Which is at the right end?|Travel|Art|Music|There is no book at the right end|The three-book order is Art,Music,Travel; Travel is rightmost.
24|Three boxes have different weights. Blue is heavier than red, and red is heavier than yellow. Which is lightest?|Yellow|Red|Blue|All weigh the same|Blue > red > yellow, so yellow is lightest.
25|Nia arrives before Omar. Pia arrives before Nia. Who arrives first among these three?|Pia|Nia|Omar|They arrive together|Pia precedes Nia, who precedes Omar; Pia is first.
26|Five beads are in the order red, blue, green, yellow, white. Which bead has exactly two beads on each side?|Green|Blue|Yellow|White|The third bead is green and has two before and two after.
27|A queue contains four people. Sam joins at the back. Nobody leaves. What is Sam's position from the front?|Fifth|Fourth|Third|Sixth|Four people remain ahead of Sam, making Sam fifth.
28|In a queue, you are third from the front and second from the back. How many people are there?|Four|Three|Five|Six|Two ahead + you + one behind = four; do not double-count yourself.
29|A row reads A, B, C, D, E. Swap B and D. Which letter is immediately right of C?|B|A|D|E|The resulting order A,D,C,B,E puts B immediately right of C.
30|A red cube is below a blue cube. A green cube is above that blue cube. Which cube is in the middle of these three?|Blue|Red|Green|None of them|Bottom to top red,blue,green, so blue is middle.
31|You face east and make one quarter-turn to your left. Which direction do you face?|North|South|East|West|Left 90 degrees from east points north.
32|You face south and turn halfway around. Which direction do you face?|North|East|South|West|A half-turn reverses south to north, regardless of rotation direction.
33|You face west and make two quarter-turns to your right. Which way do you face?|East|North|South|West|West to north to east: two right quarter-turns make a half-turn.
34|You walk three equal steps north, then three equal steps south along the same line. Where do you finish?|At the starting point|Three steps north of it|Six steps south of it|Three steps east of it|Equal opposite displacements cancel; the same-line condition rules out different routes.
35|On a square map, the library is directly east of the school. Which direction is the school from the library?|West|East|North|South|Reversing an eastward relationship gives west.
36|A toy car points north. Rotate it a quarter-turn clockwise, then another quarter-turn clockwise. Where does it point?|South|North|East|West|North to east to south through two clockwise quarter-turns.
37|A token moves one square up, one right, one down and one left on a grid. Where is it now?|On its starting square|One square above the start|One square right of the start|Two squares below the start|The four directed moves form a closed square and cancel.
38|A clock's minute hand points at 12. Move it clockwise by a quarter-circle. Which number does it point at?|3|6|9|12|Clockwise 90 degrees from 12 reaches 3.
39|You face north. A person stands directly behind you. In which compass direction are they?|South|North|East|West|Behind someone facing north is south.
40|A row of arrows is up, right, down, left. Rotate every arrow a half-turn. What does the second arrow become?|Left|Up|Right|Down|The second arrow starts right; a half-turn makes it left.
41|A machine's rule is 'add 3'. You put in 4. What comes out?|7|1|12|43|Explicit addition rule gives 4+3=7; multiplication and concatenation are not the rule.
42|A machine doubles its input, then adds 1. You put in 3. What comes out?|7|6|8|9|Order is 3*2+1=7, not (3+1)*2.
43|A code changes A to 1, B to 2 and C to 3. What does BCA become?|231|123|312|213|Letterwise B=2,C=3,A=1 gives 231; no unspecified alphabet mapping is required.
44|A rule repeats red, blue, red, blue, forever. What is the seventh colour?|Red|Blue|Green|Yellow|Odd positions in the explicitly alternating rule are red; seventh is odd.
45|A sequence starts at 5 and adds 2 each time. What is its third number?|9|7|10|11|The specified sequence begins 5,7,9; third is 9.
46|A sequence starts at 12 and subtracts 4 each time. What is its fourth number?|0|4|8|16|The explicit rule gives 12,8,4,0; fourth is zero.
47|A code swaps every A for B and every B for A. What does ABBA become?|BAAB|ABAB|BBAA|AABB|Apply simultaneous letter substitutions A->B,B->A,B->A,A->B; BAAB.
48|Reverse the order of the three words in 'cats chase mice', leaving each word unchanged. What do you get?|mice chase cats|stac esahc ecim|chase cats mice|cats mice chase|Word order reversal, not letter reversal, produces mice chase cats.
49|A rule says 'write the last letter first, then the others in their original order'. What does FROG become?|GFRO|GORF|ROGF|FGR O|Move G to front and keep F,R,O ordered; GFRO.
50|A machine halves a number. Its output is 6. What number went in?|12|3|6|18|Input/2=6, so input is 12; the output is not the input.
51|A bag contains one red ball and one blue ball. You remove the red ball. What colour is the ball left inside?|Blue|Red|Green|There is no ball left|Exactly two initially; removing red leaves the sole blue ball.
52|Three cups are marked A, B and C. A marble starts under A. Swap A with B, then swap B with C. Which marked cup now covers the marble?|A|B|C|None of them|The marble stays under the cup marked A if cups and covered marble move together; original wording needs review of whether marble moves with cups.
53|A jar contains five coins. You move two of those coins into your pocket. How many of those coins are now in your pocket?|Two|Three|Five|Seven|The question asks transferred coins in the pocket, not coins remaining in jar; two.
54|A box has six pencils. You give half of them away. How many remain in the box?|Three|Two|Six|Twelve|Half of six is three given away and three retained.
55|You have three pairs of gloves, with one left and one right glove in each pair. How many gloves do you have?|Six|Three|Four|Nine|Three pairs at two gloves per pair gives six individual gloves.
56|A room has four corners and a chair in each corner. Two people sit on each chair. How many people are sitting?|Eight|Four|Six|Ten|Four occupied chairs times two people each is eight; no extra people are stated.
57|A basket contains four oranges. You take three and keep them. How many oranges did you take?|Three|One|Four|Seven|The question directly asks the number taken, three, rather than the one left behind.
58|There are seven birds on a fence. Two fly away and none arrive. How many remain on the fence?|Five|Two|Seven|Nine|The explicit departure-only condition gives 7-2=5 without a hidden all-fly-away assumption.
59|A shop gives one sticker with each notebook. You buy four notebooks. How many stickers should you receive?|Four|One|Three|Eight|One per notebook and four notebooks implies four stickers.
60|There are three red blocks and two blue blocks. You add one green block without removing any. How many blocks are there now?|Six|Five|Four|Three|The groups total 3+2+1=6; colours do not change the count.
61|A light starts on. You switch it off, then on, then off. What is its final state?|Off|On|It must blink|It is halfway on|The explicit final action is off, so final state off.
62|A coin starts tails up. You turn it over twice. Which side is up at the end?|Tails|Heads|Both sides|Neither side|Two flips restore the original side, tails.
63|A door starts closed. Each push toggles it between open and closed. After four pushes, what is its state?|Closed|Open|Half-open|It cannot be determined|Even number of toggles restores the starting closed state.
64|A page has three empty checkboxes. You tick the first and third, then untick the first. Which remains ticked?|Only the third|Only the first|The first and third|All three|First tick is undone; third remains ticked and second untouched.
65|A board reads YES. Each button press switches it between YES and NO. What does it show after three presses?|NO|YES|YES NO|Nothing|Three toggles from YES give NO,YES,NO.
66|A counter starts white. Painting it red covers its old colour; painting it blue afterwards covers the red. What colour is visible?|Blue|Red|White|Purple|The stated covering rule excludes colour mixing; final opaque coat is blue.
67|You open an empty box, put a ball in it and close it. Without opening it again, you move the box upstairs. Where is the ball?|Inside the box upstairs|Inside the box downstairs|Outside the box upstairs|It has disappeared|Moving the closed containing box carries the ball upstairs; no removal occurs.
68|A toy has only two settings, slow and fast. Each press changes to the other setting. It starts fast. What is it after one press?|Slow|Fast|Stopped|Medium|The explicit two-state toggle sends fast to slow; no third setting exists.
69|A token starts on square 2. A move always advances it one square. After three moves, which square is it on?|5|3|4|6|Three successive increments take 2->3->4->5.
70|A lift is on floor 4. It goes down one floor, then up two. On which floor does it finish?|5|3|4|6|4-1+2=5; ordinary consecutive floors are intended and should be stated in review.
71|Only one of three boxes contains a prize. A clue says 'It is not in A or B'. Which box contains it?|C|A|B|None|Excluding A and B from exactly one prize among three forces C.
72|A red envelope contains a letter. The letter is moved into a blue envelope, leaving the red one empty. Where is the letter?|In the blue envelope|In the red envelope|In both envelopes|In neither envelope|Only relocation described puts the one letter in blue, not red.
73|Two people choose different fruits from apple and pear, one fruit each. Lia chooses pear. What does Max choose?|Apple|Pear|Both|Neither|Two people, two choices and different selections force Max to apple.
74|Ada, Bo and Cy have one hat each: red, blue and green, all different. Ada has red and Bo has green. What colour is Cy's hat?|Blue|Red|Green|Yellow|Unused colour among three is blue; yellow is outside the stated set.
75|Three bags hold a book, a ball and a bell, one object each. Bag A has the bell; bag B has the book. What is in bag C?|The ball|The book|The bell|All three objects|Ball is the only unassigned object under one-per-bag rule.
76|A hidden number is either 4, 5 or 6. It is odd. What is it?|5|4|6|All three fit|Five is the only odd option in the explicit candidate set.
77|A secret number is one of 10, 20 or 30. It is greater than 10 and less than 30. What is it?|20|10|30|None of them|Strict inequalities exclude endpoints and leave 20.
78|A code uses two digits. Its first digit is 4 and its last digit is 7. What is the code?|47|74|44|77|Two positions specified yield 47; no extra unstated positions.
79|A two-letter code has different letters, chosen only from X and Y. It begins with Y. What is it?|YX|XY|YY|XX|Different letters forces X second once Y is first.
80|A three-digit code ends in 6. Its first two digits are 2 then 4. What is it?|246|264|426|642|Concatenating the supplied ordered positions yields 246.
81|Anna is Bella's mother. Bella is Chris's mother. How is Anna related to Chris?|Grandmother|Sister|Aunt|Daughter|Mother of a parent is grandmother, not aunt, sibling or descendant.
82|Leo and Mina have the same two parents. Leo is a boy and Mina is a girl. How is Mina related to Leo?|Sister|Mother|Aunt|Daughter|Children sharing both parents are siblings; Mina is his sister.
83|Omar is Pia's father. Pia is a girl. How is Pia related to Omar?|Daughter|Mother|Sister|Grandmother|A female child of a father is his daughter; relationship direction matters.
84|Tia has one son, Uma has one son, and these are two different children. How many sons have been mentioned?|Two|One|Three|Four|The explicit different-children condition prevents shared-child ambiguity; two sons.
85|There are two adults and their three children in a room, with nobody else present. How many people are there?|Five|Three|Four|Six|Two adults plus three children gives five distinct people.
86|A parent has exactly three children: a girl and two boys. How many brothers does the girl have?|Two|One|Three|None|The two other children are both boys, so she has two brothers.
87|Rosa is Sam's sister. Sam is Tom's father. How is Rosa related to Tom?|Aunt|Sister|Mother|Daughter|Father's sister is aunt; the other relations do not follow.
88|Eli is Finn's son. Finn is Gia's son. How is Eli related to Gia?|Grandson|Father|Brother|Uncle|Son of a son is grandson; Eli's sex is stated by son.
89|A family photo shows a grandmother, her daughter and that daughter's son, with nobody else. How many generations are shown?|Three|One|Two|Four|Grandmother, daughter and grandson occupy three successive generations.
90|June is Kai's daughter. Kai is Lee's brother. What is June to Lee?|A niece|A nephew|A mother|A grandmother|Brother's daughter is niece, independent of Lee's sex.
91|There are three empty seats in a row. One person sits in the middle. How many seats are still empty?|Two|One|Three|None|Three minus the one occupied seat leaves two.
92|Two pairs of shoes stand by a door. Each pair contains two shoes. How many shoes are there?|Four|Two|Three|Six|Two pairs times two shoes gives four; units explicitly distinguish pairs and shoes.
93|A calendar marker starts on Tuesday. Move it forward one day, then back two days. Where does it end?|Monday|Tuesday|Wednesday|Thursday|Tuesday->Wednesday->Tuesday->Monday yields Monday.
94|Yesterday was Sunday. What day is tomorrow?|Tuesday|Monday|Sunday|Wednesday|Today Monday, tomorrow Tuesday; two steps from yesterday.
95|A game lets you move only to a higher-numbered square. You are on square 5. Which move is allowed?|To square 8|To square 4|To square 5|To square 2|Eight is the sole destination strictly higher than five; staying on five is not higher.
96|A rule allows exactly one item in a box. The box already contains a ball. What must you do before putting in a book instead?|Remove the ball|Add another ball|Leave the ball inside|Put both in together|Replacing the single allowed item requires removal; other actions violate exactly-one rule.
97|Three friends each need their own ticket. You have two tickets, and tickets cannot be shared. How many more do you need?|One|Two|Three|None|Three needed minus two held leaves one additional ticket.
98|A box can hold at most four blocks. It already has three. How many more can you add without removing any?|One|Two|Three|Four|Capacity4 minus current3 leaves one place; without removal fixes the constraint.
99|You have a red pen, a blue pen and a green pen. You lend out every pen except the blue one. Which pen do you keep?|Blue|Red|Green|None|Except blue excludes blue from the loan; other two are lent.
100|Three runners enter a race, all finish and there are no ties. You finish ahead of exactly one runner. What is your position?|Second|First|Third|Fourth|Exactly one behind among three means one ahead and one behind; second.
'''
if __name__=='__main__':
    q=[]
    for line in rows.strip().splitlines():
        n,prompt,answer,*rest=line.split('|');assert len(rest)==4 and int(n)==len(q)+1
        q.append({'draftID':f'easy-33-{int(n):03d}','categoryID':'33','difficulty':'easy','prompt':prompt,'answers':[answer,*rest[:3]],'correctIndex':0,'rationale':rest[3],
        'sourceURL':'https://github.com/krabople/Quizfolk-iOS/blob/main/audit/individual-2026-11/easy-33/author.py','reviewStatus':'draft_awaiting_author_final_check'})
    assert len(q)==100
    (HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print('100 original candidates, not reviewed or approved.')
