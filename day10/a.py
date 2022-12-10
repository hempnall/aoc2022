f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

checkpoints=[40,80,120,160,200,240]
accumulator=0
micro_instructions=[]
x_register=1

def clock_cycle_check():
    pass

def get_micro_instructions(line,idx):
    if line.startswith("noop"):
        return [(1,0,line,idx)]
    elif line.startswith("addx"):
        return [(1,0,line,idx),(2,int(line.split(" ")[1]),line,idx)]

def expand_instructions(lines):
    global micro_instructions
    for idx in range(len(lines)):
        line_micro_instructions=get_micro_instructions(lines[idx],idx+1)
        micro_instructions = [*micro_instructions, *line_micro_instructions ]

def draw_pixel(clock_cycle,x_reg):
    end_line=""
    col=clock_cycle % 40
    if col== 0:
        end_line="\n"
    sprite_pos=[x_register-1,x_register,x_register+1]
    char_to_draw="."
    if (col-1) in sprite_pos:
        char_to_draw="#"
    print(char_to_draw, end=end_line)

def process_instructions(insts):
    global accumulator, x_register
    for idx in range(len(insts)):
        if (idx + 1) in checkpoints:
            increase = (idx + 1) * x_register
            accumulator += increase
        draw_pixel(idx+1,x_register)
        x_register+=insts[idx][1]

expand_instructions(lines)
process_instructions(micro_instructions)
print (accumulator)