"""Supplementary exhaustive checks, not a substitute for the recorded editorial pass."""
import collections,itertools,json,pathlib
q=json.loads((pathlib.Path(__file__).parent/'draft.json').read_text(encoding='utf8'))
def unique(n,predicate):
    row=q[n-1];valid=[a for a in row['answers'] if predicate(a)]
    assert valid==[row['answers'][row['correctIndex']]],(n,valid)
unique(41,lambda s:set(s)<=set('25') and s[0]==s[-1] and s[1]!=s[0])
unique(57,lambda s:collections.Counter(s)==collections.Counter('SILENT'))
unique(58,lambda s:collections.Counter(s)==collections.Counter('HEART'))
unique(61,lambda s:len(set(s))==2 and all(int(c)%2==0 for c in s) and s[0]>s[1])
unique(77,lambda s:int(s[0])==int(s[1])-1)
unique(78,lambda s:s[0]==s[2]=='4' and s[1]=='3')
unique(79,lambda s:collections.Counter(s)==collections.Counter('XY') and s>'XY')
unique(80,lambda s:s==s[::-1] and s[1]=='6')
unique(96,lambda s:len(s)==len(set(s))==3)
# Exhaust all three-child sex assignments, including same-sex families.
possible=[]
for children in itertools.product('GB',repeat=3):
    if all(children.count('G')-(sex=='G')==1 and children.count('B')-(sex=='B')==1 for sex in children):possible.append(children)
assert possible==[] and q[83]['answers'][0]=='No such group is possible'
assert ''.join({'A':'1','B':'2','C':'3'}[s] for s in 'BCA')==q[42]['answers'][0]
assert ''.join({'A':'B','B':'A'}[s] for s in 'ABBA')==q[46]['answers'][0]
assert ' '.join(reversed('cats chase mice'.split()))==q[47]['answers'][0]
assert 'FROG'[-1]+'FROG'[:-1]==q[48]['answers'][0]
assert ((5-1+3)%6)+1==int(q[68]['answers'][0])
assert sorted([s for s in itertools.permutations('AB')])==[('A','B'),('B','A')]
print('Passed explicit-option uniqueness, exhaustive sibling constraints, code transformations and ring wrap checks. Editorial review remains separately recorded.')
