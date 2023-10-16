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
        if re.search(fr"^[{sym}]", rule):
            return True
    return False

#The inputs are read from 'input' file in the root directory of the program.
f = open('input', 'r', encoding='UTF-8')
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
            s = re.search(fr"^[{symbol[j]}]", symbols_)
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
            s = re.search(fr"^[{symbol[i]}]", sym)
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
            s = re.search(fr"^[{t}]", r)
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

def check_valid(rule):
    if not rule:
        return True
    for nt in sym_n_terms:
        p = "".join([f"[{c}]" for c in nt])
        s = re.search(fr"^{p}", rule)
        if s:
            return True
    for t in sym_terms:
        p = "".join([f"[{c}]" for c in t])
        s = re.search(fr"^{p}", rule)
        if s:
            return True
    return False

def get_nt(rule):
    for nt in sym_n_terms:
        p = "".join([f"[{c}]" for c in nt])
        s = re.search(fr"^{p}", rule)
        if s and check_valid(rule[s.end():]):
            return rule[:s.end()]
            
    return None 

def get_t(rule):
    for t in sym_terms:
        p = "".join([f"[{c}]" for c in t])
        s = re.search(fr"^{p}", rule)
        if s and check_valid(rule[s.end():]):
            return (rule[:s.end()], s)
    return None

generate_terminal_non_terminals(p_rules)

print(sym_terms)
print(sym_n_terms)

# Implementation of FIRST
def FIRST(nt_sym, rules):
    # print(nt_sym)
    for rule in rules:
        nt = get_nt(rule)
        if nt:
            FIRST_T[nt_sym].add(nt)
        while not nt:
            t = get_t(rule)
            if t:
                t, s = t[0], t[1]
                FIRST(t, p_rules[t])
                FIRST_T[nt_sym] = FIRST_T[nt_sym].union(FIRST_T[t])
                if 'ε' in FIRST_T[nt_sym]:
                    rule = rule[s.end():]
                    if not rule:
                        if not FIRST_T[nt_sym]: FIRST_T[nt_sym].add('ε')
                        break
                    FIRST_T[nt_sym].remove('ε')
                else:
                    break


            else:
                nt = get_nt(rule)
                if nt:
                    FIRST_T[nt_sym].union(nt)
                    break


                
for nt_sym in p_rules:
    FIRST(nt_sym, p_rules[nt_sym])


#printing FIRST
for s in p_rules:
    print(f"FIRST {s} = {sorted(FIRST_T[s])}")



#####################################
# Calculating FOLLOW
FOLLOW_T = defaultdict(set)
FOLLOW_T[list(p_rules.keys())[0]].add("$")


def FOLLOW(nt_sym):
    for sym in p_rules:
        for rule in p_rules[sym]:
            s = re.search(nt_sym, rule)
            if s and check_valid(rule[s.end():]):
                # print(nt_sym, sym, rule)
                rule = rule[s.end():]
                if rule:
                    nt = get_nt(rule)
                    if nt:
                        FOLLOW_T[nt_sym].add(nt)
                    if not nt:
                        t = get_t(rule)
                        while t:
                            t, s = t[0], t[1]
                            FOLLOW_T[nt_sym] = FOLLOW_T[nt_sym].union(FIRST_T[t])
                            if 'ε' in FOLLOW_T[nt_sym]:
                                FOLLOW_T[nt_sym].remove('ε')
                                rule = rule[s.end():]
                                if rule:
                                    t = get_t(rule)
                                    if not t:
                                        nt = get_nt(rule)
                                        FOLLOW_T[nt_sym].add(nt)
                                        break
                                elif sym != nt_sym:
                                    FOLLOW(sym)
                                    FOLLOW_T[nt_sym] = FOLLOW_T[nt_sym].union(FOLLOW_T[sym])
                                    break
                            else:
                                break
                else:
                    if sym != nt_sym:
                        FOLLOW(sym)
                        FOLLOW_T[nt_sym] = FOLLOW_T[nt_sym].union(FOLLOW_T[sym])

            





for nt_sym in p_rules:
    FOLLOW(nt_sym)

#printing FOLLOW
for s in p_rules:
    print(f"FOLLOW {s} = {sorted(FOLLOW_T[s])}")