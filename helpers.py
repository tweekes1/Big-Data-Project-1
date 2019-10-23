# Will be used to determine the node type
NODE_DICT = {
    'A' : 'ANATOMY',
    'C' : 'COMPOUND',
    'D' : 'DISEASE',
    'G' : 'GENE'
}

# Will be used to find the relationship between two nodes
RELATIONSHIP_DICT = {
    'a' : 'ASSOCIATES',
    'b' : 'BINDS',
    'c' : 'COVARIES',
    'd' : 'DOWNREGULATES',
    'e' : 'EXPRESSES',
    'i' : 'INTERACTS',
    'l' : 'LOCALIZES',
    'p' : 'PALLIATES',
    't' : 'TREATS',
    'u' : 'UPREGULATES',
    'r' : 'RESEMBLES',
    'r>' : 'REGULATES'
    } 

'''-
Splits a string that is delimited by tabs
and outputs them as a list. Keeps code 
clean and readable

@file_line: A string from a file that
@return: A list (split_string)  of the line
'''

def process_string(file_line):
    split_string = file_line.split('\t')
    return split_string

'''
Will determine the relationship between two nodes
using @RELATIONSHIP_DICT 

@edge: a list of the values in the edges.txt file.
Will display what the relationship is between nodes.
'''
