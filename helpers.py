# Will be used to look up the second letter of a metaedge in the edges.txt file
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

'''
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

def determine_relationship(edge):
    source, metaedge, target = process_string(edge)
    relationship = RELATIONSHIP_DICT[metaedge[1]]

    print(f'{source} {relationship} {target}')
