#!/bin/bash
# Usage: upload_files.sh CHUNKER_ROUTE TOPIC_DISPLAY_NAME DOCUMENT_DIRECTORY [TOKEN_CHUNK_SIZE]

CHUNKER_ROUTE="${1}"
TOPIC_DISPLAY_NAME="${2}"
DOCUMENT_DIRECTORY="${3:-./OS-CF-docs-Apr-2024/}"
TOKEN_CHUNK_SIZE="${4:-512}"

if [[ -z "$CHUNKER_ROUTE" || -z "$TOPIC_DISPLAY_NAME" || -z "$DOCUMENT_DIRECTORY" ]]; then
    echo "Usage: $0 <CHUNKER_ROUTE> <TOPIC_DISPLAY_NAME> <DOCUMENT_DIRECTORY> [TOKEN_CHUNK_SIZE]"
    exit 1
fi

# Function to upload a single file
upload_file() {
    local file_path="$1"
    abs_path=$(realpath "$file_path")
    
    curl -s -X POST https://${CHUNKER_ROUTE}/upload_files \
        -F "files=@${abs_path}" \
        -F "topic_display_name=${TOPIC_DISPLAY_NAME}" \
        -F "token_chunk_size=${TOKEN_CHUNK_SIZE}"
    
    echo "Uploaded file: ${file_path}"
}

export -f upload_file
export CHUNKER_ROUTE TOPIC_DISPLAY_NAME TOKEN_CHUNK_SIZE

echo "Starting file uploads..."
# Find files and pass each to upload_file function using xargs for parallel execution
find "${DOCUMENT_DIRECTORY}" -type f | grep -v index | xargs -I {} -P 10 bash -c 'upload_file "{}"'

echo "File uploads completed."
