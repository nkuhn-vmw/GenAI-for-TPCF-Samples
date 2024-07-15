#!/bin/bash

function parse_vcap_services () {
  if [[ -z "$VCAP_SERVICES" ]]; then
    return 0
  fi
  export OPENAI_API_BASE_URL=$(       echo "$VCAP_SERVICES" | jq -r ".genai[0].credentials.api_base")
  export OPENAI_API_KEY=$(       echo "$VCAP_SERVICES" | jq -r ".genai[0].credentials.api_key")
}

parse_vcap_services