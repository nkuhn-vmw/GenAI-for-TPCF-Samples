#!/bin/bash

cf create-service genai-service shared-ai-plan genai
cf create-service postgres on-demand-postgres-db postgres-db

# Initial sleep to allow some time for service provisioning to start
sleep 30

# Maximum number of attempts to check service status
max_attempts=30
attempt_count=0

echo "Checking Postgres DB service creation status..."

# Loop to check service status
while [ $attempt_count -lt $max_attempts ]
do
    # Extract the status of the service
    status=$(cf service postgres-db | grep 'status:' | awk -F ':' '{print $2}' | xargs)

    echo "Current status: $status"

    # Check if the service creation succeeded
    if [ "$status" == "create succeeded" ]; then
        echo "Service creation succeeded."
        break
    elif [ "$status" == "create failed" ]; then
        echo "Service creation failed."
        exit 1
    fi

    # Increment the attempt counter and sleep before retrying
    ((attempt_count++))
    echo "Waiting for next check... ($attempt_count/$max_attempts)"
    sleep 20
done

# If the loop exits without service creation succeeding, print an error message
if [ "$status" != "create succeeded" ]; then
    echo "Service creation did not succeed after $max_attempts attempts."
    exit 1
fi