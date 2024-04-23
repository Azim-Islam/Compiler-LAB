.DATA
    t11 DW ?';
    t13 DW ?' ;
    t12 DW ?';
    t9 DW ?';
    t14 DW ?' ;
    t11 DW ?' ;
    t13 DW ?';
    t9 DW ?' ;
    c DW ?' ;
    a DW ?' ;
    t7 DW ?' ;
    d DW ?' ;
    t7 DW ?';
    b DW ?' ;
    t12 DW ?' ;
    t10 DW ?' ;
    t8 DW ?';
    t10 DW ?';
    t8 DW ?' ;
    x DW ?';
    0 DW ?' ;
    t14 DW ?';
.CODE
MAIN PROC
    MOV AX, @DATA      ; Point AX to the data segment
    MOV DS, AX
    MOV AX, a ; MOVING OP1 INTO AX
    MUL b ; MULTIPLYING
    MOV t7, AX ; EQUALS TO = AX
    MOV t7, b
    MOV AX, a ; MOVING OP1 INTO AX
    ADD AX, b ; Adding OP2 TO AX
    MOV t10, AX ; OP3 EQUALS TO = AX
    MOV t10, b
    MOV AX, t7 ; MOVING OP1 INTO AX
    ADD AX, c ; Adding OP2 TO AX
    MOV t8, AX ; OP3 EQUALS TO = AX
    MOV t8, c
    MOV AX, t10 ; MOVING OP1 INTO AX
    ADD AX, c ; Adding OP2 TO AX
    MOV t11, AX ; OP3 EQUALS TO = AX
    MOV t11, c
    MOV AX, t8 ; MOVING OP1 INTO AX
    ADD AX, d ; Adding OP2 TO AX
    MOV t9, AX ; OP3 EQUALS TO = AX
    MOV t9, d
    MOV AX, t11 ; MOVING OP1 INTO AX
    ADD AX, d ; Adding OP2 TO AX
    MOV t12, AX ; OP3 EQUALS TO = AX
    MOV t12, d
    MOV AX, 0 ; MOVING OP1 INTO AX
    SUB AX, t9 ; Substracting OP2 TO AX
    MOV t13, AX ; OP3 = AX
    MOV AX, 0 ; MOVING OP1 INTO AX
    XOR DX, DX ; Clear DX (necessary to ensure the upper 16 bits are zero)
    MOV BX, t9 ; Move the divisor to BX
    DIV BX
    MOV t13, DX  ; Store the remainder in the 'remainder' variable
    MOV AX, t13 ; MOVING OP1 INTO AX
    SUB AX, t12 ; Substracting OP2 TO AX
    MOV t14, AX ; OP3 = AX
    MOV AX, t13 ; MOVING OP1 INTO AX
    XOR DX, DX ; Clear DX (necessary to ensure the upper 16 bits are zero)
    MOV BX, t12 ; Move the divisor to BX
    DIV BX
    MOV t14, DX  ; Store the remainder in the 'remainder' variable
    MOV x, t14
    MOV AH, 4CH        ; Exit program
INT 21H
MAIN ENDP