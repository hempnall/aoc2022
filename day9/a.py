f = open("input.txt","r")
lines=[ l.strip() for l in f.readlines() ]
def step_tuple(l):
    return (l[0],int(l[1]))
steps=[ step_tuple(l.split(" ")) for l in lines ]

tail_pos_set=set()

knot_positions = [
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0),
    (0,0)
]

moves={
    (-2,1): (-1,1),
    (-1,2): (-1,1),
    (0,2): (0,1),
    (1,2): (1,1),
    (2,1): (1,1),
    (2,0): (1,0),
    (2,-1): (1,-1),
    (1,-2): (1,-1),
    (0,-2): (0,-1),
    (-1,-2): (-1,-1),
    (-2,-1): (-1,-1),
    (-2,0): (-1,0),
    (-2,-2): (-1,-1),
    (2,2): (1,1),
    (-2,2): (-1,1),
    (2,-2): (1,-1)
}

def move_tail(head_pos,tail_pos):
    diff_vect=(head_pos[0]-tail_pos[0],head_pos[1]-tail_pos[1])
    if not diff_vect in moves:
        return (tail_pos)
    else:
        move=moves[diff_vect]
        #print(f'head_pos={head_pos} tail_pos={tail_pos} diff_vect={diff_vect} move={move}')
        return (tail_pos[0] + move[0],tail_pos[1]+move[1])

def move_knot(knot_pos,move):
    return (knot_pos[0]+move[0],knot_pos[1]+move[1])

for step in steps:
    print()
    print(f'move = {step}')
    for idx in range(step[1]):   ## how many steps are we taking?
        print(f'- step {idx+1}')
        head_pos=knot_positions[0]
        if step[0] == "R":
            head_pos=move_knot(head_pos,(1,0))
        elif step[0] == "U":
            head_pos=move_knot(head_pos,(0,1))
        elif step[0] == "D":
            head_pos=move_knot(head_pos,(0,-1))
        elif step[0] == "L":
            head_pos=move_knot(head_pos,(-1,0))
        else:
            raise Exception("invalid command")
        print(f'new head pos={head_pos}')
        knot_positions[0]=head_pos
        for knot_idx in range(1,len(knot_positions)):
            head_pos=knot_positions[knot_idx-1]
            tail_pos=knot_positions[knot_idx]
            #print(f'idx={idx} head_pos={head_pos} tail_pos={tail_pos}')
            knot_positions[knot_idx]=move_tail(head_pos,tail_pos)
            #print(f'idx={knot_idx} new_head_pos={knot_positions[knot_idx-1]} new_tail_pos={knot_positions[knot_idx]}')
            tail_pos_set.add(knot_positions[9])

print(len(list(tail_pos_set)))
