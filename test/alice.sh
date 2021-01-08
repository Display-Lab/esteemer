#!/usr/bin/env bash

# Start by assuming it was the path invoked.
THIS_SCRIPT="$0"

# Handle resolving symlinks to this script.
# Using ls instead of readlink, because bsd and gnu flavors
# have different behavior.
while [ -h "$THIS_SCRIPT" ] ; do
  ls=`ls -ld "$THIS_SCRIPT"`
  # Drop everything prior to ->
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    THIS_SCRIPT="$link"
  else
    THIS_SCRIPT=`dirname "$THIS_SCRIPT"`/"$link"
  fi
done

# Get path to the scripts directory.
SCRIPT_DIR=$(dirname "${THIS_SCRIPT}")

ESTEEMER="${SCRIPT_DIR}/../bin/esteemer.sh"
TEST_SPEK="${SCRIPT_DIR}/alice_spek.json"


CANDIDATE_TYPE="http://purl.obolibrary.org/obo/cpo_0000053"

${ESTEEMER} -s ${TEST_SPEK} |\
  jq --arg t "$CANDIDATE_TYPE" '."@graph"[] | select(."@type" == $t and ."AncestorPerformer" == "_:pAlice")' |\
  grep --color -E '"promoted_by.*"|^'

