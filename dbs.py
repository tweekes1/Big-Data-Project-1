from csv import DictReader
import os.path
from py2neo import *
from helpers import *
from queries import label_queries, relationship_queries

class Database:
    def __init__(self):
        self.graph = Graph(password='Temp1234$')
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
            
    def commit(self):
        return self.graph.begin().commit

    def execute_cypher(self, query):
        self.graph.run(query)

    def initialize_db(self, filename):
        return 0

    def create_graph_nodes(self, filename):
        print('=================IMPORTING NODES===================')     
        constraint_query = '''
            CREATE CONSTRAINT ON (a:Node) ASSERT a.id IS UNIQUE
        '''

        import_query = '''
            USING PERIODIC COMMIT 500
            LOAD CSV WITH HEADERS FROM "file:///%s" AS LINE
            FIELDTERMINATOR '\t'
            MERGE(n:Node {id: LINE.id, name: LINE.name, kind: LINE.kind})
        ''' % (filename)

        self.execute_cypher(constraint_query)
        self.execute_cypher(import_query)    


    def create_graph_edges(self, filename):
        print('=================IMPORTING EDGES===================')

        import_query = '''
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM "file:///%s" AS LINE
            FIELDTERMINATOR '\t' 
            MATCH (A:Node{id: LINE.source})
            MATCH (B:Node{id: LINE.target})
            CREATE (A)-[:RELATES{type: LINE.metaedge}]->(B)
        ''' % (filename)

        self.execute_cypher(import_query)

    def create_node_labels(self):
        for query in label_queries:
            self.execute_cypher(query)
            self.commit()         

    def create_relationship_labels(self):
        for query in relationship_queries:
            self.execute_cypher(query)
            self.commit()

    def initialize_graph(self, node_file, edge_file):
        print('=================CREATING GRAPH====================')
        self.create_graph_nodes(node_file)
        self.create_graph_edges(edge_file)
        self.create_relationship_labels()
        self.create_node_labels()


    def clear_database(self):
        print('=================CLEARING DATABASE=================')
        self.graph.delete_all()

db = Database()
db.clear_database()
# db.initialize_graph('nodes.tsv', 'edges.tsv')

            