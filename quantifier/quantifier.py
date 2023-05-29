import re
import string

forall = '∀'
exists = '∃'
epsilon = '∈'
notin = '∉'
land = '∧'
lor = '∨'
lnot = '¬'
implies = '⇒'
iff = '⇔'
neq = '≠'

'∃v ∃u∈f ~pair(u,_,v) ∧ (something about v)'

#isStationary doesn't assume input is a subset
#domainEq and rangeEqish assume input is function
#isFuncFromTo doesn't check for image, just range, doesn't have to be surjective

#Soloveyyyyy
goal = '∀a ∀b ((~isCardinal(a)) ∧ (~isRegular(a)) ∧ (~isStationary(b,a)) ∧ ¬(~isOmega(a))) ⇒ ∃c ((~isPartition(c,b)) ∧ (~eqSize(c,a)) ∧ ∀d∈c (~isStationary(d,a)))'

definitions = {
    'transitive': '(x)=∀y∈x ∀z∈y z∈x',
    'linOrdByEpsilon': '(x)=∀y∈x ∀z∈x (y∈z ∨ z∈y)',
    'ord': '(x)=(~transitive(x)) ∧ (~linOrdByEpsilon(x))',
    'size2': '(x)=∃y∈x ∃z∈x (y≠z ∧ (∀a∈x (a=y ∨ a=z)))',
    'size1': '(x)=∃y∈x ∀z∈x z=y',
    'unipair': '(x)=(~size1(x)) ∧ ∃z∈x (~size1(z))', # x = {{y}}, useful because (y, y) = {{y}, {y, y}} = {{y}}
    'isOrderedPair': '(x)=((~size2(x)) ∧ ∃y∈x ∃z∈x ((~size2(y)) ∧ (~size1(z)) ∧ (∃a∈z a∈y))) ∨ (~unipair(x))',
    'pair': '(p,a,b)=(~isOrderedPair(p)) ∧ ((∃y∈p ∃z∈p ((~size2(y)) ∧ (~size1(z)) ∧ (a∈z ∧ a∈y ∧ b∈y ∧ a≠b))) ∨ (a=b ∧ (~size1(p)) ∧ ∃q∈p a∈q))',
    'isFunction': '(f)=(∀p∈f (~isOrderedPair(p))) ∧ (∀a∈f ∀b∈f (a≠b ⇒ (∃v ∃u∈f ~pair(u,a,v) ∧ (∃i ∃j∈f ~pair(j,b,i) ∧ (i≠v)))))',
    'disjoint': '(x,y)=¬(∃a (a∈x ∧ a∈y))',
    'isPartition': '(a,b)=(∀x∈b ∃y∈a x∈y) ∧ (∀x∈a ∃y∈x) ∧ (∀x∈a ∀y∈a (~disjoint(x,y)))',
    'isSubset': '(a,b)=∀x∈a x∈b',
    'imageEq': '(f,i)=∀x ((∃p∈f ∃y (~pair(p,y,x))) ⇔ x∈i)',
    'domainEq': '(f,d)=∀x (x∈d ⇔ (∃p∈f ∃y (~pair(p,x,y))))',
    'rangeEqish': '(f,r)=∀x ((∃i ((~imageEq(f,i)) ∧ x∈i)) ⇒ x∈r)',
    'isFuncFromTo': '(f,d,r)=(~isFunction(f)) ∧ (~domainEq(f,d)) ∧ (~rangeEqish(f,r))',
    'isSurjection': '(f,r)=~imageEq(f,r)',
    'isInjection': '(f)=∀p∈f ∀q∈f ((∃s ∃a ∃b ((~pair(p,a,s)) ∧ (~pair(q,b,s)))) ⇒ p=q)',
    'isBijection': '(f,b)=(~isInjection(f)) ∧ (~isSurjection(f,b))',
    'eqSize': '(a,b)=∃f ((~isFuncFromTo(f,a,b)) ∧ (~isBijection(f,b)))',
    'isCardinal': '(k)=(~ord(k)) ∧ ∀o∈k ¬(~eqSize(k,o))',
    'isUnbounded': '(c,k)=∀a∈k ∃b∈c a∈b',
    'isLimit': '(x)=(~ord(x)) ∧ ¬(∃m∈x ∀n∈x (n∈m ∨ n=m))',
    'isIntersection': '(i,a,b)=∀x (x∈i ⇔ (x∈a ∧ x∈b))',
    'isClosed': '(c,k)=∀x∈k (((~isLimit(x)) ∧ (∃i ((~isIntersection(i,x,c)) ∧ (~isUnbounded(i,x))))) ⇒ x∈c)',
    'isClub': '(c,k)=(~isSubset(c,k)) ∧ (~isClosed(c,k)) ∧ (~isUnbounded(c,k))',
    'isInductive': '(w)=(∃e∈w (∀x x∉e)) ∧ (∀x∈w ∃y∈w (∀z (z∈y ⇔ (z=x ∨ z∈x))))',
    'isOmega': '(w)=∀x ((~isInductive(x)) ⇒ (~isSubset(w,x)))',
    'isStationary': '(s,k)=∀c ((~isClub(c,k)) ⇒ ∃x (x∈c ∧ x∈s))',
    'isRegular': '(k)=∀o∈k ∀f ((~isFuncFromTo(f,o,k)) ⇒ ¬(∃i ((~imageEq(f,i)) ∧ (~isUnbounded(i,k)))))',
    'isRelation': '(r)=∀x∈r (~isOrderedPair(x))',
    'isProduct': '(p,x,y)=∀e e∈p ⇔ (∃a∈x ∃b∈y (~pair(p,a,b)))',
    'isOne': '(x)=∃e ((∀a a∉e) ∧ e∈x ∧ ∀z∈x (z=e))',
    'divides_w': '(d,n,w)=∃c∈w ∃p ((~isProduct(p,d,c)) ∧ ∃f ((~isFuncFromTo(f,n,p)) ∧ (~isInjection(f)) ∧ (~isSurjection(f,p))))',
    'isPrime_omega': '(n,w)=∀d∈w ((~divides_w(d,n,w)) ⇒ ((~isOne(d)) ∨ d=n))',
    'infinitePrimes': '()=∃w ((~isOmega(w)) ∧ ∀n∈w ∃m∈w (n∈m ∧ (~isPrime_omega(m,w))))'
}

def main():
    formula = goal #!!!
    #formula = '~isRegular(k)'
    
    #formula = '~infinitePrimes()'
    availableSymbols = list(string.ascii_lowercase)

    print(unwrapFormula(formula, availableSymbols))

def unwrapFormula(formula, availableSymbols):
    oldFormula = ''

    while oldFormula != formula:
        oldFormula = formula
        formula = openFirstDefinition(formula, availableSymbols[:])

    return formula
    
    
def openFirstDefinition(formula, availableSymbols):
    unwrapped = ''
    
    inSkip = False
    changed = False
    
    for i in range(len(formula)):
        if inSkip:
            if formula[i] == ')':
                inSkip = False
                continue
            else:
                continue
            
        if changed:
            unwrapped += formula[i]
            continue
        
        if formula[i] != '~':
            unwrapped += formula[i]
        else:
            currOpened = openDefinition(formula[i + 1: formula.find(')', i) + 1], availableSymbols)
            unwrapped += currOpened
            inSkip = changed = True

    return unwrapped

'''
greater(x,y) -> y∈x
minimum(x) -> ∀y x∈y
'''
def openDefinition(defInput, availableSymbols):    
    openned = ''
    rawDefinition = definitions[defInput[:defInput.find('(')]]

    definition = rawDefinition[rawDefinition.find('=') + 1:]

    letterMappings = {}
    assignedLettersDestinations = re.split('\(|,|\)', defInput)[1: -1]
    assignedLetters = re.split('\(|,|\)', rawDefinition)[1: rawDefinition[:rawDefinition.find('=')].count(',') + 2]

    for i in range(len(assignedLetters)):
        letterMappings[assignedLetters[i]] = assignedLettersDestinations[i]
        if assignedLettersDestinations[i] in availableSymbols:
            availableSymbols.remove(assignedLettersDestinations[i])
    
    inText = False
    for l in definition:
        if inText:
            if l == '(':
                inText = False
            else:
                openned += l
                continue

        if l != '~':
            if not l.isalpha():
                openned += l
            elif l in letterMappings:
                openned += letterMappings[l]
            else:
                letterMappings[l] = availableSymbols[0]
                del availableSymbols[0]
                openned += letterMappings[l]
        else:
            inText = True
            openned += '~'

    if openned.count('~') == 0:
        return openned


    return unwrapFormula(openned, availableSymbols)
    
if __name__ == '__main__':
    main()

