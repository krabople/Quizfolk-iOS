"""Accessible original civics candidates; unapproved until individual final check."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
rows='''1|suffrage|In politics, what does suffrage mean?|The right to vote|The power to collect taxes|The duty to serve in the army|The right to issue currency
2|referendum|What is a referendum?|A direct public vote on a particular question|A private meeting of judges|An appointment made by a monarch|An annual list of tax rates
3|ballot|What is a ballot paper used for in an election?|Recording a voter's choice|Setting the national budget|Appointing judges automatically|Publishing a party's accounts
4|polling-station|Where do voters go to cast their votes in person on election day?|A polling station|An embassy reception|A court hearing|A cabinet meeting
5|manifesto|What does a political party's election manifesto usually set out?|Its policies and plans if elected|The personal diary of every candidate|The final vote count|The names of every voter
6|incumbent|What is an incumbent politician?|The person currently holding a particular office|A candidate who has never held office|A journalist reporting on elections|A person counting votes
7|coalition|What is a coalition government?|A government formed by two or more political parties working together|A government with no ministers|A government that bans all elections|A government led by the courts alone
8|opposition|In a parliamentary system, what is the main role of the opposition?|Challenging and scrutinising the government|Commanding every court|Counting all votes personally|Replacing the civil service with journalists
9|cabinet|In government, what is a cabinet?|A group of senior ministers|A committee of all registered voters|A panel of election observers only|A group of foreign ambassadors
10|constituency|In an election, what is a constituency?|An area whose voters elect a representative|A government's annual spending plan|A list of treaties|A judge's written verdict
11|candidate|In an election, who is a candidate?|Someone seeking election to office|Only the person who counts the votes|Every person watching the result|Only a retired judge
12|canvass|What are campaigners doing when they canvass voters?|Seeking their support or opinions|Changing the legal voting age themselves|Issuing passports|Swearing in judges
13|exit-poll|When is an exit poll conducted?|After voters leave the polling station|Only before candidates are selected|Only after a government has served a full term|During a court's private deliberations
14|opinion-poll|What does an opinion poll try to measure?|The views of a sample of people|The exact future with certainty|Only the number of parliament buildings|The legal wording of every new law
15|bipartisan|What does bipartisan cooperation involve?|Cooperation between two political parties|A ban on political parties|Only cooperation between two courts|The rule of a single hereditary family
16|hung-parliament|What is a hung parliament?|A parliament in which no party has an overall majority|A parliament with no elected members|A parliament that meets only outdoors|A parliament ruled by one judge
17|by-election|What is a UK parliamentary by-election normally held to do?|Fill a seat that becomes vacant between general elections|Elect the monarch|Choose every MP at once|Appoint all Supreme Court judges
18|devolution|In UK politics, what does devolution involve?|Transferring powers from central government to governments in parts of the country|Replacing all laws with opinion polls|Handing every government power to a private company|Abolishing every elected assembly
19|federalism|What is a central feature of federalism?|Power is divided between a national government and constituent states or regions|All powers belong to foreign embassies|Every law is decided by a private company|Local and national government are forbidden
20|bicameral|What does it mean if a legislature is bicameral?|It has two chambers|It has two prime ministers|It sits only twice a year|It represents only two voters
21|unicameral|How many chambers does a unicameral legislature have?|One|Two|Three|Four
22|legislature|What is the main function of a legislature?|Making laws|Forecasting the weather|Printing all newspapers|Running every private shop
23|executive|In government, what does the executive branch mainly do?|Puts laws and government policy into effect|Acts as every country's highest court|Writes every newspaper headline|Replaces all elections with sporting events
24|judiciary|What does the term judiciary refer to?|The judges and courts of a legal system|The members of a country's sports teams|The staff of every embassy only|The candidates in one election
25|veto|What does it mean to veto a proposed measure?|Use an official power to reject or block it|Publish it as an opinion poll|Approve it unanimously|Automatically rewrite it as a treaty
26|impeachment|In US politics, impeachment of a federal official is what?|A formal accusation of wrongdoing by the House of Representatives|Automatic removal from office without any further process|An ordinary general election|A grant of hereditary office
27|term|What is a term of office?|The period for which someone holds a public position|A country's total land area|The size of an election poster|A government's collection of flags
28|adjourn|What does it mean when a parliamentary meeting is adjourned?|The meeting is suspended or ended until another time|Every member is permanently removed|All existing laws are cancelled|A new country is created
29|recess|What is a parliamentary recess?|A break when parliament is not sitting|A vote to declare war|A permanent ban on elections|The title of the head of state
30|quorum|What is a quorum at a formal meeting?|The minimum number of members required for valid business|The number of pages in the minutes|The highest possible tax rate|The name of the winning candidate
31|amendment|What is an amendment to a proposed law?|A change to its wording or provisions|A list of every voter|An ambassador's official residence|A new national flag
32|bill|In a legislature, what is a bill?|A proposal for a new law|A judge's retirement party|A list of diplomatic guests|A military rank
33|petition|What is a petition in public life?|A formal request, often supported by signatures|A secret code used to count money|A compulsory military order|A hereditary title
34|lobbying|What does political lobbying involve?|Trying to influence public decisions or decision-makers|Automatically replacing elected representatives|Counting only postal votes|Publishing weather forecasts for parliament
35|pressure-group|What does a pressure group usually try to do?|Influence policy on an issue or set of interests|Form a hereditary royal dynasty|Run every national election itself|Issue its own court sentences
36|grass-roots|A grassroots political movement mainly develops from which level?|Ordinary people at the local or community level|Only foreign monarchs|Only the highest-ranking judges|Only professional diplomats abroad
37|whip|In parliamentary politics, what is one role of a party whip?|Helping organise party members' attendance and voting|Presiding over every criminal trial|Managing the national weather service|Choosing the monarch's successor
38|backbencher|In UK politics, what is a backbencher?|An MP who is not a minister or an opposition frontbench spokesperson|The most senior judge|The head of every political party|An ambassador serving overseas
39|crossbencher|In the UK House of Lords, a Crossbencher is best described as what?|A member who does not take a party whip|A member representing every party at once|An elected mayor|The official who counts every general-election vote
40|speaker|What is a parliamentary Speaker primarily responsible for during debates?|Chairing proceedings and maintaining order|Writing every speech for every member|Personally deciding every court appeal|Commanding the armed forces during every debate
41|division|In the UK Parliament, what is a division?|A formal vote|A party's election poster|A royal wedding|A judge's written sentence
42|filibuster|What is a filibuster intended to do?|Delay or obstruct legislative business through prolonged debate or other tactics|Speed every proposal into law automatically|Select candidates by lottery|Replace every voter with a judge
43|gerrymandering|What is gerrymandering?|Manipulating electoral boundaries for political advantage|Counting votes in alphabetical order|Holding elections on a weekend|Giving every voter the same ballot paper
44|proportional-representation|What is proportional representation intended to make seats broadly reflect?|Parties' shares of the vote|Candidates' heights|The age of parliament buildings|The size of campaign posters
45|first-past-the-post|Under first-past-the-post voting in a single-member constituency, who wins the seat?|The candidate with the most votes|The oldest candidate|The candidate with the shortest name|The candidate selected by the previous winner
46|runoff|What is a runoff election?|A further round of voting to decide a winner|A ban on all candidates|A vote held only by the judiciary|A ceremony to appoint ambassadors
47|primary|In US elections, what is a party primary used to help choose?|The party's candidate for an election|The country's national anthem|The legal voting age|The winner of the final general election automatically
48|caucus|In US presidential candidate selection, a caucus is typically what?|A meeting of party members or supporters to express their preferences|A trial conducted by the Supreme Court|A meeting open only to foreign ambassadors|A session that elects a king
49|inauguration|What is a president's inauguration?|The formal ceremony marking the start of the presidency|The announcement of their retirement pension|A routine local council meeting|A private party with no official significance
50|dissolution|In parliamentary politics, dissolution means what?|Ending a parliament so an election can take place|Adding a second chamber automatically|Giving every minister a hereditary title|Replacing the constitution with a manifesto
51|head-of-state|What is a head of state?|The person who formally represents a country at the highest constitutional level|Always the leader of the opposition|Always the most senior newspaper editor|Every elected councillor collectively
52|head-of-government|What is a head of government primarily responsible for?|Leading the work of the government|Leading only the largest opposition party|Managing all foreign newspapers|Personally deciding every court case
53|republic|In a republic, the head of state is generally what?|A person who is not a hereditary monarch|Always a hereditary king|Always a hereditary queen|Always a religious archbishop
54|constitutional-monarchy|In a constitutional monarchy, the monarch's powers are governed by what?|A constitutional framework|The monarch's unlimited personal wishes alone|An annual sports tournament|The private rules of a political club
55|absolute-monarchy|What characterises an absolute monarchy?|The monarch holds supreme governing authority|Every policy must be decided by public referendum|The head of state is always elected for one year|There is no monarch
56|democracy|In a democracy, political authority is ultimately meant to come from whom?|The people|Only one hereditary family|Only foreign ambassadors|Only the wealthiest corporation
57|direct-democracy|What distinguishes direct democracy from representative democracy?|Citizens vote on policies or laws themselves|Citizens never vote on anything|All power belongs to a hereditary ruler|Judges select every citizen's representative in secret
58|representative-democracy|In a representative democracy, citizens normally make political choices by doing what?|Electing people to make decisions on their behalf|Choosing a new hereditary monarch each week|Giving all authority to private banks|Abolishing every elected assembly
59|autocracy|What is an autocracy?|A system in which one ruler holds concentrated power|A system with no political authority of any kind|A system run entirely by competing newspapers|A system in which every decision requires unanimity of all citizens
60|dictatorship|A dictatorship is typically characterised by what?|Power concentrated in an authoritarian ruler or ruling group|Guaranteed open competition for every public office|No authority to enforce any rules|A requirement that every law be approved by a jury
61|oligarchy|What is an oligarchy?|Government or control by a small group|Government by every citizen voting on every decision|Government that has no officials|Government by a randomly selected child
62|theocracy|In a theocracy, political authority is closely tied to what?|Religious authority|The ownership of football clubs|The operation of stock exchanges alone|The results of opinion polls alone
63|plutocracy|What is a plutocracy?|Rule or dominant political influence by the wealthy|Rule by the youngest citizens|Rule by the oldest university|Rule by rotating sports captains
64|diplomacy|What is diplomacy in international relations?|Managing relations between states through negotiation and communication|Only counting domestic election votes|Only drawing local constituency maps|Automatically declaring war after every disagreement
65|ambassador|What is an ambassador?|A senior official representing a state in another country|A person who automatically becomes a foreign monarch|Any tourist entering another country|A candidate for every local council seat
66|embassy|What is an embassy?|A state's diplomatic mission or its premises in another country|A court that hears every domestic criminal trial|A place that automatically becomes a new sovereign country|A private political party's campaign office
67|treaty|What is a treaty?|A formal agreement between states or other subjects of international law|An informal opinion from a television presenter|A single voter's ballot paper|A routine weather warning
68|armistice|What does an armistice agreement provide for?|A halt in fighting|The automatic merger of all armies|The immediate election of a monarch|A compulsory change of every country's name
69|sanction|What are international sanctions generally intended to do?|Put pressure on a state or other target to change its behaviour|Award a trophy to every elected official|Guarantee that no trade rules exist|Replace all diplomacy with sporting contests
70|sovereignty|In politics, sovereignty concerns what?|Supreme authority over a state or territory|The number of royal palaces alone|The popularity of one newspaper|The age of a national flag
71|multilateral|A multilateral agreement involves how many parties?|More than two|Exactly one|Exactly two|None
72|bilateral|A bilateral agreement is between how many parties?|Two|Three|Four|Ten
73|domestic-policy|Domestic policy mainly concerns what?|Matters within a country's own borders|Only relations with foreign governments|Only decisions about the moon|Only a diplomat's private travel plans
74|foreign-policy|Foreign policy concerns a state's approach to what?|Other countries and international affairs|Only local refuse collection|Only school lunch menus|Only private family celebrations
75|fiscal-policy|Fiscal policy mainly concerns which government tools?|Taxation and public spending|The design of national sports kits|The appointment of theatre critics|The issue of weather forecasts
76|monetary-policy|Monetary policy mainly concerns what?|Money supply and the cost of borrowing|Only the design of election posters|Only local road names|Only the seating plan in parliament
77|budget|What is a government budget?|A plan for public income and spending|A list of every foreign language|A map of every electoral boundary|A register of all royal titles
78|deficit|A government budget deficit occurs when what happens?|Spending exceeds revenue|Revenue exceeds spending|Spending and revenue are exactly equal|No public money is spent or collected
79|surplus|A government budget surplus occurs when what happens?|Revenue exceeds spending|Spending exceeds revenue|Spending and revenue are exactly equal|All taxes are automatically abolished
80|public-sector|What does the public sector include?|Organisations owned or controlled by government|Only privately owned shops|Only foreign political parties|Only independent family businesses
81|nationalization|What does nationalisation involve?|Bringing an industry or business into public ownership|Selling a state-owned business to private owners|Changing a country's national anthem|Removing citizenship from every worker
82|privatization|What does privatisation involve?|Transferring a state-owned business into private ownership|Bringing every private company into state ownership|Choosing a national flag|Giving every citizen a diplomatic passport
83|welfare-state|What does the idea of a welfare state involve?|Public provision to support people's health and social well-being|A state that only organises sporting events|A state with no public services|A state that grants only hereditary titles
84|civil-service|What is the civil service?|The permanent administrative staff working for government|All the candidates in an election|Only members of the armed forces|Only foreign ambassadors
85|ombudsman|What does an ombudsman generally investigate?|Complaints about organisations or public administration|The weather forecast for election day|Only the age of national monuments|The rules of every board game
86|deputy|What does deputy mean in a political job title?|Someone authorised to act in place of a more senior official|A person who can never hold authority|A person automatically entitled to a throne|A person who only counts opinion polls
87|mayor|A mayor is most closely associated with governing which level of community?|A town or city|An entire continent|The whole United Nations|Every country sharing a language
88|councillor|What does an elected local councillor serve on?|A local council|An international criminal jury|Every national cabinet|A hereditary royal court
89|ward|In local elections, what is a ward?|An electoral area within a local authority|A country's overseas embassy|A cabinet minister's private diary|A section of a national anthem
90|municipal|What does municipal usually mean in government?|Relating to a town or city and its local administration|Relating only to international treaties|Relating only to royal succession|Relating only to the armed forces
91|electorate|What is the electorate?|The people entitled to vote in an election|Only the winning candidates|Only those who spoil their ballots|Only the journalists reporting the result
92|turnout|What does voter turnout measure?|How many eligible or registered voters actually vote|How many ministers own cars|The total length of campaign speeches|The number of buildings in a capital city
93|abstain|What does it mean to abstain in a formal vote?|Choose not to vote for or against|Vote twice for the same proposal|Automatically veto the proposal|Become the chair of the meeting
94|secret-ballot|What is the purpose of a secret ballot?|Protecting the privacy of each voter's choice|Keeping the election date secret from every voter|Hiding every candidate's name until after voting|Preventing any vote from being counted
95|spoiled-ballot|What is a spoiled ballot?|A ballot that cannot be counted as a valid vote|A ballot cast by the winning candidate|Every ballot sent by post|Every vote cast before noon
96|universal-suffrage|Universal adult suffrage is the principle that which people should be able to vote?|All adult citizens, subject to general eligibility rules|Only adults who own land|Only adults with university degrees|Only members of the governing party
97|majority|In a vote, what does an absolute majority mean?|More than half of the relevant total|Exactly one quarter|The largest share even if less than half|Any result containing an odd number
98|unanimous|What does a unanimous decision mean?|Everyone taking part in the decision agrees|Only the chair agrees|Exactly half agree|No decision has been made
99|mandate|What is an electoral mandate generally understood to be?|Authority voters give elected representatives to pursue their programme|A guarantee that every future election is cancelled|An automatic exemption from every law|A permanent hereditary title
100|political-party|What is a political party?|An organised group seeking political power to pursue shared policies|Any gathering held on a public holiday|A court made up only of foreign judges|A private dinner with no political purpose
'''
if __name__=='__main__':
 out=[]
 for line in rows.strip().splitlines():
  n,key,prompt,*answers=line.split('|');assert int(n)==len(out)+1 and len(answers)==4
  out.append({'draftID':f'easy-24-{int(n):03d}','categoryID':'24','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'Candidate meaning and alternatives require individual final review.','sourceURL':'https://dictionary.cambridge.org/dictionary/english/'+key,'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100
 (HERE/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved accessible Politics candidates')
