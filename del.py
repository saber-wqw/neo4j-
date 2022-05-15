from py2neo import Graph

graph = Graph("http://localhost:7474", auth=("neo4j", "shz"))
graph.delete_all()