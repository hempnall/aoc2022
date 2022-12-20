f = open("input.txt","r")
multiplier=811589153
#multiplier=1
lines = [ int(l)*multiplier for l in f.readlines() ]
print(f'no_of_lines={len(lines)}')

index_of_0=lines.index(0)

location_map=[ x for x in range(len(lines ))]
original_locations=[ x for x in range(len(lines ))]

def get_effective_array_element(idx):
    return lines[original_locations[idx]]

def get_effective_array():
    return [   
        get_effective_array_element(idx)
        for idx in range(len(lines))
    ]

modlen= len(lines)-1

def move_number_to_right(eff_idx,dist):
    for i in range(dist % len(lines)):
        first=(eff_idx + i) % len(lines)
        second=(eff_idx + i + 1) % len(lines)
        tmp_orig=original_locations[first]
        original_locations[first]=original_locations[second]
        location_map[tmp_orig] = (location_map[tmp_orig] + 1) % len(lines)
        location_map[original_locations[second]] = (location_map[tmp_orig] - 1) % len(lines)
        original_locations[second]=tmp_orig

def move_number_to_left(eff_idx,dist):
    for i in range(dist % (len(lines)-1)):
        first=(eff_idx - i ) % len(lines)
        second=(eff_idx - i -1) % len(lines)
        tmp_orig=original_locations[first]
        original_locations[first]=original_locations[second]
        location_map[tmp_orig] = (location_map[tmp_orig] - 1) % len(lines)
        location_map[original_locations[second]]= (location_map[tmp_orig] + 1) % len(lines)
        original_locations[second]=tmp_orig

def in_range( idx ):
    return idx % len(lines)

def swap_numbers(idx1,idx2):
    idx1_r=in_range(idx1)
    idx2_r=in_range(idx2)
    tmp_orig_loc=original_locations[idx1_r]
    original_locations[idx1_r]=original_locations[idx2_r]
    original_locations[idx2_r]=tmp_orig_loc
    tmp_loc_map=location_map[original_locations[idx1_r]]
    location_map[original_locations[idx1_r]]=location_map[original_locations[idx2_r]]
    location_map[original_locations[idx2_r]]=tmp_loc_map

def swap_numbers_in_range( start , end ):
    step=1 if end > start else -1 
    for idx in range(start,end,step):
        swap_numbers(idx,idx+step)

def move_number( lines, index ):
    number=lines[index]
    cur_pos_of_num=location_map[index]
    assert(get_effective_array_element(cur_pos_of_num)==number)
    if number == 0:
        return

    new_pos=get_move_params(cur_pos_of_num,len(lines),number)
    swap_numbers_in_range(cur_pos_of_num,new_pos) #(number % (len(lines)-1)))

def get_move_params(cur_pos,size,val):
    if val > 0:
        return (cur_pos + val) % (size -1)
    else:
        i = (cur_pos + val) % (size -1)
        if i == 0:
            return size-1
        else:
            return i

for itera in range(0,10):
    for idxs in range(len(lines)):
        move_number(lines,idxs)
        #eff_arr=get_effective_array()
    #assert(eff_arr == arrays[idxs])


eff_arr=get_effective_array()
print(eff_arr)

tests = [
    (0,7,1,1),
    (0,7,2,2),
    (1,7,-3,4),
    (2,7,3,5),
    (2,7,-2,6),
    (3,7,0,3),
    (5,7,4,3),
    (3,7,1,4),
    (1,7,-2,5)
]

for cur,sz,val,ex in tests:
    ac=get_move_params(cur,sz,val)
    if ac == ex:
        print(f'PASS: {(cur,sz,val,ex)}')
    else:
        print(f'FAIL: {(cur,sz,val,ex)} {ac}')


eff_arr=get_effective_array()

effective_array=get_effective_array()

idx=effective_array.index(0)
idx_1000= ( idx+1000 ) % len(lines)
idx_2000= ( idx+2000 ) % len(lines)
idx_3000= ( idx+3000 ) % len(lines)

print(f'idx_1000={idx_1000} val={effective_array[idx_1000]}')
print(f'idx_2000={idx_2000} val={effective_array[idx_2000]}')
print(f'idx_3000={idx_3000} val={effective_array[idx_3000]}')
print(effective_array[idx_1000] + effective_array[idx_2000] + effective_array[idx_3000] )
