#!/bin/bash

function parse_vcap_services () {
  if [[ -z "$VCAP_SERVICES" ]]; then
    return 0
  fi
  export OPENAI_API_BASE_URLS=$(    echo "$VCAP_SERVICES" | jq -r '[.genai[] | .credentials.api_base] | join(";")')
  export OPENAI_API_KEYS=$(         echo "$VCAP_SERVICES" | jq -r '[.genai[] | .credentials.api_key] | join(";")')
  # export OPENID_PROVIDER_URL=$(     echo "$VCAP_SERVICES" | jq -r '.["p-identity"][0].credentials.auth_domain')
  # export OAUTH_CLIENT_ID=$(         echo "$VCAP_SERVICES" | jq -r '.["p-identity"][0].credentials.client_id')
  # export OAUTH_CLIENT_SECRET=$(     echo "$VCAP_SERVICES" | jq -r '.["p-identity"][0].credentials.client_secret')
  # export OAUTH_PROVIDER_NAME="uaa"
  export RAG_OPENAI_API_BASE_URL=$( echo "$VCAP_SERVICES" | jq -r '.genai[].credentials |  select(.model_capabilities[]=="embedding") | .api_base')
  export RAG_OPENAI_API_KEY=$( echo "$VCAP_SERVICES" | jq -r '.genai[].credentials |  select(.model_capabilities[]=="embedding") | .api_key')
  export RAG_EMBEDDING_ENGINE="openai"
  export RAG_EMBEDDING_MODEL=$( echo "$VCAP_SERVICES" | jq -r '.genai[].credentials |  select(.model_capabilities[]=="embedding") | .model_name')
  export ENABLE_OLLAMA_API=false
}

function load_platform_certs () {
  export REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
}

parse_vcap_services
load_platform_certs