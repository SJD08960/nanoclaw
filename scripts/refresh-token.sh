#!/bin/bash
# Syncs Claude OAuth token from ~/.claude/.credentials.json to .env

set -e

CREDENTIALS="$HOME/.claude/.credentials.json"
ENV_FILE="$HOME/nanoclaw/.env"
ENV_CONTAINER="$HOME/nanoclaw/data/env/env"

if [ ! -f "$CREDENTIALS" ]; then
  echo "No credentials file found"
  exit 0
fi

NEW_TOKEN=$(python3 -c "import json; d=json.load(open('$CREDENTIALS')); print(d['claudeAiOauth']['accessToken'])")

if [ -z "$NEW_TOKEN" ]; then
  echo "Could not read token"
  exit 0
fi

CURRENT_TOKEN=$(grep '^CLAUDE_CODE_OAUTH_TOKEN=' "$ENV_FILE" | cut -d= -f2-)

if [ "$NEW_TOKEN" = "$CURRENT_TOKEN" ]; then
  echo "Token unchanged, nothing to do"
  exit 0
fi

echo "Token changed, updating..."
sed -i "s|^CLAUDE_CODE_OAUTH_TOKEN=.*|CLAUDE_CODE_OAUTH_TOKEN=$NEW_TOKEN|" "$ENV_FILE"
cp "$ENV_FILE" "$ENV_CONTAINER"
systemctl --user restart nanoclaw
echo "Token updated and nanoclaw restarted"
