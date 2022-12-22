from hashlib import new
import re
filen="input.txt"
f = open(filen,"r")
lines = [ l.rstrip() for l in f.readlines()]

directions=['>','V','<','^']
current_dir=0
step_vec=[(1,0),(0,1),(-1,0),(0,-1)]
max_line_length=0
flat_pak=set()
cube_dim=50 if filen=="input.txt" else 4
def get_flat_pak_coord( coord ):
    return (coord[0]//cube_dim,coord[1]//cube_dim)

def add_vec_simpl( vec, offs):
    return (vec[0]+offs[0],vec[1]+offs[1])

def change_dir(current_dir,turn):
    if turn == 'L':
        new_dir=current_dir-1
        if new_dir==-1:
            return 3
        else:
            return new_dir
    else:
        new_dir=current_dir+1
        if new_dir==4:
            return 0
        else:
            return new_dir

def parse_row(lines,row_idx,map,row_specs,col_specs,cube_dim):
    global max_line_length
    line=lines[row_idx]
    start_col=len(line)- len(line.strip())
    end_col=len(line)
    row_specs[row_idx]=(start_col,end_col)
    max_line_length=max(max_line_length,len(line))
    
    for col_idx in range(start_col,end_col,1):
        flat_pak_coord=get_flat_pak_coord((col_idx,row_idx))
        flat_pak.add(flat_pak_coord)
        if line[col_idx] == "#":
            map.add((col_idx,row_idx))
        if col_idx in col_specs:
            col_specs[col_idx]=(min(row_idx,col_specs[col_idx][0]),max(row_idx+1,col_specs[col_idx][1]))
        else:
            col_specs[col_idx]=(row_idx,row_idx+1)

def parse_input( lines ):
    
    map=set()
    row_specs={}
    col_specs={}
    break_line=lines.index("")
    for row_idx in range(break_line):
        parse_row(lines,row_idx,map,row_specs,col_specs,cube_dim)
    path=lines[break_line+1]
    result=re.finditer(r"(([0-9]+)([LR])?)",path)
    path_arr=[ ( int(m.group(2)), m.group(3) ) for m in list(result)]
    return row_specs,col_specs,break_line,map,path_arr, cube_dim

def render_map( height, map, rowspec,trace,start_point):
    def get_map_tile_disp( coord ):
        if coord in map:
            return '#'
        elif coord in trace:
            return trace[coord]
        else:
            return '.'
    print(f'start_point={start_point}')
    for idx in range(100,110):#range(height):
        left_pad = " " * rowspec[idx][0]
        maprow_arr=[ get_map_tile_disp((col_idx,idx))for col_idx in range(rowspec[idx][0],rowspec[idx][1])]
        print(f'{left_pad}{"".join(maprow_arr)}   {idx}={rowspec[idx]}')

rowspecs, colspecs,breakline,map,path_spec,cube_dim = parse_input(lines)
start_point=(rowspecs[0][0],0)
trace={}

def addvec( pos,vec ):
    # test for wrapping
    new_loc = (pos[0]+vec[0],pos[1]+vec[1])
    #print(f'pos={pos} vec={vec} new_loc={new_loc}')
    if vec[0] == 0:
        #print(f'colspec={colspecs[pos[0]]}')
        
        loc_y_max=colspecs[pos[0]][1]
        loc_y_min=colspecs[pos[0]][0]
        #print(f'y: {loc_y_min} --> {loc_y_max}')
        if new_loc[1] >= loc_y_max:
            return (pos[0],loc_y_min),True
        if new_loc[1] < loc_y_min:
            return (pos[0],loc_y_max-1),True
        return new_loc,None
    elif vec[1] == 0:
        #print(f'rowspec={rowspecs[pos[1]]}')
        loc_x_max=rowspecs[pos[1]][1]
        loc_x_min=rowspecs[pos[1]][0]
        #print(f'x: {loc_x_min} --> {loc_x_max}')
        if new_loc[0] >= loc_x_max:
            return (loc_x_min,pos[1]),True
        if new_loc[0] < loc_x_min:
            return (loc_x_max-1,pos[1]),True
        return new_loc,False

FLIP=True
DONTFLIP=False
INVERT=True
DONTINVERT=False

SAMPLE_BOXES={
    (2,0):1,
    (0,1):2,
    (1,1):3,
    (3,1):4,
    (2,2):5,
    (3,2):6
}

SAMPLE_OFFSETS={
    box_no: (coord[0] * cube_dim,coord[1] * cube_dim) for coord,box_no in SAMPLE_BOXES.items() 
}

SAMPLE_OFFSETS_TR={box_no: (coord[0] + cube_dim -1,coord[1] ) for box_no,coord in SAMPLE_OFFSETS.items() }
SAMPLE_OFFSETS_BR={box_no: (coord[0] + cube_dim -1,coord[1] + cube_dim -1) for box_no,coord  in SAMPLE_OFFSETS.items() }
SAMPLE_OFFSETS_BL={box_no: (coord[0] ,coord[1]  + cube_dim -1) for box_no,coord in SAMPLE_OFFSETS.items() }

INPUT_BOXES={
    (1,0):1,
    (2,0):2,
    (1,1):3,
    (0,2):4,
    (1,2):5,
    (0,3):6
}

INPUT_OFFSETS={
    box_no: (coord[0] * cube_dim,coord[1] * cube_dim) for coord,box_no in INPUT_BOXES.items() 
}

INPUT_OFFSETS_TR={box_no: (coord[0] + cube_dim -1,coord[1] ) for box_no,coord in INPUT_OFFSETS.items() }
INPUT_OFFSETS_BR={box_no: (coord[0] + cube_dim -1,coord[1] + cube_dim -1) for box_no,coord  in INPUT_OFFSETS.items() }
INPUT_OFFSETS_BL={box_no: (coord[0] ,coord[1]  + cube_dim -1) for box_no,coord in INPUT_OFFSETS.items() }

def get_transition_sample( next_pos, start_dir ):
    fp_coord = get_flat_pak_coord(next_pos)
    box = SAMPLE_BOXES[fp_coord]
    diff_x = next_pos[0] % cube_dim
    diff_y = next_pos[1] % cube_dim
    if start_dir == 1:
        if box==1:
            # must have come from 5 - need to go to 2 invert and bounce direction
            return add_vec_simpl(SAMPLE_OFFSETS_BR[2],(-diff_x,0)),3,0
        elif box==3:
            # must have come from 3 need to go to 5 and invert and turn left
            return add_vec_simpl(SAMPLE_OFFSETS_BL[5],(0,-diff_x)),3,0
        elif box==2:
            # must have come from 2 need 
            return add_vec_simpl(SAMPLE_OFFSETS_BR[6],(-diff_x,0)),3,0
        elif box == 6:
            # must have come from 6 - go into top of 5 invert
            return add_vec_simpl(SAMPLE_OFFSETS_BR[5],(-diff_x,0)),3,0
        else:
            assert(False)
    elif start_dir == 0:
        if box == 1:
            return add_vec_simpl(SAMPLE_OFFSETS_BR[6],(0,-diff_y)),2,0
        elif box == 2:
            return add_vec_simpl(SAMPLE_OFFSETS_TR[6],(-diff_y,0)),1 ,0       
        elif box == 5:
            return add_vec_simpl(SAMPLE_OFFSETS_TR[1],(0,-diff_y)),1 ,0
        else:
            assert(False)
    elif start_dir ==2:
        if box == 1:
            return add_vec_simpl(SAMPLE_OFFSETS_TR[3],(0,-diff_y)),2,0
        elif box == 4:
            return add_vec_simpl(SAMPLE_OFFSETS_BR[6],(-diff_y,0)),3 ,0       
        elif box == 6:
            return add_vec_simpl(SAMPLE_OFFSETS_BR[3],(-diff_y,0)),1,0 
        else:
            assert(False)
    elif start_dir ==3:
        if box == 2:
            return add_vec_simpl(SAMPLE_OFFSETS_BR[1],(-diff_x,0)),1
        elif box == 3:
            return add_vec_simpl(SAMPLE_OFFSETS[1],(0,diff_x)),0,0       
        elif box == 5:
            return add_vec_simpl(SAMPLE_OFFSETS_TR[2],(-diff_x,0)),1 ,0
        else:
            assert(False)
    else:
        assert(False)



def get_transition_input( next_pos, start_dir ):
    fp_coord = get_flat_pak_coord(next_pos)
    box = INPUT_BOXES[fp_coord]
    diff_x = next_pos[0] % cube_dim
    diff_y = next_pos[1] % cube_dim
    #print(f'start_dir={start_dir} box={box}')
    if start_dir == 0:
        # 12
        # 3
        #45
        #6
        if box==1:
            # must have come from 2 
            return add_vec_simpl(INPUT_OFFSETS_BR[5],(0,-diff_y)),2,5
        elif box==3:
            # must have come from 3 need to go to 5 and invert and turn left
            return add_vec_simpl(INPUT_OFFSETS_BL[2],(diff_y,0)),3,2
        elif box==4:
            # must have come from 2 need 
            return add_vec_simpl(INPUT_OFFSETS_BR[2],(0,-diff_y)),2,2
        elif box == 6:
            # must have come from 6 - go into top of 5 invert
            return add_vec_simpl(INPUT_OFFSETS_BL[5],(diff_y,0)),3,5
        else:
            assert(False)
    elif start_dir == 1:
        if box == 1:
            return add_vec_simpl(INPUT_OFFSETS_TR[6],(0,diff_x)),2,6
        elif box == 2:
            return add_vec_simpl(INPUT_OFFSETS_TR[3],(0,diff_x)),2  ,3      
        elif box == 4:
            return add_vec_simpl(INPUT_OFFSETS[2],(diff_x,0)),1 ,2
        else:
            assert(False)
    elif start_dir ==2:
        if box == 2:
            return add_vec_simpl(INPUT_OFFSETS_BL[4],(0,-diff_y)),0,4
        elif box == 3:
            return add_vec_simpl(INPUT_OFFSETS[4],(diff_y,0)),1      ,4  
        elif box == 5:
            return add_vec_simpl(INPUT_OFFSETS_BL[1],(0,-diff_y)),0 ,1
        elif box == 6:
            return add_vec_simpl(INPUT_OFFSETS[1],(diff_y,0)),1 ,1
        else:
            assert(False)
    elif start_dir ==3:
        if box == 6:
            return add_vec_simpl(INPUT_OFFSETS[3],(0,diff_x)),0,3
        elif box == 5:
            return add_vec_simpl(INPUT_OFFSETS[6],(0,diff_x)),0,6  
        elif box == 2:
            return add_vec_simpl(INPUT_OFFSETS_BL[6],(diff_x,0)),3,6
        else:
            assert(False)
    else:
        assert(False)


def trace_path_segment(
    map,
    pathtrace,
    start_pos,
    start_dir,
    count,
    honour_walls=True):
    segvec=step_vec[start_dir]
    curpos=start_pos
    trace[curpos]=directions[start_dir]
    for step in range(count):
        nextpos,wrapped=addvec(curpos,segvec)
        #print(f'next_pos={nextpos}')
        tmp_start_dir=start_dir
        if wrapped:
            nextpos,start_dir,new_box=get_transition_input(nextpos,start_dir)
            #print(f'new_box={new_box}')
        if honour_walls and nextpos in map:
            #print("BLOCKED")
            return curpos,tmp_start_dir
        else:
            curpos=nextpos
            segvec=step_vec[start_dir]
            pathtrace[curpos]=directions[start_dir]
    return curpos,start_dir


def follow_path( 
    map, 
    pathspec, 
    trace,
    start_point, 
    current_dir ):
    new_dir=current_dir
    for idx,segment in enumerate(pathspec):
        print(f'{idx}: move {directions[current_dir]} for {segment[0]} steps - start_point={start_point} then {segment[1]}')
        start_point,new_dir=trace_path_segment(
            map,
            trace,
            start_point,
            current_dir,
            segment[0])
        
        #render_map(breakline,map,rowspecs,trace,start_point)
        if segment[1] is None:
            print(start_point)
            print(f'{start_point[1]+1} {(start_point[0]+ 1)} {current_dir}') 
            return 1000 * (start_point[1]+1) + 4 * (start_point[0]+ 1) + current_dir 
        else:
            #render_map(breakline,map,rowspecs,trace,start_point)
            current_dir=change_dir(new_dir,segment[1])

TOP_LEFT=(0,0)
TOP_RIGHT=(49,0)
BOTTOM_LEFT=(0,49)
BOTTOM_RIGHT=(49,49)

def get_coord(box,off,d=(0,0)):
    return (INPUT_OFFSETS[box][0]+off[0]+d[0],INPUT_OFFSETS[box][1]+off[1]+d[1])

# test_cases= [
    # ((75,0),3,3,None),
    # ((125,0),3,3,None),
    # ((149,25),0,3,None),
    # ((125,29),1,3,None),
    # ((99,75),0,3,None),
    # ((99,125),0,3,None),
    # ((75,149),1,3,None),
    # ((49,175),0,3,None),
    # ((25,199),1,3,None),
    # ((0,175),2,3,None),
    # ((0,125),2,3,None),
    # ((50,75),2,3,None),
    # ((50,25),2,3,None),
    # ((75,25),0,50,None),
    # ((75,25),1,50,None),
    # ((75,75),1,50,None),
    # ((75,125),3,50,None),
    # ((25,125),1,50,None),
    # ((25,175),1,50,None),
    # ((25,175),1,5000,None),
    # (get_coord(1,TOP_LEFT),3,1,get_coord(6,TOP_LEFT)),
    # (get_coord(1,TOP_RIGHT),3,1,get_coord(6,BOTTOM_LEFT)),
    # (get_coord(2,TOP_LEFT),3,1,get_coord(6,BOTTOM_LEFT)),
    # (get_coord(2,TOP_RIGHT),3,1,get_coord(6,BOTTOM_RIGHT)),
    # (get_coord(2,TOP_RIGHT),0,1,get_coord(5,BOTTOM_RIGHT)),
    # (get_coord(2,BOTTOM_RIGHT),0,1,get_coord(5,TOP_RIGHT)),
    # (get_coord(3,TOP_RIGHT),0,1,get_coord(2,BOTTOM_LEFT)),
    # (get_coord(3,BOTTOM_RIGHT),0,1,get_coord(2,BOTTOM_RIGHT)),
    # (get_coord(1,BOTTOM_LEFT),1,1,get_coord(3,TOP_LEFT)),
    # (get_coord(5,TOP_RIGHT),0,1,get_coord(2,BOTTOM_RIGHT)),
    # (get_coord(5,BOTTOM_RIGHT),0,1,get_coord(2,TOP_RIGHT)),
    # (get_coord(5,BOTTOM_LEFT),1,1,get_coord(6,TOP_RIGHT)),
    # (get_coord(5,BOTTOM_RIGHT),1,1,get_coord(6,BOTTOM_RIGHT)),
    # (get_coord(6,TOP_RIGHT),0,1,get_coord(5,BOTTOM_LEFT)),
    # (get_coord(6,BOTTOM_RIGHT),0,1,get_coord(5,BOTTOM_RIGHT)),
    # (get_coord(6,BOTTOM_LEFT),1,1,get_coord(2,TOP_LEFT)),
    # (get_coord(6,BOTTOM_RIGHT),1,1,get_coord(2,TOP_RIGHT)),
    # (get_coord(6,TOP_LEFT),2,1,get_coord(1,TOP_LEFT)),
    # (get_coord(6,BOTTOM_LEFT),2,1,get_coord(1,TOP_RIGHT)),
    # (get_coord(3,TOP_LEFT),2,1,get_coord(4,TOP_LEFT)),
    # (get_coord(3,BOTTOM_LEFT),2,1,get_coord(4,TOP_RIGHT)),
    # (get_coord(1,TOP_LEFT),2,1,get_coord(4,BOTTOM_LEFT)),
#     # (get_coord(1,BOTTOM_LEFT),2,1,get_coord(4,TOP_LEFT)),
#     # (get_coord(1,TOP_LEFT),3,5,get_coord(6,TOP_LEFT,(4,0))),
#     # (get_coord(1,TOP_RIGHT),3,5,get_coord(6,BOTTOM_LEFT,(4,0))),
#     # (get_coord(2,TOP_LEFT),3,5,get_coord(6,BOTTOM_LEFT,(0,-4) )),
#     # (get_coord(2,TOP_RIGHT),3,5,get_coord(6,BOTTOM_RIGHT,(0,-4) ))
#     # (get_coord(2,TOP_RIGHT),0,5,get_coord(5,BOTTOM_RIGHT,(-4,0))),
#     # (get_coord(2,BOTTOM_RIGHT),0,5,get_coord(5,TOP_RIGHT,(-4,0))),
#     (get_coord(3,TOP_RIGHT),0,5,get_coord(2,BOTTOM_LEFT,(0,-4))),
#     (get_coord(3,BOTTOM_RIGHT),0,5,get_coord(2,BOTTOM_RIGHT,(0,-4))),
#     # (get_coord(1,BOTTOM_LEFT),1,5,get_coord(3,TOP_LEFT)),
#     (get_coord(5,TOP_RIGHT),0,5,get_coord(2,BOTTOM_RIGHT,(-4,0))),
#     (get_coord(5,BOTTOM_RIGHT),0,5,get_coord(2,TOP_RIGHT,(-4,0))),
#     (get_coord(5,BOTTOM_LEFT),1,5,get_coord(6,TOP_RIGHT,(-4,0))),
#     (get_coord(5,BOTTOM_RIGHT),1,5,get_coord(6,BOTTOM_RIGHT,(-4,0))),
#     (get_coord(6,TOP_RIGHT),0,5,get_coord(5,BOTTOM_LEFT,(0,-4))),
#     (get_coord(6,BOTTOM_RIGHT),0,5,get_coord(5,BOTTOM_RIGHT,(0,-4))),
#     (get_coord(6,BOTTOM_LEFT),1,5,get_coord(2,TOP_LEFT,(0,4))),
#     (get_coord(6,BOTTOM_RIGHT),1,5,get_coord(2,TOP_RIGHT,(0,4))),
#     (get_coord(6,TOP_LEFT),2,5,get_coord(1,TOP_LEFT,(0,4))),
#     (get_coord(6,BOTTOM_LEFT),2,5,get_coord(1,TOP_RIGHT,(0,4))),
#     (get_coord(3,TOP_LEFT),2,5,get_coord(4,TOP_LEFT,(0,4))),
#     (get_coord(3,BOTTOM_LEFT),2,5,get_coord(4,TOP_RIGHT,(0,4))),
#     (get_coord(1,TOP_LEFT),2,5,get_coord(4,BOTTOM_LEFT)),
#     (get_coord(1,BOTTOM_LEFT),2,5,get_coord(4,TOP_LEFT)),
# ]

# for tc in test_cases:
#     new1_pos, dir1 = trace_path_segment(
#         map,{},tc[0],tc[1],tc[2],False
#     )
#     new2_pos , dir2= trace_path_segment(
#         map,{},new1_pos,(dir1+2)% 4,tc[2],False
#     )
#     new3_pos , dir3= trace_path_segment(
#         map,{},new2_pos,(dir2+2)% 4,tc[2],False
#     )
#     new4_pos , dir4= trace_path_segment(
#         map,{},new3_pos,(dir3+2)% 4,tc[2],False
#     )
#     if new4_pos == tc[0] :
#         if not tc[3] is None and tc[3] != new1_pos:
#             print(f'FAIL: expected={tc[3]} received={new1_pos}')
#         else:
#             print(f'PASS: {tc}')
#     else:
#         print(f'FAIL: {new4_pos} {dir4} {new2_pos} {dir4} CASE={tc}')

# path_spec=[
#    (32,"L"),(7,"R"),(29,"R")
# ]
# start_point=(29,106)
# current_dir=0
a = follow_path(map,path_spec,trace,start_point,current_dir)
#print(colspecs)
render_map(breakline,map,rowspecs,trace,start_point)
print(a)



