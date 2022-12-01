#! /usr/bin/env python
f = open("input.txt","r")
lines = f.readlines()
current_elf=1
elf_totals={}
for line in lines:
    if line.strip() == "":
        current_elf+=1
        continue
    calories=int(line)
    if not current_elf in elf_totals:
        elf_totals[current_elf] = calories
    else:
        elf_totals[current_elf] += calories

print( max(elf_totals, key=elf_totals.get) )
elf_keys = sorted(elf_totals, key=elf_totals.get, reverse=True)[:3]
print( elf_keys )
top_elf_cals = [ elf_totals[idx] for idx in elf_keys ]
print(top_elf_cals)
print(sum(top_elf_cals))