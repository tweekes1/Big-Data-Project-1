import os.path
import pandas as pd
from py2neo import *
from queries import *

class HetioGraph:
    def __init__(self, password=None):
        self.graph = Graph(password=password)
        pd.set_option('display.max_rows', 200000)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def commit(self):
        return self.graph.begin().commit

    def execute_cypher(self, query):
        return self.graph.run(query)

    def create_graph_nodes(self):
        print('CREATING NODES')    

        self.execute_cypher(node_import_query)    

    def create_graph_edges(self):
        print('CREATING EDGES')
        self.execute_cypher(edge_import_query)

    def create_node_labels(self):
        for query in label_queries:
            self.execute_cypher(query)
            self.commit()         

    def create_relationship_labels(self):
        for query in relationship_queries:
            self.execute_cypher(query)
            self.commit()

    def initialize_graph(self):
        print('INITIALIZING GRAPH')
        self.clear_database()
        self.create_graph_nodes()
        self.create_graph_edges()
        self.create_relationship_labels()
        self.create_node_labels()

    def discover_new_treatments(self):
        print('FINDING NEW TREATMENTS')
        data = self.execute_cypher(discover_new_treatments_query).data()

        print(pd.DataFrame(data))

    def clear_database(self):
        print('CLEARING GRAPH')
        self.graph.delete_all()
        