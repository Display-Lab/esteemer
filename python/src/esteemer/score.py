import json
import random
import sys
import warnings

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

warnings.filterwarnings("ignore")


def score(meaningful_messages_final):
    len = meaningful_messages_final.shape[0]
    score = [1] * len
    #score = random.sample(range(10, 1000), len)
    meaningful_messages_final["score"] = score
    meaningful_messages_final.reset_index(drop=True, inplace=True)
    meaningful_messages_final.to_csv("df_es1.csv")
    return meaningful_messages_final
    # meaningful_messages_final.to_csv("df_es1.csv")

def apply_indv_preferences(meaningful_messages_final,indv_preferences_read):
    indv_preferences_df = pd.json_normalize(indv_preferences_read)
    indv_preferences_df.to_csv('individual_preferences.csv')
    return meaningful_messages_final



def select(meaningful_messages_final):
    # max value of score
    column = meaningful_messages_final["score"]
    max_value = column.max()
    # print(max_value)

    h = meaningful_messages_final["score"].idxmax()
    # print(h)
    message_selected_df = meaningful_messages_final.iloc[h, :]
    message_selected_df = message_selected_df.T
    # print(message_selected_df)
    # message_selected_df.to_csv("Selected_Message.csv")
    data = message_selected_df.to_json(orient="index", indent=2 )

    return data.replace("\\", "")
