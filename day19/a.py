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
ROBOT_PURCHASE_OPTIONS=[None,"ore","clay"]#,"obsidian","geode"]
MAX_MINUTES=3

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

def get_purchase_combos(remaining_purchase_options,purchased,blueprint,invent,options):
    for idx in range(len(remaining_purchase_options)):
        purchase_option=remaining_purchase_options[idx]
        if purchase_option is None:
            options.append(purchased)
        else:
            cost = blueprint[purchase_option]
            if is_robot_affordable(cost,invent):
                get_purchase_combos(
                    remaining_purchase_options,
                    [*purchased,purchase_option],
                    blueprint,
                    inventory_after_payment(invent,cost),
                    options)
            else:
                get_purchase_combos(
                    remaining_purchase_options[1:],
                    [*purchased,purchase_option],
                    blueprint,
                    inventory_after_payment(invent,cost),
                    options)         

def accumulate_material(invent,robots):
    return {
        k: (invent[k] + robots[k]) for k in invent
    }

def purchase_robots(robots,purchase_combo,invent):
    return new_robots, new_invent

def get_max_geodes(
    blueprint,
    minute,
    start_inventory,
    start_robots):
    if minute == MAX_MINUTES:
        return start_inventory["geode"]
    print(f'minute={minute} start_inventory={start_inventory}')
    purchase_combos=[]
    get_purchase_combos(
        ROBOT_PURCHASE_OPTIONS,
        [],
        blueprint,
        start_inventory,
        purchase_combos
    )
    for combo in purchase_combos:
    new_robots=start_robots.copy()
    new_invent=accumulate_material(start_inventory,start_robots)
    get_max_geodes(
        blueprint,
        minute+1,
        new_invent,
        new_robots
    )
    
options=[]
get_max_geodes(blueprints[1],0,start_inventory,start_robots)
