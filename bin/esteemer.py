from rdflib import Graph,URIRef
from rdflib.namespace import RDFS,SKOS
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import SPARQLWrapper,XML
import random
import pandas as pd
import sys
import warnings
import json
from load import read ,transform
from score import score , select

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
contenders_graph=read(sys.argv[1])
meaningful_messages_final = transform(contenders_graph)
meaningful_messages_final = score(meaningful_messages_final)
finalData = select(meaningful_messages_final )
#contenders_graph=graph_from_file(sys.argv[1])
print(finalData)
with open('data.json', 'a') as f:
    f.write(finalData + '\n')
