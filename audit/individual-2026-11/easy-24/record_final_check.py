"""Individual author editorial decisions, never independent review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
2:{'answers':['A direct public vote on a particular question','A vote held only by cabinet ministers','A court ruling on a disputed law','A private vote to elect a party leader']},
3:{'answers':["Recording a voter's choice",'Listing the policies of every party','Showing the final result of the count','Recording a candidate\'s campaign expenses']},
4:{'answers':['A polling station','A constituency surgery','A cabinet meeting','A party selection meeting']},
5:{'answers':['Its policies and plans if elected','The final vote count in every constituency','A confidential record of cabinet discussions','A list of all eligible voters']},
6:{'answers':['The person currently holding a particular office','The person selected to count votes','The candidate who finished second last time','The person reporting election news']},
8:{'prompt':'In a parliamentary system, which is a key role of the opposition?','answers':['Challenging and scrutinising the government','Implementing the government\'s entire programme','Acting as the country\'s highest court','Appointing every civil servant']},
9:{'answers':['A group of senior ministers','All the judges in the highest court','All the registered voters in one district','A group of foreign ambassadors']},
10:{'answers':['An area whose voters elect a representative','A government\'s annual spending plan','A formal agreement between countries','A list of proposed changes to a bill']},
11:{'answers':['Someone seeking election to office','The official supervising the count','A voter who has already voted','A reporter announcing the result']},
12:{'answers':['Seeking their support or opinions','Counting completed ballot papers','Drawing constituency boundaries','Swearing elected members into office']},
13:{'answers':['As voters leave the polling station after voting','Before the names of the candidates are announced','Only after the final official count is complete','Before a voter has cast a ballot']},
14:{'answers':['The views of a sample of people','The official final count of every vote','The exact outcome of every future election','Only the membership of the cabinet']},
15:{'answers':['Cooperation between two political parties','A government formed without political parties','Cooperation restricted to one party\'s members','The merger of two courts']},
16:{'answers':['A parliament in which no party has an overall majority','A parliament in which every seat is vacant','A parliament with a single chamber','A parliament in which one party holds every seat']},
18:{'sourceURL':'https://www.parliament.uk/site-information/glossary/devolution/','answers':['Transferring powers from central government to governments in parts of the country','Transferring powers from regional governments back to the centre','Transferring ownership of public businesses to private investors','Merging several countries into one state']},
19:{'sourceURL':'https://www.archives.gov/legislative/resources/education/federalism','answers':['Power is divided between a national government and constituent states or regions','All governing powers belong exclusively to local councils','All decisions must be made by direct referendum','The national government has no authority of its own']},
22:{'answers':['Making laws','Conducting foreign diplomacy','Commanding military operations','Hearing appeals against criminal convictions']},
23:{'answers':['Puts laws and government policy into effect','Hears court cases and gives judgments','Acts as a chamber for debating proposed laws','Runs only the opposition\'s election campaign']},
24:{'answers':['The judges and courts of a legal system','The senior ministers in the cabinet','The elected members of a legislature','The staff of diplomatic missions']},
25:{'answers':['Use an official power to reject or block it','Approve it without changes','Suggest a change while allowing it to proceed','Refer it to an opinion poll for advice']},
26:{'sourceURL':'https://www.senate.gov/about/powers-procedures/impeachment.htm'},
27:{'answers':['The period for which someone holds a public position','The area represented by an elected member','The number of votes needed to win a seat','The amount a candidate spends campaigning']},
28:{'answers':['The meeting is suspended or ended until another time','Every member permanently loses their seat','The parliament is dissolved for a general election','A proposal automatically becomes law']},
29:{'answers':['A break when parliament is not sitting','The permanent end of a parliament before an election','A formal vote on a disputed motion','A meeting of the governing cabinet']},
30:{'answers':['The minimum number of members required for valid business','The number of votes a proposal receives','The maximum number of speeches in a debate','The total number of seats held by the largest party']},
31:{'answers':['A change to its wording or provisions','The final official count of an election','A diplomatic agreement with another state','A list of people entitled to vote']},
32:{'answers':['A proposal for a new law','A formal agreement between countries','A decision reached by a judge','A party\'s list of election promises']},
33:{'answers':['A formal request, often supported by signatures','A record of the final votes in an election','A list of government ministers','A formal agreement between states']},
34:{'answers':['Trying to influence public decisions or decision-makers','Supervising the official count at an election','Delivering a court judgment','Appointing diplomatic staff']},
35:{'answers':['Influence policy on an issue or set of interests','Count ballots as the official election authority','Hear appeals as the highest court','Act as the government\'s permanent administration']},
36:{'answers':['Ordinary people at the local or community level','Only the national cabinet','Only senior judges','Only career diplomats overseas']},
37:{'answers':["Helping organise party members' attendance and voting",'Chairing the legislature impartially','Overseeing the national election count','Judging whether an accused official is guilty']},
38:{'sourceURL':'https://www.parliament.uk/about/mps-and-lords/members/partysystem/'},
39:{'sourceURL':'https://www.parliament.uk/site-information/glossary/crossbench-peers/','answers':['An independent peer outside the party groups','A minister who represents all political parties','An elected member of the House of Commons','The official responsible for counting general-election votes']},
40:{'answers':['Chairing proceedings and maintaining order','Writing the governing party\'s election manifesto','Counting votes at every public election','Leading negotiations with foreign governments']},
41:{'sourceURL':'https://www.parliament.uk/site-information/glossary/divisions/'},
44:{'answers':["Parties' shares of the vote",'The length of time each party has existed','The total number of party members','The amount each party spends on posters']},
45:{'answers':['The candidate with the most votes','The candidate with the most first-time voters only','The candidate selected by the previous representative','The candidate whose party wins nationally, regardless of the local count']},
46:{'answers':['A further round of voting to decide a winner','A recount of exactly the same ballot papers','An opinion poll before candidates are selected','A ceremony marking the start of a presidency']},
47:{'answers':["The party's candidate for an election",'The final winner of the general election automatically','The official who supervises every ballot count','The person who chairs the Supreme Court']},
48:{'answers':['A meeting of party members or supporters to express their preferences','A court hearing to settle a disputed election','An official recount of general-election ballots','A ceremony to swear in the president']},
49:{'answers':['The formal ceremony marking the start of the presidency','The selection of a party\'s election candidate','The official count on election night','The formal announcement of a president\'s retirement']},
50:{'prompt':'In UK politics, what is the dissolution of Parliament?','answers':['The formal end of a Parliament before a general election','A temporary break between parliamentary sittings','A reshuffle of cabinet ministers','A formal vote on a proposed law'],'sourceURL':'https://www.parliament.uk/site-information/glossary/dissolution/'},
51:{'answers':['The person who formally represents a country at the highest constitutional level','The chief organiser of every election campaign','The most senior newspaper editor','The representative of one local ward']},
52:{'prompt':'In the UK, which officeholder leads the government?','answers':['The Prime Minister','The Speaker of the House of Commons','The Leader of the Opposition','The Lord Chief Justice'],'sourceURL':'https://www.gov.uk/government/how-government-works'},
53:{'answers':['A person who is not a monarch','Always a hereditary king','Always a hereditary queen','Always the leader of a religious institution']},
54:{'prompt':"In a constitutional monarchy, what limits the monarch's governing powers?",'answers':['A constitutional framework','The monarch\'s wishes alone','The personal rules of a royal servant','The views of one private company'],'sourceURL':'https://www.royal.uk/the-role-of-the-monarchy'},
55:{'prompt':'What characterises political absolutism?','answers':['A ruler or ruling group holds complete governing power','The national government has no authority','Every policy is decided by direct public vote','Political authority is divided equally among all citizens'],'sourceURL':'https://dictionary.cambridge.org/dictionary/english/absolutism'},
57:{'answers':['Citizens vote on policies or laws themselves','Citizens choose representatives to decide every policy for them','Citizens have no voting rights','Only the cabinet is allowed to vote']},
58:{'answers':['Electing people to make decisions on their behalf','Voting directly on every government decision','Allowing a monarch to appoint every representative','Letting judges choose all legislative members']},
59:{'answers':['A system concentrating power in a ruler or small ruling group','A system requiring every citizen to agree to each decision','A system with no governing authority','A system that distributes power equally to all citizens']},
61:{'answers':['Government or control by a small powerful group','Government through direct voting by the entire population','Government with no officials or institutions','Government controlled by every citizen equally']},
62:{'answers':['Religious authority','Independent sporting bodies','Only commercial stock exchanges','Only public opinion surveys']},
63:{'answers':['Rule or dominant political influence by the wealthy','Rule based only on military rank','Rule based only on religious office','Rule by citizens selected at random']},
64:{'answers':['Managing relations between states through negotiation and communication','Drawing boundaries between local electoral wards','Counting ballots in a domestic election','Passing judgment in a domestic criminal case']},
65:{'answers':['A senior diplomatic representative of a state','A tourist automatically granted political office','A candidate seeking election in every district','A judge who hears all international disputes']},
67:{'answers':['A formal agreement between states','An unofficial television opinion','A single voter\'s choice on a ballot','A political party\'s internal campaign leaflet']},
68:{'answers':['A halt in fighting','A compulsory merger of the states involved','An automatic change of national leadership','A final settlement of every disputed issue']},
69:{'answers':['Put pressure on a state or other target to change its behaviour','Guarantee unrestricted trade with the target','Recognise the target as a new sovereign state automatically','Give the target a seat in every international organisation']},
70:{'answers':['Supreme authority over a state or territory','The popularity of one governing party','The number of seats in a parliament','The size of a diplomatic delegation']},
73:{'answers':["Matters directly affecting people within a country",'Only relations with foreign governments','Only the work of embassies overseas','Only treaties between military allies']},
74:{'answers':['Other countries and international affairs','Only the organisation of local refuse collection','Only the management of domestic school admissions','Only the opening hours of local libraries']},
75:{'answers':['Taxation and public spending','Interest rates and money supply alone','The drawing of electoral boundaries','The appointment of ambassadors']},
76:{'answers':['Money supply and the cost of borrowing','Only the boundaries of constituencies','Only the selection of election candidates','Only the appointment of cabinet ministers']},
77:{'answers':['A plan for public income and spending','A list of all election candidates','A record of treaties with other countries','A map of local government areas']},
80:{'answers':['Organisations owned or controlled by government','Only privately owned businesses','Only foreign political parties','Only independent family firms']},
81:{'answers':['Bringing an industry or business into public ownership','Selling a state-owned business to private owners','Moving powers from national to regional government','Changing the citizenship rules for workers']},
82:{'answers':['Transferring a state-owned business into private ownership','Bringing a private company into state ownership','Moving authority from regional to central government','Extending voting rights to more people']},
83:{'answers':["Public provision to support people's health and social well-being",'A requirement that every public service be privately funded','A government with no social services','A system concerned only with military spending']},
84:{'answers':['The civilian administrative departments and staff of government','All candidates competing in an election','Only members of the armed forces','Only the elected cabinet ministers']},
85:{'answers':['Complaints about organisations or public administration','The results of every public opinion poll','The military strategy of every country','The selection of every election candidate']},
86:{'answers':['Someone authorised to act for or assist a more senior official','Someone automatically entitled to inherit a throne','Someone who has retired permanently from public office','Someone who can never exercise official authority']},
87:{'answers':['A town or city','An entire continent','The United Nations as a whole','Every country sharing a language']},
88:{'answers':['A local council','The national cabinet automatically','The highest court automatically','A diplomatic mission abroad']},
89:{'answers':['An electoral area within a local authority','An overseas diplomatic mission','A national political party\'s manifesto','A formal agreement between states']},
90:{'answers':['Relating to a town or city and its local administration','Relating only to international treaties','Relating only to royal succession','Relating only to military command']},
91:{'answers':['The people entitled to vote in an election','Only the candidates seeking office','Only the people who count ballots','Only the people who actually voted']},
92:{'answers':['The number or proportion of eligible or registered voters who actually vote','The proportion of seats won by the largest party','The amount spent by the winning candidate','The number of candidates standing for election']},
95:{'prompt':'At an English local election count, what happens to a ballot paper judged invalid?','answers':['It is rejected rather than counted for a candidate','It is automatically given to the leading candidate','It is counted twice to compensate for the error','It is counted for every candidate equally'],'sourceURL':'https://www.electoralcommission.org.uk/guidance-returning-officers-administering-local-government-elections-england/verification-and-count/count/doubtful-ballot-papers'},
96:{'sourceURL':'https://www.un.org/en/about-us/universal-declaration-of-human-rights'},
99:{'answers':['Authority voters give elected representatives to pursue their programme','A guarantee that every future election is cancelled','An automatic exemption from every law','A permanent hereditary title']},
100:{'answers':['An organised group seeking political power to pursue shared policies','An impartial body that administers election counts','A court hearing disputes about an election','A permanent department that implements government policy']},
}
notes='''1|Suffrage is voting right. Tax powers, military service and currency issue not synonyms. Election scope explicit, ordinary British wording correct; actual dictionary suffrage definition inspected.
2|Referendum direct public question vote, not cabinet-only vote, judicial ruling or internal party leadership ballot. Improve distractors to real civic procedures. No claim all referendums are legally binding.
3|Ballot-paper sense records voter's choice. Policy document, final results and expense return different documents. Read paper sense rather than investment-share allotment sense; apostrophe voter's correct.
4|Polling station is in-person voting place. Constituency surgery,cabinet,selection meeting not election-day voting site. No claim postal/proxy voters must attend; wording explicitly in person.
5|Manifesto sets policies/plans. Vote counts,confidential minutes,electoral roll different records. Usually permits parties publishing other material; possessive party's correct.
6|Incumbent currently holds office. Vote counter,previous runner-up,reporter not definition. Relevant elected-position sense checked among duty/business meanings. Does not mean automatically seeking re-election.
7|Coalition joins parties in governing. No-minister,banned-election,courts-only alternatives wrong. Two or more permits more than two and does not confuse minority single-party administration with coalition.
8|Opposition scrutiny/challenge is a key role. It does not implement government's entire programme,act as judiciary or appoint all civil servants. Key role replaces main to avoid oversimplifying multiple legitimate functions.
9|Cabinet senior ministers, not judiciary,electorate or foreign diplomatic corps. Political noun sense rather than furniture. Size and membership vary, so no universal number specified.
10|Constituency area electing representative. Budget,treaty,amendment list not geographic electoral units. Read area sense as well as voter/group meanings; question in an election supplies context.
11|Candidate seeks election. Supervisor,voter,reporter different roles; a candidate may also vote but a voter merely having voted does not define candidacy. Remove only-retired-judge distractor.
12|Canvassing seeks support/opinions. Counting votes,boundary setting,swearing-in different acts. Dictionary supports support and survey senses; not canvas fabric spelling.
13|Exit poll asks after vote as voters leave. Before ballot or candidate announcement wrong; only-after-final-count not exit polling. Change after voters leave to as they leave for precise timing.
14|Opinion poll samples views. It is not official complete count,certainty about future or cabinet membership. No claim sample is invariably representative or prediction accurate.
15|Bipartisan means two parties/both sides. No-party government,one-party-only cooperation,court merger not meaning. Does not require parties to merge or govern together.
16|Hung parliament means no single-party overall majority, not empty seats,one chamber or one party owning every seat. Parliamentary rather than furniture meaning; remove sitting-outdoors joke option.
17|UK by-election fills vacancy between generals. Monarch and Supreme Court judges not elected this way; all-MP election is general. Normally qualifies uncontested/administrative edge cases without changing central meaning.
18|UK devolution transfers powers away from centre to territorial institutions; reverse centralisation,privatisation,state merger distinct. Parliament glossary consulted because generic dictionary central-to-local wording too broad for precise UK devolved governments.
19|Federalism shares/divides authority among national and constituent levels. Only-local,no-national-authority and obligatory direct referendum not definitions. National Archives school lesson explicitly defines divided responsibilities; supersedes oversimplified dictionary first definition.
20|Bicameral means two chambers. Two PMs,two yearly sittings,two voters unrelated counts. Parliament/congress scope explicit; not requirement that chambers have equal power.
21|Unicameral one chamber;two/three/four wrong. Dictionary says only one group of members. No conflation with one-party government.
22|Legislature chiefly makes laws. Diplomacy,military command,criminal appeals are other functions. Main function qualifier accommodates oversight/tax approval and constitutional variations; replace retail/weather distractors.
23|Executive puts laws/policy into effect. Judicial judgments,legislative debating chamber,opposition campaign are different. Actual government noun sense inspected among corporate executive definitions.
24|Judiciary judges/courts, not cabinet,legislature,diplomatic staff. Dictionary explicitly legal-system branch. Replace sports-team distractor; no assertion judges can never have any other public roles.
25|Veto official block/rejection, not approval,merely proposing amendment or advisory poll. Does not claim every veto is permanent or cannot be overridden; official power qualification important.
26|US House impeachment accusation differs from conviction/removal. Senate official account explicitly separates charges from trial/conviction. General election and heredity wrong; federal scope excludes differing state procedures.
27|Term period holding public office, not district,vote threshold or campaign cost. Relevant job/government period sense inspected among school/pregnancy/mathematical definitions; no universal fixed duration claimed.
28|Adjourn pauses/temporarily ends meeting. Members losing seats,dissolution,automatic lawmaking not it. Until another time preserves temporary nature; distinguishes dissolution and recess.
29|Recess break in sitting, not end of Parliament,vote or cabinet meeting. Parliamentary noun sense checked, not school break/alcove. No claim members stop all constituency/committee work.
30|Quorum minimum required participants for valid business. Vote outcome,speech cap,largest-party seat count not meaning. No arbitrary universal numeric quorum invented.
31|Amendment change to proposed text/provisions. Count,treaty,electorate list not it. Proposed-law qualifier narrows legal meaning; relevant draft-law dictionary sense checked.
32|Bill proposed law, not treaty,judicial decision or manifesto. Legislative context excludes banknote,bird's bill,invoice and programme billing. More plausible civic distractors added.
33|Petition formal request often signed. Election result,minister list,treaty not it. Often allows parliamentary petitions presented through representative and other lawful forms; avoids arbitrary minimum signatures.
34|Lobbying seeks to influence decisions. Count supervision,judicial judgment,diplomatic appointments not definition. No suggestion lobbying necessarily illegal or always involves money.
35|Pressure group aims to influence policy/interests, unlike election authority,court,civil service. Usually accommodates different tactics; not claimed every pressure group becomes electoral party.
36|Grassroots ordinary people/community, not exclusivelycabinet/judges/diplomats. Relevant people sense inspected. A politician may participate but top-down official control is not defining source.
37|Whip organises member attendance/party voting. Speaker,election counter,trial judge distinct. Actual political whip sense checked, not leather tool/food/car. One role qualifier allows welfare/communication duties.
38|Backbench MP lacks ministerial or opposition frontbench spokesperson role. Judge,party head,ambassador not meaning. Parliament party-system text directly inspected to refine dictionary broad no-official-position formulation.
39|Crossbencher non-party peer outside party groups. Multi-party minister,Commons MP,election counter wrong. Cambridge guessed crossbencher entry had no definition; replace with Parliament explicit Crossbench Peers description. Do not assert every unwhipped peer is automatically a Crossbencher.
40|Speaker chairs debate/maintains order. Party-manifesto author,public election counter,diplomatic negotiator not defining job. Parliamentary sense checked beyond loudspeaker/orator; no claim all countries choose Speakers identically.
41|Division formal parliamentary vote. Poster,royal wedding,court sentence not it. Cambridge entry did not cover parliamentary division; Parliament glossary explicitly describes counting for/against through lobbies.
42|Filibuster delays/obstructs legislative business with speeches/rules. Automatic speed-through,candidate lottery,voter replacement wrong. Dictionary includes tactics as well as prolonged speeches; not overrestricted to one country.
43|Gerrymandering manipulates electoral boundaries for advantage. Alphabetical counting,weekend voting,same ballot paper not it. No partisan accusation or current boundary opinion included.
44|PR seats broadly reflect vote shares, not party age,membership or advertising. Broadly accommodates thresholds/rounding/formula differences. No claim perfect exact proportionality in every implementation.
45|FPTP most votes in single-member seat. Not only first-time voters,named predecessor's pick or national winner regardless of local votes. Does not require more than half; specify local constituency to distinguish national totals.
46|Runoff further voting round, not recount of same ballots,preselection survey,inauguration. Relevant electoral sense checked beyond water runoff. No single worldwide qualification threshold imposed.
47|Primary helps choose party nominee, not automatically general-election winner,count supervisor or chief justice. Helps accommodates delegate/convention processes; relevant US political noun sense inspected beyond school/first/main.
48|Caucus candidate-selection meeting of party supporters,membership rules vary. Court,count,inauguration not it. Typically avoids claiming every caucus means only election meeting; legislative caucuses also exist.
49|Inauguration formal start ceremony, not nomination,count or retirement announcement. No claim inauguration alone is legal source of term start in all constitutions. President possessive correct.
50|UK dissolution formal Parliament end before general election. Temporary break,reshuffle,bill vote distinct. Jurisdiction narrowed and Parliament glossary used; avoid confusing prorogation/session end with entire Parliament end.
51|Head of state formal highest representative;campaign organiser,editor,ward representative not definition. It can be monarch or president and executive or ceremonial, so no claim always powerless.
52|Guessed head-of-government dictionary entry lacked definition. Replace with concrete UK office: PM leads government. Speaker,opposition leader,Lord Chief Justice different roles. GOV.UK institutional description inspected; no current personal name used.
53|Republic's head of state not monarch. Hereditary king/queen and always religious leader wrong. Remove hereditary-only wording from correct choice because elective monarchies remain monarchies; generally allows complex historical terminology without claiming every republic democratic.
54|Constitutional framework limits monarch's powers. Monarch's wishes alone/private servant/company not source of constitutional restrictions. Royal official explanation specifies Parliament's legislative role; do not assert every constitution must be one codified written document.
55|Absolute-monarchy guessed page only examples,no definition. Replace with political absolutism, dedicated Cambridge entry explicitly complete power by ruler/group/party. No-authority,direct-every-policy,equal citizen authority opposite concepts; do not confuse absolute with merely hereditary.
56|Democratic authority meant to originate with people. Exclusivelydynasty,foreign ambassadors or corporation not principle. Ultimately meant to allows imperfect actual practice and avoids assessing disputed present-day regimes.
57|Direct democracy citizens decide policies/laws directly. Representation-only,no-voting,cabinet-only not defining. Different from58's representative route; no claim systems cannot combine both forms.
58|Representative democracy elects decision-makers. Every direct decision,monarch appointment,judge appointment alternatives not electoral representation. Normally accommodates referendums alongside representative institutions.
59|Cambridge autocracy allows ruler or small group, so expand original one-ruler-only answer. Unanimous-all,equal-power-all,no-government not meaning. Avoid confusing narrow common singular-ruler usage with universal claim.
60|Dictatorship authoritarian concentrated power. Guaranteed open competition,no enforcing authority,mandatoryjury-for-all-laws not characteristics. Typically recognises varying institutional forms; no present country labelled.
61|Oligarchy small powerful group. Whole-population direct rule,no institutions,equalallcitizens not definition. All options inspected; remove random child comic distractor.
62|Theocracy links political and religious authority. Sports bodies,stock exchange only,polls only wrong. Dictionary religious-leader rule checked; no assertion every religious country is theocracy.
63|Plutocracy wealthy dominance, not militaryrank/religiousoffice/randomcitizens as defining selection. Dominant influence permits informal as well as formal rule; no current political insinuation.
64|Diplomacy manages interstate relations via communication/negotiation. Local boundaries,domestic counts,courtjudgments different. International relations scope excludes personal tact sense.
65|Ambassador senior diplomatic representative. Not automaticroyalstatus,candidate in everydistrict or all-disputejudge. Broaden answer beyond only another-country posting to allow ambassadors to international organisations.
66|Embassy diplomatic mission/building. Not all-domestic court,new sovereign country or party office. Mission or premises wording reflects both dictionary senses; embassy land not magically separate sovereign state.
67|Treaty formal interstate agreement. Presenter opinion,individual ballot,internalleaflet not treaty. Simplify specialist subjects-of-international-law wording to states without claiming treaties can never involve international organisations.
68|Armistice halt in fighting, not automaticmerger,leadershipchange or finalsettlementallissues. Dictionary explicitly temporary halt and possible peace talks. Distinguish armistice from permanent peace treaty.
69|Sanctions pressure behaviour. Not necessarilyunrestrictedtrade,newstate recognition or universalseats. Relevant international punitive meaning inspected; sanction can mean approval in other contexts, hence international sanctions scope.
70|Sovereignty supreme governing authority. Party popularity,seatcount,delegationsize not it. Supreme authority wording within politics, not a claim no international obligations can exist.
71|Multilateral more than two participants, not one/two/none. Dictionary explicit more than two. Parties means participating states/entities, not necessarily political parties.
72|Bilateral two parties, not three/four/ten. Same international-agreement meaning distinct from multilateral. No claim parties must be countries rather than organisations.
73|Domestic policy matters directly affecting people within country. Foreigngovernments-only,embassies-only,militarytreaties-only wrong. Direct-effects wording more faithful than rigid border claim; domestic policy may have external effects too.
74|Foreign policy dealings with other states/international affairs. Onlylocalrefuse,domesticschooladmissions,libraryhours not definition. Scope avoids saying trade/defence are the only elements.
75|Fiscal taxation/publicspending, not money-supply/interestrates alone,electoral maps,ambassadors. Dictionary fiscalplan checked. Government borrowing also fiscal but answer lists maintools, not exhaustivealltools.
76|Monetary policy money supply/costofborrowing. Constituencies,candidates,cabinetappointment not it. Does not claim politicians personally set rates everywhere; neutral financial-policy concept fits Politics.
77|Government budget income/spending plan. Candidate list,treaty register,wardmap different. Relevant financial/UKgovernment senses inspected, not low-price adjective or time budget.
78|Deficit spending exceeds revenue. Opposite surplus,equalbalanced,nothingcollectedorspent wrong. Government budget context excludes trade/current-account deficits; not confused with total debt.
79|Surplus revenue exceeds spending, unlike deficit/equality/abolitionofalltax. Budgetfinancial sense checked. No assertion surplus means government has no existing debt.
80|Public sector government owned/controlled organisations. Privatelyownedbusinesses,foreignparties,independentfamilyfirms not defining. No claim every publicly accessible shop is public sector.
81|Nationalisation moves industry into public ownership. Oppositeprivatisation,devolution,citizenshiprulechange different. British spelling nationalisation retained though dictionary URLAmerican nationalization.
82|Privatisation moves state-owned business to private ownership. Oppositenationalisation,centralisation,votingexpansion not it. British spelling; no claim every privatisation must transfer100percentatonce.
83|Welfare state public health/socialprovision. No-public-services,private-onlyfunding,military-only not principle. Does not promise everyone receives identical benefits or free services in every system.
84|Civil service civilian administrative staff/departments. Candidates,military-only,electedcabinet-only not it. Revise permanent-only wording because fixed-term civilian staff exist; relevant administrative senses checked.
85|Ombudsman investigates complaints about organisations/administration. Pollresults,globalmilitarystrategy,allcandidate selection not job. Generally allows public/private schemes; no binding powers claimed universally.
86|Deputy acts for or assists seniorofficial. Hereditaryentitlement,permanentretirement,noauthority not meaning. Broaden act-in-place-only wording to include assisting while principal present.
87|Mayor town/city office, not continent/UN/alllanguagecountries. Closelyassociated accommodates differing local titles and ceremonial/executive roles. No universal elected-vs-appointed assertion.
88|Councillor on local council. Not automatic nationalcabinet,court or diplomaticmission. Electedlocal qualifier avoids other historical councillor titles; double-l British spelling correct.
89|Electoral ward localauthority area. Embassy,manifesto,treaty not it. Local-election sense inspected among hospital/prison/guardianship meanings; no claim every country uses wards.
90|Municipal town/city administration. Foreign treaties,royalsuccession,military-only not definition. Dictionary municipal government sense checked, not municipal-bond investment question.
91|Electorate entitled voters, not candidates,counters or onlythosewhovoted. Clear distinction from turnout. Read all allowed-to-vote definition; no particular voter-eligibility rule invented.
92|Turnout number or proportion actually voting among eligible/registered population. Seatshare,campaignspend,candidatecount different. Denominators differ by reporting system, so expressly allow eligible or registered; does not count every eligible non-voter.
93|Abstention decliningfor/against, not doublevote,veto or chairappointment. Formalvote context excludes abstaining from alcohol/work. No claim every jurisdiction formally records abstentions identically.
94|Secret ballot protects choice privacy. Date/candidate-name secrecy and preventingcounting wrong. Secretvote sense clear; not claim officials cannot know who attendedpollingstation.
95|Spoiled-ballot guessed entry lacked definition; replace with official invalidballot handling in English local elections. Rejected vote not allocatedleader,twicecounted,equallyallocated. Electoral Commission actual rejection criteria inspected; no claim every unusual mark invalid.
96|Universal adult suffrage principle adultcitizensvote rather than landowners/graduates/partyonly. Generaleligibilityrules allows age/residence/other lawfulconditions. UNArticle21 universal/equalsuffrage inspected; conceptual principle, not advice about any person's eligibility.
97|Absolute majority more than half of relevant total. Quarter,pluralitylessthanhalf,oddnumber wrong. Absolute qualifier distinguishes British election majority-as-winningmargin sense in dictionary.
98|Unanimous allparticipantsagree, not chaironly,exacthalf or nodecision. Relevant groupdecision definition checked. Takingpart avoids saying absentpersons must agree too.
99|Electoral mandate authority from voters for programme. Not legalexemption,cancelfutureelections,hereditarytitle. Generallyunderstood avoids suggesting every pledge has a legallybinding mandate; relevant electionauthority sense, not bank instruction/UNmandate.
100|Political party organised sharedpolicy/power group. Impartialelectionauthority,court,permanentadministration other institutions. Organisation's political nature explicit, not holidayparty. No claim every party necessarily wins or contests every available election.
'''
out=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 # Replace placeholder rationale with the actual item-specific final judgment.
 edits.setdefault(n,{})['rationale']=note
 out.append({'row':n,'prompt':draft[n-1]['prompt'],'action':'edit','note':note,'recommendedChanges':edits[n],'sourceReview':'Author second editorial pass of this item and all four choices: meaning, sole correct answer, grammar and Politics relevance checked against the applicable dictionary sense or the specified parliamentary/government/electoral reference. Not independent review.'})
assert [x['row'] for x in out]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,'sourceAccessNote':'100 individually considered items. Placeholder rationales replaced with actual per-item decisions, civic distractors improved, parliamentary references substituted where dictionary senses were missing or too broad. Impeachment distinguished from removal; absolute majority from plurality; federalism checked with National Archives; missing head-of-government/absolute-monarchy/spoiled-ballot entries replaced with verified concrete questions. Private extracts remain private; indexed or web inspection distinguished from direct retrieval.','rows':out},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 individual author second-pass judgments; all rationales recorded, substantive edits noted')
