import pandas as pd
from py2neo import Graph, Node, Relationship,NodeMatcher

test_graph = Graph("http://localhost:7474", auth = ('neo4j','password'), name = 'test')

test_graph.delete_all()

data = pd.read_csv('data/data1.csv')

entity1 = data.iloc[:,0]
rela = data.iloc[:,1]
entity2 = data.iloc[:,2]

label = [] 
for i in range(0,data.shape[1]):
    label.append(data.columns[i])

node_matcher = NodeMatcher(test_graph)

nodeA = Node(label[0], name = 'A')
nodeB = Node(label[0], name = 'B')

test_graph.create(nodeA)
test_graph.create(nodeB)
# Loading data into Neo4j
# for i in range(0, data.shape[0]):

#     if(test_graph.nodes.match(label[0], name=entity1[i]).count() == 0):
#         node1 = Node(label[0], name = entity1[i])
#         test_graph.create(node1)
#     else:
#         node1 = node_matcher.match(label[0]).where(name = entity1[i]).first()
    
#     if(test_graph.nodes.match(label[2], name=entity2[i]).count() == 0):
#         node2 = Node(label[2], name = entity2[i])
#         test_graph.create(node2)
#     else:
#         node2 = node_matcher.match(label[2]).where(name = entity2[i]).first()
    
#     relation1 = Relationship(node1,rela[i],node2)
    
#     test_graph.create(relation1)

# test_graph.run('MATCH (n: City) WITH n.name AS name, COLLECT(n) AS nodelist, COUNT(*) AS count WHERE count>1 CALL apoc.refactor.mergeNodes(nodelist) YIELD node RETURN node')
# test_graph.run('MATCH (n: Job) WITH n.name AS name, COLLECT(n) AS nodelist, COUNT(*) AS count WHERE count>1 CALL apoc.refactor.mergeNodes(nodelist) YIELD node RETURN node')

for i in range(0, data.shape[0]):

    if(entity1[i]=='A'):
        node1 = node_matcher.match(label[0]).where(name = 'A').first()
    elif(entity1[i]=='B'):
        node1 = node_matcher.match(label[0]).where(name = 'B').first()
    elif(test_graph.nodes.match(label[2], name=entity1[i]).count() != 0):
        node1 = node_matcher.match(label[2]).where(name = entity1[i]).first()
    else:
        node1 = Node(label[0], name = entity1[i])
        test_graph.create(node1)
    
    if(test_graph.nodes.match(label[2], name=entity2[i]).count() == 0):
        node2 = Node(label[2], name = entity2[i])
        test_graph.create(node2)
    else:
        node2 = node_matcher.match(label[2]).where(name = entity2[i]).first()
    
    relation1 = Relationship(node1,rela[i],node2)
    
    test_graph.create(relation1)