import sys
print(sys.setrecursionlimit(20000))
moves = {
    "^": (0,-1),
    ">": (1,0),
    "V": (0,1),
    "<": (-1,0)
}

f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def get_size_of_grid(lines):
    return (len(lines[0]),len(lines))

def get_distance_score_grid(size):
    return [ [ None ] * size[0]  for _ in range(size[1]) ]

def get_render_grid(size):
    return [ [ '.' ] * size[0] ] * size[1]

def find_point(end_point_char):
    for row_idx in range(len(lines)):
        if end_point_char in lines[row_idx]:
            return (lines[row_idx].index(end_point_char),row_idx)
    raise Exception("end point not found")

def get_height(grid,pos):
    letter = grid[pos[1]][pos[0]]
    if letter == 'S':
        return ord('a')
    if letter == 'E':
        return ord('z')
    return ord(letter)

def is_location_valid(loc):
    if loc[0] < 0 or loc[0] >= GRID_SIZE[0]:
        return False
    if loc[1] < 0 or loc[1] >= GRID_SIZE[1]:
        return False
    return True

def get_gradient(start_pos,end_pos):
    return get_height(GRID,end_pos) - get_height(GRID,start_pos)

def set_distance(coord,val):
    DISTANCES[coord[1]][coord[0]]=val

def get_distance(coord):
    return DISTANCES[coord[1]][coord[0]]

def add_coord(start,diff):
    return ( start[0]+diff[0], start[1]+diff[1])

def debug(cur_pos):
    context_size=5
    x_range=range(cur_pos[0]-context_size,cur_pos[0]+context_size)
    y_range=range(cur_pos[1]-context_size,cur_pos[1]+context_size)
    debug_out=[
        [ f'{DISTANCES[y_idx][x_idx]}-{GRID[y_idx][x_idx]}' if is_location_valid((x_idx,y_idx)) else 'X' for x_idx in x_range ]
            for y_idx in y_range
    ]
    for row in debug_out:
        print(row)

def process_pos( prev_pos , start_pos, end_pos, cur_dist ):
    set_distance(start_pos,cur_dist)
    if get_height(GRID,start_pos) == ord('a'):
        return cur_dist
    scores=[9999999]
    for (k,v) in moves.items():
        next_pos=add_coord(start_pos,v)
        if next_pos == prev_pos:
            continue
        if not is_location_valid(next_pos):
            continue 
        gradient=get_gradient(start_pos,next_pos)
        if gradient < -1:
            continue
        next_pos_dist=get_distance(next_pos)
        if next_pos_dist is None or next_pos_dist > (cur_dist+1):
            scores.append(process_pos(start_pos, next_pos,end_pos,cur_dist+1))
    # print("========")
    # debug(start_pos)
    return(min(scores))
    raise Exception(f'never found End')

def render_scores():
    for row in range(GRID_SIZE[1]):
        print(DISTANCES[row])

GRID_SIZE=get_size_of_grid(lines)
GRID=lines
DISTANCES=get_distance_score_grid(GRID_SIZE)

start_point=find_point('E')
end_point=find_point('S')
print(f'GRIDSIZE={GRID_SIZE} start={start_point} end={end_point}')
dist=process_pos(  None, start_point, end_point , 0)
print(dist)
#render_scores()






