id_algus="6020124389"
id_algus="6050310199"
summa=0
for i in range(0,len(id_algus)):
    summa+=((i+1)*int(id_algus[i]))
print(summa%11)