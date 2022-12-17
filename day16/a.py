is_real=False

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
time_limit=30
current_max=0

def maximise_rate(node_st,current_total,increase,current_time):
    global current_max
    #print(f'[{current_time}] {node_st} {current_total} {on_taps}')
    if current_time>time_limit:
        #print(f'{node_st} {current_total}')
        return current_total

    current_total += increase
    current_max=max(current_max,current_total)
    next_node=node_st[-1]
    current_node=simplified_graph[next_node]

    for k,v in current_node.items():
        if k in node_st:
            continue
        next_time=current_time+v+1
        rate=graph_nodes[k]["rate"]
        increase=(time_limit-next_time)*rate
        maximise_rate(
            [*node_st,k],
            current_total,
            increase,
            next_time)

max_steam=maximise_rate(["AA"],0,0,0)
print(current_max)




