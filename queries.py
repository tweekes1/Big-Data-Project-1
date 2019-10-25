node_import_query = '''
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM "file:///nodes.tsv" AS LINE
    FIELDTERMINATOR '\t'
    MERGE(n:Node {id: LINE.id, name: LINE.name, kind: LINE.kind})
''' 

edge_import_query = '''
    USING PERIODIC COMMIT 10000
    LOAD CSV WITH HEADERS FROM "file:///edges.tsv" AS LINE
    FIELDTERMINATOR '\t' 
    MATCH (A:Node{id: LINE.source})
    MATCH (B:Node{id: LINE.target})
    CREATE (A)-[:RELATES{type: LINE.metaedge}]->(B)
'''

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
    CREATE (a)-[:UPREGULATES {property: 'upregulates'}]->(b)
    DELETE r
'''

downregulates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['AdG', 'CdG', 'DdG']
    CREATE (a)-[:DOWNREGULATES {property: 'downregulates'}]->(b)
    DELETE r
'''

resembles_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CrC', 'DrD']
    CREATE (a)-[:RESEMBLES {property: 'resembles'}]->(b)
    DELETE r
'''

interacts_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['GiG']
    CREATE (a)-[:INTERACTS {property: 'interacts'}]->(b)
    DELETE r
'''

covaries_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['GcG']
    CREATE (a)-[:COVARIES {property: 'covaries'}]->(b)
    DELETE r
'''

regulates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['Gr>G']
    CREATE (a)-[:REGULATES {property: 'regulates'}]->(b)
    DELETE r
'''

expresses_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['AeG']
    CREATE (a)-[:EXPRESSES {property: 'expresses'}]->(b)
    DELETE r
'''

associates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['DaG']
    CREATE (a)-[:ASSOCIATES {property: 'associates'}]->(b)
    DELETE r
'''

binds_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CbG']
    CREATE (a)-[:BINDS {property: 'binds'}]->(b)
    DELETE r
'''

palliates_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['CdP']
    CREATE (a)-[:PALLIATES {property: 'palliates'}]->(b)
    DELETE r
'''

localizes_rel_query = '''
    MATCH (a:Node)-[r]->(b:Node)
    WHERE r.type IN ['DlA']
    CREATE (a)-[:LOCALIZES {property: 'localizes'}]->(b)
    DELETE r
'''

discover_new_treatments_query = '''
    MATCH (new_treatment:Compound)-[:UPREGULATES]->(G:Gene)<-[:DOWNREGULATES]-(:Anatomy)<-[:LOCALIZES]-(new_disease:Disease)
    OPTIONAL MATCH (similar)-[:RESEMBLES]-(new_treatment)
    WHERE similar IS NOT NULL
    WITH collect(new_treatment) + collect(similar)  AS nodes, new_disease.name as Disease
    UNWIND nodes as treatments
    RETURN treatments.name as Treatment, Disease 
    UNION
    MATCH (new_treatment:Compound)-[:DOWNREGULATES]->(G:Gene)<-[:UPREGULATES]-(:Anatomy)<-[:LOCALIZES]-(new_disease:Disease)
    OPTIONAL MATCH (similar)-[:RESEMBLES]-(new_treatment)
    WHERE similar IS NOT NULL
    WITH collect(new_treatment) + collect(similar)  AS nodes, new_disease.name as Disease
    UNWIND nodes as treatments
    RETURN DISTINCT treatments.name as Treatment, Disease 
'''

label_queries = [anatomy_labels_query, compound_labels_query, 
                 disease_labels_query, gene_labels_query]

relationship_queries = [associates_rel_query, binds_rel_query, covaries_rel_query, downregulates_rel_query,
                        expresses_rel_query, interacts_rel_query, localizes_rel_query, palliates_rel_query,
                        regulates_rel_query, resembles_rel_query, treats_rel_query, upregulates_rel_query]