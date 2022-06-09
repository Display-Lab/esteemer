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
import transform
import json
from load import read ,transform
warnings.filterwarnings("ignore")

def score (meaningful_messages_final):
    len = meaningful_messages_final.shape[0]
    score = random.sample(range(10,1000), len)
    meaningful_messages_final["score"]=score
    meaningful_messages_final.reset_index(drop=True, inplace=True)
    return meaningful_messages_final
    #meaningful_messages_final.to_csv("df_es1.csv")
def select(meaningful_messages_final):
    #max value of score
    column = meaningful_messages_final["score"]
    max_value = column.max()
    #print(max_value)

    h=meaningful_messages_final['score'].idxmax()
    #print(h)
    message_selected_df = meaningful_messages_final.iloc[h, :]
    message_selected_df =message_selected_df.T
    #print(message_selected_df)
    #message_selected_df.to_csv("Selected_Message.csv")
    data = message_selected_df.to_json(orient='index')

    finalData = data.replace("\\", "")
    return finalData
