from cmd import Cmd
from hetio_graph import HetioGraph
from hetio_mongo import HetioMongo


class Terminal(Cmd):
    
    def __init__(self):
        super().__init__()
        self.prompt = 'HetioDB> '
        self.initialized = False
        self.mongo_db = HetioMongo('nodes.tsv', 'edges.tsv')
        self.graph_db = HetioGraph(password='Temp1234$')

    def do_init(self, args):
        if not self.initialized:
            # self.mongo_db.initialize_mongo()
            # self.graph_db.initialize_graph()
            print('HETIO DB INITIALIZED')
            self.initialized = True
            return
        print('HETIO DB ALREADY INITIALIZED')
        
    def do_discover(self, args):
        self.is_initialized()
        self.graph_db.discover_new_treatments()

    def do_id(self, args):
        self.is_initialized()
        self.mongo_db.find_disease('id', args)

    def do_name(self, args):
        self.is_initialized()
        self.mongo_db.find_disease('name', args)
        
    def do_exit(self, exit): 
        return True

    def emptyline(self):
        return 

    def is_initialized(self):
        if not self.initialized:
            print('HETIO NOT INITIALIZED')
            print('type \'init\'')
            return

term = Terminal()
term.cmdloop()
