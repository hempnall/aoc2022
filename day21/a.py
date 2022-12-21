f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
numbers = [ str(n) for n in range(0,10) ]
IS_PART2=False
LEAF_NODE='humn'
ROOT_NODE='root'
REVERSE_OPS=['+','-','*','/']
def parse_node( line ):
    var_name = line[0:4]
    if line[6] in numbers:
        return var_name, ('N',int(line[6:]))
    else:
        if IS_PART2 and var_name == ROOT_NODE:
            return  var_name, ('=',line[6:10],line[13:19])
        return  var_name, (line[11],line[6:10],line[13:19])

def evaluate_tree(nodes,root,parents,parent):
    global ast_parents
    current_node=nodes[root]
    parents[root]=parent
    if current_node[0] == 'N':
        return current_node[1]
    else:
        left_node=current_node[1]
        right_node=current_node[2]
        operation = current_node[0]
        left_tree=evaluate_tree(ast,left_node,parents,root)
        right_tree=evaluate_tree(ast,right_node,parents,root)
        if operation == '+':
            return left_tree + right_tree
        elif operation == '-':
            return left_tree - right_tree
        elif operation == '*':
            return left_tree * right_tree
        elif operation == '/':
            return left_tree / right_tree
        elif operation == '=':
            assert(1==2)
        else:
            raise Exception("unknown operation")

def get_sibling(node,sibling):
    if node[0]=='N':
        return '',None
    if node[1] == sibling:
        return "L",node[2]
    elif node[2] == sibling:
        return "R",node[1]
    else:
        raise Exception("unknown sibling")


start_val_f=0
def reverse_tree( child, leaf_node, reverse_tree_st ):
    global start_val_f
    leaf_node_op=ast[leaf_node]
    print(f'child=>{child} op[{leaf_node}]={leaf_node_op}')
    side,sibling_var_name=get_sibling(leaf_node_op,child)
    if not sibling_var_name is None:
        sibl_val=evaluate_tree(ast,sibling_var_name,{},leaf_node)
        print(f' - {sibling_var_name} = {sibl_val}')
        sibling_op=ast[leaf_node][0]
        if sibling_op in REVERSE_OPS:
            reverse_op = (
                sibling_op ,
                sibl_val,
                side
            )
            print(f' - {reverse_op}')
            reverse_tree_st.append( reverse_op)

    if leaf_node == ROOT_NODE:
        print(reverse_tree_st)
        start_val=reverse_tree_st.pop()[1]
        while len(reverse_tree_st) > 0:
            next_op = reverse_tree_st.pop()
            if next_op[2] == "R":
                if next_op[0] == '+':
                    start_val = start_val - next_op[1]
                elif next_op[0] == '-':
                    start_val = next_op[1] - start_val
                elif next_op[0] == '*':
                    start_val  = start_val / next_op[1]
                elif next_op[0] == '/':
                    start_val  =  next_op[1] / start_val
                else:
                    raise Exception("shouldnt get here")
            elif next_op[2] == "L":
                if next_op[0] == '+':
                    start_val = start_val - next_op[1]
                elif next_op[0] == '-':
                    start_val = start_val + next_op[1]
                elif next_op[0] == '*':
                    start_val  = start_val / next_op[1]
                elif next_op[0] == '/':
                    start_val  = start_val * next_op[1]
                else:
                    raise Exception("shouldnt get here")
            else:  
                raise Exception("shouldnt get here")              
        start_val_f=int(start_val)
        print(start_val_f)
        print("at root")
        return
    reverse_tree(leaf_node, ast_parents[leaf_node], reverse_tree_st)
    


ast_nodes=[ parse_node(l) for l in lines]
ast_parents={

}
ast={
    vari: expr for vari,expr in ast_nodes
}

print(evaluate_tree(ast,ROOT_NODE,ast_parents,None))

reverse_st=[]
reverse_tree(None,LEAF_NODE,reverse_st)
print(reverse_st)
ast["humn"]=('N',start_val_f)
print(ast["humn"])
print(evaluate_tree(ast,"mrnz",{},None))
print(evaluate_tree(ast,"jwrp",{},None))
