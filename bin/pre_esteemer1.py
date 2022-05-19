from SPARQLWrapper import SPARQLWrapper,XML
sparql = SPARQLWrapper("http://localhost:3030/ds/sparql")
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
print(results.serialize(format="turtle"))
