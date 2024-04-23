from collections import defaultdict
import re
from collections import deque

table = defaultdict(list)
operators = set(["/", "+", "-", "*", "^"])

def valid(string):
    if len(string) <= 3:
        return False
    for c in string:
        if c not in table and c not in operators:
            return True
    return False

def gen_var(string):
    return f"t{len(table)+1}"

def get_bracket(string):
    stack = []
    opening = 0
    closing = 0
    start = float('inf')
    end = -1
    for i, c in enumerate(string):
        if c == "(":
            opening += 1
            start = min(start, i)
        elif c == ")":
            closing += 1
            end = max(end, i)
        if opening and opening == closing:
            return (start, end+1)
    return None

def get_op(string, op):
    try:
        t = string.index(op)
        start = t-1
        end = t+2
        return (start, end)
    except ValueError:
        return False
    
def gen_tac(string):
    while valid(string): # While the string does not only consists of temporary variables and operators.
        # Checking for bracket "()"
        v = get_bracket(string)
        if v:
            start = v[0]
            end = v[1]
            # print(v[0], v[1], string[start:end])
            var = gen_var(string[start:end])
            table[var] = gen_tac(string[start+1:end-1])
            string[start:end] = string[start+1:end-1]
            # string[start:end] = table[var]
            continue
        # Checking for power "^"
        v = get_op(string, "^")
        if v:
            start = v[0]
            end = v[1]
            var = gen_var(string)
            table[var] = string[start:end]
            string[start:end]=[var]
            # print(string, var, table)
            gen_tac(string)
            continue        
        # Checking for division "/"
        v = get_op(string, "/")
        if v:
            start = v[0]
            end = v[1]
            var = gen_var(string)
            table[var] = string[start:end]
            string[start:end]=[var]
            # print(string, var, table)
            gen_tac(string)
            continue        
        # Checking for multiplication "*"
        v = get_op(string, "*")
        if v:
            start = v[0]
            end = v[1]
            var = gen_var(string)
            table[var] = string[start:end]
            string[start:end]=[var]
            # print(string, var, table)
            gen_tac(string)
            continue        # Checking for addition "+"
        v = get_op(string, "+")
        if v:
            start = v[0]
            end = v[1]
            var = gen_var(string)
            table[var] = string[start:end]
            string[start:end]=[var]
            # print(string, var, table)
            gen_tac(string)
            continue
        # Checking for substraction "-"
        v = get_op(string, "-")
        if v:
            start = v[0]
            end = v[1]
            var = gen_var(string)
            table[var] = string[start:end]
            string[start:end]=[var]
            # print(string, var, table)
            gen_tac(string)
            continue    
        # Checking for assignment "="
        v = get_op(string, "=")
        if v:
            start = v[0]
            end = v[1]
            # var = gen_var(string)
            table[v] = string[end-1:]
            return string
            # string[start:end]=[var]
            # print(string, var, table)
            # gen_tac(string)
            continue      
    
    return string


def gen_assembly(table, out):
    stack = deque()
    visited = set()
    tac_lines = deque()
    for c in out:
        if c in table:
            stack.append(c)
            visited.add(c)

    while stack:
        v = stack.popleft()
        tac_lines.appendleft([v, table[v]])
        for c in table[v]:
            if c in table and c not in visited:
                stack.append(c)
                visited.add(c)

    tac_lines.append([out[0], out[2:]])
    # ".DATA\n.CODE\nMAIN PROC\n\nMOV AX, @DATA      ; Point AX to the data segment\nMOV DS, AX"
    # print(tac_lines)
    data_section = set([])
    code_section = [".CODE\nMAIN PROC\n    MOV AX, @DATA      ; Point AX to the data segment\n    MOV DS, AX"]

    for line in tac_lines:
        data_section.add(" "*4 + f"{line[0]} DW ?';")

        if "*" in line[1]: #OP3 = OP1 * OP2
            data_section.add(" "*4 + f"{line[1][0]} DW ?' ;")
            data_section.add(" "*4 + f"{line[1][2]} DW ?' ;")
            code_section.append(" "*4 + f"MOV AX, {line[1][0]} ; MOVING OP1 INTO AX")
            code_section.append(" "*4 + f"MUL {line[1][2]} ; MULTIPLYING")
            code_section.append(" "*4 + f"MOV {line[0]}, AX ; EQUALS TO = AX")

        if "+" in line[1]: #OP3 = OP1 + OP2
            data_section.add(" "*4 + f"{line[1][0]} DW ?' ;")
            data_section.add(" "*4 + f"{line[1][2]} DW ?' ;")
            code_section.append(" "*4 + f"MOV AX, {line[1][0]} ; MOVING OP1 INTO AX")
            code_section.append(" "*4 + f"ADD AX, {line[1][2]} ; Adding OP2 TO AX")
            code_section.append(" "*4 + f"MOV {line[0]}, AX ; OP3 EQUALS TO = AX")
            
        if "-" in line[1]: #OP3 = OP1 - OP2
            data_section.add(" "*4 + f"{line[1][0]} DW ?' ;")
            data_section.add(" "*4 + f"{line[1][2]} DW ?' ;")
            code_section.append(" "*4 + f"MOV AX, {line[1][0]} ; MOVING OP1 INTO AX")
            code_section.append(" "*4 + f"SUB AX, {line[1][2]} ; Substracting OP2 TO AX")
            code_section.append(" "*4 + f"MOV {line[0]}, AX ; OP3 = AX")

        if "-" in line[1]: #OP3 = OP1 / OP2
            data_section.add(" "*4 + f"{line[1][0]} DW ?' ;")
            data_section.add(" "*4 + f"{line[1][2]} DW ?' ;")
            code_section.append(" "*4 + f"MOV AX, {line[1][0]} ; MOVING OP1 INTO AX")
            code_section.append(" "*4 + f"XOR DX, DX ; Clear DX (necessary to ensure the upper 16 bits are zero)")
            code_section.append(" "*4 + f"MOV BX, {line[1][2]} ; Move the divisor to BX")
            code_section.append(" "*4 + f"DIV BX")
            code_section.append(" "*4 + f"MOV {line[0]}, DX  ; Store the remainder in the 'remainder' variable")
        
        else:
            data_section.add(" "*4 + f"{line[1][-1]} DW ?' ;")
            code_section.append(" "*4 + f"MOV {line[0]}, {line[1][-1]}")

    code_section.append("    MOV AH, 4CH        ; Exit program\nINT 21H\nMAIN ENDP")
    print("\n".join([".DATA"]+list(data_section)+code_section))

ln = input()
while ln:
    out = gen_tac(ln.split(" "))
    ln = input()
    print(f'{out[0]} := {" ".join(out[2:])}')
    stack = deque()
    visited = set()
    for c in out:
        if c in table:
            stack.append(c)
            visited.add(c)

    while stack:
        v = stack.popleft()
        print(f'{v} := {" ".join(table[v])}')
        for c in table[v]:
            if c in table and c not in visited:
                stack.append(c)
                visited.add(c)
    # print(table)
    print("#"*10+"Assembly Code Start"+"#"*10)
    gen_assembly(table, out)
    print("#"*10+"Assembly Code End"+"#"*10)
