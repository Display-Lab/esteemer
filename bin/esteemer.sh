#!/usr/bin/env bash

# Usage message
read -r -d '' USE_MSG <<'HEREDOC'
Usage:
  esteemer.sh -h
  esteemer.sh -p causal_pathway.json
  esteemer.sh -s spek.json  

Esteemer reads a spek from stdin or provided file path.  

Options:
  -h | --help   print help and exit
  -s | --spek   path to spek file (default to stdin)
HEREDOC

# Parse args
PARAMS=()
while (( "$#" )); do
  case "$1" in
    -h|--help)
      echo "${USE_MSG}"
      exit 0
      ;;
    -p|--pathways)
      CP_FILE="${2}"
      shift 2
      ;;
    -s|--spek)
      SPEK_FILE="${2}"
      shift 2
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
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
  echo >&2 "Fuseki not running locally."; 

  # Try to start custom fuseki locally
  FUSEKI_DIR=/opt/fuseki/apache-jena-fuseki-3.10.0
  ${FUSEKI_DIR}/fuseki-server --mem --update /ds 1> fuseki.out 2>&1 &

  exit 1;
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
  ?candi a cpo:cpo_0000053 .
  ?candi slowmo:acceptable_by ?o
}
SPARQL


# Read from SPEK_FILE or pipe from stdin
#   Use '-' to instruct curl to read from stdin
if [[ -z ${SPEK_FILE} ]]; then
  SPEK_FILE="-"
fi

# Load spek into fuseki
curl --silent -X PUT --data-binary "@${SPEK_FILE}" \
  --header 'Content-type: application/ld+json' \
  'http://localhost:3030/ds?graph=spek' >&2

# run update sparql
curl --silent -X POST --data-binary "${UPD_SPARQL}" \
  --header 'Content-type: application/sparql-update' \
  'http://localhost:3030/ds/update' >&2

# get updated spek
curl --silent -X GET --header 'Accept: application/ld+json' \
  'http://localhost:3030/ds?graph=spek'

