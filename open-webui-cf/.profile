#!/bin/bash

function parse_vcap_services () {
  if [[ -z "$VCAP_SERVICES" ]]; then
    return 0
  fi
  export OPENAI_API_BASE_URLS=$(    echo "$VCAP_SERVICES" | jq -r '.genai[] | .credentials.endpoint.api_base + "/openai"')
  export OPENAI_API_KEYS=$(         echo "$VCAP_SERVICES" | jq -r '.genai[] | .credentials.endpoint.api_key')
  export ENABLE_OLLAMA_API=false
}

function load_platform_certs () {
  export REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
}

parse_vcap_services
load_platform_certs