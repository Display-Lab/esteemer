# Esteemer Scripts
The main purpose of Esteemer stage is to promote the candidate messages that are marked as accepted by think pudding. 

The `esteemer` script should load the Think Pudding graph, extract relevant message parts, and mark one candidate per ancestor performer in the graph as `promoted` based on some criteria (tbd).

## Install the Esteemer package globally

```sh
pip install [/path/or/url/to/esteemer-0.1.0-py3-none-any.whl]
```

## Installing the Esteemer package in development mode

```sh
pip install -e [path/to/module/displaylab/esteemer/python]
```

## Running the Esteemer script 
```sh
python -m esteemer.esteemer [/path/to/spek_tp.json]
```

## Running the pfp pipeline (pfp.sh)
Note: This assumes that you installed the pfp pipeline installed and you have installed the esteemer package

```sh
cd $DISPLAY_LAB_HOME/vert-ramp-affirmation/vignettes/aspire
./$DISPLAY_LAB_HOME/vert-ramp-affirmation/pfp.sh
```
See vert-ramp-affirmation readme docs for more info

## How it works

#### Query inside
```PREFIX obo: <http://purl.obolibrary.org/obo/>
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
```
### Esteemer

Evaluate acceptable candidates for promotion to figure generation.

#### Use (in progress):
Options:
- `-h | --help` print help and exit
- `-p | --pathways` path to causal pathways
- `-s | --spek` path to spek file (default to stdin)



#### Default Esteemer Criteria
Provides a passthrough for all acceptable candidates.
Any candidate that is `acceptable_by` is annotated as `promoted_by http://example.com/slowmo#esteemer_default_criteria`
