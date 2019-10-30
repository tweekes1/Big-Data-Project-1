from cmd import Cmd
from hetio_graph import HetioGraph
from hetio_mongo import HetioMongo

'''
@class Terminal

Driver class for the Hetio Database. If you want to use different files to run
different test cases change the them in the __init__ method.
'''
class Terminal(Cmd):
    
    def __init__(self):
        super().__init__()
        self.prompt = 'HetioDB> '
        self.is_initialized = False
        self.mongo_db = HetioMongo('nodes.tsv', 'edges.tsv')
        self.graph_db = HetioGraph(password='Temp1234$')
        print('Welcome to the Hetio Database type \'init\' to begin')

    def do_init(self, args):
        if self.is_initialized:
            print('Hetio is already initialized')
        else: 
            self.mongo_db.initialize_mongo()
            self.graph_db.initialize_graph()
            print('The Hetio Database is initialized')
            self.is_initialized = True
            return
        
    def do_discover(self, args):
        if self.is_initialized:
            self.graph_db.discover_new_treatments() 
        else:
            print('The HetioDB is not initialized')           

    def do_id(self, args):
        if self.is_initialized:
            self.mongo_db.find_disease('id', args)
        else: 
            print('The HetioDB is not initialized')

    def do_name(self, args):
        if self.is_initialized:
            self.mongo_db.find_disease('name', args)
        else: 
            print('The HetioDB is not initialized')

    def default(self, args):
        if args is not 'init':
            print('The HetioDB is not initialized')
        else:
            print('Enter \'discover\' to find all the hidden treatmnents')
            print('Enter \'id\' <DISEASE_ID> to find all the information about a disease')
            print('Enter \'name\' <DISEASE_NAME> to find all the information about a disease')
        
    def do_exit(self, exit): 
        print('Goodbye!')
        return True

    def emptyline(self):
        return 

term = Terminal()
term.cmdloop()
