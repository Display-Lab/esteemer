import sys
import warnings
import time
import logging
import json
#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

# from .load_for_real import load
from .load import read, transform,read_contenders,read_measures,read_comparators
from .score import score, select,apply_indv_preferences

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
start_time = time.time()
graph_read = read(sys.argv[1])
f=open(sys.argv[2])
indv_preferences_read = json.load(f)
f1=open(sys.argv[3])
message_code= json.load(f1)
#indv_preferences_read_df = pd.read_json(sys.argv[2], lines=True)
contenders_graph = read_contenders(graph_read)
measures_graph = read_measures(graph_read)
comparator_graph = read_comparators(graph_read)
# print(contenders_graph)
# contenders_graph=graph_from_sparql_endpoint("http://localhost:3030/ds/sparql")
# print(contenders_graph.serialize(format="ttl"))
# Transform dataframe to more meaningful dataframe
meaningful_messages_final = transform(contenders_graph,measures_graph,comparator_graph)
# print(meaningful_messages_final)
# assign score for each of meaningful_messages
start_time1 = time.time()
meaningful_messages_final = score(meaningful_messages_final)
#apply individual preferences
applied_individual_messages,max_val = apply_indv_preferences(meaningful_messages_final,indv_preferences_read)
val = max_val.split('_')
print(val[0])
#
# select maximum of the meaningful_messages

finalData = select(applied_individual_messages,val[0],message_code)
logging.critical("--score and select %s seconds ---" % (time.time() - start_time1))
print(finalData)

time_taken = time.time()-start_time
logging.critical("---total esteemer run time according python script %s seconds ---" % (time.time() - start_time))
#print("--- %s seconds ---" % (time.time() - start_time))
"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""
