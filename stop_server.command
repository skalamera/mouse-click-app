#!/bin/bash
# Double-clickable script to stop the Mouse Click Simulator server

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🛑 Stopping Mouse Click Simulator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Kill all processes on port 8765
for pid in $(lsof -ti:8765 2>/dev/null); do
    kill -9 $pid 2>/dev/null
done

# Also kill any web_server.py processes
pkill -9 -f "web_server.py" 2>/dev/null

sleep 2

# Verify
if lsof -ti:8765 > /dev/null 2>&1; then
    echo "✗ Some processes still using port 8765"
    echo "Trying again..."
    for pid in $(lsof -ti:8765 2>/dev/null); do
        kill -9 $pid 2>/dev/null
    done
    sleep 1
fi

if lsof -ti:8765 > /dev/null 2>&1; then
    echo "✗ Failed to stop server completely"
else
    echo "✓ Server stopped successfully"
fi

echo ""
echo "Closing in 2 seconds..."
sleep 2
osascript -e 'tell application "Terminal" to close front window' 2>/dev/null &

