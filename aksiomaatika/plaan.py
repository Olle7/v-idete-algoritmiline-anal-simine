"""Selles failis proovin enda jaoks kirjutada viisi kuidas ühe kvantori ja ühe N algmõistega seost arvutiloetavalt kirja panna.

rida: [algmõistete vahelised seosed] AND IGA_x([x-omadus1] TO [x-kuulumise võimalused alghulkadesse])AND NOT IGA_x([x-omadus1] TO [x-kuulumise võimaluste alghulkadesse almhulk]) AND IGA_x([x-omadus2] TO [x-kuulumise võimalused alghulkadesse])AND NOT IGA_x([x-omadus2] TO [x-kuulumise võimaluste alghulkadesse almhulk]) AND IGA_x([x-omadus3] TO [x-kuulumise võimalused alghulkadesse])AND NOT IGA_x([x-omadus3] TO [x-kuulumise võimaluste alghulkadesse almhulk]) ... AND IGA_x([x-omadusn] TO [x-kuulumise võimalused alghulkadesse])AND NOT IGA_x([x-omadusn] TO [x-kuulumise võimaluste alghulkadesse almhulk])
rea näide: NOT A in A AND IGA_x(NOT A in x AND NOT x in x TO NOT X in A) AND NOT IGA_x(NOT A in x AND NOT x in x TO False) AND
  9?"""

#from veerud import Seos
N=int(input("algmoisteid:"))
K=1#K=input("kvantoreid:")
veerud = []
for i in range(0, N):
    for j in range(0, N):
        veerud.append(str(i) + " in " + str(j))
print(veerud)
mnimi= [K for K, v in locals().iteritems() if v is veerud][0]
print(mnimi)