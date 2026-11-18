"""Resolve initial reference candidates; no editorial approval occurs here."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
p=HERE/'draft.json';q=json.loads(p.read_text(encoding='utf8'))
refs={
16:'https://www.theoi.com/Khthonios/PotamosStyx.html',
17:'https://www.theoi.com/greek-mythology/underworld-gods.html',
21:'https://www.theoi.com/Ther/DrakonHydra.html',
23:'https://art.thewalters.org/object/54.1037/',
24:'https://www.loc.gov/exhibits/dreamofflight/dream-dream.html?loclr=blogadm',
34:'https://www.theoi.com/Kosmos/Tartaros.html',
46:'https://guides.uflib.ufl.edu/classics/godsandgoddesses',
49:'https://routledgetextbooks.com/textbooks/9781138543898/chapter-5.php',
50:'https://www.theoi.com/Titan/Eos.html',
51:'https://www.getty.edu/cona/CONAIconographyRecord.aspx?iconid=901001704',
52:'https://www.theoi.com/Daimon/Tykhe.html',
53:'https://www.collezionegalleriaborghese.it/en/opere/relief-of-remus-and-romulus',
54:'https://www.collezionegalleriaborghese.it/en/opere/relief-of-remus-and-romulus',
55:'https://classics.mit.edu/Virgil/aeneid.8.viii.html',
61:'https://historiska.se/en/explore-history/history-hub/odin-leader-of-the-gods/',
62:'https://www.etymonline.com/word/Valkyrie',
63:'https://www.historiskmuseum.no/english/exhibitions/midgardr/index.html',
64:'https://www.historiskmuseum.no/english/exhibitions/midgardr/index.html',
65:'https://en.wikipedia.org/wiki/Loki',
66:'https://myndir.uvic.ca/Nks1867-098v.html',
67:'https://historiska.se/en/explore-history/history-hub/odin-leader-of-the-gods/',
68:'https://historiska.se/en/explore-history/history-hub/freyja-goddess-of-fertility-and-war/',
70:'https://www.metmuseum.org/art/collection/search/545969',
72:'https://www.ucl.ac.uk/museums-static/digitalegypt/religion/deitiesplaces.html',
73:'https://fitzmuseum.cam.ac.uk/explore-our-collection/highlights/E221955',
74:'https://fitzmuseum.cam.ac.uk/learn-with-us/look-think-do/the-scarab-beetle',
85:'https://www.english-heritage.org.uk/members-area/kids/kids-myths-legends/kids-king-arthur/',
86:'https://d.lib.rochester.edu/camelot/text/frequently-asked-questions.html',
87:'https://www.coreknowledge.org/wp-content/uploads/2017/02/CKHG-G4-U3-FE4-Guinivere-and-the-Round-Table.pdf',
88:'https://visitsherwood.co.uk/about-robin-hood/',
89:'https://visitsherwood.co.uk/about-robin-hood/',
90:'https://read.gov/aesop/091.html',
91:'https://jameelcentre.ashmolean.org/collection/921/object/12708',
92:'https://idp.bl.uk/discover/learning/chinese-astronomy/articles/astrology-and-myth/chang-e-or-the-archer-and-the-moon-goddess/',
93:'https://idp.bl.uk/discover/learning/chinese-astronomy/articles/astrology-and-myth/chang-e-or-the-archer-and-the-moon-goddess/',
94:'https://morikami.org/online-exhibitions/masquerade/',
95:'https://morikami.org/online-exhibitions/masquerade/',
98:'https://ces.ufl.edu/wp-content/uploads/sites/416/Baba-Yaga-informational-material-1.pdf',
99:'https://www.nma.gov.au/about/media/media-releases-listing-by-year/2023/adam-duncan-bunyip-stars-book',
100:'https://www.metmuseum.org/de/perspectives/seven-necessary-dragons',
}
for n in range(36,45):refs[n]='https://guides.uflib.ufl.edu/classics/godsandgoddesses'
for n,url in refs.items():q[n-1]['sourceURL']=url
p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Resolved references for inspection; candidates remain unapproved.')
