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
    display_preferences_df =indv_preferences_df [['Utilities.Display_Format.short_sentence_with_no_chart', 'Utilities.Display_Format.bar_chart','Utilities.Display_Format.line_graph']]
    message_preferences_df =indv_preferences_df[['Utilities.Message_Format.top_performer','Utilities.Message_Format.top_performer','Utilities.Message_Format.performance_dropped_below_peer','Utilities.Message_Format.no_message_data_displayed_in_chart_only','Utilities.Message_Format.may_have_opportunity_to_improve','Utilities.Message_Format.performance_approaching_MPOG_goal','Utilities.Message_Format.performance_improving','Utilities.Message_Format.your_performance_is_getting_worse','Utilities.Message_Format.one_of_your_patients_had_an_adverse_event']]
    
    display_preferences = displaypreferences(meaningful_messages_final,display_preferences_df)
    display_preferences_df.to_csv('display_preferences.csv')
    message_preferences_df.to_csv('message_preferences_df.csv')
    indv_preferences_df.to_csv('individual_preferences.csv')
    return meaningful_messages_final

def displaypreferences(meaningful_messages_final,display_preferences_df):
    no_chart_pref=display_preferences_df.at[0,'Utilities.Display_Format.short_sentence_with_no_chart']
    bar_pref=display_preferences_df.at[0,'Utilities.Display_Format.bar_chart']
    line_pref=display_preferences_df.at[0,'Utilities.Display_Format.line_graph']
    line_pref = int(line_pref)
    bar_pref = int(bar_pref)
    no_chart_pref = int(no_chart_pref)
    #print(type(line_pref))
    for index, row in meaningful_messages_final.iterrows():
        display_pref = row['psdo:PerformanceSummaryDisplayCompatibletype{Literal}']
        x = display_pref.split(", ")
        print(x)
    return line_pref
    







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
