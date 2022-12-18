f = open("input.txt","r")
lines=f.readlines()
line=lines[0].strip()
BIGNUM=1_000_000_000_000

shapes = [
    [ (2,3),(3,3),(4,3),(5,3) ] ,
    [ (3,3),(3,4),(3,5),(2,4),(4,4) ],
    [ (2,3),(3,3),(4,3),(4,4),(4,5)],
    [ (2,3),(2,4),(2,5),(2,6)],
    [ (2,3),(3,3),(3,4),(2,4)]
]
vectors={
    '<': (-1,0),
    'V': (0,-1),
    '>': (1,0)
}

floor=0
shape_count=len(shapes)
gusts_len=len(line)
initial_height=10
current_gust=0
brick_guage=[]
brick_guage_rev={}

def render(still_rocks,current_shape,summit,bottom_row=-1):
    start_height=max(initial_height,summit)
    print(f'height={start_height} summit={summit}')
    for h in range(start_height,bottom_row,-1):
        print('|',end='')
        for w in range(7):
            if (w,h) in still_rocks:
                print('#',end='')
            elif (w,h) in current_shape:
                print('@',end='')
            else:
                print('.',end='')
        if h in brick_guage_rev:
            print(f'| {h+1} {brick_guage_rev[h]}')
        else:
            print(f'| {h+1}')
    print('---------')

def new_shape(idx,summit):
    shape = shapes[idx % shape_count]
    return [ (x,y+summit) for x,y in shape  ]

def is_collision(shp,still_rocks):
    for pixel in shp:
        if pixel[1] == -1:
            return True
        if pixel[0] in [-1,7]:
            return True
        if pixel in still_rocks:
            return True
    return False

def is_stop(shp,still_rocks):
    for pixel in shp:
        if pixel[1]==-1:
            return True
        if pixel in still_rocks:
            return True
    return False

def animate_shape(shp,vector):
    return [ (x+vector[0],y+vector[1]) for x,y in shp]

def apply_gust(shp,key):
    vector=vectors[key]
    #print(f'applying gust={key}')
    return animate_shape(shp,vector)

def game_loop(still_rocks,current_shape,frame,summit):

    current_shape_index=0
    gust_idx=0

    def refresh_shape(current_shape, current_shape_index,summit):
        #print("**** NEW SHAPE *****")

        for x,y in current_shape:
            summit=max(y+1,summit)
            still_rocks.add((x,y))

        brick_guage.append(summit)
        current_shape_index+=1
        if not (summit-1) in brick_guage_rev:
            brick_guage_rev[summit-1]=[current_shape_index]
        else:
            brick_guage_rev[summit-1].append(current_shape_index)

        return (current_shape_index,summit,new_shape(current_shape_index,summit))

    while current_shape_index<7000:
        gust=line[gust_idx % len(line)]
        gust_idx+=1
        tmp_shp=apply_gust(current_shape,gust)
        if not is_collision(tmp_shp,still_rocks):
            tmp_shp2=apply_gust(tmp_shp,'V')
            if not is_stop(tmp_shp2,still_rocks):
                current_shape=tmp_shp2
            else:
                current_shape_index,summit,current_shape=refresh_shape(tmp_shp,current_shape_index,summit)
        else:
            #print("** GUST HAS NO EFFECT **")
            tmp_shp=apply_gust(current_shape,'V')
            if not is_stop(tmp_shp,still_rocks):
                current_shape=tmp_shp
            else:
                current_shape_index,summit,current_shape=refresh_shape(current_shape,current_shape_index,summit)

def compare_areas(still_rocks,start_height,period):
    if period == 1:
        return False
    for diff in range(period):
        for w in range(7):
            start_per_coord=(w ,start_height + diff)
            end_per_coord=(w,start_height + period + diff)
            if start_per_coord in still_rocks and not end_per_coord in still_rocks:
                return False
            if start_per_coord not in still_rocks and end_per_coord in still_rocks:
                return False
    return True


def find_period(
    still_rocks,
    start_initial_search,
    max_initial_search,
    min_period_len,
    max_period_len):
    if min_period_len == max_period_len:
        return
    if start_initial_search == max_initial_search:
        return
    for start in range(start_initial_search,max_initial_search):
        #show_pct(start_initial_search,max_initial_search,start)
        for per in range(min_period_len,max_period_len):
            if compare_areas(still_rocks,start,per):
                print(f'start={start} per={per}')
                return start+1,per

still_rocks=set()
current_shape=new_shape(0,0)
game_loop(still_rocks,current_shape,0,0)
render(still_rocks,current_shape,4000)

# start,per = find_period(
#     still_rocks,
#     10,1_000_000,20,20000)
start,per = 210 , 2659
print(f'found period start_idx={start} len={per}')
for hm in range(3):
    h1 = start + hm * per 
    h2 = start + (hm + 1) * per
    # print(f'height={h1} bricks={brick_guage_rev[h2]} diff={brick_guage_rev[h2][0]-brick_guage_rev[h1][0]}')
    # print(f'height_per_per={h2-h1}')

bricks_to_reach_start=brick_guage_rev[start]
height_at_start=start
print(f'bricks_to_reach_start={bricks_to_reach_start}')
print(f'height_at_start={height_at_start}')
bulk= (BIGNUM - bricks_to_reach_start[0])
print(f'bulk={bulk}')
bricks_per_per=1725 #max(brick_guage_rev[start + per -2])-max(brick_guage_rev[start  -2])
height_per_per=2659
number_of_per_repeats=bulk // bricks_per_per
print(f'number_of_repeats={number_of_per_repeats}')
print()
leftover=bulk % bricks_per_per
print(f'leftover={leftover}')
height_at_start_per=brick_guage[bricks_to_reach_start[0]-2]
height_at_per_1469=brick_guage[bricks_to_reach_start[0]-1+leftover]
print(f'height_at_start_per={height_at_start_per}')
print(f'brick_guage_to_reach_1469={height_at_per_1469}')
height_diff_1469=height_at_per_1469-height_at_start_per
height_before_left_over=210 + number_of_per_repeats * height_per_per
print(height_before_left_over)
print(height_before_left_over+height_diff_1469)
print(brick_guage[1598:1602])
# print(height_at_start + number_of_per_repeats * per)

