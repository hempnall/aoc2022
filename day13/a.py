f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines()]

divider1=[[2]]
divider2=[[6]]

codes=[divider1,divider2]

def parse_file(lines):
    for line in lines:
        if line=="":
            continue
        item1=eval(line)
        codes.append(item1)

def code_comparer(code1,code2):
    return in_right_order((code1,code2))

def in_right_order(pair):
    type1int=type(pair[0])==int
    type2int=type(pair[1])==int
    # print(f'compare {pair[0]}')
    # print(f'with {pair[1]}')
    if type1int and type2int:
        diff = pair[0] - pair[1]
        if diff < 0:
            return 1
        elif diff > 0:
            return -1
        else:
            return 0
    elif type1int:
        return in_right_order(([pair[0]],pair[1]))
    elif type2int:
        return in_right_order((pair[0],[pair[1]]))
    else:
        for idx in range(len(pair[0])):
            if (idx+1) > len(pair[1]):
                # right side ran out of items
                return -1
            order = in_right_order((pair[0][idx],pair[1][idx]))
            if order != 0:
                return order
        # left side ran out of items
        if len(pair[0])==len(pair[1]):
            return 0
        else:
            return 1

from functools import cmp_to_key         
parse_file(lines)
print(codes)
sorted_codes=sorted(codes,key=cmp_to_key(code_comparer),reverse=True)
print(sorted_codes)
print(sorted_codes.index(divider1)+1)
print(sorted_codes.index(divider2)+1)
answer = (sorted_codes.index(divider1)+1) * (sorted_codes.index(divider2)+1)
print(answer)
# def run_test_case(idx,test_case):
#     expected=test_case[1]
#     order = expected #in_right_order(test_case[0])
#     reverse=(test_case[0][1],test_case[0][0])
#     order_reverse= in_right_order(reverse)
#     if order==expected and order_reverse == -expected:
#         print(f'{idx} PASS')
#     else:
#         print(f'{idx} FAIL {expected}!={order} or {-1 *expected}!={order_reverse}')

# testcases=[
#     # ((
#     #     [1,1,3,1,1],
#     #     [1,1,5,1,1]
#     # ),1),
#     ((
#         [[1],[2,3,4]],
#         [[1],4]
#     ),1),    
# ]

# for idx,test in enumerate(testcases):
#     run_test_case(idx,test)
