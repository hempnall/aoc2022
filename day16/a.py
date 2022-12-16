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

def simplify_graph(complex_graph):
    non_zero_nodes=[ k for k,v in complex_graph.items() if v["rate"] > 0 ]
    non_zero_nodes.append("AA")
    def set_distance_sub(distances,s,e,d):
        if not s in distances:
            distances[s]={e:d}
        else:
            if not e in distances[s]:
                distances[s][e]=d
            else:
                if d < distances[s][e]:
                    distances[s][e] = d
    def set_distance(distances,s,e,d):
        set_distance_sub(distances,s,e,d)
        set_distance_sub(distances,e,s,d)

    def get_distance(distances,s,e):
        if s < e:
            x,y=s,e
        else:
            x,y=e,s
        if x in distances:
            if y in distances[x]:
                return distances[x][y]
        return None
        
    def get_shortest_distance(distances,orig_s,node_s,node_e,visited):
        current_node=complex_graph[node_s]
        print(f'checking current_node={node_s} current_node={current_node}  {orig_s} {node_s} {node_e} {len(visited)} {visited}')
        if node_s==node_e:
            return len(visited) -1
        else:
            for tunnel in current_node["tunnels"]:
                if not tunnel in visited:
                    print(f'checking {visited} + {tunnel}')
                    distance = get_shortest_distance(distances,orig_s,tunnel,node_e,[*visited,tunnel])
                    print(f'distance = {distance}')
                    if not distance is None:
                        print(f'checking current_node={node_s} current_node={current_node}  {orig_s} {node_s} {node_e} {len(visited)} {visited}')
                        set_distance(distances,orig_s,tunnel,distance)
                        return distance 
                    return None
                return None # reached dead end
            # return none if nowehere to go - i.e. wind back
            return None

    distances={  }
    for node_idx_s in non_zero_nodes[:1]:
        for node_idx_e in non_zero_nodes[1:2]:
            if node_idx_s == node_idx_e:
                continue
            else:
                print(f'top_level={node_idx_s} {node_idx_e}')
                get_shortest_distance(distances,node_idx_s,node_idx_s,node_idx_e,[node_idx_s])
            
    print(distances)
    

graph_nodes=construct_graph(lines)
simplified_graph=simplify_graph(graph_nodes)


