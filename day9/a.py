f = open("input.txt","r")
lines=[ l.strip() for l in f.readlines() ]
def step_tuple(l):
    return (l[0],int(l[1]))
steps=[ step_tuple(l.split(" ")) for l in lines ]

head_pos=(0,0)
tail_pos=head_pos

tail_pos_set=set()
tail_pos_set.add(tail_pos)

moves={
    (-2,1): (-1,1),
    (-1,2): (-1,1),
    (0,2): (0,1),
    (1,2): (1,1),
    (2,1): (1,1),
    (2,0): (1,0),
    (2,-1): (1,-1),
    (1,-2): (-1,-1),
    (0,-2): (0,-1),
    (-1,-2): (-1,-1),
    (-2,-1): (-1,-1),
    (-2,0): (-1,0)
}

def move_tail(head_pos,tail_pos):
    diff_vect=(head_pos[0]-tail_pos[0],head_pos[1]-tail_pos[1])
    if not diff_vect in moves:
        return (tail_pos)
    else:
        move=moves[diff_vect]
        print(f'head_pos={head_pos} tail_pos={tail_pos} move={move}')
        return (tail_pos[0] + move[0],tail_pos[1]+move[1])


for step in steps:
    print()
    print(f'move = {step}')
    for idx in range(step[1]):
        print(f'idx={idx}')
        if step[0] == "R":
            head_pos=(head_pos[0]+1,head_pos[1])
        elif step[0] == "U":
            head_pos=(head_pos[0],head_pos[1]+1)
        elif step[0] == "D":
            head_pos=(head_pos[0],head_pos[1]-1)
        elif step[0] == "L":
            head_pos=(head_pos[0]-1,head_pos[1])
        else:
            raise Exception("invalid command")
        print(f'head_pos={head_pos} tail_pos={tail_pos}')
        tail_pos=move_tail(head_pos,tail_pos)
        print(f'new_tail_pos={tail_pos}')
        tail_pos_set.add(tail_pos)
    sanity_check=(head_pos[0]-tail_pos[0],head_pos[1]-tail_pos[1])
    if abs(sanity_check[0])>1 or abs(sanity_check[1])>1:
        print(f'head={head_pos} tail={tail_pos} sanity={sanity_check}')
        raise Exception("NOT SANE!!!!")


print("=======head_pos")
print(str(head_pos))
print("tail_pos")
print( str(tail_pos))
print(tail_pos_set)
print(len(list(tail_pos_set)))