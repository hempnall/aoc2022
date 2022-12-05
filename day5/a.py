f = open("input.txt","r")
lines = f.readlines()

def prepare_stacks(lines,base,top,count):
    stacks = {}
    for stk in range(0,count):
        stacks[stk+1]=[]
        col=1 + (stk * 4)
        for lineno in range(base-1,top-1,-1):
            crate = lines[lineno][col]
            if crate != ' ':
                stacks[stk+1].append(crate)
    return stacks

def get_instruction(line):
    parts = line.split(" ")
    return ( int(parts[1]), int(parts[3]), int(parts[5]))

def get_instructions(lines,first):
    instructions=lines[first:]
    return [ get_instruction(line.strip()) for line in instructions ]

def enact_instruction(stacks, src,dest,count):
    print("move %d from %d to %d\n" % (count,src,dest))
    for idx in range(0,count):
        crate=stacks[src].pop()
        stacks[dest].append(crate)

def enact_instruction9001(stacks, src,dest,count):
    print("move %d from %d to %d\n" % (count,src,dest))
    temp_stack=[]
    for idx in range(0,count):
        crate=stacks[src].pop()
        temp_stack.append(crate)
    for idx in range(0,count):
        crate=temp_stack.pop()
        stacks[dest].append(crate)

def enact_instructions(insts,stacks):
    for inst in insts:
        enact_instruction(stacks,inst[1],inst[2],inst[0])

def enact_instructions9001(insts,stacks):
    for inst in insts:
        enact_instruction9001(stacks,inst[1],inst[2],inst[0])

def get_tops(stacks,count):
    pass

stacks = prepare_stacks(lines,8,0,9)
instructions = get_instructions(lines,10)
enact_instructions9001(instructions,stacks)
print(stacks)
tops=get_tops(stacks,9)
print(tops)

# TPFFBDRJD