f = open("sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

DIRS={
    "N": (0,-1),
    "NE": (1,-1),
    "E": (1,0),
    "SE": (1,1),
    "S": 
}

def parse_file(lines):
    elves=set()
    for rowidx,line in enumerate(lines):
        elves_in_line=[
            (colidx,rowidx) for colidx in range(len(line)) if line[colidx]=="#"
        ] 
        elves.update(elves_in_line)
    return elves

elves=parse_file(lines)
print(elves)




