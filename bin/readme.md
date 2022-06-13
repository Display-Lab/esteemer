# Esteemer Scripts
The main purpose of Esteemer stage is to promote the candidate messages that are marked as accepted by think pudding. 

The first stage `presteemer` creates a sub graph of all candidates that includes their `AncestorPerformer` attribute so that esteemer has that available to do its work.

Then, the `esteemer` script should mark one candidate per ancestor performer in the graph as `promoted` based on some criteria (tbd).

## Presteemer
Constructs a graph of all candidates with their AncestorPerformer attributes using the spek loaded in.
### Use
Options:
- `-h | --help`     print help and exit
- `-s | --spek`     path to spek file (default to stdin)

##### Example
```bash
$DISPLAY_LAB_HOME/esteemer/bin/presteemer.sh \
  -s ./outputs/spek_tp.json \
  2>> vignette.log > ./outputs/spek_pe.ttl
```

#### Query inside
```sql
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
  ?candidate ?p ?o .
  ?candidate obo:RO_0000091 ?disposition .
  ?disposition ?p2 ?o2 .
  ?candidate slowmo:AncestorPerformer ?performer .
}
```
### Esteemer

Evaluate acceptable candidates for promotion to figure generation.

#### Use
Options:
- `-h | --help` print help and exit
- `-p | --pathways` path to causal pathways
- `-s | --spek` path to spek file (default to stdin)

##### Example
```bash
$DISPLAY_LAB_HOME/esteemer/bin/esteemer.sh \
    -s ./outputs/spek_pe.ttl \
    -p ${KNOWLEDGE_BASE_DIR}/causal_pathways.json \
    2>> vignette.log > .outputs/spek_es.json
```

#### Default Esteemer Criteria
Provides a passthrough for all acceptable candidates.
Any candidate that is `acceptable_by` is annotated as `promoted_by http://example.com/slowmo#esteemer_default_criteria`
