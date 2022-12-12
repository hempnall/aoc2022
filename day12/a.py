import sys

moves = {
    "^": (0,-1),
    ">": (1,0),
    "V": (0,1),
    "<": (-1,0)
}

f = open("sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def get_size_of_grid(lines):
    return (len(lines[0]),len(lines))

def get_distance_score_grid(size):
    return [ [ None ] * size[0] ] * size[1]

def get_render_grid(size):
    return [ [ '.' ] * size[0] ] * size[1]

def find_point(end_point_char):
    for row_idx in range(len(lines)):
        if end_point_char in lines[row_idx]:
            return (lines[row_idx].index(end_point_char),row_idx)
    raise Exception("end point not found")

def get_height(grid,pos):
    return ord(grid[pos[1]][pos[0]])

def is_move_possible(cur_pos,dir):
    move=moves(dir)
    next_pos=add_coord(cur_pos,move)
    if not (get_height(GRID,next_pos) - get_height(GRID,cur_pos)) in [0,1]:
        return False
    if next_pos[0] < 0 or next_pos >= GRID_SIZE[0]:
        return False
    if next_pos[1] < 0 or next_pos >= GRID_SIZE[1]:
        return False
    return True

def set_distance(coord,val):
    DISTANCES[coord[1]][coord[0]]=val

def add_coord(start,diff):
    return ( start[0]+diff[0], start[1]+diff[1])

def process_pos( start_pos, end_pos, cur_dist ):
    for (k,v) in moves.items():
        if not is_move_possible(start_pos,v):
            continue
        next_pos=add_coord(start_pos,v)

        process_pos(next_pos,end_pos,cur_dist+1)


GRID_SIZE=get_size_of_grid(lines)
GRID=lines
DISTANCES=get_distance_score_grid(GRID_SIZE)
start_point=find_point('S')
end_point=find_point('E')
print(f'{start_point} {end_point}')
process_pos( lines , start_point, end_point , 0)




