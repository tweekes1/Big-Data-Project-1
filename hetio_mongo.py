from csv import DictReader
from pymongo import MongoClient

class HetioMongo():

    def __init__(self):
        self.mongo_db = MongoClient()['hetio_db']
        self.mongo_collection = self.mongo_db['hetio_collection']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def insert(self, query):
        self.mongo_collection.insert(query)

    def create_documents(self, filename):
        print('CREATING DOCUMENTS')
        try: 
            with open(filename) as input_file:
                reader = DictReader(input_file, delimiter='\t')

                for row in reader:
                    query = {'id': row['id'], 'name': row['name'], 'kind': row['kind']}
                    self.insert(query)

        except FileNotFoundError as e:
            print(e)
  
    def get_update_query(self, dict, key):
        query_builder_dict = {
                'DaG' : ({'id' : dict['source']}, {'$push' : {'associates' : dict['target'] }}),
                'DlG' : ({'id' : dict['source']}, {'$push' : {'localizes' : dict['target'] }}),
                'CtD' : ({'id' : dict['target']}, {'$push' : {'treat' : dict['source'] }}),
                'CpD' : ({'id' : dict['target']}, {'$push' : {'palliates' : dict['source'] }})
            }   
    
        return query_builder_dict.get(key, "")
    
    def create_properties(self, filename):
        print('CREATING PROPERTIES')
        try: 
            with open(filename) as input_file:
                reader = DictReader(input_file, delimiter='\t')

                for row in reader:
                    if row['metaedge'] in ['DaG', 'DlG', 'CtD', 'CpD']:
                        queries = self.get_update_query(row, row['metaedge'])
                        self.mongo_collection.update(queries[0], queries[1])
        
        except FileNotFoundError as e:
            print(e)

    def initialize_mongo(self):
        self.create_documents('nodes.tsv')
        self.create_properties('edges.tsv')
