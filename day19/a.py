f = open("sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

quality_levels={}
start_inventory={
    "ore":0,
    "clay":0,
    "obsidian":0,
    "geode":0,
}
start_robots={
    "ore":1,
    "clay":0,
    "obsidian":0,
    "geode":0,   
}
MAX_MINUTES=24

def blueprint(l):
    words = l.split(" ")
    return {
        "ore": {
            "ore": int(words[6])
        },
        "clay": {
            "ore": int(words[12])
        },
        "obsidian": {
            "ore": int(words[18]),
            "clay": int(words[21])
        },
        "geode": { 
            "ore": int(words[27]),
            "obsidian": int(words[30])
        }
    }

blueprints={
    idx + 1: blueprint(l) for idx, l in enumerate(lines)
}

def is_robot_affordable(cost,invent):
    for k,v in cost:
        if not k in invent:
            return False
        if invent[k]<cost[k]:
            return False
    return True

def inventory_after_payment(invent,costs):
    return {
        material: invent[material] - cost for material , cost in costs
    }     

def buy_robot(robots,robot):
    tmp = robots.copy()
    tmp[robot]+=1
    return tmp

def get_max_geodes(
    blueprint,
    minute,
    start_inventory,
    start_robots):
    if minute == MAX_MINUTES:
        return start_inventory["geode"]
    affordable_robots=[
        robot for robot,cost in blueprint.items() if is_robot_affordable(cost,start_inventory)
    ]
    buy_robot_cost = 0
    dont_buy_robot_cost = 0
    next_day_cost=0
    for robot in affordable_robots:
        buy_robot_cost = get_max_geodes(
            blueprint,
            minute,
            inventory_after_payment(start_inventory,blueprint[robot]),
            buy_robot(start_robots,robot)   
        )
        dont_buy_robot_cost=get_max_geodes(
            blueprint,
            minute,
            start_inventory,
            start_robots  
        )
    next_day_cost = get_max_geodes(
            blueprint,
            minute+1,
            start_inventory,
            start_robots  
        )
    new_inventory_levels={
        k: v + start_robots[k] for k,v in start_inventory.items()
    }
    return max(buy_robot_cost,dont_buy_robot_cost,next_day_cost)
    


print(blueprints)