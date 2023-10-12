from collections import defaultdict
import re
import sys
# sys.setrecursionlimit(10**9) 

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
print(p_rules)
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
    for nt in sym_n_terms:
        s = re.search("^"+nt, rule)
        if s:
            return rule[:s.end()]
    return None 

def get_t(rule):
    for t in sym_terms:
        s = re.search("^"+t, rule)
        if s:
            return (rule[:s.end()], s)
    return None
generate_terminal_non_terminals(p_rules)

print(sym_terms)
print(sym_n_terms)

# Implementation of FIRST
def FIRST(nt_sym, rules):
    for rule in rules:
        nt = get_nt(rule)
        if nt:
            FIRST_T[nt_sym].add(nt)
        temp = set()
        while not nt:
            t = get_t(rule)
            if t:
                t, s = t[0], t[1]
                FIRST(t, p_rules)
                temp = temp.union(FIRST_T[t])
                if len(temp) == 1 and 'ε' in temp:
                    rule = rule[s.end():]
                    print(rule)
                    if not rule:
                        FIRST_T[nt_sym].add('ε')
                        break
                elif len(temp) > 1:
                    temp.remove('ε')
                    FIRST_T[nt_sym] = FIRST_T[nt_sym].union(temp)
                    break
            else:
                nt = get_nt(rule)
                if nt:
                    FIRST_T[nt_sym].add(nt)
                else:
                    FIRST_T[nt_sym].add('ε')
                    break


                
# for nt_sym in p_rules:
#     FIRST(nt_sym, p_rules[nt_sym])


# #printing FIRST
# for s in p_rules:
#     print(f"FIRST {s} = {sorted(FIRST_T[s])}")



