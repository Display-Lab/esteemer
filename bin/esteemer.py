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
warnings.filterwarnings("ignore")
def graph_from_file(file):
    g=Graph()
    g.parse(file)
    qres = g.query('''
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX slowmo: <http://example.com/slowmo#>
    construct {
    ?candidate ?p ?o .
    ?candidate obo:RO_0000091 ?disposition .
    ?disposition ?p2 ?o2 .
    ?candidate slowmo:acceptable_by ?o3 .
    }
    WHERE {
    ?candidate a obo:cpo_0000053 .
    ?candidate slowmo:AncestorPerformer ?performer .
    ?candidate obo:RO_0000091 ?disposition .
    ?candidate ?p ?o .
    ?disposition ?p2 ?o2 .
    ?candidate slowmo:acceptable_by ?o3 .
    }
    ''')
    return qres.graph


def graph_from_sparql_endpoint(endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("""
      PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX slowmo: <http://example.com/slowmo#>
    construct {
      ?candidate ?p ?o .
      ?candidate obo:RO_0000091 ?disposition .
      ?disposition ?p2 ?o2 .
    }
    FROM <http://localhost:3030/ds/spek>
    WHERE {
      ?candidate a obo:cpo_0000053 .
      ?candidate slowmo:AncestorPerformer ?performer .
      ?candidate obo:RO_0000091 ?disposition .
      ?candidate ?p ?o .
      ?disposition ?p2 ?o2 .
    }
    """)
    results = sparql.queryAndConvert()
    return results


# TODO: process command line args if using graph_from_file()
contenders_graph=graph_from_file(sys.argv[1])
contenders_graph.bind("obo",'http://purl.obolibrary.org/obo/')
contenders_graph.bind("slowmo",'http://example.com/slowmo#')
# contenders_graph=graph_from_sparql_endpoint("http://localhost:3030/ds/sparql")
#print(contenders_graph.serialize(format="ttl"))

#start implementation of esteemer algorithm
contender_messages_df=to_dataframe(contenders_graph)
contender_messages_df.reset_index(inplace=True)
contender_messages_df = contender_messages_df.rename(columns = {'index':'id'})
#contender_messages_df.to_csv("df_es.csv")
column_values =['obo:RO_0000091{BNode}[0]','obo:RO_0000091{BNode}[1]','obo:RO_0000091{BNode}[2]','obo:RO_0000091{BNode}[3]','obo:RO_0000091{BNode}[4]','obo:RO_0000091{BNode}[5]','obo:RO_0000091{BNode}[6]','obo:RO_0000091{BNode}[7]','obo:RO_0000091{BNode}[8]','obo:RO_0000091{BNode}[9]','obo:RO_0000091{BNode}[10]']


reference_df = contender_messages_df.filter(['id','rdf:type{URIRef}','slowmo:RegardingComparator{BNode}','slowmo:RegardingMeasure{BNode}'], axis=1)
meaningful_messages_df =contender_messages_df[contender_messages_df['slowmo:AncestorPerformer{Literal}'].notna()]
reference_df1 =reference_df.dropna()

RegardingComparator=[]
RegardingMeasure=[]
disposition=[]
values=[]

for rowIndex, row in meaningful_messages_df.iterrows(): #iterate over rows
    b=0
    for columnIndex, value in row.items():
        if columnIndex in column_values:
            a=reference_df1.loc[reference_df1['id'] == value]
            if not a.empty:
                if b == 0:
                    a.reset_index(drop=True, inplace=True)
                    disposition.append(a['rdf:type{URIRef}'][0])
                    values.append(value)
                    RegardingComparator.append(a['slowmo:RegardingComparator{BNode}'][0])
                    RegardingMeasure.append(a['slowmo:RegardingMeasure{BNode}'][0])
                    b=b+1
            #RegardingComparator1 = list(set(RegardingComparator))

#print(' '.join(map(str, disposition)))
#print(' '.join(map(str, RegardingComparator)))
#print(' '.join(map(str, RegardingMeasure)))
#print(' '.join(map(str, values)))
#print(len(values))
#print(meaningful_messages_df.shape)

meaningful_messages_df["RegardingComparator"] = RegardingComparator
meaningful_messages_df["RegardingMeasure"] = RegardingMeasure
meaningful_messages_df["disposition"]=disposition
meaningful_messages_df["reference_values"]=values
meaningful_messages_final= meaningful_messages_df.filter(['id','slowmo:AncestorPerformer{Literal}','slowmo:AncestorTemplate{Literal}','disposition','reference_values','rdf:type{URIRef}','psdo:PerformanceSummaryDisplay{Literal}','psdo:PerformanceSummaryTextualEntity{Literal}','RegardingComparator','RegardingMeasure','slowmo:acceptable_by{URIRef}[0]','slowmo:acceptable_by{URIRef}[1]'], axis=1)

#random generation of score
len = meaningful_messages_final.shape[0]
score = random.sample(range(10,1000), len)
meaningful_messages_final["score"]=score
meaningful_messages_final.reset_index(drop=True, inplace=True)
meaningful_messages_final.to_csv("df_es1.csv")

#max value of score
column = meaningful_messages_final["score"]
max_value = column.max()
#print(max_value)

h=meaningful_messages_final['score'].idxmax()
#print(h)
message_selected_df = meaningful_messages_final.iloc[h, :]
message_selected_df =message_selected_df.T
#print(message_selected_df)
message_selected_df.to_csv("Selected_Message.csv")
