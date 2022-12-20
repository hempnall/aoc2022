f = open("day20/input.txt","r")
lines = [ int(l) for l in f.readlines() ]
print(lines)
rel_pos_after_mixing=[0] * len(lines)

index_of_0=lines.index(0)

print(index_of_0)

def number_at_pos(lines,new_pos,pos):
    return lines[ new_pos[pos] ]



def move_number( lines, curr_arr , relative_pos, index ):
    number=lines[index]
    cur_pos_of_num=index + rel_pos_after_mixing[index]
    new_pos_for_number=cur_pos_of_num + number
    new_pos_of_num=0
    if new_pos_for_number > 0:
        new_pos_of_num=new_pos_for_number % len(lines)
    else:
        new_pos_of_num=len(lines) + ((cur_pos_of_num + number) % -len(lines)) -1
    print(new_pos_for_number)
    if new_pos_of_num > cur_pos_of_num:
        for idx in range(cur_pos_of_num,new_pos_of_num):
            relative_pos[idx+1]-=1
            effective_array[idx]=effective_array[idx+1]
        relative_pos[index]+= (new_pos_of_num - cur_pos_of_num)
        effective_array[new_pos_of_num]=number
    elif new_pos_of_num < cur_pos_of_num:
        for idx in range(cur_pos_of_num,new_pos_of_num+1,-1):
            relative_pos[idx-1]+=1
            effective_array[idx]=effective_array[idx-1]
        relative_pos[index] += (new_pos_of_num + 1- cur_pos_of_num)
        effective_array[new_pos_of_num+1]=number
    else:
        pass



#1, 2, -3, 3, -2, 0, 4
arrays=[
    [2, 1, -3, 3, -2, 0, 4],
    [1, -3, 2, 3, -2, 0, 4],
    [1, 2, 3, -2, -3, 0, 4],
    [1, 2, -2, -3, 0, 3, 4],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 4, 0, 3, -2]
]

effective_array=lines.copy()
for idx in range(0,7):
    if idx == 6:
        print()
    print(move_number(lines,effective_array,rel_pos_after_mixing,idx))
    print(f'effective_array={effective_array}')
    assert(effective_array == arrays[idx])

