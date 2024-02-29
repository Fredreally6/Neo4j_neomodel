from neomodel import db,config
from norm import tNorm, sNorm
from weights import InHypOWA

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

weights = [1.0]
layer = 3
alpha = 0.5

def OneGraphA2B(a, b, level, x, y):

    global weights

    if level >= layer:
        return 0

    #Match nodes
    if (a == 'A' or a == 'B'):
        queryA = "MATCH (i:Rootnode {name: \'"+ a +"\' })-[j]->(k) return i,j,k"
    else:
        queryA = "MATCH (i:Normalnode {name: \'"+ a +"\' })-[j]->(k) return i,j,k"
    
    if (b == 'B' or b == 'A'):
        queryB = "MATCH (i:Rootnode {name: \'"+ b +"\' })-[j]->(k) return i,j,k"
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
        rela_weight = r[1]._properties['weight']
        result_list_A.append((start_node, rela_type, end_node, rela_weight))

    for r in results_B:
        start_node = r[0]._properties['name']
        end_node = r[2]._properties['name']
        rela_type = r[1].type
        rela_weight = r[1]._properties['weight']
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
                    pair_result.append((i[2], j[2],i[3],j[3]))

    if level==0:
        if len(numelist)==0:
            v = 1
        else:
            v = len(numelist)
        if layer < 3:
            weights.append(alpha)
        else:
            weights = weights + InHypOWA(v,layer-1)
        print(weights)

    for i in range(len(result_list_A)):
        denoA = denoA + result_list_A[i][3]

    for i in range(len(result_list_B)):
        denoB = denoB + result_list_B[i][3]

    for i in range(len(numelist)):
        nume = nume + numelist[i]

    print("*****************************")
    print("Comparing "+a+" and "+b+" on level "+str(level))
    print("Results of T-norm:" + str(nume) + " and A: " + str(denoA) + " B: " + str(denoB))
    print("Next pair waiting to calculate: ")
    print(pair_result)
    print(" ")

    if denoA == 0:
        return 0

    tmp = 0
    for it in pair_result:
        tmp = tmp + OneGraphA2B(it[0],it[1],level+1,it[2],it[3])
        # print(tNorm(it[2],it[3]),weights[level],"now")

    if level > 0:
        # print(tNorm((nume+tmp)/deno,tNorm(x,y))*weights[level],level)
        # print(nume,tmp,deno)
        return tNorm((nume+tmp)/denoA,tNorm(x,y))*weights[level]
    
    if level == 0:
        # print(weights[level]*(nume+tmp)/deno)
        # print(nume,tmp,deno)
        return weights[level]*(nume+tmp)/denoA


sim = OneGraphA2B('B','A', 0, 1, 1)
print("Similarity A to B is %.4f" %(sim))

# simA2B = OneGraphA2B('A','B', 0, 1, 1)
# simB2A = OneGraphA2B('B','A', 0, 1, 1)
# print("Similarity A to B is %.4f" %(simA2B))
# print("Similarity B to A is %.4f" %(simB2A))