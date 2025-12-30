#!/bin/bash
# Double-clickable script to start the Mouse Click Simulator GUI
# Just double-click this file in Finder to launch!

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Kill any existing server on port 8765
if lsof -ti:8765 > /dev/null 2>&1; then
    echo "Stopping existing server..."
    lsof -ti:8765 | xargs kill -9 2>/dev/null
    sleep 1
fi

# Start the server in the background
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🖱️  Mouse Click Simulator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting web server..."
python web_server.py > /tmp/mouse_click_server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server started successfully
if ps -p $SERVER_PID > /dev/null && curl -s http://localhost:8765/gui.html > /dev/null 2>&1; then
    echo "✓ Server started successfully!"
    echo "Opening browser..."
    
    # Open the browser
    open "http://localhost:8765/gui.html"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Server is running (PID: $SERVER_PID)"
    echo "  Browser should have opened automatically"
    echo ""
    echo "  To stop: Press any key in this window"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Wait for user to press a key
    read -n 1 -s
    
    # Stop the server when user presses a key
    echo ""
    echo "Stopping server..."
    kill $SERVER_PID 2>/dev/null
    lsof -ti:8765 | xargs kill -9 2>/dev/null
    echo "✓ Server stopped."
    echo ""
    echo "Press any key to close this window..."
    read -n 1
else
    echo "✗ Failed to start server."
    echo ""
    echo "Error log:"
    cat /tmp/mouse_click_server.log
    echo ""
    echo "Press any key to close..."
    read -n 1
    exit 1
fi

