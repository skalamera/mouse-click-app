#!/usr/bin/env python3
"""
Simple HTTP server for the web-based GUI.
Uses only Python standard library - no pyobjc dependencies.
"""

import http.server
import socketserver
import json
import subprocess
import os
import sys
import re
from urllib.parse import urlparse, parse_qs


PORT = 8765
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_venv_python():
    """Get the path to the venv Python executable."""
    venv_python = os.path.join(SCRIPT_DIR, 'venv', 'bin', 'python')
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


class MouseClickHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/position':
            self.handle_get_position()
        elif parsed_path.path == '/' or parsed_path.path == '/gui.html':
            self.send_file('gui.html')
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/click':
            self.handle_click()
        else:
            self.send_error(404)
    
    def handle_get_position(self):
        """Get current mouse position."""
        try:
            script_path = os.path.join(SCRIPT_DIR, 'mouse_click_sim.py')
            venv_python = get_venv_python()
            
            result = subprocess.run(
                [venv_python, script_path, '--show-position'],
                capture_output=True,
                text=True,
                timeout=2,
                cwd=SCRIPT_DIR
            )
            
            if result.returncode == 0 and result.stdout:
                match = re.search(r'\((\d+),\s*(\d+)\)', result.stdout)
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                    self.send_json_response({'success': True, 'x': x, 'y': y})
                    return
            
            self.send_json_response({'success': False, 'error': 'Failed to get position'})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)})
    
    def handle_click(self):
        """Handle click request."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            script_path = os.path.join(SCRIPT_DIR, 'mouse_click_sim.py')
            venv_python = get_venv_python()
            
            cmd = [venv_python, script_path, '--button', data['button'], '--clicks', str(data['clicks'])]
            
            if data.get('x') and data.get('y'):
                cmd.extend(['--x', str(data['x']), '--y', str(data['y'])])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=SCRIPT_DIR
            )
            
            if result.returncode == 0:
                position = f"({data.get('x', 'current')}, {data.get('y', 'current')})"
                self.send_json_response({'success': True, 'position': position})
            else:
                self.send_json_response({'success': False, 'error': result.stderr or 'Click failed'})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)})
    
    def send_file(self, filename):
        """Send a file."""
        filepath = os.path.join(SCRIPT_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            if filename.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce logging noise."""
        pass


def main():
    """Start the web server."""
    os.chdir(SCRIPT_DIR)
    
    with socketserver.TCPServer(("", PORT), MouseClickHandler) as httpd:
        print(f"🌐 Mouse Click Simulator Web GUI")
        print(f"📡 Server running at http://localhost:{PORT}/gui.html")
        print(f"🖱️  Open this URL in your web browser")
        print(f"⏹️  Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")


if __name__ == '__main__':
    main()

