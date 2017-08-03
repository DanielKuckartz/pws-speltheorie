def is_bankroetprobleem(bedrag, *claims):
    if False in [x >= 0 for x in claims]:
        return 'Error: negatieve argumenten ingevoerd'
    if sum(claims) < bedrag:
        return 'Error: het bedrag is groter dan de totale claim'

def BK_2(bedrag,claim_laag,claim_hoog):
    Error = is_bankroetprobleem(bedrag,claim_laag,claim_hoog)
    if Error:
        return Error
    claim_laag2 = max(0, bedrag - claim_hoog)
    claim_hoog2 = max(0, bedrag - claim_laag)
    
    # fifty-fifty de rest van het bedrag verdelen
    bedrag -= (claim_laag2 + claim_hoog2)
    claim_laag2 += bedrag/2
    claim_hoog2 += bedrag/2

    # Noot: er is een unieke BK-oplossing
    return round(claim_laag2,2), round(claim_hoog2,2)

def BK(bedrag, *claims):
    from collections import OrderedDict
    claims = sorted(list(claims))
    coalitie = len(claims)
    result = []

    # komt neer op coalitionele procedure van Aumann en Maschler
    for i in range(coalitie-1):
        subbedrag = min(claims[i],bedrag) / 2
        if subbedrag >= bedrag/coalitie:
            subbedrag = bedrag/coalitie
            for j in range(i,i+coalitie):
                result.append(round(subbedrag,2))
            break
        else:
            result.append(round(subbedrag,2))
            bedrag -= subbedrag
        coalitie -= 1

    # de laatste persoon krijgt de rest van het bedrag
    result.append(round(bedrag,2))
    print(result,claims)
    return OrderedDict(zip(claims,result))

def is_BK_consistent(dict):
    # controleert of een verdeling van claims en uitbetalingen BK-consistent is
    from itertools import combinations
    bedrag = sum(dict.values())
    paren = combinations(dict.keys(),2)
    for x in paren:
        A = dict[x[0]]
        B = dict[x[1]]
        if not BK_2(A+B, x[0], x[1]) == (A, B):
            return False
    return True

# fixen van de situatie BK(200,100,110,120)
def BK(bedrag, *claims):
    Error = is_bankroetprobleem(bedrag,*claims)
    if Error:
        return Error
    # komt neer op coalitionele procedure van Aumann en Maschler
    from collections import OrderedDict
    claims = sorted(list(claims))
    subclaims = sum(claims)
    coalitieomvang = len(claims)
    result = []
    
    for i in range(coalitieomvang - 1):
        subbedrag = min(claims[i],bedrag) / 2
        verlies = claims[i] - subbedrag
        # iemand met een lagere claim dient niet meer uitbetaald te krijgen dan iemand met een hogere claim
        if subbedrag >= bedrag/coalitieomvang:
            subbedrag = bedrag/coalitieomvang
            for j in range(i,i + coalitieomvang):
                result.append(round(subbedrag,2))
            break
        # iemand met een lagere claim dient niet meer te verliezen dan iemand met een hogere claim
        elif (subclaims - coalitieomvang * verlies) < bedrag:
            print('hoog',subbedrag,bedrag/coalitieomvang,i)
            verlies = (subclaims - bedrag) / coalitieomvang
            for j in range(i,i + coalitieomvang):
                result.append(round(claims[j] - verlies, 2))
            break
        else:
            result.append(round(subbedrag,2))
            bedrag -= subbedrag
        coalitieomvang -= 1
        subclaims -= claims[i]

    # de laatste persoon krijgt de rest van het bedrag
    result.append(round(bedrag,2))
    
    #return result
    return OrderedDict(zip(claims,result))
