from csv import DictReader
from helpers import pretty_print_dictionary
from pymongo import MongoClient
import pandas as pd

class HetioMongo():

    def __init__(self, nodes_file=None, edges_file=None):
        self.mongo_client = MongoClient()['hetio_db']
        self.mongo_collection = self.mongo_client['hetio_collection']
        self.nodes_file = nodes_file
        self.edges_file = edges_file
        
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
                'DlA' : ({'id' : dict['source']}, {'$push' : {'localizes' : dict['target'] }}),
                'CtD' : ({'id' : dict['target']}, {'$push' : {'treatments' : dict['source'] }}),
                'CpD' : ({'id' : dict['target']}, {'$push' : {'palliates' : dict['source'] }})
            }   
    
        return query_builder_dict.get(key, "")
    
    def create_properties(self, filename):
        print('CREATING PROPERTIES')
        try: 
            with open(filename) as input_file:
                reader = DictReader(input_file, delimiter='\t')

                for row in reader:
                    if row['metaedge'] in ['DaG', 'DlA', 'CtD', 'CpD']:
                        queries = self.get_update_query(row, row['metaedge'])
                        self.mongo_collection.update(queries[0], queries[1])
        
        except FileNotFoundError as e:
            print(e)

    def clear_collection(self):
        print('CLEARING DOCUMENTS')
        self.mongo_collection.remove({})

    def resolve_name_from_id(self, id):
        query = {'id' : id}

        return self.mongo_collection.find_one(query)['name']

    def find_disease(self, identifier, value):
        query = {identifier : {'$regex': value},   
                 'kind': 'Disease'}
        query_result = self.mongo_collection.find_one(query)

        self.format_query_result(query_result)

    def format_query_result(self, document_dict):
        results = {
            'Name' : document_dict['name'],
            'Associates with' : [self.resolve_name_from_id(g_id) for g_id in document_dict.get('associates', '')],
            'Located in' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('localizes', '')],
            'Treated by' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('treats', '')],
            'Palliated by' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('palliates', '')]
        }

        pretty_print_dictionary(results)
            
    def initialize_mongo(self):
        self.clear_collection()
        self.create_documents(self.nodes_file)
        self.create_properties(self.edges_file)