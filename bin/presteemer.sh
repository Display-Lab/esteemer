#!/usr/bin/env bash
# Usage message
read -r -d '' USE_MSG <<'HEREDOC'
Usage:
  presteemer.sh -h
  presteemer.sh -s spek.json

Presteemer reads a spek from stdin or provided file path.

Options:
  -h | --help     print help and exit
  -s | --spek     path to spek file (default to stdin)
HEREDOC

# Parse args
PARAMS=()
while (("$#")); do
  case "$1" in
  -h | --help)
    echo "${USE_MSG}"
    exit 0
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

read -r -d '' GET_CANDIDATES_AND_PERFORMER_GRAPH << \
'SPARQL'
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
SPARQL
# Read from SPEK_FILE or pipe from stdin
#   Use '-' to instruct curl to read from stdin
if [[ -z ${SPEK_FILE} ]]; then
  SPEK_FILE="-"
fi

FUSEKI_DATASET_URL="http://localhost:3030/ds"
SPEK_URL="${FUSEKI_DATASET_URL}/espek"

# Load spek into fuseki
curl --silent PUT \
  --data-binary "@${SPEK_FILE}" \
  --header 'Content-type: application/ld+json' \
  "${FUSEKI_DATASET_URL}?graph=${SPEK_URL}" >&2

# run construct performer query
curl --silent GET \
  --data-binary "${GET_CANDIDATES_AND_PERFORMER_GRAPH}" \
  --header 'Content-type: application/sparql-query' \
  "${FUSEKI_DATASET_URL}/query"