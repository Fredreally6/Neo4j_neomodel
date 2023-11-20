from py2neo import Graph, NodeMatcher

graph = Graph("http://localhost:7474", auth = ('neo4j','password'), name = 'test')

node_matcher = NodeMatcher(graph)

alpha = [1,0.8,0.5,0.1]

def OneGraph(a, b, level):

    # Match two nodes
    if(a == 'A'):
        nodeA = node_matcher.match("Rootnode").where(name = a).first()
    else:
        nodeA = node_matcher.match("Normalnode").where(name = a).first()

    if(b == 'B'):
        nodeB = node_matcher.match("Rootnode").where(name = b).first()
    else:
        nodeB = node_matcher.match("Normalnode").where(name = b).first()
    

    # Get two lists of triples with the two nodes
    results_A = graph.match((nodeA,))
    results_B = graph.match((nodeB,))
    
    result_list_A=[]
    result_list_B=[]

    for r in results_A:
        start_node = r.start_node['name']
        end_node = r.end_node['name']
        rela_type = type(r).__name__
        result_list_A.append((start_node, rela_type, end_node))

    for r in results_B:
        start_node = r.start_node['name']
        end_node = r.end_node['name']
        rela_type = type(r).__name__
        result_list_B.append((start_node, rela_type, end_node))
    
    # Compare with two lists to find the relations
    abssame_count = 0
    pair_result = []
    for i in result_list_A:
        for j in result_list_B:
            if i[1]==j[1]:
                if i[2]==j[2]:
                    abssame_count += 1
                else:
                    pair_result.append((i[2], j[2]))

    print("*****************************")
    print("Comparing "+a+" and "+b+" on level "+str(level))
    print("Number of Absolutely Same Relation: "+str(abssame_count))
    print(pair_result)
    print(" ")

    length = max(len(result_list_A),len(result_list_B))

    if len(pair_result)==0 or level >= 3:
        if length == 0: 
            return 0
        else: 
            return abssame_count/length
    
    tmp = 0
    for it in pair_result:
        tmp += OneGraph(it[0],it[1],level+1)

    similarity = (abssame_count + alpha[level+1]*tmp)/length
    # print(similarity,abssame_count, length, alpha[level+1],tmp,level)
   
    # print(similarity)
    return similarity

sim = OneGraph("A","B",0)
print("Similarity between A and B is %.4f" %(sim))


