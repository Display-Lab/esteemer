# Esteemer Scripts
The main purpose of Esteemer stage is to promote the candidate messages that are marked as accepted by think pudding. 

The `esteemer` script should load the Think Pudding graph, extract relevant message parts, and mark one candidate per ancestor performer in the graph as `promoted` based on some criteria (tbd).

## Running the Esteemer script locally
```sh
python -m esteemer.esteemer [/path/to/spek_tp.json]
```
You must be in the root of the Python esteemer package.

## Install the Esteemer package globally

```sh
pip install [/path/or/url/to/esteemer-0.1.0-py3-none-any.whl]
```

## Installing the Esteemer package in development mode

```sh
pip install -e [path/to/module/displaylab/esteemer/python]
```


## How it works

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
