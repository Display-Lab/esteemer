from rdflib import Graph,URIRef
from rdflib.namespace import RDFS,SKOS
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import SPARQLWrapper,XML
import pandas as pd
import sys
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
    }
    WHERE {
    ?candidate a obo:cpo_0000053 .
    ?candidate slowmo:AncestorPerformer ?performer .
    ?candidate obo:RO_0000091 ?disposition .
    ?candidate ?p ?o .
    ?disposition ?p2 ?o2 .
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
print(contenders_graph.serialize(format="ttl"))

#start implementation of esteemer algorithm
a=to_dataframe(contenders_graph)



# a.to_csv("df_es.csv",index = True, index_label = "@id")
