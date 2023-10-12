from collections import defaultdict
import re


######################################################################
################ LEFT RECURSION REMOVE START #########################
#Checks if a production rule has left recursion
#By checking the symbols of production rules using regular expression.
def checkLeftRec(p_rules, sym):
    for rule in p_rules[sym]:
        if re.search("^"+sym, rule):
            return True
    return False

#The inputs are read from 'input' file in the root directory of the program.
f = open('input', 'r')
p_rules = defaultdict(list) #This dictionary contains the production rules as in ['P'] -> ['Y', 'Z', 'e']

#input from 'input file'
for line in f:
    if line.strip():
        t1 = line.strip().split("->")
        left = t1[0] #The left symbol
        production = t1[1] #The production rules associated with ...
        p_rules[left] += production.split("|")

symbol = list(p_rules.keys()) #The 'producing' symbols are read. ie the symbols which have production (left symbols).
for i in range(0, len(symbol)):
    for j in range(0, i):
        new_rules = []
        betas = p_rules[symbol[j]]
        for symbols_ in p_rules[symbol[i]]:
            alphas = []
            phis = [] 
            #if such rule Ai -> Aja + phi
            s = re.search("^"+symbol[j], symbols_)
            if s:
                #then  Ai -> B1a | B2a | B3a ...+ phi ...
                #given Aj -> B1 | B2 | B3...
                alpha = alphas.append(symbols_[s.end():])
            else:
                phis.append(symbols_)
            if alphas:
                for alpha in alphas:
                    for beta in betas:
                        new_rules.append(beta+alpha)
            new_rules += phis
            if new_rules:
                p_rules[symbol[i]] = new_rules

    #Left recursion removal of Ai
    if checkLeftRec(p_rules, symbol[i]):
        alphas = []
        betas = []
        for sym in p_rules[symbol[i]]:
            s = re.search("^"+symbol[i], sym)
            if s:
                alphas.append(sym[s.end():])
            else:
                betas.append(sym)
        new_rules = []
        prime_sym = symbol[i]+"`"
        for beta in betas:
            new_rules.append(beta+prime_sym)
        p_rules[symbol[i]] = new_rules
        new_rules = []
        for alpha in alphas:
            new_rules.append(alpha+prime_sym)
        p_rules[prime_sym] = new_rules
        if new_rules:
            p_rules[prime_sym].append("ε")
    

#output
print("Left Recursion Removed")
for k in p_rules:
    print(f"{k} -> "+" | ".join(p_rules[k]))


######################################################################
################ LEFT RECURSION REMOVE END ###############################
sym_n_terms = set()
sym_terms = []
FIRST_T = defaultdict(set)
def extract_terms(r):
    while r:
        for t in sym_terms:
            # print(f"Searching {'^'+t}: {r}")
            s = re.search("^"+t, r)
            if s:
                # print(r[:s.end()])
                r = r[s.end():]
                break
        else:
            if r:
                sym_n_terms.add(r[0])
                r = r[1:]

def generate_terminal_non_terminals(p_rules):
    # Identifying Terminal Symbols
    for s in p_rules:
        sym_terms.append(s)
    # Identifying Non-Terminal Symbols
    sym_terms.sort(key=lambda x: len(x), reverse=True)
    for s in p_rules:
        for r in p_rules[s]:
            extract_terms(r[:])

def get_nt(rule):
    for t in sym_terms:
        s = re.search("^"+t, rule)
        if s:
            return rule[:s.end()]
    return None
generate_terminal_non_terminals(p_rules)

print(sym_terms)
print(sym_n_terms)

# Implementation of FIRST
def FIRST(nt_sym, rules):
    for rule in rules:
        _nt_ = get_nt(rule)
        print(_nt_, rule)
        rule = rule[:]
        temp = set()
        while _nt_:
            FIRST(_nt_, p_rules[_nt_])
            # print(nt_sym, _nt_, FIRST_T[nt_sym], FIRST_T[_nt_])
            # FIRST_T[nt_sym] = FIRST_T[nt_sym].union(FIRST_T[_nt_])
            temp = temp.union(FIRST_T[_nt_])
            if len(temp) == 1 and 'ε' in temp:
                for t in sym_terms:
                    s = re.search("^"+t, rule)
                    if s:
                        # print(r[:s.end()])
                        _nt_ = rule[:s.end()]
                        rule = rule[s.end():]
                        break
            else:
                _nt_ = None
        if not get_nt(rule):
            FIRST_T[nt_sym].add(rule[0])
        else:
            FIRST_T[nt_sym] = FIRST_T[nt_sym].union(temp)

for nt_sym in p_rules:
    FIRST(nt_sym, p_rules[nt_sym])


#printing FIRST
for s in p_rules:
    print(f"FIRST {s} = {sorted(FIRST_T[s])}")



