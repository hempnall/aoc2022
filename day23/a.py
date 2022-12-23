f = open("sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

DIRS={
    "N": (0,-1),
    "NE": (1,-1),
    "E": (1,0),
    "SE": (1,1),
    "S": (0,1),
    "SW": (-1,1),
    "W": (-1,0),
    "NW": (-1,-1)
}

def addvec(vec1,vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

def parse_file(lines):
    elves=set()
    for rowidx,line in enumerate(lines):
        elves_in_line=[
            (colidx,rowidx) for colidx in range(len(line)) if line[colidx]=="#"
        ] 
        elves.update(elves_in_line)
    return elves

def has_adjacent_elf(  elves, elf  ):
    for DIR in DIRS.values():
        adj_pos = addvec(elf,DIR)
        if adj_pos in elves:
            return True
    return False
        
def elves_bounding_box_area(elves):
    minx=min([ x for x,_ in elves])
    miny=min([ y for _,y in elves])
    maxx=max([ x for x,_ in elves])
    maxy=max([ y for _,y in elves])
    return (maxx-minx+1) * (maxy - miny+1)



elves=parse_file(lines)
print(elves)
boundingbox_area=elves_bounding_box_area(elves)
print(boundingbox_area)



