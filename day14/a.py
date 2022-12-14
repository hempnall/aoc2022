f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
sand_source=(500,0)

cave_map={}
max_depth=0
sand_start=(500,0)

def get_cave_bounds(includeSandSource=False):
    context=2
    depths=[ k[1] for k in cave_map ]
    horiz_posez=[ k[0] for k in cave_map ]
    if includeSandSource:
        depths.append(0)
        horiz_posez.append(500)
    return (
        (min(horiz_posez)-context,max(horiz_posez)+context),
        (0,max(depths))
    )

def render_cave():
    cave_bounds=get_cave_bounds(True)
    print(f'horiz_range={cave_bounds[0]} vert_range={cave_bounds[1]} max_depth={max_depth}')
    for y_idx in range(cave_bounds[1][0],cave_bounds[1][1]+4):
        for x_idx in range(cave_bounds[0][0],cave_bounds[0][1]+1):
            cave_loc=(x_idx,y_idx)
            if cave_loc in cave_map:
                print(cave_map[cave_loc],end="")
            elif cave_loc == sand_start:
                print("+",end="")
            elif y_idx==(max_depth+2):
                print("#",end="")
            else:
                print(".",end="")
        print()

def drawline(start,end):
    global max_depth
    def inclusive_range(s,e):
        if s>e:
            return range(e,s+1)
        elif s<e:
            return range(s,e+1)
        else:
            return [s]
    x_range=inclusive_range(start[0],end[0])
    y_range=inclusive_range(start[1],end[1])
    for x in x_range:
        for y in y_range:
            if y>max_depth:
                max_depth=y
            cave_map[(x,y)]='#'

def construct_cave():
    for line in lines:
        new_line = line.replace("->","),(")
        co_ord_array_str=f'[({new_line})]'
        coords=eval(co_ord_array_str)
        for idx in range(len(coords)-1):
            drawline(coords[idx],coords[idx+1])

def coord_in_cavemap(coord):
    return (coord[1]==max_depth+2) or coord in cave_map 

# returns None if drops to infinity
def next_sand(coord):
    down=(coord[0],coord[1]+1)
    downleft=(coord[0]-1,coord[1]+1)
    downright=(coord[0]+1,coord[1]+1)
    if not coord_in_cavemap(down):
        return next_sand(down)
    elif not coord_in_cavemap(downleft):
        return next_sand(downleft)
    elif not coord_in_cavemap(downright):
        return next_sand(downright)
    else:
        return coord
        

construct_cave()

while not sand_start in cave_map:
    sand_loc=next_sand(sand_start)
    cave_map[sand_loc]='o'

render_cave()
answer = sum(1 for v in cave_map.values() if v =="o")
print(answer)
