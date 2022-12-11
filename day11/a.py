from operator import ne
from tokenize import triple_quoted

monkey_mod=1

sample_monkeys=[
    {
        "items": [79,98],
        "operation": ("*",19),
        "test": 23,
        "true":2,
        "false":3,
        "inspection_count": 0 
    },
    {
        "items": [54,65,75,74],
        "operation": ("+",6),
        "test": 19,
        "true":2,
        "false":0,
        "inspection_count": 0
    },
    {
        "items": [79,60,97],
        "operation": ("**",2),
        "test": 13,
        "true":1,
        "false":3,
        "inspection_count": 0 
    },
    {
        "items": [74],
        "operation": ("+",3),
        "test": 17,
        "true":0,
        "false":1,
        "inspection_count": 0 
    }
]

actual_monkeys=[
    {
        "items": [50, 70, 54, 83, 52, 78],
        "operation": ("*",3),
        "test": 11,
        "true":2,
        "false":7,
        "inspection_count": 0 
    },
    {
        "items": [71, 52, 58, 60, 71],
        "operation": ("**",2),
        "test": 7,
        "true":0,
        "false":2,
        "inspection_count": 0 
    },
    {
        "items": [66, 56, 56, 94, 60, 86, 73],
        "operation": ("+",1),
        "test": 3,
        "true":7,
        "false":5,
        "inspection_count": 0 
    },
    {
        "items": [83,99],
        "operation": ("+",8),
        "test": 5,
        "true":6,
        "false":4,
        "inspection_count": 0 
    },
    {
        "items": [98,98,79],
        "operation": ("+",3),
        "test": 17,
        "true":1,
        "false":0,
        "inspection_count": 0 
    },
    {
        "items": [76],
        "operation": ("+",4),
        "test": 13,
        "true":6,
        "false":3,
        "inspection_count": 0 
    },
    {
        "items": [52, 51, 84, 54],
        "operation": ("*",17),
        "test": 19,
        "true":4,
        "false":1,
        "inspection_count": 0 
    },
    {
        "items": [82, 86, 91, 79, 94, 92, 59, 94],
        "operation": ("+",7),
        "test": 2,
        "true":5,
        "false":3,
        "inspection_count": 0 
    }
]

def new_worry_item( op , current_score):
    if op[0] == "*":
        return current_score * op[1]
    elif op[0] == "+":
        return current_score + op[1]       
    elif op[0] == "**":
        return current_score * current_score
    else:
        raise Exception(f'unsupported operation {op}')

def pre_process_monkeys(monkeys):
    global monkey_mod
    for monkey_idx in range(len(monkeys)):
        monkey_mod *= monkeys[monkey_idx]["test"]

def do_exercise(ex_monkeys):
    pre_process_monkeys(ex_monkeys)
    print(monkey_mod)
    counts = [0] * len(ex_monkeys)
    for round_idx in range(10000):
        for index, monkey in enumerate(ex_monkeys):
            for item in monkey["items"]:
                op=monkey["operation"]
                test=monkey["test"]
                true_monkey=monkey["true"]
                false_monkey=monkey["false"]
                new_worry_score=new_worry_item(op,item)
                new_worry_score %= monkey_mod
                if new_worry_score % test == 0:
                    ex_monkeys[true_monkey]["items"].append(new_worry_score)
                else:
                    ex_monkeys[false_monkey]["items"].append(new_worry_score)
            counts[index] += len(monkey["items"])
            monkey["items"]=[]
            if (round_idx % 10) == 0:
                pass
        if (round_idx +1) in [1,20,10000]:
            print(f'round={round_idx+1}')
            sortedc = sorted(counts)
            print(sortedc[-1] * sortedc[-2])

do_exercise(actual_monkeys)

