from sympy.abc import symbols
veerud_sympy_formaadis=symbols(['a∈a', 'a∈b', 'b∈a', 'b∈b'])

rida1=~veerud_sympy_formaadis[0]&veerud_sympy_formaadis[1]&veerud_sympy_formaadis[2]&veerud_sympy_formaadis[3]
print(rida1)