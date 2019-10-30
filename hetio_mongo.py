from csv import DictReader
from helpers import pretty_print_dictionary
from pymongo import MongoClient

'''
@class HetioMongo
@param nodes_file: A file that will be used to create documents based on the nodes provided.
@param edges_file: A file that will be used to add properties to the documents.

Provides mongo db functionality to store all the items in the nodes.tsv file as documents and 
uses the edges.tsv file to update the 'Disease' documents to appending the IDs to the 
associates, localizes, palliates, and treats lists. 
'''
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

    def create_documents(self, filename):
        print('CREATING DOCUMENTS')
        try: 
            with open(filename) as input_file:
                reader = DictReader(input_file, delimiter='\t')

                for row in reader:    
                    self.mongo_collection.insert_one({'id': row['id'], 'name': row['name'], 'kind': row['kind']})

        except FileNotFoundError as e:
            print(e)
  
    '''
    @param dict: A dictionary that is used to retrieve the value of a line from the edges.tsv file. 
    @param key: The key that will be used to access the dictionary.
    @return: A tuple of the value accessed by the key.

    Method that is used to get the Disease id and id of the entity it has a relationship with. Used
    by @method create_properties.
    '''
    def get_update_query(self, dict, key):
        query_builder_dict = {
                'DaG' : ({'id' : dict['source']}, {'$push' : {'associates' : dict['target'] }}),
                'DlA' : ({'id' : dict['source']}, {'$push' : {'localizes' : dict['target'] }}),
                'CpD' : ({'id' : dict['target']}, {'$push' : {'palliates' : dict['source'] }}),
                'CtD' : ({'id' : dict['target']}, {'$push' : {'treatments' : dict['source'] }})
            }   
    
        return query_builder_dict.get(key, "")
    
    '''
    @param filename: File that we be used to retrieve the edges for the relationships. Requires
    param just incase for alternative testing.

    Method that is used to append the id of an entity to a one of a Disease's relationship lists.
    '''
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

    '''
    @param id: The id of the entity whose name is to be accessed.
    @return: Returns the name attribute for the document.
    '''
    def resolve_name_from_id(self, id):
        query = {'id' : id}

        return self.mongo_collection.find_one(query)['name']

    '''
    @param identifier: The way the mongo db will be queried for the information on a disease
    @param value: The value to use to query the database

    Method queries the mongo db using a regular expression based on the value given and will 
    return one record if found. 
    '''
    def find_disease(self, identifier, value):
        query = {identifier : {'$regex': value},   
                 'kind': 'Disease'}
        query_result = self.mongo_collection.find_one(query)

        if query_result is None:
            print(f'There is no disease with the {identifier} \'{value}\'')
            return

        self.format_query_result(query_result)

    '''
    @param documnet_dict: The dictionary that will be printed in a understandable format 
    '''
    def format_query_result(self, document_dict):
        results = {
            'Name' : document_dict['name'],
            'Associates with' : [self.resolve_name_from_id(g_id) for g_id in document_dict.get('associates', '')],
            'Located in' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('localizes', '')],
            'Treated by' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('treatments', '')],
            'Palliated by' : [self.resolve_name_from_id(a_id) for a_id in document_dict.get('palliates', '')]
        }

        pretty_print_dictionary(results)
            
    '''
    Method to initialize the mongo db. 
    '''
    def initialize_mongo(self):
        self.clear_collection()
        self.create_documents(self.nodes_file)
        self.create_properties(self.edges_file)