from neomodel import db,config, StructuredNode,StructuredRel, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom
from model import Normalnode, Rootnode

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

alpha = [1, 0.8, 0.5, 0.1]

# results, _ = db.cypher_query("MATCH (i:Normalnode {name: \'X1\' })-[j]->(k) return i,j,k")

# result_list_A = []

# for r in results:
#     start_node = r[0]._properties['name']
#     end_node = r[2]._properties['name']
#     rela_type = r[1].type
#     result_list_A.append((start_node, rela_type, end_node))

# print(result_list_A)

def OneGraph(a, b, level):

    #Match nodes
    if (a == 'A'):
        queryA = "MATCH (i:Rootnode {name: \'A\' })-[j]->(k) return i,j,k"
    else:
        queryA = "MATCH (i:Normalnode {name: \'"+ a +"\' })-[j]->(k) return i,j,k"
    
    if (b == 'B'):
        queryB = "MATCH (i:Rootnode {name: \'B\' })-[j]->(k) return i,j,k"
    else:
        queryB = "MATCH (i:Normalnode {name: \'"+ b +"\' })-[j]->(k) return i,j,k"

    results_A, _ = db.cypher_query(queryA)
    results_B, _ = db.cypher_query(queryB)

    result_list_A = []
    result_list_B = []

    for r in results_A:
        start_node = r[0]._properties['name']
        end_node = r[2]._properties['name']
        rela_type = r[1].type
        result_list_A.append((start_node, rela_type, end_node))

    for r in results_B:
        start_node = r[0]._properties['name']
        end_node = r[2]._properties['name']
        rela_type = r[1].type
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


sim = OneGraph('A','B', 0)
print("Similarity between A and B is %.4f" %(sim))