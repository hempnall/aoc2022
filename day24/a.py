import sys
import math
from threading import currentThread 
f = open("input.txt","r")
print(sys.setrecursionlimit(20000))
lines = [ l.strip() for l in f.readlines() ]
height=len(lines)-2
width=len(lines[0])-2
depth_period=700 #height*width #// math.gcd(height,width)
options=[(0,0),(1,0),(-1,0),(0,1),(0,-1)]
start_options=[(0,0),(0,1)]
blizzard_dir="><v^"
start_pos=(0,-1)
me_loc=(0,start_pos) # at start time=0 , and i'm at 0,-1
end_loc=(width-1,height)
#end_loc=(2,1)
print(f'start_loc={start_pos} end_loc={end_loc} height={height} width={width}')

class Blizzard:
    def __init__(self,start_loc,dir,art):
        self.location=start_loc
        self.dir=dir
        self.dirart=art
    def location_after_n(self,n):
        return ((self.location[0] + n * self.dir[0]) % width,(self.location[1] + n * self.dir[1]) % height)
    def blizzard_after_n(self,n):
        new_loc=self.location_after_n(n)
        return Blizzard(new_loc,self.dir)
    def __repr__(self):
        return f'loc={self.location} dir={self.dir}'

def parse_file(lines):
    blizzards=[]
    for row_idx in range(1,height+1):
        for col_idx in range(1,width+1):
            dir=lines[row_idx][col_idx] 
            if dir in blizzard_dir:
                loc=(col_idx-1,row_idx-1)
                vec_idx=blizzard_dir.index(dir)+1
                blizzards.append(Blizzard(loc,options[vec_idx],dir))
    return blizzards

def make_maze(blizzards,period):
    maze={}
    for minute in range(period):
        maze[minute]={}
        for blizzard in blizzards:
            location_at_minute=blizzard.location_after_n(minute)
            if not location_at_minute in maze[minute]:
                maze[minute][location_at_minute]=[blizzard.dirart]
            else:
                maze[minute][location_at_minute].append([blizzard.dirart])

    return maze

def render_maze(maze,minute,current_loc=None):
    maze_min=maze[minute]
    if current_loc in maze_min:
        print(f'*** ERROR *** {current_loc}' )
        exit(1)
    else:
        for row in range(height):
            for col in range(width):
                coord=(col,row)
                if coord==current_loc:
                    print('E',end='')
                else:
                    if coord in maze_min:
                        blizzard_count=len(maze_min[coord])
                        if blizzard_count==1:
                            print(maze_min[coord][0],end='')
                        else:
                            if blizzard_count > 9:
                                print('+',end='')
                            else:
                                print(blizzard_count,end='')
                        
                    else:
                        print('.',end='')
            print()
        print()



blizzards=parse_file(lines)
maze=make_maze(blizzards,depth_period)
print("maze_constructed")
min_time=None
dead_end_cache=set()

def search_maze(
    destination,
    minute,
    start_loc,
    move_st,
    still_minutes):

    global min_time,destinations,maze

    loc=start_loc
    wrapped_minute=minute % depth_period
    
    if loc == destination:
        if min_time is None:
            min_time=len(move_st)
        else:
            min_time=min(len(move_st),min_time)
        return False

    if not loc in [ start_pos , end_loc]:
        if loc[0] < 0 or loc[0]>=width:
            return True
        if loc[1] < 0 or loc[1]>=height:
            return True

    if loc in maze[wrapped_minute]:
        return True

    if still_minutes > depth_period:
        return True

    is_dead_end=True
    for move in options:
        cache_key=(wrapped_minute,loc,move,destination)
        if not cache_key in dead_end_cache:
            if move == (0,0):
                still_minutes+=1
            next_loc=(loc[0] + move[0],loc[1] + move[1])
            search_maze(
                destination,
                minute+1,
                next_loc,
                [*move_st,move],
                still_minutes)
            dead_end_cache.add(cache_key)

def render_path(loc,path):
    for mint, move in enumerate(path):
        print(f'minute={mint} move={move}')
        loc=(loc[0]+move[0],loc[1]+move[1])
        render_maze(maze,mint,loc)

current_minute=0
search_cache_end={}

move_st=[(0,0)]
destinations=[end_loc,start_pos,end_loc]
current_dest=0

for j in range(0,3):
    print(f'{j}')
    min_time=None
    move_st=[(0,0)]
    dead_end_cache=set()
    search_maze(
        end_loc if j in [0,2] else start_pos,
        current_minute,
        start_pos if j in [0,2] else end_loc,
        move_st,
        0)
    current_minute+=(min_time-(1+j))
    print(current_minute)
print(f'dist={min_time}')
# total=min_time-1
# min_time=None
# move_st=[(0,0)]
# search_maze(
#     start_pos,
#     221,
#     end_loc,
#     move_st,
#     0)
# print(min_time-1)
# move_st=[(0,0)]
# total+=(min_time-1)
# print(f'dist={total}')
# min_time=None
# tmp_min_time=min_time
# min_time=None
# total=0
# move_st=[(0,0)]
# min_time=None
# search_maze(
#     end_loc,
#     41,
#     start_pos,
#     move_st,
#     0)
# total+=(min_time-1)
# print(f'dist={total}')






