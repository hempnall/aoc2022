
is_real=True

f=open("sample.txt","r")
lines=[ l.strip() for l in f.readlines() ]
if is_real:
    f=open("input.txt","r")
    lines=[ l.strip() for l in f.readlines() ]

# e.g. Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
def construct_graph(lines):
    def node_name(line):
        return line.split(" ")[1]
    def construct_node(line):
        line_arr=line.split(" ")
        rate=int(line_arr[4][5:-1])
        tunnels=[ tun if len(tun)==2  else tun[:2]  for tun in line_arr[9:]]
        return {
            "rate": rate,
            "tunnels": tunnels
        }
    return { node_name(l) : construct_node(l) for l in lines }

def render_complex_graph(graph):
    print("graph {")
    already_drawn=set()
    def node_link_text(k1,k2):
        node1rt=graph[k1]["rate"]
        node2rt=graph[k2]["rate"]
        node1rttxt=''
        node2rttxt=''
        if node1rt>0:
            node1rttxt=f' ({node1rt})'
        if node2rt>0:
            node2rttxt=f' ({node2rt})'
        return f'"{k1}{node1rttxt}" -- "{k2}{node2rttxt}";'
            
    for k in graph.keys():
        for tun in graph[k]["tunnels"]:
            if not node_link_text(k,tun) in already_drawn and not node_link_text(tun,k) in already_drawn:
                already_drawn.add(node_link_text(k,tun))
                print(node_link_text(k,tun))
    print("}")

def render_simple_graph(simple_graph):
    print("graph {")
    already_drawn=set()
    def simple_edge(k1,k2):
        return f'{k1} -- {k2} [label="{simple_graph[k1][k2]}"] ;'
    for k in simple_graph.keys():
        for ki,v in simple_graph[k].items():
            ab=simple_edge(k,ki)
            ba=simple_edge(ki,k)
            if not ab in already_drawn and not ba in already_drawn:
                already_drawn.add(ab)
                print(ab)

    print("}")


def simplify_graph(complex_graph):
    non_zero_nodes=[ k for k,v in complex_graph.items() if v["rate"] > 0 ]
    non_zero_nodes.append("AA")
    def set_distance_sub(distances,s,e,d):
        if not s in distances:
            distances[s]={ e: int(d)}
        else:
            if e in distances[s]:
                if d < distances[s][e]:
                    distances[s][e]=int(d)
            else: 
                distances[s][e]=int(d)

    def set_distance(distances,s,e,d):
        set_distance_sub(distances,s,e,d)
        set_distance_sub(distances,e,s,d)
        
    def get_shortest_distance(distances,orig_s,node_s,node_e,visited):
        current_node=complex_graph[node_s]
        #print(f'checking current_node={node_s} current_node={current_node}  {orig_s} {node_s} {node_e} {len(visited)} {visited}')
        if node_s==node_e:
            d=len(visited)-1
            set_distance(distances,orig_s,node_e,d)
        else:
            for tunnel in current_node["tunnels"]:
                if not tunnel in visited:
                    get_shortest_distance(distances,orig_s,tunnel,node_e,[*visited,tunnel])

    distances={  }
    for node_idx_s in non_zero_nodes:
        for node_idx_e in non_zero_nodes:
            if node_idx_s == node_idx_e:
                continue
            else:
                #print(f'top_level={node_idx_s} {node_idx_e}')
                get_shortest_distance(distances,node_idx_s,node_idx_s,node_idx_e,[node_idx_s])
            
    return distances
    

graph_nodes=construct_graph(lines)
# #render_graph(graph_nodes)
simplified_graph=simplify_graph(graph_nodes)
#render_simple_graph(simplified_graph)
time_limit=26
current_max=0
max_time=0

def calculate_tap_score(taps):
    tap_score=0
    for k,v in taps.items():
        tap_score += (time_limit - v["on_time"] ) * v["rate"]
    return tap_score

def show_tap_scores(taps):
    in_ord=dict(sorted(taps.items(), key=lambda item: item[1]["on_time"]))
    for k,v in in_ord.items():
        print(f'{k}: on_time={v["on_time"]} rate={v["rate"]} by={v["by"]} total={(time_limit - v["on_time"] ) * v["rate"]}')
    print(calculate_tap_score(taps))
    print() 


def compare_stack(stack2,stack1):
    return stack1 == stack2[:len(stack1)]

def sum_maxs(mp):
    return sum(mp.values())

def maximise_rate(
    me_stack,
    el_stack,
    you_remain, # in transit remaining distance for me
    el_remain, # in transit remaining for ele
    current_time,
    tap_scores,
    score_maxs):   # current time

    global current_max, max_time
    DEBUG=False
    assert(el_remain>=0)
    assert(you_remain>=0)
    me_dest=me_stack[-1]
    el_dest=el_stack[-1]
    max_time=max(current_time,max_time)

    if current_time > time_limit:
        return

    total=calculate_tap_score(tap_scores)
    if total > current_max:
        current_max=max(current_max,total)

    if total + ((time_limit-current_time - 2) * sum_maxs(score_maxs)) <= current_max:
        return

    def get_effective_node(remain,node):
        next_node=node
        if remain > 0:
            return True , { next_node: remain }
        else:
            return False, simplified_graph[next_node]

    def new_stack( cur_stack , is_virtual, new_dest ):
        if is_virtual:
            return cur_stack
        else:
            return [*cur_stack,new_dest]

    el_virtual, el_next_node = get_effective_node(el_remain,el_dest)
    me_virtual, me_next_node = get_effective_node(you_remain,me_dest)

    for k_me,v_me in me_next_node.items():
        if k_me == "AA":
            continue
        if not me_virtual and k_me in tap_scores:
            continue

        for k_ele,v_ele in el_next_node.items():
            if k_ele == "AA":
                continue
            if k_me == k_ele:
                continue
            if not el_virtual and k_ele in tap_scores:
                continue

            new_ele_stack = new_stack(el_stack,el_virtual,k_ele)
            new_me_stack = new_stack(me_stack,me_virtual,k_me)

            next_tap_scores=tap_scores.copy()
            new_maxes=score_maxs.copy()

            if not el_virtual:
                del new_maxes[k_ele]
                next_tap_scores[k_ele]={
                    "on_time": current_time+v_ele+1,
                    "rate": graph_nodes[k_ele]["rate"],
                    "by": "ele"
                }

            if not me_virtual:  
                del new_maxes[k_me]
                next_tap_scores[k_me]={
                    "on_time": current_time+v_me+1,
                    "rate": graph_nodes[k_me]["rate"],
                    "by": "me"
                }


            time_delta=0
            el_rm=0
            me_rm=0

            #print(f'you_remain={you_remain} el_remain={el_remain} v_e={v_ele} v_m={v_me}')
            if you_remain == 0 and el_remain == 0:
                time_delta=min(v_me,v_ele)+1
                el_rm=1 + v_ele-time_delta
                me_rm=1 + v_me-time_delta
            elif you_remain==0 and el_remain >0:
                time_delta=min(v_me+1,v_ele)
                el_rm=v_ele-time_delta
                me_rm=1 + v_me-time_delta
            elif you_remain>0 and el_remain == 0:
                time_delta=min(v_me,v_ele+1)
                el_rm=1 + v_ele-time_delta
                me_rm=v_me-time_delta
            else:
                raise Exception("impossible")

            next_time=current_time + time_delta

            maximise_rate(
                new_me_stack,
                new_ele_stack,
                me_rm,
                el_rm,
                next_time,
                next_tap_scores,
                new_maxes
            )

tap_scores={}
max_tap_scores = {
    k:graph_nodes[k]["rate"] for k in graph_nodes.keys()
}
max_steam=maximise_rate(["AA"],["AA"],0,0,0,tap_scores,max_tap_scores)
print(tap_scores)
print(current_max)
print(max_time)




