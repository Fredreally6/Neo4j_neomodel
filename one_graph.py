from neomodel import db,config
from norm import tNorm, sNorm

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

alpha = [1, 0.8, 0.5, 0.1]

# results, _ = db.cypher_query("MATCH (i:Normalnode {name: \'X1\' })-[j]->(k) return i,j,k")

# print(results[0][1]._properties['weights'])

# result_list_A = []

# for r in results:
#     start_node = r[0]._properties['name']
#     end_node = r[2]._properties['name']
#     rela_type = r[1].type
#     rela_weight = r[1]._properties['weights']
#     result_list_A.append((start_node, rela_type, end_node, rela_weight))

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
        rela_weight = r[1]._properties['weights']
        result_list_A.append((start_node, rela_type, end_node, rela_weight))

    for r in results_B:
        start_node = r[0]._properties['name']
        end_node = r[2]._properties['name']
        rela_type = r[1].type
        rela_weight = r[1]._properties['weights']
        result_list_B.append((start_node, rela_type, end_node, rela_weight))


    # Compare with two lists to find the relations
    numelist = []
    nume = 0
    denoA = 0
    denoB = 0
    pair_result = []
    for i in result_list_A:
        for j in result_list_B:
            if i[1]==j[1]:
                if i[2]==j[2]:
                    numelist.append(tNorm(i[3],j[3]))
                else:
                    pair_result.append((i[2], j[2]))


    for i in range(len(result_list_A)):
        denoA = sNorm(denoA, result_list_A[i][3])

    for i in range(len(result_list_B)):
        denoB = sNorm(denoB, result_list_B[i][3])

    for i in range(len(numelist)):
        nume = sNorm(nume, numelist[i])

    deno = max(denoA, denoB)

    print("*****************************")
    print("Comparing "+a+" and "+b+" on level "+str(level))
    print("Results of T-norm:" + str(nume) + " and T-conorm: " + str(deno) )
    print("Next pair waiting to calculate: ")
    print(pair_result)
    print(" ")

    length = max(len(result_list_A),len(result_list_B))

    if len(pair_result)==0 or level >= 3:
        if length == 0: 
            return 0
        else: 
            return nume/deno
    
    tmp = 0
    for it in pair_result:
        tmp += OneGraph(it[0],it[1],level+1)/deno
        # print(tmp)

    similarity = (nume + alpha[level+1]*tmp)/deno
    # print(similarity,t_count, tmp, alpha[level+1],level)

    return similarity


sim = OneGraph('A','B', 0)
print("Similarity between A and B is %.4f" %(sim))