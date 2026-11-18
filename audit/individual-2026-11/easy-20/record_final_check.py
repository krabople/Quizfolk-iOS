"""Explicit item-by-item author second pass, not an independent review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
30:{'prompt':"In Hesiod's account of Greek myth, what does Atlas hold up?"},
31:{'answers':['The chariot of the Sun',"Poseidon's boat","Hermes's wagon","Hades's coach"]},
47:{'prompt':'Which weapons does Cupid commonly carry in classical art?'},
49:{'answers':['Saturn','Neptune','Mercury','Vulcan']},
54:{'prompt':'Which of these legendary figures is associated with the founding of Rome?','answers':['Romulus','Castor','Pollux','Achilles']},
60:{'prompt':'What kind of creature is Jormungandr in Norse mythology?'},
85:{'sourceURL':'https://www.collinsdictionary.com/dictionary/english/excalibur'},
87:{'sourceURL':'https://en.wikipedia.org/wiki/Round_Table'},
90:{'prompt':"In Aesop's fable about a goose killed by its greedy owner, what had the goose been laying?"},
91:{'prompt':'Sun Wukong, the magical hero of Journey to the West, is what kind of animal?'},
99:{'prompt':'Bunyip stories originate in Aboriginal traditions in which country?'},
}
notes='''1|Aphrodite alone is the conventional love/beauty goddess among Demeter,Hestia,Artemis. Walters object identifies all their roles; no overlapping love deity offered. Prompt and four names spelled correctly.
2|Artemis is goddess of hunting, unlike Aphrodite,Hestia,Demeter. Walters hunt identification and UF table agree. Especially associated avoids claiming each deity has only one sphere.
3|Demeter is agriculture/harvest, unlike Hestia hearth,Hera marriage,Aphrodite love. Museum wheat-sheaf description supports grain/harvest association. Similar wording to an existing Hera question asks a different deity/domain fact.
4|Hestia is hearth/home. Artemis,Aphrodite,Athena have other principal roles. Museum and UF table explicitly support; no Roman Vesta in Greek answer choices.
5|Hermes is divine messenger; Ares war,Hephaestus metalwork,Dionysus wine. Museum and UF definitions agree. All options Greek gods and exactly one standard messenger.
6|Hades rules lower world, as Theoi's classical-source entry states. Zeus and Apollo do not; Hermes guides souls but is not ruler. Ruling wording prevents psychopomp overlap.
7|Mount Olympus is the Olympians' home in Cambridge's mythological sense. Etna,Vesuvius,Sinai are other named mountains. Highest-mountain geography is not the queried fact.
8|Poseidon carries trident with three prongs. Bow,sling,one-point spear differ. Museum object explicitly identifies trident; the one-point qualifier avoids arguing a trident is broadly a spear.
9|Zeus's thunderbolt is the museum's stated attribute. Trident,bow,hammer identify other divine weapons. Familiar-attribute framing does not claim he could never use other weapons.
10|Athena's owl is explicit in museum object. Swan,peacock,dove are other deity associations. No second owl-associated deity is asked; question names Athena.
11|Theoi distinguishes Homer's golden sandals from later artistic winged ankle/sandal depictions. Prompt explicitly asks art and says often; wings only offered matching attribute. Wheels,claws,hooves not the common sandals feature.
12|Theoi lists peacock as Hera's ordinary attribute. Owl,eagle,swallow are not her familiar identifying bird. Classical includes later Greek/Roman imagery, avoiding assertion that every early Greek representation had a peacock.
13|Theoi's Hesiodic account has Aphrodite emerge from sea foam. Burning tree,cave,raincloud wrong. 'A familiar account' preserves alternate Zeus/Dione parentage traditions.
14|Demeter is Persephone's mother in the inspected Theoi entry. Hera,Hestia,Artemis are different goddesses. Similar spelling to Perseus does not duplicate the existing Danae question; possessive correctly placed.
15|Charon is ferryman of shades. Chiron centaur,Cronus Titan,Cerberus hound. A river avoids falsely insisting every source uses Styx rather than Acheron; all names distinct.
16|Theoi explicitly calls Styx the underworld river. Thames,Nile,Tiber are not that mythic river. Real rivers can appear in stories but wording asks the mythological underworld, making one appropriate answer.
17|Theoi underworld list says three-headed Cerberus. Other head counts occur in ancient variants, so familiar-depictions qualifier is necessary and retained. One,two,seven are not the standard familiar portrayal.
18|Theoi describes Medusa's serpentine hair. Feathers,flowers,antlers not the familiar Gorgon appearance. Prompt qualifies familiar Greek depictions rather than claiming an invariant appearance in every source.
19|Theoi gives petrification of those who look at Medusa. Invisibility,birds,shadow loss not the effect. Direct viewing distinguishes Perseus's reflected image method already queried elsewhere; the new question asks the danger itself.
20|Theoi identifies a single eye in the forehead, particularly Polyphemus. Three eyes,two stalked eyes,no eyes do not identify Cyclops. Singular Cyclops and plural beings not conflated.
21|Lernaean Hydra is many-headed serpent, directly supported by Theoi's Hydra entry and nine-head primary passages. Winged horse,one-eyed giant,centaur descriptions are different monsters. No fixed head count required across variants.
22|Theoi heroes list calls Theseus slayer of Minotaur. Jason,Orpheus,Perseus have other quests. This asks slayer, unlike existing bull-head/parent/Ariadne questions.
23|Walters Daidalos/Ikaros object describes Daedalus making feather/wax wings for himself and son Icarus. Minos,Theseus,Midas not father/inventor. Familiar English spelling Daedalus retained.
24|Library of Congress describes Icarus's fatal near-Sun flight and wax wings. Melting wax is the familiar failure, not stone wings,divinity or halted Sun. No real-world physics claim is made; myth scope explicit.
25|Theoi Midas account describes golden touch and food becoming gold. Silver,stone,ice not the granted transformation. King's possessive correctly formed.
26|Theoi states Narcissus loves his own reflection. Father,Zeus,Apollo wrong. Whose reflection wording unambiguous; the answer 'His own' has clear antecedent.
27|Ovid passage on Theoi explicitly limits Echo to repeating others' final words. Birdsong,own name,first word are wrong. Last words does not claim only last single syllable across all retellings.
28|Theoi quotes and summary identify Elpis/Hope remaining inside jar. Youth,gold,victory not named remainder. Jar is historically preferable to later box; no disputed interpretation of hope's value is tested.
29|Theoi heroes list says Arachne becomes a spider. Bee,butterfly,scorpion differ. Weaving clue meaningful and grammar correct; no claim the myth is zoological history.
30|Theoi notes different Atlas traditions, including heaven and earth interpretations. Scope final question explicitly to Hesiod's heaven-bearing account, making sky uniquely correct over Earth,Moon,sea. This is a substantive ambiguity correction.
31|Theoi Phaethon account identifies Sun's chariot. Other divine vehicles not his attempted ride. Standardise all possessives to Hermes's/Hades's; vehicle relation and Sun capitalisation checked.
32|Cambridge's mythological nectar sense is divine drink. Armour,underworld river,weapon are distinct categories. Botanical nectar sense excluded by Greek mythology scope.
33|Cambridge defines ambrosia as gods' food. Crown,shield,monster not possible definitions. Commonly described acknowledges literary variation without offering another food/drink as competing answer.
34|Theoi Tartarus entry describes deep cosmic pit and prison, later punitive realm. Singing mountain,horse,cloak not Tartarus. Definition covers shared core of ancient variants rather than conflating all Hades with eternal punishment.
35|Theoi Hypnos identifies sleep, distinguished from Thanatos death,Eros desire,Ares war. Existing Thanatos question is a different personification. Hypnos transliteration familiar and consistent.
36|UF comparison identifies Zeus/Jupiter king of gods. Mercury,Mars,Vulcan have other principal functions. Roman scope distinguishes existing Greek Zeus kingship question.
37|UF identifies Juno with Hera and marriage; familiar Jupiter consort relationship also follows classical pairing. Venus,Diana,Minerva not Jupiter's wife. Both clues align; no claim Juno only marriage goddess.
38|UF Neptune/Poseidon domain seas. Jupiter,Mercury,Vulcan not sea ruler. Existing Greek-counterpart question mentions Neptune but this asks Roman deity/domain, a new primary fact query.
39|UF Venus/Aphrodite love/beauty. Minerva wisdom,Diana hunt,Ceres harvest different. Roman name required, no Greek synonym option.
40|UF Mercury/Hermes messenger. Mars,Neptune,Vulcan other roles. Travel/trade overlap among gods does not offer second divine messenger here.
41|UF Diana/Artemis hunting. Venus,Juno,Ceres different principal roles. All are Roman goddesses and source table directly supports sole intended answer.
42|UF Minerva/Athena wisdom. Venus,Diana,Juno other domains. Especially qualifier allows deities with many functions; no competing conventional wisdom deity offered.
43|UF Ceres/Demeter harvest/agriculture. Diana,Juno,Venus do not conventionally identify grain goddess. Grain clue sharpens domain and grammar.
44|UF Bacchus/Dionysus wine. Mercury,Mars,Neptune not conventional wine god. Roman Bacchus name and alternatives spelled correctly.
45|Cambridge Vesta definition explicitly hearth/home. Venus,Diana,Juno are not hearth goddess. Sacred-fire wording matches cult context; not generic every ritual fire.
46|Replace astronomy-only Cambridge Pluto reference with UF's Hades/Pluto underworld table. Mercury may guide souls but does not rule; Jupiter/Mars not underworld ruler. Only one option fits ruling role.
47|Cambridge Cupid describes winged boy shooting arrows, supporting bow/arrows. Hammer/tongs,trident/net,sword/shield differ. Rephrase prompt to clearer 'Which weapons does Cupid commonly carry' while keeping scope classical art.
48|Cambridge Janus definition says two faces looking forward/back. Other depictions can be four-faced, so usually qualifier retained. One,three,four not the conventional two-faced image.
49|Routledge textbook explicitly calls Saturn god of sowing. Mars has agricultural associations too, so replace Mars distractor with Neptune; Mercury/Vulcan not sowing deity. Ceres deliberately not offered. This removes a plausible second answer.
50|Theoi Eos page lists Roman name Aurora and dawn translation. Deep sea,hearth,harvest other domains. Replace physical polar-aurora dictionary sense with the proper deity reference.
51|Getty iconography record explicitly identifies Flora as goddess of flowering plants. Sea storms,blacksmithing,warfare wrong. Replace generic plant-flora dictionary entry; proper-name capitalisation preserved.
52|Theoi Tykhe page lists Roman Fortuna and fortune/chance. Diana,Juno,Vesta not personification of fortune. Luck/fortune wording is a paraphrase, not speculative cult history.
53|Borghese relief account directly describes she-wolf nursing twins. Lioness,mare,doe wrong. Roman foundation legend explicitly identifies narrative rather than asserting zoological/historical event.
54|Borghese account treats both twins as foundation figures. Remove Remus from competing options and ask which offered legendary figure is associated with founding Rome. Romulus fits; Castor,Pollux,Achilles do not. Avoids disputed sole-founder phrasing.
55|MIT's Virgil Aeneid text identifies Aeneas and his Trojan/Latian journey, consistent with epic protagonist. Achilles,Theseus,Jason other heroes. Replace heroes list that lacked Aeneas with primary epic text.
56|Oslo museum describes Thor's sky journey producing thunder/lightning. Moon,underworld dead,law-writing not his defining domain. Especially associated qualifier retained; Norse scope avoids Marvel powers.
57|Stockholm museum calls Odin one-eyed after wisdom sacrifice. Two original eyes before sacrifice but one after; three/four wrong. Temporal phrase essential and retained.
58|Oslo and Stockholm museums both call Sleipnir eight-legged. Four,six,ten incorrect. Existing question asks rider Odin; new one asks extraordinary leg count.
59|Oslo identifies Fenrir as wolf. Horse,eagle,dragon wrong. Existing Loki offspring question did not ask the animal form; giant adjective not needed for sole answer.
60|Oslo identifies Jormungandr/Midgard Serpent as enormous serpent. Eagle,dog,horse wrong. Remove explanatory 'the Midgard Serpent' from prompt because it gave away the answer.
61|Stockholm says battle-slain warriors go to Valhalla, not only sea-lost sailors,children or farmers. 'Especially associated' avoids asserting every warrior/all dead go there; other halls/traditions exist.
62|Etymonline derives Valkyrie as chooser of slain and describes escorting battle-dead to Valhalla. Apples,forging hammer,holding sky are different tasks. No claim all women warriors were Valkyries.
63|Oslo says humans live in Midgard. Only giants,dwarfs,dragons do not define human realm. Human beings is the sole group associated with its standard meaning.
64|Oslo says gods live in Asgard. Answer specifies Aesir rather than implying all divine beings exclusively live there. Mortal kings,sea monsters,farmers do not define its inhabitants.
65|Inspected Loki article discusses shapeshifting forms and trickster interpretation. Thor,Baldr,Heimdall not chiefly characterised as the trickster. Norse framing excludes Marvel biography; especially known phrasing recognises scholarly complexity.
66|UVic MyNDIR illustration/caption explicitly depicts Fenrir with Tyr's severed hand during binding. Thor,Baldr,Njord not the hand-sacrificing god. Does not specify which hand, avoiding unnecessary variant detail.
67|Stockholm museum calls Gungnir Odin's spear. Hammer,bow,axe wrong. Object-type question unambiguous and distinct from Thor's existing hammer-name question.
68|Stockholm explicitly says Freyja's chariot pulled by cats. Goats are Thor's, wolves/horses other animals. No invented names for cats or claim every portrayal identical.
69|UCL calls Ra sun-god. Osiris,Anubis,Sobek not conventional Sun deity among options. Ra/Re spelling variation does not create second option.
70|Met Isis/Horus object says Isis wife of Osiris and mother of Horus. Nut,Sekhmet,Bastet not Osiris's wife in this narrative. Existing Horus parent question is different fact emphasis, not same prompt/answer.
71|UCL shows Horus falcon and describes celestial kingship. Owl,swan,peacock not his usual head. Possessive bird answers read correctly after 'which bird's head'.
72|UCL directly identifies crocodile power with Sobek. Cat,ibis,ram other deities. Distinct from existing Bastet-cat question despite same template.
73|Fitzwilliam Taweret description identifies hippopotamus head/body, lion legs and crocodile tail. Asking body selects hippopotamus, not lioness/cow/eagle. Composite nature acknowledged, not misleadingly called a pure hippo.
74|Fitzwilliam beetle learning page names Khepri scarab beetle god. Butterfly,dragonfly,mosquito wrong. Source confirms specific insect, not a generic scarab good-luck claim.
75|UCL identifies Osiris god of dead, the familiar ruler of their realm. Sobek,Khnum,Bes other functions. Anubis not offered to blur funerary associations with rulership.
76|Cambridge ankh is ancient Egyptian life sign. War,silence,winter not its meaning. Cross-with-loop shape not necessary to answer and not confused with modern religious cross.
77|Cambridge familiar unicorn has single horn. Two,three,four wrong. European/familiar qualifiers avoid applying description to every Asian unicorn-like being.
78|Cambridge phoenix rises from ashes. Ice,buried stone egg,whirlpool wrong. Familiar legend qualification avoids disputed ancient accounts of burial rather than fiery rebirth.
79|Cambridge griffin combines eagle head/wings and lion body. Horse,bull,deer differ. Spelling griffin accepted English; not confused with hippogriff's horse hindquarters.
80|Cambridge mermaid human upper/fish lower body. Horse,lion,bird tails wrong. Commonly shown qualifier permits artistic variation and distinguishes existing question about mermaid singing.
81|Cambridge werewolf transforms human/wolf. Bear,fox,bat wrong. Does not insist every version needs full moon; that unnecessary restriction omitted from new question.
82|Cambridge folklore vampire drinks blood. Nectar,sap,honey wrong. Folklore qualifier distinguishes real vampire bats and modern metaphorical energy vampires.
83|Cambridge dragon definition includes fire from mouth. Snow,glass,sand not familiar European trait. Many European qualifier prevents universalising over Chinese water/rain dragons.
84|Cambridge kraken is enormous octopus/squid-like sea monster. Desert,volcano,mine wrong habitats. Type of sea monster deliberately not narrowed to one modern species.
85|Collins explicitly calls Excalibur Arthur's magic sword. Crown,shield,cup wrong. Replace failed Cambridge headword/nonmatching English Heritage extraction with exact dictionary reference; no sword-in-stone versus lake origin claim.
86|Rochester Camelot FAQ explicitly calls Guinevere Arthur's wife/queen. Mark,Uther,Pellinore wrong. Romances have variants but the conventional Guinevere relationship unambiguous among these choices.
87|Round Table reference explains no head seat and equal status, unlike rectangular ranking. Gold,every-king ownership,one-chair not equality rationale. Replace Core Knowledge excerpt that discussed chivalry but did not directly explain this geometry.
88|Sherwood visitor site's history traces Robin Hood in Sherwood and local tradition. New Forest,Epping,Ashdown not the conventional setting. Especially allows broader ballad settings without changing the famous association.
89|Same site's historical-ballad account calls Sheriff of Nottingham sworn enemy. York,Exeter,Dover not this traditional antagonist. Existing Merry Men questions concern companions, so new target distinct.
90|Library of Congress Aesop text gives goose laying golden eggs before greedy owner kills it. Specify this fable, avoiding Grimm's different Golden Goose tale and generic financial metaphor. Silver apples,diamond feathers,bronze coins wrong.
91|Ashmolean identifies Sun Wukong as Monkey King in Journey to the West. Remove Monkey King epithet from prompt so question no longer states answer. Monkey fits; tiger,dragon,crane wrong.
92|British Library Chang E narrative explicitly settles her on Moon. Mars,Saturn,Sun wrong for goddess; Sun is associated with husband in some variants, not her home. Standard Chang'e spelling preserved.
93|British Library calls Hou Yi archer and describes raising his bow. Trident,hammer,sling not his defining weapon. Legend scope and familiar spelling correct; no unstated exact sun count asked.
94|Morikami mask text identifies fox/kitsune. Badger,cat,crane different folklore creatures. Japanese folklore scope excludes Greek-letter or zoological mistranslation.
95|Morikami identifies kappa as water-dwelling. Rivers/ponds fits; desert,volcanic craters,snowfields do not. Replace Greek-alphabet kappa dictionary sense with relevant Japanese museum reference.
96|Cambridge kelpie entry describes Scottish river/lake shapeshifting horse. Lion,eagle,wolf not its common form. Commonly qualifier necessary because kelpies also assume human forms.
97|Cambridge selkie sheds seal skin to become human. Dolphin,otter,whale wrong. Scottish/Irish folklore phrasing covers Celtic seal-person tradition without claiming a single local version.
98|UF folklore notes describe chicken-legged hut, also acknowledging other variants. Familiar Russian tales qualifier means standard chicken-leg motif, not every story. Wheels,mushrooms,golden pillars not familiar answer.
99|National Museum of Australia's Biripi-author context and bunyip exhibit locate tradition in Aboriginal Australia. Rephrase to Aboriginal traditions, avoiding implication every Indigenous Australian people tells one identical story. Norway,Japan,Peru wrong.
100|Met's Quetzalcoatl discussion breaks name into quetzal bird and coatl snake, supporting feathered serpent. Golden eagle,jaguar king,moon rabbit wrong. Commonly translated allows precious/plumed renderings not offered as competing correct answers.
'''
rows=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 d={'row':n,'action':'edit' if n in edits else 'keep','prompt':draft[n-1]['prompt'],'note':note,
 'sourceReview':'Author second editorial pass of prompt, all four answers, unique correct choice, grammar, tradition/variant scope and topic relevance. Relevant museum, classical-text, dictionary, academic or specified encyclopaedic reference inspected; blocked direct requests were distinguished from web-source inspection.'}
 if n in edits:d['recommendedChanges']=edits[n]
 rows.append(d)
assert [x['row'] for x in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'One hundred explicit author second-pass judgments, not an independent review or automated approval. Checked actual dictionary senses (planet Pluto/Saturn, generic flora/aurora/change and Greek kappa were unsuitable references), replaced failed or irrelevant initial targets, inspected classical quotations and museum descriptions, and qualified traditions with alternate versions. Corrected giveaway wording, plausible Mars agricultural distractor and Romulus/Remus founder ambiguity. Full extracted reference text stays private; public metadata retains failed retrievals honestly. Loki and Round Table use explicitly identified encyclopaedic entries alongside predominantly museum/classical/dictionary/academic references.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit author final checks recorded; apply edits before publication.')
