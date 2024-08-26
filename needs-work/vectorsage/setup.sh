#!/bin/bash
# Usage: setup.sh [TOPIC_DISPLAY_NAME] [TOPIC_DOMAIN] [EMBEDDING_VECTOR_SIZE]

# WARNING: This setup assumes you have logged into CF, and have a blank database of embeddings
# this script will clear out all pre-created embeddings.  Run upload-files.sh on its own if you wish to
# experiment with different files.

set +x

TOPIC_DISPLAY_NAME="${1:-Cloud Foundry OSS Docs}" 
TOPIC_DOMAIN="${2:-Cloud Foundry}"
EMBEDDING_VECTOR_SIZE="${3:-768}"

SKIP_PUSH="${SKIP_PUSH:-false}"

if [[ "$SKIP_PUSH" == "false" ]]; then

    echo "Creating services..."
    ./create-services.sh
    
    echo "Deploying apps..."
    ./deploy-ragapi.sh

    CHUNKER_APP_NAME=$(awk '/^[ ]*- name:/{print $NF}' RAGAPI/manifest.yml | tr -d '[:space:]')
    CHUNKER_ROUTE=$(cf app "$CHUNKER_APP_NAME" | awk '/routes/{print $2}' | cut -d, -f1)

    ./create-knowledge-base.sh "$CHUNKER_ROUTE" "$TOPIC_DISPLAY_NAME" "$EMBEDDING_VECTOR_SIZE" "$TOPIC_DOMAIN"

    ./deploy-vectorsage.sh

    VS_APP_NAME=$(awk '/^[ ]*- name:/{print $NF}' VectorSage-UI/manifest.yml | tr -d '[:space:]')
    VECTORSAGE_ROUTE=$(cf app "$VS_APP_NAME" | awk '/routes/{print $2}' | cut -d, -f1)

    CONTEXT_PAYLOAD='[
        {
            "role": "user",
            "content": "Who are you? Or what are you?"
        },
        {
            "role": "assistant",
            "content": "I am an assistant on Cloud Foundry topics."
        },
        {
            "role": "user",
            "content": "What does CF stand for?"
        },
        {
            "role": "assistant",
            "content": "CF is Cloud Foundry."
        }
    ]'

    curl "https://${CHUNKER_ROUTE}/update_context_learning" \
                -F "topic_display_name=${TOPIC_DISPLAY_NAME}" \
                -F "context_learning=${CONTEXT_PAYLOAD}"
else
    echo "Using existing app deployments..."
    # Assumed services and apps have been pushed already
    CHUNKER_APP_NAME=$(awk '/^[ ]*- name:/{print $NF}' RAGAPI/manifest.yml | tr -d '[:space:]')
    CHUNKER_ROUTE=$(cf app "$CHUNKER_APP_NAME" | awk '/routes/{print $2}' | cut -d, -f1)
    VS_APP_NAME=$(awk '/^[ ]*- name:/{print $NF}' VectorSage-UI/manifest.yml | tr -d '[:space:]')
    VECTORSAGE_ROUTE=$(cf app "$VS_APP_NAME" | awk '/routes/{print $2}' | cut -d, -f1)
    ./create-knowledge-base.sh "$CHUNKER_ROUTE" "$TOPIC_DISPLAY_NAME" "$EMBEDDING_VECTOR_SIZE" "$TOPIC_DOMAIN"

    CONTEXT_PAYLOAD='[
        {
            "role": "user",
            "content": "Who are you? Or what are you?"
        },
        {
            "role": "assistant",
            "content": "I am an assistant on Cloud Foundry topics."
        },
        {
            "role": "user",
            "content": "What does CF stand for?"
        },
        {
            "role": "assistant",
            "content": "CF is Cloud Foundry."
        }
    ]'

    curl "https://${CHUNKER_ROUTE}/update_context_learning" \
                -F "topic_display_name=${TOPIC_DISPLAY_NAME}" \
                -F "context_learning=${CONTEXT_PAYLOAD}"
fi

# Clear out all embeddings for the knowledge base before starting the upload.
curl "https://${CHUNKER_ROUTE}/clear_embeddings" \
            -F "topic_display_name=${TOPIC_DISPLAY_NAME}"

./upload-files.sh "$CHUNKER_ROUTE" "$TOPIC_DISPLAY_NAME" "./OS-CF-docs-Apr-2024/"

echo "Routes for the apps:"
echo "Chunker: https://${CHUNKER_ROUTE}"
echo "VectorSage-UI: https://${VECTORSAGE_ROUTE}"
