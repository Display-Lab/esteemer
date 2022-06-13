import sys
import warnings
from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

# from .load_for_real import load
from .load import read, transform
from .score import score, select

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
contenders_graph = read(sys.argv[1])
# print(contenders_graph)
# contenders_graph=graph_from_sparql_endpoint("http://localhost:3030/ds/sparql")
# print(contenders_graph.serialize(format="ttl"))
# Transform dataframe to more meaningful dataframe
meaningful_messages_final = transform(contenders_graph)
# print(meaningful_messages_final)
# assign score for each of meaningful_messages
meaningful_messages_final = score(meaningful_messages_final)
# select maximum of the meaningful_messages
finalData = select(meaningful_messages_final)

print(finalData)
"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""
