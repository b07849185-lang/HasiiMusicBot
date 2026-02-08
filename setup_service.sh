#!/bin/bash
# ==============================================================================
# Hasii Music Bot - System Service Setup
# ==============================================================================
# This script configures the bot to run as a background service
# ==============================================================================

set -e

echo "======================================"
echo "🚀 Hasii Music Bot - Service Setup"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run with sudo or as root"
    exit 1
fi

# Stop bot if it's currently running manually
echo "1️⃣ Checking for existing bot processes..."
if pgrep -f "python3 -m HasiiMusic" > /dev/null; then
    echo "⚠️  Bot is currently running. Please stop it first (Ctrl+C in the terminal)"
    echo "   Or kill it with: pkill -f 'python3 -m HasiiMusic'"
    read -p "   Press Enter after stopping the bot..."
fi

# Copy service file to systemd directory
echo "2️⃣ Installing service file..."
cp hasiimusic.service /etc/systemd/system/
chmod 644 /etc/systemd/system/hasiimusic.service

# Reload systemd to recognize new service
echo "3️⃣ Reloading systemd daemon..."
systemctl daemon-reload

# Enable service to start on boot
echo "4️⃣ Enabling service to start on boot..."
systemctl enable hasiimusic.service

# Start the service
echo "5️⃣ Starting the bot service..."
systemctl start hasiimusic.service

# Wait a moment for startup
sleep 3

# Check status
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
systemctl status hasiimusic.service --no-pager -l
echo ""
echo "📋 Useful Commands:"
echo "   systemctl status hasiimusic     # Check bot status"
echo "   systemctl restart hasiimusic    # Restart bot"
echo "   systemctl stop hasiimusic       # Stop bot"
echo "   systemctl start hasiimusic      # Start bot"
echo "   journalctl -u hasiimusic -f     # View live logs"
echo "   journalctl -u hasiimusic -n 50  # View last 50 log lines"
echo ""
echo "🔄 To update bot:"
echo "   ./update_bot.sh"
