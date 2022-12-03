f = open("input.txt","r")
lines=f.readlines()

def splitLine(line):
    length = len(line)
    if not length % 2 == 0:
        raise Exception("line is not an even length")
    half_length = int(length / 2)
    return [ line[: half_length] , line[half_length:len(line)] ]
    
def getCommonLetter(parts):
    intersection = set(parts[0]).intersection(parts[1])
    if len(intersection) != 1:
        raise Exception("more than 1 common letter")
    return list(intersection)[0]

def getCommonLetter3(parts):
    print(parts[0])
    print(parts[1])
    print(parts[2])
    intersection = set(parts[0]).intersection(parts[1]).intersection(parts[2])
    print(intersection)
    if len(intersection) != 1:
        raise Exception("more than 1 common letter")
    return list(intersection)[0]

def scoreLetter( letter ):
    ascii = ord(letter[0])
    if ascii >= 97 and ascii <= 122:
        return ascii - 96
    elif ascii >= 65 and ascii <= 90:
        return ascii - 38
    else:
        raise Exception("not a valid letter")

scores = [ scoreLetter( getCommonLetter( splitLine(line.strip()))) for line in lines ]
print(sum(scores))
if not len(lines) %3 == 0:
    raise Exception("not a multiple og three lines")

number_of_chunks = int( len(lines) / 3 )
elf_chunks = [ [ lines[(i*3)+0].strip() , lines[(i*3)+1].strip(), lines[(i*3)+2].strip()] for i in range(number_of_chunks) ]
chunk_scores = [ scoreLetter( getCommonLetter3( chunk )) for chunk in elf_chunks]
print(sum(chunk_scores))
print(len(lines))
print (len(elf_chunks))

