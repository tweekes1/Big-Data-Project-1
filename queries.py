anatomy_labels_query = '''
    MATCH (a:Node)
    WHERE a.kind = 'Anatomy'
    REMOVE a:Node
    SET a:Anatomy
'''

compound_labels_query = '''
    MATCH (a:Node)
    WHERE a.kind = 'Compound'
    REMOVE a:Node
    SET a:Compound
'''

disease_labels_query = '''
    MATCH (a:Node)
    WHERE a.kind = 'Disease'
    REMOVE a:Node
    SET a:Disease
'''

gene_labels_query = '''
    MATCH (a:Node)
    WHERE a.kind = 'Gene'
    REMOVE a:Node
    SET a:Gene
'''

treats_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CtD']
    CREATE (a)-[:TREATS]->(b)
    DELETE r
'''

upregulates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['AuG', 'CuG', 'DuG']
    CREATE (a)-[:UPREGULATES]->(b)
    DELETE r
'''

downregulates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['AdG', 'CdG', 'DdG']
    CREATE (a)-[:DOWNREGULATES]->(b)
    DELETE r
'''

resembles_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CrC', 'DrD']
    CREATE (a)-[:RESEMBLES]->(b)
    DELETE r
'''

interacts_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['GiG']
    CREATE (a)-[:INTERACTS]->(b)
    DELETE r
'''

covaries_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['GcG']
    CREATE (a)-[:COVARIES]->(b)
    DELETE r
'''

regulates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['Gr>G']
    CREATE (a)-[:REGULATES]->(b)
    DELETE r
'''

expresses_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['AeG']
    CREATE (a)-[:EXPRESES]->(b)
    DELETE r
'''

associates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['DaG']
    CREATE (a)-[:ASSOCIATES]->(b)
    DELETE r
'''

binds_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CbG']
    CREATE (a)-[:BINDS]->(b)
    DELETE r
'''

palliates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CdP']
    CREATE (a)-[:PALLIATES]->(b)
    DELETE r
'''

localizes_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['DlA']
    CREATE (a)-[:LOCALIZES]->(b)
    DELETE r
'''

label_queries = [anatomy_labels_query, compound_labels_query, 
                 disease_labels_query, gene_labels_query]

relationship_queries = [associates_rel_query, binds_rel_query, covaries_rel_query, downregulates_rel_query,
                        expresses_rel_query, interacts_rel_query, localizes_rel_query, palliates_rel_query,
                        regulates_rel_query, resembles_rel_query, treats_rel_query, upregulates_rel_query]