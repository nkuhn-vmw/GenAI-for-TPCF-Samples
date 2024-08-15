#!/usr/bin/env bash

PGVECTOR_SERVICE_NAME="vector-db"
PGVECTOR_PLAN_NAME="on-demand-postgres-db"

GENAI_CHAT_SERVICE_NAME="genai-chat" 
GENAI_CHAT_PLAN_NAME="meta-llama/Meta-Llama-3-8B-Instruct" # plan must have chat capabilty

GENAI_EMBEDDINGS_SERVICE_NAME="genai-embed" 
GENAI_EMBEDDINGS_PLAN_NAME="nomic-embed-text" # plan must have Embeddings capabilty

APP_NAME="spring-music-ai-taylors-version" # If you want to override the app name manifest.yml

case $1 in
cf)
    
    echo && printf "\e[37mℹ️  Creating services ...\e[m\n" && echo

    cf create-service postgres $PGVECTOR_PLAN_NAME $PGVECTOR_SERVICE_NAME #-c '{"svc_gw_enable": true, "router_group": "default-tcp", "external_port": 1025}' -w
    echo
	printf "Waiting for service $PGVECTOR_SERVICE_NAME to create."
	while [ `cf services | grep 'in progress' | wc -l | sed 's/ //g'` != 0 ]; do
  		printf "."
  		sleep 5
	done

	echo "$PGVECTOR_SERVICE_NAME creation completed."
 
	echo && printf "\e[37mℹ️  Creating $GENAI_CHAT_SERVICE_NAME and $GENAI_EMBEDDINGS_SERVICE_NAME GenAI services ...\e[m\n" && echo

    cf create-service genai $GENAI_CHAT_PLAN_NAME $GENAI_CHAT_SERVICE_NAME 
    cf create-service genai $GENAI_EMBEDDINGS_PLAN_NAME $GENAI_EMBEDDINGS_SERVICE_NAME 
 
    echo && printf "\e[37mℹ️  Deploying $APP_NAME application ...\e[m\n" && echo
    cf push $APP_NAME -f manifest.yml --no-start

    echo && printf "\e[37mℹ️  Binding services ...\e[m\n" && echo

    cf bind-service $APP_NAME $PGVECTOR_SERVICE_NAME
    cf bind-service $APP_NAME $GENAI_CHAT_SERVICE_NAME
    cf bind-service $APP_NAME $GENAI_EMBEDDINGS_SERVICE_NAME
    cf start $APP_NAME

    ;;
cleanup)
    cf delete-service $PGVECTOR_SERVICE_NAME -f
    cf delete-service $GENAI_CHAT_SERVICE_NAME -f
    cf delete-service $GENAI_EMBEDDINGS_SERVICE_NAME -f
    cf delete $APP_NAME -f -r
    ;;
*)
    echo && printf "\e[31m⏹  Usage: cf/cleanup \e[m\n" && echo
    ;;
esac

