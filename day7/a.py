f=open("input.txt","r")
lines=[ l.strip() for l in f.readlines()]

dir_stack=[]
dir_sizes={}

def dir_size(lines,idx):
    pass

def add_size_to_dir(size):
    for dir in dir_stack:
        pass

def directory_key(size):
    pass

def process_cd(str):
    if str == "..":
        last_dir=dir_stack.pop()
    else:
        dir_stack.append(str)
    current_dir="_".join(dir_stack)

def post_file_size(size):
    for depth in range(len(dir_stack)):
        dir_key="_".join(dir_stack[:depth+1])
        if not dir_key in dir_sizes:
            dir_sizes[dir_key]=size
        else:
            dir_sizes[dir_key]+=size

def process_command(str):
    if str.startswith("ls"):
        pass
    elif str.startswith("cd"):
        process_cd(str[2:].strip())
    else:
        raise Exception("unknown command " + str)

for line in lines:
    if line[0] == '$':
        process_command(line[1:].strip())
    else:
        line_parts=line.split(" ")
        if line_parts[0] == "dir":
            pass
        else:
            post_file_size(int(line_parts[0]))

less_than_100000 = {k: v for k, v in dir_sizes.items() if v<=100000}

print(sum(less_than_100000.values()))
available_size = 70000000 - dir_sizes["/"]  
print("size_needd= %d"%available_size)
extra_size_needed=30000000 - available_size
print("size_needd= %d"%extra_size_needed)

candidates = {k: v for k, v in dir_sizes.items() if v>extra_size_needed}



print(candidates)


