from rdflib import Graph,URIRef
from rdflib.namespace import RDFS,SKOS
from rdflib.serializer import Serializer
from rdflib.collection import Collection
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD
g=Graph()
#myGraph.namespace_manager.bind('prefix', URIRef('scheme:my-namespace-uri:'))
#obo = Namespace('http://purl.obolibrary.org/obo/')
#slowmo = Namespace('http://example.com/slowmo#')
#ns =dict(obo=obo,slowmo=slowmo)
#g.bind('obo',obo, override=True)
#g.bind('slowmo',slowmo ,override=True)
#print("python script works")
g.parse('spek_tp.json')
l=len(g)
print(l)
#for index , (sub,pred,obj) in enumerate(g):
#    print(sub,pred,obj)
#    if index == 10:
#        break

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
results = qres
#context= {"slowmo": "http://example.com/slowmo#","obo": "http://purl.obolibrary.org/obo/","@vocab": "http://schema.org/"}
print(qres.serialize(format='ttl').decode('u8'))
