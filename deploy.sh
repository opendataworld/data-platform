#!/bin/bash
set -e

DOMAIN=${DOMAIN:-open-data.world}
INSTALL_DIR="/opt/data-platform"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

echo ""
echo "🚀 Data Platform Deployment (Core)"
echo "=================================="
echo ""

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash deploy.sh"
    exit 1
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    log_info "Installing Docker..."
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
    systemctl enable docker
    systemctl start docker
    log_success "Docker installed"
fi

# Docker Compose v2 is usually included with docker
log_info "Docker version: $(docker --version)"

# Clone repository
GITHUB_REPO="https://github.com/open-data-world/data-platform.git"
if [ ! -d "$INSTALL_DIR" ]; then
    log_info "Cloning Data Platform repository..."
    git clone --depth 1 "$GITHUB_REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
else
    log_info "Updating repository..."
    cd "$INSTALL_DIR"
    git pull
fi

# Set environment
log_info "Setting up environment..."
cp .env.coolify .env 2>/dev/null || true

# Start core services only
log_info "Starting core services (minimal)..."
docker compose -f docker-compose.core.yml up -d

# Wait for services
log_info "Waiting for services..."
sleep 30

echo ""
echo "✅ Data Platform Core Deployed!"
echo ""
echo "📍 Service URLs (Core - Running Now):"
echo "===================================="
echo ""
echo "🔌 Main API:     https://api.${DOMAIN}"
echo "📖 API Docs:    https://api.${DOMAIN}/docs"
echo "🧠 Agent:       https://api.${DOMAIN}/agent"
echo "🛠️  MCP Server:   https://api.${DOMAIN}/mcp"
echo ""
echo "🔀 LangFlow:    https://flow.${DOMAIN}"
echo "💰 Billing:    https://billing.${DOMAIN}"
echo "📚 Docs:       https://docs.${DOMAIN}"
echo ""
echo "📦 To deploy more services:"
echo "   docker compose -f docker-compose.yml --profile ml up -d"
echo "   docker compose -f docker-compose.yml --profile ingest up -d"
echo ""
echo "======================================"
echo "To stop: cd $INSTALL_DIR && docker compose -f docker-compose.core.yml down"
echo "======================================"
