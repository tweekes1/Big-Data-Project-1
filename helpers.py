'''
@param dictionary: a dictionary to be printed.

Function that will display a disctionary in a nicer fashion
'''
def pretty_print_dictionary(dictionary):
    for key in dictionary.keys():
        print(str(key) + ':') 
        if isinstance(dictionary[key], (list,)):
            for value in dictionary[key]:
                print('\t' + str(value))
        else:
            print('\t' + str(dictionary[key]))