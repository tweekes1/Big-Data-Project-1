# Simple function to make dictionary printing nicer
def pretty_print_dictionary(dictionary):
    for key in dictionary.keys():
        print(str(key) + ':') 
        if isinstance(dictionary[key], (list,)):
            for value in dictionary[key]:
                print('\t' + str(value))
        else:
            print('\t' + str(dictionary[key]))