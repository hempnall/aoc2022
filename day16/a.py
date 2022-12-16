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

    
graph_nodes=construct_graph(lines)
print(graph_nodes)

