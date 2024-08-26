#!/bin/bash
# Usage: create_knowledge_base.sh CHUNKER_ROUTE TOPIC_DISPLAY_NAME EMBEDDING_VECTOR_SIZE TOPIC_DOMAIN

set -e  # Exit on error

CHUNKER_ROUTE="${1}"
TOPIC_DISPLAY_NAME="${2}"
EMBEDDING_VECTOR_SIZE="${3:-768}"
TOPIC_DOMAIN="${4}"

if [[ -z "$CHUNKER_ROUTE" || -z "$TOPIC_DISPLAY_NAME" || -z "$EMBEDDING_VECTOR_SIZE" || -z "$TOPIC_DOMAIN" ]]; then
    echo "Usage: $0 <CHUNKER_ROUTE> <TOPIC_DISPLAY_NAME> <EMBEDDING_VECTOR_SIZE> <TOPIC_DOMAIN>"
    exit 1
fi

echo "Creating knowledge base on ${CHUNKER_ROUTE}..."
curl -X POST "https://${CHUNKER_ROUTE}/create_knowledge_base" \
    -d "topic_display_name=${TOPIC_DISPLAY_NAME}&vector_size=${EMBEDDING_VECTOR_SIZE}&topic_domain=${TOPIC_DOMAIN}"

echo "Knowledge base created successfully."
