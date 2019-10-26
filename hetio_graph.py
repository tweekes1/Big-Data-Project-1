import os.path
from py2neo import *
from queries import *

class HetioGraph:
    def __init__(self, password):
        self.graph = Graph(password=password)
            
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def commit(self):
        return self.graph.begin().commit

    def execute_cypher(self, query):
        return self.graph.run(query)

    def create_graph_nodes(self):
        print('IMPORTING NODES')    

        self.execute_cypher(node_import_query)    

    def create_graph_edges(self):
        print('IMPORTING EDGES')
        self.execute_cypher(edge_import_query)

    def create_node_labels(self):
        for query in label_queries:
            self.execute_cypher(query)
            self.commit()         

    def create_relationship_labels(self):
        for query in relationship_queries:
            self.execute_cypher(query)
            self.commit()

    def initialize_graph(self, node_file, edge_file):
        print('INITIALIZING GRAPH')
        self.clear_database()
        self.create_graph_nodes()
        self.create_graph_edges()
        self.create_relationship_labels()
        self.create_node_labels()

    def discover_new_treatments(self):
        print('FINDING NEW TREATMENTS')
        print(self.execute_cypher(discover_new_treatments_query).data())

    def clear_database(self):
        print('CLEARING DATABASE')
        self.graph.delete_all()
        