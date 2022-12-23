f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

DIR_VECS={
    "N": (0,-1),
    "NE": (1,-1),
    "NW": (-1,-1),
    "S": (0,1),
    "SE": (1,1),
    "SW": (-1,1),
    "E": (1,0),
    "W": (-1,0),
}
DIRS=["N","S","W","E"]
DIR_PRIOR={
    "N":["N","NE","NW"],
    "S":["S","SE","SW"],
    "W":["W","NW","SW"],
    "E":["E","NE","SE"],
}

def addvec(vec1,vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

class Elf:
    def __init__(self, x, y):
        self.location=(x,y)
        self.move_pref=0
        self.proposal=None

    def has_adjacent_elf( self , elves  ):
        for DIR in DIR_VECS.values():
            adj_pos = addvec(self.location,DIR)
            if adj_pos in elves:
                return True
        return False

    def next_move_pref(self):
        return (self.move_pref + 1 ) % 4

    def round1(self,locations):
        if not self.has_adjacent_elf(locations):
            self.proposal=None
            return None,self.proposal
        first_direction=DIRS[self.move_pref]
        for c in range(4):
            direction=DIRS[(self.move_pref + c)%4]
            if not any([ addvec(self.location,DIR_VECS[dirvec]) in locations for dirvec in DIR_PRIOR[direction] ]):
                self.proposal=addvec(self.location,DIR_VECS[direction])
                return direction , self.proposal
        self.proposal=None
        return None,self.proposal

    def round2(self,hist,locations):
        if hist[self.proposal]==1:
            self.location=self.proposal
        locations.add(self.location)
        self.move_pref=self.next_move_pref()

def get_locations( elves ):
    return [ e.location for e in elves ]

def parse_file(lines):
    elves=set()
    for rowidx,line in enumerate(lines):
        elves.update([
            Elf(colidx,rowidx) for colidx in range(len(line)) if line[colidx]=="#"
        ]) 
    return elves , get_locations(elves)

def get_bounding_box(elves):
    minx=min([ elf.location[0] for elf in elves])
    miny=min([ elf.location[1] for elf in elves])
    maxx=max([ elf.location[0] for elf in elves])
    maxy=max([ elf.location[1] for elf in elves])
    return (minx,maxx), (miny,maxy)

def elves_bounding_box_area(elves):
    bbx,bby = get_bounding_box(elves)
    return (bbx[1]-bbx[0]+1) * (bby[1] - bby[0]+1)

def render_grid(elves,locations):
    bbx,bby = get_bounding_box(elves)
    for rows in range(bby[0],bby[1]+1):
        for cols in range(bbx[0],bbx[1]+1):
            if (cols,rows) in locations:
                print("#",end='')
            else:
                print(".",end='')
        print()

def add_to_histogram( hist , item ):
    if item in hist:
        hist[item] += 1
    else:
        hist[item] = 1

def proposal_hist( proposals ):
    hist={}
    for v in proposals:
        add_to_histogram(hist,v)
    return hist

elves,locations=parse_file(lines)
render_grid(elves,locations)

def do_round(rnd,elves):
    print(f'START OF ROUND {rnd}')
    locations=get_locations(elves)
    proposals=[ e.round1(locations)[1] for e in elves ]
    hist=proposal_hist(proposals)
    count_of_moving_elves=len( [ loc for loc,v in hist.items() if v == 1 ] )
    if count_of_moving_elves == 0:
        print(f'{rnd+1}')
        exit()
    locations=set()
    for elf in elves:
        elf.round2(hist,locations)
    render_grid(elves,locations)

for rnd in range(0,1000000):
    do_round(rnd,elves)

answer=elves_bounding_box_area(elves) - len(list(elves))
print(answer)









