# LEIA x
li $v0, 5
syscall
move $x, $v0
# IF_FALSE x GOTO L1
beq $x, $zero, L1
# ESCREVA "Valor
li $a0, "Valor
li $v0, 1
syscall
li $i, 0
L2:
# IF_FALSE i GOTO L3
beq $i, $zero, L3
# ESCREVA "Contando..."
li $a0, "Contando..."
li $v0, 1
syscall
move $i, $?
j L2
L3:
L1: