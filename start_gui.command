#!/bin/bash
# Double-clickable script to start the Mouse Click Simulator GUI
# Just double-click this file in Finder to launch!

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run everything in a subshell and detach Terminal immediately
(
    # Activate virtual environment
    source venv/bin/activate

# Kill any existing server on port 8765
echo "Checking for existing server..."
# Kill all processes using port 8765
PIDS=$(lsof -ti:8765 2>/dev/null)
if [ ! -z "$PIDS" ]; then
    echo "Found existing server, stopping..."
    for pid in $PIDS; do
        kill -9 $pid 2>/dev/null
    done
fi
# Also kill any web_server.py processes
pkill -9 -f "web_server.py" 2>/dev/null
# Wait for processes to die
sleep 3
# Double-check and kill again if needed
PIDS=$(lsof -ti:8765 2>/dev/null)
if [ ! -z "$PIDS" ]; then
    echo "Force killing remaining processes..."
    for pid in $PIDS; do
        kill -9 $pid 2>/dev/null
    done
    sleep 2
fi

# Start the server completely detached from Terminal
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🖱️  Mouse Click Simulator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting web server..."
# Use nohup and redirect all output to completely detach
nohup python web_server.py > /tmp/mouse_click_server.log 2>&1 &
SERVER_PID=$!
# Disown the process so it's completely detached
disown $SERVER_PID 2>/dev/null || true

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
    echo "  ✓ Server started successfully!"
    echo "  ✓ Browser opened"
    echo ""
    echo "  Server running in background (PID: $SERVER_PID)"
    echo "  To stop: Double-click stop_server.command"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Success - server is running
    exit 0
else
    echo "✗ Failed to start server."
    echo ""
    echo "Error log:"
    cat /tmp/mouse_click_server.log
    echo ""
    echo "Closing window in 5 seconds..."
    sleep 5
    exit 1
fi
) &

# Close Terminal window immediately after starting the background process
sleep 1
osascript -e 'tell application "Terminal" to close front window' 2>/dev/null
exit 0

