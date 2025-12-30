#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-/opt/energy_platform}"
COMPOSE_FILE="$APP_DIR/infra/prod/docker-compose.prod.yml"
ENV_FILE="$APP_DIR/infra/prod/.env.prod"

echo "📦 Deploying in: $APP_DIR"
cd "$APP_DIR"

echo "🔐 Logging into GHCR (uses GITHUB_TOKEN passed by workflow if configured)"
# In our workflow we do docker login already; this is here if you ever run manually:
# echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

echo "⬇️ Pull latest images"
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull

echo "🚀 Restart stack"
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d

echo "⏳ Waiting for API..."
sleep 4

echo "✅ Health check"
curl -fsS http://localhost/api/health >/dev/null

echo "🎉 Deploy complete"