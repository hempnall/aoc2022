f = open("input.txt","r")
lines = [ line.strip() for line in f.readlines() ]
tree_visble=[
    [ False for tree in line]
        for line in lines
]
# tree_house_scores=[
#       [ 0 for tree in line]
#         for line in lines  
# ]

def get_tallest_tree_deets(ln):
    tallest_height=max(ln)
    return (tallest_height, ln.index(tallest_height))

def get_count_of_visible_trees_in_line(ln):
    deets=get_tallest_tree_deets(ln)

def process_row( row , rowidx):
    deets=get_tallest_tree_deets(row)
    max=-1
    for idx in range(deets[1]+1):
        if int(row[idx])>max:
            max=int(row[idx])
            tree_visble[rowidx][idx]=True
    max=-1
    for idx in range(len(row)-1,deets[1],-1):
        if int(row[idx])>max:
            max=int(row[idx])
            tree_visble[rowidx][idx]=True
    

def process_col( col , colidx):
    deets=get_tallest_tree_deets(col)
    max=-1
    for idx in range(deets[1]+1):
        if int(col[idx])>max:
            max=int(col[idx])
            tree_visble[idx][colidx]=True
    max=-1
    for idx in range(len(col)-1,deets[1],-1):
        if int(col[idx])>max:
            max=int(col[idx])
            tree_visble[idx][colidx]=True

for rowidx in range(len(lines)):
    process_row(lines[rowidx],rowidx)

for colidx in range(len(lines[0])):
    col=[ line[colidx] for line in lines ]
    process_col(col,colidx)

vis_in_rows=[ len( [ tree for tree in row if tree]) for row in tree_visble]

def score_in_direction(start_x,start_y,max_height, x_step,y_step):
    current_x = start_x + x_step
    current_y = start_y + y_step
    if current_x<0 or current_x==len(lines[0]):
        return 0
    if current_y<0 or current_y==len(lines):
        return 0
    height=int(lines[current_y][current_x])
    if height >= max_height:
        return 1 
    else:
        return 1 + score_in_direction(current_x,current_y,max_height,x_step,y_step)

def tree_score(x,y):
    height=int(lines[y][x])
    up_score=score_in_direction(x,y,height,0,-1)
    down_score=score_in_direction(x,y,height,0,1)
    left_score=score_in_direction(x,y,height,-1,0)
    right_score=score_in_direction(x,y,height,1,0)
    return up_score*down_score*left_score*right_score

tree_house_scores = [
    [ tree_score(x,y) for y in range(len(lines[0]))]
    for x in range(len(lines))
]

max_by_rows = [ max(row) for row in tree_house_scores ]
maxmax = max(max_by_rows)



print(maxmax)