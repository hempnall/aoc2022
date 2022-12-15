is_real=True
limit_max=20
limit_min=0
f = open("sample.txt","r")
if is_real:
    f = open("input.txt","r")
    limit_max=4_000_000

lines = [ l for l in f.readlines() ]
target_row=10
#target_row=2_000_000
S=0
B=1
impossible_locations=set()
sensors=set()
beacons=set()

def get_sensor_beacons(line):
    def get_coord(arr,idx,rtr=True):
        if rtr:
            return int(arr[idx][2:-1])
        else:
            return int(arr[idx][2:])
    parts=line.split()
    return (
        (get_coord(parts,2),get_coord(parts,3)),
        (get_coord(parts,8),get_coord(parts,9,False))
    )

def manhattan_distance(sensor,beacon):
    return abs(sensor[0]-beacon[0]) + abs(sensor[1]-beacon[1])

def get_x_range_on_row(row,sensor,beacon):
    distance=manhattan_distance(sensor,beacon)
    row_diff=abs(row-sensor[1])
    if distance > row_diff:
        x_diff=abs(distance-row_diff)
        return (max(limit_min,sensor[0]-x_diff),min(limit_max,sensor[0]+x_diff))
    else:
        return None

def make_sets():
    source_data = [ get_sensor_beacons(line) for line in lines ]
    for data in source_data:
        sensors.add(data[S])
        beacons.add(data[B])
    return source_data

def render(st,en,row):
    for r in range(row-2,row+2,1):
        for c in range(st,en+1,1):
            if (c,r) in beacons:
                print("B",end="")
            elif (c,r) in sensors:
                print("S",end="")
            elif r==row and c in impossible_locations:
                print("#",end="")
            else:
                print(f'.',end="")
        print(f'  {en}')


source_data=make_sets()
#distances = [ manhattan_distance(p[S],p[B]) for p in source_data]
# ranges = [ get_x_range_on_row(target_row,source_data[idx][S],source_data[idx][B]) for idx in range(len(distances))]

def run_test( test_case):
    rng=get_x_range_on_row(test_case[2],test_case[0],test_case[1])
    if rng==test_case[3]:
        print("PASS")
    else:
        print(f'FAIL s={test_case[0]} b={test_case[1]} r={test_case[2]} e={test_case[3]} != {rng}')

# 0 = sensor, 1=beacon, 2=row, 3=expected
# test_beacons= [
#     ((10,10),(5,10),10,(5,15)),
#     ((10,10),(6,9),10,(5,15)),
#     ((10,10),(10,5),10,(5,15)),
#     ((10,10),(11,6),10,(5,15)),
#     ((10,10),(15,10),10,(5,15)),
#     ((10,10),(14,11),10,(5,15)),
#     ((10,10),(10,15),10,(5,15)),
#     ((10,10),(9,14),10,(5,15)),
#         ((10,10),(9,14),17,None),

def calc_freq(col,row):
    return 4000000 * col + row

def is_cand_in_ranges(cand,ranges):
    for subr in ranges:
        if candidate >= subr[0] and candidate<=subr[1]:
            return True
    return False


for row in range(1,limit_max+1):
    all_ranges = [ get_x_range_on_row(row,source_data[idx][S],source_data[idx][B]) for idx in range(len(source_data)) ]
    ranges = [ r  for r in all_ranges if not r is None]
    sorted_ranges=sorted(ranges)
    padded_sorted_ranges=[(-2,-1),*sorted_ranges,(limit_max+1,limit_max+2)]
    for idx in range(0,len(padded_sorted_ranges)-1):
        #print(padded_sorted_ranges[idx])
        if (padded_sorted_ranges[idx][1] + 2) == (padded_sorted_ranges[idx+1][0]):
            candidate = padded_sorted_ranges[idx][1] +1
            if is_cand_in_ranges(candidate,ranges):
                continue
            print(f'{idx+1} {row} {padded_sorted_ranges[idx][1] +1} {calc_freq(padded_sorted_ranges[idx][1] +1,row)}')
            exit()


    # for srange in ranges:
    #     if not srange is None:
    #         for loc in range(srange[0],srange[1]+1):
    #             if not (loc,target_row) in beacons:
    #                 impossible_locations.add(loc)

# render(-3,25,10)

# print(sorted(list(impossible_locations)))
# print(distances)
# print(ranges)
print (len(list(impossible_locations)))

