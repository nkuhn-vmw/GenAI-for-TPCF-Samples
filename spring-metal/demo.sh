#!/usr/bin/env bash

PGVECTOR_SERVICE_NAME="vector-db"
PGVECTOR_PLAN_NAME="on-demand-postgres-db"
PGVECTOR_EXTERNAL_PORT=1025

GENAI_CHAT_SERVICE_NAME="genai-chat" 
GENAI_CHAT_PLAN_NAME="meta-llama/Meta-Llama-3-8B-Instruct" # plan must have chat capabilty

GENAI_EMBEDDINGS_SERVICE_NAME="genai-embed" 
GENAI_EMBEDDINGS_PLAN_NAME="nomic-embed-text" # plan must have Embeddings capabilty

APP_NAME="spring-metal" # overridable, necessary for TPK8s ingress route



case $1 in
cf)
    
    echo && printf "\e[37mℹ️  Creating services ...\e[m\n" && echo

    cf create-service postgres $PGVECTOR_PLAN_NAME $PGVECTOR_SERVICE_NAME -c "{\"svc_gw_enable\": true, \"router_group\": \"default-tcp\", \"external_port\": $PGVECTOR_EXTERNAL_PORT}" -w
	printf "Waiting for service $PGVECTOR_SERVICE_NAME to create."
	while [ `cf services | grep 'in progress' | wc -l | sed 's/ //g'` != 0 ]; do
  		printf "."
  		sleep 5
	done

	echo "$PGVECTOR_SERVICE_NAME creation completed."
 
	echo && printf "\e[37mℹ️  Creating $GENAI_CHAT_SERVICE_NAME and $GENAI_EMBEDDINGS_SERVICE_NAME GenAI services ...\e[m\n" && echo

    cf create-service genai $GENAI_CHAT_PLAN_NAME $GENAI_CHAT_SERVICE_NAME 
    cf create-service genai $GENAI_EMBEDDINGS_PLAN_NAME $GENAI_EMBEDDINGS_SERVICE_NAME 
 
    echo && printf "\e[37mℹ️  Deploying spring-metal application ...\e[m\n" && echo
    cf push $APP_NAME -f runtime-configs/tpcf/manifest.yml --no-start

    echo && printf "\e[37mℹ️  Binding services ...\e[m\n" && echo

    cf bind-service $APP_NAME $PGVECTOR_SERVICE_NAME
    cf bind-service $APP_NAME $GENAI_CHAT_SERVICE_NAME
    cf bind-service $APP_NAME $GENAI_EMBEDDINGS_SERVICE_NAME
    cf start $APP_NAME

    ;;

prepare-k8s)
    echo && printf "\e[35m▶ Creating service keys for GenAI and Postgres \e[m\n" && echo

    cf create-service-key $PGVECTOR_SERVICE_NAME key
    PGVECTOR_GUID=$(cf service-key $PGVECTOR_SERVICE_NAME key --guid)
    PGVECTOR_SERVICE_JSON=$(cf curl "/v3/service_credential_bindings/$PGVECTOR_GUID/details") 
    PGVECTOR_HOST=$(echo -n $PGVECTOR_SERVICE_JSON | jq -r -c '.credentials.service_gateway.host' | base64)
    PGVECTOR_PORT=$(echo -n $PGVECTOR_SERVICE_JSON | jq -r -c '.credentials.service_gateway.port' | base64)
    PGVECTOR_USERNAME=$(echo -n $PGVECTOR_SERVICE_JSON | jq -r -c '.credentials.user' | base64)
    PGVECTOR_PASSWORD=$(echo -n $PGVECTOR_SERVICE_JSON | jq -r -c '.credentials.password'| base64)

    cf create-service-key $GENAI_CHAT_SERVICE_NAME key
    CHAT_GUID=$(cf service-key $GENAI_CHAT_SERVICE_NAME key --guid)
    CHAT_SERVICE_JSON=$(cf curl "/v3/service_credential_bindings/$CHAT_GUID/details") 
    CHAT_MODEL_CAPABILITIES=$(echo -n $CHAT_SERVICE_JSON | jq -r -c '.credentials.model_capabilities| @csv' | sed 's/\"//g'| base64)
    CHAT_MODEL_NAME=$(echo -n $CHAT_SERVICE_JSON | jq -r -c '.credentials.model_name'| base64)
    CHAT_API_URL=$(echo -n $CHAT_SERVICE_JSON | jq -r -c '.credentials.api_base'| base64)
    CHAT_API_KEY=$(echo -n $CHAT_SERVICE_JSON | jq -r -c '.credentials.api_key'| base64)

    cf create-service-key $GENAI_EMBEDDINGS_SERVICE_NAME key
    EMBED_GUID=$(cf service-key $GENAI_EMBEDDINGS_SERVICE_NAME key --guid)
    EMBED_SERVICE_JSON=$(cf curl "/v3/service_credential_bindings/$EMBED_GUID/details") 
    EMBED_MODEL_CAPABILITIES=$(echo -n $EMBED_SERVICE_JSON | jq -r -c '.credentials.model_capabilities| @csv' | sed 's/\"//g'| base64)
    EMBED_MODEL_NAME=$(echo -n $EMBED_SERVICE_JSON | jq -r -c '.credentials.model_name'| base64)
    EMBED_API_URL=$(echo -n $EMBED_SERVICE_JSON | jq -r -c '.credentials.api_base'| base64)
    EMBED_API_KEY=$(echo -n $EMBED_SERVICE_JSON | jq -r -c '.credentials.api_key'| base64)

    echo && printf "\e[35m▶ Copying and templating runtime-configs/tpk8s/tanzu-changeme to .tanzu/config and .tanzu/config \e[m\n" && echo

    rm -rf .tanzu/config
    mkdir -p .tanzu/config

    sed "s/CHANGE_ME/$APP_NAME/g" runtime-configs/tpk8s/tanzu-changeme/spring-metal.yml > .tanzu/config/spring-metal.yml
    sed "s/CHANGE_ME/$APP_NAME/g" runtime-configs/tpk8s/tanzu-changeme/httproute.yml > .tanzu/config/httproute.yml

    if [[ "$OSTYPE" == "darwin"* ]]; then
        SED_INPLACE_COMMAND="sed -i.bak"
    else
        SED_INPLACE_COMMAND="sed -i"
    fi
      
    sed "s/CHAT_MODEL_CAPABILITIES/$CHAT_MODEL_CAPABILITIES/" runtime-configs/tpk8s/tanzu-changeme/genai-external-service.yml > .tanzu/config/genai-external-service.yml
    $SED_INPLACE_COMMAND "s|CHAT_MODEL_NAME|$CHAT_MODEL_NAME|" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s|CHAT_API_URL|$CHAT_API_URL|" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s|CHAT_API_KEY|$CHAT_API_KEY|" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s/EMBED_MODEL_CAPABILITIES/$EMBED_MODEL_CAPABILITIES/" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s|EMBED_MODEL_NAME|$EMBED_MODEL_NAME|" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s|EMBED_API_URL|$EMBED_API_URL|" .tanzu/config/genai-external-service.yml 
    $SED_INPLACE_COMMAND "s|EMBED_API_KEY|$EMBED_API_KEY|" .tanzu/config/genai-external-service.yml 
    
    sed "s/CHANGE_ME/$APP_NAME/" runtime-configs/tpk8s/tanzu-changeme/genai-service-binding.yml > .tanzu/config/genai-service-binding.yml

    sed "s/PGVECTOR_HOST/$PGVECTOR_HOST/" runtime-configs/tpk8s/tanzu-changeme/postgres-external-service.yml > .tanzu/config/postgres-external-service.yml
    $SED_INPLACE_COMMAND "s/PGVECTOR_PORT/$PGVECTOR_PORT/" .tanzu/config/postgres-external-service.yml
    $SED_INPLACE_COMMAND "s/PGVECTOR_USERNAME/$PGVECTOR_USERNAME/" .tanzu/config/postgres-external-service.yml
    $SED_INPLACE_COMMAND "s|PGVECTOR_PASSWORD|$PGVECTOR_PASSWORD|" .tanzu/config/postgres-external-service.yml

    sed "s/CHANGE_ME/$APP_NAME/" runtime-configs/tpk8s/tanzu-changeme/postgres-service-binding.yml > .tanzu/config/postgres-service-binding.yml

    rm .tanzu/config/*.bak

    ;;

k8s)
    echo && printf "\e[35m▶ tanzu deploy and bind \e[m\n" && echo
    tanzu deploy -y
    
    ;;
cleanup)
    cf delete-service $PGVECTOR_SERVICE_NAME -f
    cf delete-service $GENAI_CHAT_SERVICE_NAME -f
    cf delete-service $GENAI_EMBEDDINGS_SERVICE_NAME -f
    cf delete $APP_NAME -f -r
    kubectl delete -f .tanzu/config
    ;;
*)
    echo && printf "\e[31m⏹  Usage: cf/prepare-k8s/k8s/cleanup \e[m\n" && echo
    ;;
esac
