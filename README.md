# Mouse Click Simulator for macOS

A Python application to simulate mouse clicks on macOS using `pyautogui`. Available as both a command-line script and a graphical user interface (GUI).

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## macOS Permissions

**Important**: macOS requires Accessibility permissions for this script to work.

### Step-by-Step Instructions:

1. **Open System Settings**
   - Click the Apple menu (🍎) in the top-left corner
   - Select **System Settings** (or **System Preferences** on older macOS versions)

2. **Navigate to Privacy & Security**
   - In the sidebar, click **Privacy & Security**
   - If you don't see it, you may need to scroll down

3. **Open Accessibility Settings**
   - Click **Accessibility** (or **Accessibility** under the Privacy section)
   - You may need to click the lock icon (🔒) at the bottom and enter your password to make changes

4. **Enable Terminal/Python**
   - Look for **Terminal** in the list of applications
   - Toggle the switch next to Terminal to **ON** (green)
   - If you're using an IDE like VS Code, PyCharm, or Cursor, also enable that application
   - If you're using Python directly (not through Terminal), look for **Python** or **Python3** in the list and enable it

5. **For Virtual Environments**
   - If you're using a virtual environment, you may also need to enable the Python executable
   - Common locations: `/usr/bin/python3`, or your venv's Python path
   - You can add it by clicking the **+** button and navigating to the Python executable

### Quick Test

After enabling permissions, test if it works:
```bash
python mouse_click_sim.py --show-position
```

If you see coordinates printed, permissions are working correctly!

## Usage

### GUI Application (Recommended)

**Web-Based GUI (No Python GUI dependencies!)**
```bash
python web_server.py
```
Then open your web browser and go to: **http://localhost:8765/gui.html**

This version uses a web interface - no Python GUI libraries, no pyobjc issues! The server uses only Python standard library.

**Features:**
- Visual interface for all click settings
- Real-time mouse position display
- Quick position buttons (Left/Middle, Center, Right/Middle)
- Start/Stop controls
- Status log showing click history
- Configurable repeat intervals

**How to use:**
1. Set click position (use current position, enter coordinates, or use quick position buttons)
2. Configure click settings (button type, number of clicks, intervals)
3. Set repeat interval (e.g., 10 seconds)
4. Click "Start Clicking" to begin
5. Click "Stop Clicking" to stop

### Command-Line Script

### Basic Usage

Click at current cursor position:
```bash
python mouse_click_sim.py
```

Click at specific coordinates:
```bash
python mouse_click_sim.py --x 100 --y 200
```

### Options

- `--x`: X coordinate (must be used with --y)
- `--y`: Y coordinate (must be used with --x)
- `--button`: Mouse button (`left`, `right`, or `middle`) - default: `left`
- `--clicks`: Number of clicks to perform - default: `1`
- `--interval`: Time between clicks in seconds - default: `0.1`
- `--delay`: Delay before clicking in seconds - default: `0`
- `--show-position`: Show current cursor position and exit

### Examples

Right click at current position:
```bash
python mouse_click_sim.py --button right
```

Double click at specific position:
```bash
python mouse_click_sim.py --x 500 --y 300 --clicks 2
```

Click after a 3-second delay:
```bash
python mouse_click_sim.py --delay 3
```

Show current cursor position:
```bash
python mouse_click_sim.py --show-position
```

## Safety Features

- **Failsafe**: Move your mouse to the top-left corner of the screen to abort any running script
- **Pause**: Small pause between actions to prevent accidental rapid clicks

## Troubleshooting

If clicks don't work:
1. Check that Accessibility permissions are enabled
2. Try running with `--show-position` to verify the script can detect your cursor
3. Make sure you're using Python 3.6 or higher


## Quick Start Examples

### Easy Launch (Recommended)

**Double-Click Script (Easiest!)**
- Simply double-click `start_gui.command` in Finder
- It will automatically:
  - Start the web server
  - Open your browser to the GUI
- To stop: Press any key in the terminal window

**Alternative: Terminal Command**
```bash
./start_gui.sh
```

**Alternative: Manual Start**
```bash
python web_server.py
```
Then open: `http://localhost:8765/gui.html`

### Using the GUI

**Click left/middle every 10 seconds:**
1. Launch using any option above
2. Click "Left/Middle" quick position button
3. Set "Repeat every" to `10` seconds
4. Click "Start Clicking"

**Command Line - Click left/middle every 10 seconds:**
```bash
cd /Users/stephen.skalamera/Documents/Projects/mouse-click-sim && source venv/bin/activate && while true; do python mouse_click_sim.py --x 378 --y 491; echo "Waiting 10 seconds before next click..."; sleep 10; done
```


