from csv import DictReader
import os.path
from py2neo import *

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
        query = '''
            USING PERIODIC COMMIT 500
            LOAD CSV WITH HEADERS FROM "file:///%s" AS LINE
            FIELDTERMINATOR '\t'
            MERGE(n:NODE {id: LINE.id, name: LINE.name, kind: LINE.kind})
        ''' % (filename)

        self.execute_cypher(query)



db = Database()
db.initialize_db('nodes.tsv')

            