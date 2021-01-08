#!/usr/bin/env bash

# Requires fuseki-server to be installed
command -v robot 1> /dev/null 2>&1 || \
  { echo >&2 "fuseki-server required but it's not in PATH.  Aborting."; exit 1; }

# Usage message
read -r -d '' USE_MSG <<'HEREDOC'
Usage:
  esteemer.sh
  esteemer.sh -h
  esteemer.sh -s spek.json  

Esteemer is currently a rubber stamp that adds 'promoted by' predicate to approved candidates.

Options:
  -h | --help   print help and exit
  -s | --spek   path to spek file (default to stdin)
HEREDOC

# From Chris Down https://gist.github.com/cdown/1163649
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

# From Chris Down https://gist.github.com/cdown/1163649
urldecode() {
    # urldecode <string>
    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}

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
  fuseki-server --mem --update /ds 1> fuseki.out 2>&1 &
  read -p "Waiting five secs for Fuseki to start..." -t 5
fi

# Define,url encode, and create param string for fully qualified graph iris.
VAL_SPEK="http://localhost:3030/ds/spek"
ENC_SPEK=$(urlencode "${VAL_SPEK}")
PARAM_SPEK="graph=${ENC_SPEK}"

VAL_SEEPS="http://localhost:3030/ds/seeps"
ENC_SEEPS=$(urlencode "${VAL_SEEPS}")
PARAM_SEEPS="graph=${ENC_SEEPS}"

# Define SPARQL Query for updating spek
read -r -d '' UPD_SPARQL <<'SPARQL'
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
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


# If spek file is not empty, load into fuseki  
#  Otherwise assume it's loaded into fuseki already.
if [[ ! -z ${SPEK_FILE} ]]; then
  # Load in spek
  curl --silent -X PUT --data-binary "@${SPEK_FILE}" \
    --header 'Content-type: application/ld+json' \
    "http://localhost:3030/ds?${PARAM_SPEK}" >&2
fi

# run update sparql
curl --silent -X POST --data-binary "${UPD_SPARQL}" \
  --header 'Content-type: application/sparql-update' \
  'http://localhost:3030/ds/update' >&2

# get updated spek
curl --silent -G --header 'Accept: application/ld+json' \
    --data-urlencode "graph=http://localhost:3030/ds/spek" \
    'http://localhost:3030/ds'
