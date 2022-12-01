from rdflib.namespace import RDF

def create_ttl(g, u, row):
    """
    resolution: 1.31
    pdbid: 6X8O
    title: BimBH3 peptide tetramer
    expmethod: X-RAY DIFFRACTION
    lignme: SCN
    glytoucan: NULL
    cids: 9322
    protacxns: O43521
    geneids: 10018
    pmids: 32966763
    dois: 10.1016/j.str.2020.09.002
    """

    Interactor_ab = create_subject_uri(row[0], row[1])
    g.add((Interactor_ab, RDF.type, molecular_interaction))

    Interactor_a = create_object_uri(row[0], db_list)
    g.add((Interactor_ab, has_interactorA, Interactor_a))
    g.add((Interactor_a, RDF.type, functional_entiry))
    Interactor_b = create_object_uri(row[1], db_list)
    g.add((Interactor_ab, has_interactorB, Interactor_b))
    g.add((Interactor_b, RDF.type, functional_entiry))

    if row[6] != "-" and row[6] != "":
        Detection_method = create_object_uri(row[6], db_list)
        g.add((Interactor_ab, detected_by, Detection_method))
    return g

