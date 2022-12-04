from cgitb import small


f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def detect_overlap(smallest,largest):
    return  smallest[0] >= largest[0] and smallest[1] <= largest[1]

def range_size(range):
    return range[1]-range[0]

def detect_complete_overlap(range1, range2):
    rsize1=range_size(range1)
    rsize2=range_size(range2)
    if (rsize1 < rsize2):
        return detect_overlap(range1,range2)
    elif rsize1 == rsize2:
        return range1[0] == range2[0]
    else:
        return detect_overlap(range2,range1)

def range_set(range_tuple):
    return set(range(range_tuple[0],range_tuple[1]+1))

def detect_partial_overlap(range1,range2):
    r1_set=range_set(range1)
    r2_set=range_set(range2)
    intersect=r1_set.intersection(r2_set)
    return len(list(intersect))>0

def get_range(range):
    limits = range.split("-")
    return ( int(limits[0] ) , int(limits[1]))

def get_ranges(line):
    ranges = line.split(",")
    return ( get_range(ranges[0]) , get_range( ranges[1] ))

ranges = [ get_ranges(l) for l in lines ]
overlaps = [ detect_complete_overlap(r[0],r[1]) for r in ranges]
partial_overlaps = [ detect_partial_overlap(r[0],r[1]) for r in ranges]
print (len([overlap for overlap in overlaps if overlap]))
print (len([overlap for overlap in partial_overlaps if overlap]))