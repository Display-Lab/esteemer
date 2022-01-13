#!/usr/bin/env bash

# Usage message
read -r -d '' USE_MSG <<'HEREDOC'
Usage:
  esteemer.sh -h
  esteemer.sh -p causal_pathway.json
  esteemer.sh -s spek.json  

Esteemer reads a spek from stdin or provided file path.  

Options:
  -h | --help     print help and exit
  -p | --pathways path to causal pathways
  -s | --spek     path to spek file (default to stdin)
HEREDOC

urlencode() {
    # urlencode <string>
    old_lc_collate=$LC_COLLATE
    LC_COLLATE=C
    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:$i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf '%s' "$c" ;;
            *) printf '%%%02X' "'$c" ;;
        esac
    done
    LC_COLLATE=$old_lc_collate
}

# Parse args
PARAMS=()
while (("$#")); do
  case "$1" in
  -h | --help)
    echo "${USE_MSG}"
    exit 0
    ;;
  -p | --pathways)
    CP_FILE="${2}"
    shift 2
    ;;
  -s | --spek)
    SPEK_FILE="${2}"
    shift 2
    ;;
  --) # end argument parsing
    shift
    break
    ;;
  -* | --*=) # unsupported flags
    echo "Aborting: Unsupported flag $1" >&2
    exit 1
    ;;
  *) # preserve positional arguments
    PARAMS+=("${1}")
    shift
    ;;
  esac
done

# Check if FUSEKI is running.
FUSEKI_PING=$(curl -s -o /dev/null -w "%{http_code}" localhost:3030/$/ping)
if [[ -z ${FUSEKI_PING}} || ${FUSEKI_PING} -ne 200 ]]; then
  # Error
  echo >&2 "Fuseki not running locally."

  # Try to start custom fuseki locally
  #  FUSEKI_DIR=/opt/fuseki/apache-jena-fuseki-3.10.0
  ${FUSEKI_HOME}/fuseki-server --mem --update /ds 1>fuseki.out 2>&1 &

  exit 1
fi

# Define SPARQL Queries for updates and results
read -r -d '' UPD_SPARQL <<'SPARQL'
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX cpo: <http://example.com/cpo#>
PREFIX slowmo: <http://example.com/slowmo#>

INSERT {
  GRAPH <http://localhost:3030/ds/spek> {
    ?candi slowmo:promoted_by <http://example.com/slowmo#default_esteemer_criteria> .
  }
}
USING <http://localhost:3030/ds/spek>
WHERE {
  ?candi a obo:cpo_0000053 .
  ?candi slowmo:acceptable_by ?o
}
SPARQL

# Read from SPEK_FILE or pipe from stdin
#   Use '-' to instruct curl to read from stdin
if [[ -z ${SPEK_FILE} ]]; then
  SPEK_FILE="-"
fi

FUSEKI_DATASET_URL="http://localhost:3030/ds"
SPEK_URL="${FUSEKI_DATASET_URL}/spek"
ENCODED_SPEK_URL=$(urlencode "${SPEK_URL}")

# Load spek into fuseki
curl --silent -X PUT --data-binary "@${SPEK_FILE}" \
  --header 'Content-type: application/ld+json' \
  "${FUSEKI_DATASET_URL}?graph=${ENCODED_SPEK_URL}" >&2

# run update sparql
curl --silent -X POST --data-binary "${UPD_SPARQL}" \
  --header 'Content-type: application/sparql-update' \
  "${FUSEKI_DATASET_URL}/update"

# get updated spek and emit to stdout.
  curl --silent -G --header 'Accept: application/ld+json' \
    --data-urlencode "graph=${SPEK_URL}" \
    "${FUSEKI_DATASET_URL}"
