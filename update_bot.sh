#!/bin/bash
# ==============================================================================
# Hasii Music Bot - Quick Update Script
# ==============================================================================
# Updates bot with minimal downtime (3-5 seconds)
# ==============================================================================

set -e

echo "======================================"
echo "🔄 Updating Hasii Music Bot"
echo "======================================"
echo ""

# Pull latest changes
echo "1️⃣ Pulling latest code from GitHub..."
git pull

echo ""
echo "2️⃣ Checking dependencies..."
source hasiimusic/bin/activate
pip install -r requirements.txt --upgrade --quiet || echo "⚠️  Dependencies already up to date"

echo ""
echo "3️⃣ Restarting bot service..."
echo "   (Users will experience 3-5 seconds downtime)"
systemctl restart hasiimusic

# Wait for service to stabilize
sleep 3

echo ""
echo "4️⃣ Checking bot status..."
if systemctl is-active --quiet hasiimusic; then
    echo "✅ Bot updated and running successfully!"
    echo ""
    systemctl status hasiimusic --no-pager -l | head -15
else
    echo "❌ Bot failed to start! Check logs:"
    echo "   journalctl -u hasiimusic -n 50"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ Update Complete!"
echo "======================================"
