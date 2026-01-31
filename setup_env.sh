#!/bin/bash
# Setup script to create .env file

echo "Setting up environment file..."

cat > .env << 'EOF'
# OpenAI API Configuration
# (API key removed for public repo)

# Model Configuration
MODEL_NAME=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-large

# Vector Store Configuration
VECTOR_STORE_PATH=./data/vectorstore
CHROMA_PERSIST_DIR=./data/chroma_db

# Memory Configuration
MEMORY_DB_PATH=./data/memory.db

# Guardrails Configuration
MIN_CONFIDENCE_THRESHOLD=0.7
MAX_CONTEXT_LENGTH=8000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/agent_system.log
EOF

echo "✅ .env file created successfully!"
