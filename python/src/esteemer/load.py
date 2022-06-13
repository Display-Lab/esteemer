import warnings

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

warnings.filterwarnings("ignore")


def read(file):
    g = Graph()
    g.parse(file)
    qres = g.query(
        """
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
    """
    )
    return qres.graph


def transform(contenders_graph):
    contenders_graph.bind("obo", "http://purl.obolibrary.org/obo/")
    contenders_graph.bind("slowmo", "http://example.com/slowmo#")

    # start implementation of esteemer algorithm
    contender_messages_df = to_dataframe(contenders_graph)
    contender_messages_df.reset_index(inplace=True)
    contender_messages_df = contender_messages_df.rename(columns={"index": "id"})
    # contender_messages_df.to_csv("df_es.csv")
    column_values = [
        "obo:RO_0000091{BNode}[0]",
        "obo:RO_0000091{BNode}[1]",
        "obo:RO_0000091{BNode}[2]",
        "obo:RO_0000091{BNode}[3]",
        "obo:RO_0000091{BNode}[4]",
        "obo:RO_0000091{BNode}[5]",
        "obo:RO_0000091{BNode}[6]",
        "obo:RO_0000091{BNode}[7]",
        "obo:RO_0000091{BNode}[8]",
        "obo:RO_0000091{BNode}[9]",
        "obo:RO_0000091{BNode}[10]",
    ]

    reference_df = contender_messages_df.filter(
        [
            "id",
            "rdf:type{URIRef}",
            "slowmo:RegardingComparator{BNode}",
            "slowmo:RegardingMeasure{BNode}",
        ],
        axis=1,
    )

    meaningful_messages_df = contender_messages_df[
        contender_messages_df["slowmo:AncestorPerformer{Literal}"].notna()
    ]
    reference_df1 = reference_df.dropna()

    RegardingComparator = []
    RegardingMeasure = []
    disposition = []
    values = []

    for rowIndex, row in meaningful_messages_df.iterrows():  # iterate over rows
        b = 0
        for columnIndex, value in row.items():
            if columnIndex in column_values:
                a = reference_df1.loc[reference_df1["id"] == value]
                if not a.empty:
                    if b == 0:
                        a.reset_index(drop=True, inplace=True)
                        disposition.append(a["rdf:type{URIRef}"][0])
                        values.append(value)
                        RegardingComparator.append(
                            a["slowmo:RegardingComparator{BNode}"][0]
                        )
                        RegardingMeasure.append(a["slowmo:RegardingMeasure{BNode}"][0])
                        b = b + 1
    meaningful_messages_df["RegardingComparator"] = RegardingComparator
    meaningful_messages_df["RegardingMeasure"] = RegardingMeasure
    meaningful_messages_df["disposition"] = disposition
    meaningful_messages_df["reference_values"] = values
    meaningful_messages_final = meaningful_messages_df.filter(
        [
            "id",
            "slowmo:AncestorPerformer{Literal}",
            "slowmo:AncestorTemplate{Literal}",
            "disposition",
            "reference_values",
            "rdf:type{URIRef}",
            "psdo:PerformanceSummaryDisplay{Literal}",
            "psdo:PerformanceSummaryTextualEntity{Literal}",
            "RegardingComparator",
            "RegardingMeasure",
            "slowmo:acceptable_by{URIRef}[0]",
            "slowmo:acceptable_by{URIRef}[1]",
        ],
        axis=1,
    )

    return meaningful_messages_final


def graph_from_sparql_endpoint(endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(
        """
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
    """
    )
    results = sparql.queryAndConvert()
    return results
