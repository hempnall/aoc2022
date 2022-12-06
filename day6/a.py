f = open("input.txt","r")
lines = f.readlines()
line=lines[0].strip()
length_of_marker=4
length_of_message=len(line)

def all_different(txt):
    for idx in range(len(txt)):
        subtxt=txt[0:len(txt)-idx]
        print("%s %s %s" % (subtxt,subtxt[-1],subtxt[0:len(subtxt)-1]))
        if subtxt[-1] in subtxt[0:len(subtxt)-1]:
            return False
    return True

for idx in range(length_of_message-13):
    substr=line[idx:idx+14]
    if all_different(substr):
        print(idx+14)
        exit()
