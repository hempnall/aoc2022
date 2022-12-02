f = open("input.txt","r")
lines = f.readlines()
print(lines)

playerAmap={
    "A": 1,
    "B": 2,
    "C": 3
}

playerBmap={
    "X": 1,
    "Y": 2,
    "Z": 3
}

results={
    "AX":3,
    "AY":6,
    "AZ":0,
    "BX":0,
    "BY":3,
    "BZ":6,
    "CX":6,
    "CY":0,
    "CZ":3
}

newResponses={
    "A X":"Z",
    "A Y":"X",
    "A Z":"Y",
    "B X":"X",
    "B Y":"Y",
    "B Z":"Z",
    "C X":"Y",
    "C Y":"Z",
    "C Z":"X"
}

def score_line(line):
    playerAchoice=playerAmap[ line[0] ]
    playerBchoice=playerBmap[ line[2] ]
    key="%s%s" % (line[0],line[2])
    return playerBchoice + results[key]

def new_line(line):
    return "%s %s" % (line[0], newResponses[line.strip()])

mresults = [ score_line(line) for line in lines ]
print(sum(mresults))

actual_plays = [new_line(line) for line in lines]
# print(actual_plays)

new_results = [ score_line(line.strip()) for line in actual_plays ]
print(sum(new_results))



