import pandas as pd

from neomodel import db, config
from model import Rootnode, Normalnode

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

db.cypher_query("MATCH (n) DETACH DELETE n")

data = pd.read_csv('data/data_test.csv')

entity1 = data.iloc[:,0]
rela = data.iloc[:,1]
entity2 = data.iloc[:,2]
weight = data.iloc[:,3]

label = [] 
for i in range(0,data.shape[1]):
    label.append(data.columns[i])


nodea1 = Rootnode(name = 'A1').save()
nodeb1 = Rootnode(name = 'B1').save()
nodea2 = Rootnode(name = 'A2').save()
nodeb2 = Rootnode(name = 'B2').save()

for i in range(0, data.shape[0]):
    isRoot = False
    if(entity1[i]=='A1' or entity1[i]=='B1' or entity1[i]=='A2' or entity1[i]=='B2'):
        node1 = Rootnode.nodes.get(name = entity1[i])
        isRoot = True
    # elif(entity1[i]=='B1'):
    #     node1 = Rootnode.nodes.get(name = 'B1')
    #     isRoot = True
    elif(Normalnode.nodes.get_or_none(name = entity1[i])) is None:
        node1 = Normalnode(name = entity1[i]).save()
    else:
        node1 = Normalnode.nodes.get(name = entity1[i])

    if(Normalnode.nodes.get_or_none(name = entity2[i])) is None:
        node2 = Normalnode(name = entity2[i]).save()
    else:
        node2 = Normalnode.nodes.get(name = entity2[i])
    
    if isRoot:
        query1 = "MATCH (node1:Rootnode {name: \'" + entity1[i] +"\' }) MATCH (node2:Normalnode {name:\'"+ entity2[i] +"\'})"
    else:
        query1 = "MATCH (node1:Normalnode {name: \'" + entity1[i] +"\' }) MATCH (node2:Normalnode {name:\'"+ entity2[i] +"\'})"
    query2 = "CALL apoc.create.relationship(node1,\'"+ rela[i] +"\', {weights: " + str(weight[i]) + "}, node2) YIELD rel Return rel"

    db.cypher_query(query1+query2)