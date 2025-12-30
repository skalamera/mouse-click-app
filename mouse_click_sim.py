#!/usr/bin/env python3
"""
Mouse Click Simulator for macOS

This script simulates mouse clicks on macOS using pyautogui.
Note: macOS requires Accessibility permissions for this to work.
"""

import pyautogui
import time
import sys
from typing import Optional, Tuple


def click_at_position(x: Optional[int] = None, y: Optional[int] = None, button: str = 'left', clicks: int = 1, interval: float = 0.1) -> None:
    """
    Simulate a mouse click at a specific position or current cursor position.
    
    Args:
        x: X coordinate (None for current position)
        y: Y coordinate (None for current position)
        button: 'left', 'right', or 'middle'
        clicks: Number of clicks to perform
        interval: Time between clicks (seconds)
    """
    try:
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks, interval=interval)
            print(f"Clicked {button} button {clicks} time(s) at position ({x}, {y})")
        else:
            pyautogui.click(button=button, clicks=clicks, interval=interval)
            current_x, current_y = pyautogui.position()
            print(f"Clicked {button} button {clicks} time(s) at current position ({current_x}, {current_y})")
    except Exception as e:
        print(f"Error performing click: {e}", file=sys.stderr)
        sys.exit(1)


def get_current_position() -> Tuple[int, int]:
    """Get the current mouse cursor position."""
    try:
        x, y = pyautogui.position()
        return x, y
    except Exception as e:
        print(f"Error getting cursor position: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle command-line arguments and execute clicks."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Simulate mouse clicks on macOS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Click at current cursor position
  python mouse_click_sim.py
  
  # Click at specific coordinates
  python mouse_click_sim.py --x 100 --y 200
  
  # Right click at current position
  python mouse_click_sim.py --button right
  
  # Double click at specific position
  python mouse_click_sim.py --x 500 --y 300 --clicks 2
  
  # Click after a delay
  python mouse_click_sim.py --delay 3
  
  # Show current cursor position
  python mouse_click_sim.py --show-position
        """
    )
    
    parser.add_argument('--x', type=int, help='X coordinate (default: current position)')
    parser.add_argument('--y', type=int, help='Y coordinate (default: current position)')
    parser.add_argument('--button', choices=['left', 'right', 'middle'], default='left',
                       help='Mouse button to click (default: left)')
    parser.add_argument('--clicks', type=int, default=1,
                       help='Number of clicks to perform (default: 1)')
    parser.add_argument('--interval', type=float, default=0.1,
                       help='Time between clicks in seconds (default: 0.1)')
    parser.add_argument('--delay', type=float, default=0,
                       help='Delay before clicking in seconds (default: 0)')
    parser.add_argument('--show-position', action='store_true',
                       help='Show current cursor position and exit')
    
    args = parser.parse_args()
    
    # Show position and exit if requested
    if args.show_position:
        x, y = get_current_position()
        print(f"Current cursor position: ({x}, {y})")
        sys.exit(0)
    
    # Validate coordinates
    if (args.x is not None and args.y is None) or (args.x is None and args.y is not None):
        print("Error: Both --x and --y must be provided together, or neither.", file=sys.stderr)
        sys.exit(1)
    
    # Delay before clicking
    if args.delay > 0:
        print(f"Waiting {args.delay} seconds before clicking...")
        time.sleep(args.delay)
    
    # Perform the click
    click_at_position(
        x=args.x,
        y=args.y,
        button=args.button,
        clicks=args.clicks,
        interval=args.interval
    )


if __name__ == '__main__':
    # Enable failsafe - move mouse to corner to abort
    pyautogui.FAILSAFE = True
    
    # Add a small pause after each PyAutoGUI call
    pyautogui.PAUSE = 0.1
    
    main()

