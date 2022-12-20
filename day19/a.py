f = open("input.txt","r")
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
robot_cap_types=["ore","clay","obsidian"]
ROBOT_PURCHASE_OPTIONS=["geode","obsidian","clay","ore",None]
MAX_MINUTES=32
max_geodes=0
pruned_branches=0

def blueprint(l):
    words = l.split(" ")
    return {
        "ore": {
            "ore": int(words[6]),
            "clay": 0,
            "obsidian": 0
        },
        "clay": {
            "ore": int(words[12]),
            "clay": 0,
            "obsidian": 0
        },
        "obsidian": {
            "ore": int(words[18]),
            "clay": int(words[21]),
            "obsidian": 0
        },
        "geode": { 
            "clay": 0,
            "ore": int(words[27]),
            "obsidian": int(words[30])
        }
    }

blueprints={
    idx: blueprint(l) for idx, l in enumerate(lines)
}

def get_cache_key(minute,invent,robots):
    return (
        minute,
        invent["ore"],
        invent["clay"],
        invent["obsidian"],
        invent["geode"],
        robots["ore"],
        robots["clay"],
        robots["obsidian"],
        robots["geode"],
    )

def is_robot_affordable(cost,invent):
    for k,v in cost.items():
        if not k in invent:
            return False
        if invent[k]<cost[k]:
            return False
    return True

def inventory_after_payment(invent,cost):
    return {
        material: invent[material] - matcost for material , matcost in cost.items()
    }           

def accumulate_material(invent,robots):
    return {
        k: (invent[k] + robots[k]) for k in invent
    }

def purchase_robot(robots,invent,robot,cost):
    new_robots=robots.copy()
    new_invent=invent.copy()
    new_robots[robot]+=1
    for item, item_cost in cost.items():
        new_invent[item] -= item_cost
    return new_robots,new_invent

def robot_caps_for_blueprint(blueprint):
    robot_caps = {
        typ: max( [ blueprint[s][typ] for s in [*robot_cap_types,"geode"]] )
        for typ in robot_cap_types
    }
    robot_caps["geode"]=9999
    return robot_caps


minute_caches = {}


def get_max_geodes(
    blueprint,
    minute,
    start_inventory,
    start_robots,
    caps):
    global max_geodes
    if minute == MAX_MINUTES:
        #print("** MAX **")
        max_geodes=max(max_geodes,start_inventory["geode"])
        return
        
    #print(f'minute={minute} start_inventory={start_inventory} start_robots={start_robots}')
    new_invent=accumulate_material(start_inventory,start_robots)
    time_remaining=(MAX_MINUTES-minute)-1
    for robot in ROBOT_PURCHASE_OPTIONS:
        if robot is None:
            get_max_geodes(
                blueprint,
                minute+1,
                new_invent,
                start_robots.copy(),
                caps
            )
        elif start_robots[robot] * time_remaining + start_inventory[robot] < caps[robot] * time_remaining:
            if is_robot_affordable(blueprint[robot],start_inventory):
                next_robots,next_invent=purchase_robot(start_robots,new_invent,robot,blueprint[robot])
                cache_key=get_cache_key(minute+1,next_invent,next_robots)
                if not cache_key in minute_caches:
                    get_max_geodes(
                        blueprint,
                        minute+1,
                        next_invent,
                        next_robots,
                        caps
                    )
                    minute_caches[cache_key]=max_geodes
                if robot in ["ore","geode"]:
                    break
        else:
            continue
    
options=[]
mgs=[0] * 3
accum=0

for idx ,line in enumerate(lines[1:3]):
    max_geodes=0
    minute_caches={}
    caps=robot_caps_for_blueprint(blueprint(line))
    print(caps)
    get_max_geodes(
        blueprint(line),
        0,
        start_inventory,
        start_robots,
        caps
    )
    print(max_geodes)
    mgs[idx]=max_geodes
    accum += ((idx+1) * max_geodes)

print(accum)
print(25 * mgs[1] * mgs[2])
    