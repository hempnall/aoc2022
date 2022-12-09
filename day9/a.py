f = open("input.txt","r")
lines=[ l.strip() for l in f.readlines() ]
def step_tuple(l):
    return (l[0],int(l[1]))
steps=[ step_tuple(l.split(" ")) for l in lines ]

head_pos=(0,0)
tail_pos=head_pos

tail_pos_set=set()
tail_pos_set.add(tail_pos)

def move_tail(head_pos,tail_pos):
    diff_vect=(head_pos[0]-tail_pos[0],head_pos[1]-tail_pos[1])
    if abs(diff_vect[0])<2 and abs(diff_vect[1]<2):
        return tail_pos

    new_x_pos=tail_pos[0]
    new_y_pos=tail_pos[1]

    if diff_vect[0] == 2:
        new_x_pos += 1
        new_y_pos = head_pos[1]
            
    if diff_vect[0] == -2:
        new_x_pos -= 1
        new_y_pos = head_pos[1]

    if diff_vect[1] == 2:
        new_y_pos += 1
        new_x_pos = head_pos[0]

    if diff_vect[1] == -2:
        new_y_pos -= 1  
        new_x_pos = head_pos[0]

    return (new_x_pos,new_y_pos)


for step in steps:
    print()
    print(f'move = {step}')
    for idx in range(step[1]):
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


print("head_pos")
print(str(head_pos))
print("tail_pos")
print( str(tail_pos))
print(tail_pos_set)
print(len(list(tail_pos_set)))