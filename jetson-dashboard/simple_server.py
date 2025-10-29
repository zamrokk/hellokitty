#!/usr/bin/env python3
"""
Jetson Dashboard Simple Server
Serveur HTTP simple sans Flask pour éviter les dépendances
"""

import http.server
import socketserver
import json
import threading
import time
import urllib.parse
from data_collector import JetsonDataCollector

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data_collector = JetsonDataCollector()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/api/data':
            self.serve_api_data()
        elif self.path == '/api/status':
            self.serve_api_status()
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            super().do_GET()
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        try:
            with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error serving dashboard: {e}")
    
    def serve_api_data(self):
        """Serve system data as JSON"""
        try:
            data = self.data_collector.get_tegrastats_data()
            system_info = self.data_collector.get_system_info()
            
            response = {
                'data': data,
                'system': system_info,
                'timestamp': time.time()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except BrokenPipeError:
                # Client closed the connection; ignore gracefully
                self.close_connection = True
                return
        except Exception as e:
            try:
                self.send_error(500, f"Error getting data: {e}")
            except BrokenPipeError:
                # Even sending the error failed because client disconnected
                self.close_connection = True
                return
    
    def serve_api_status(self):
        """Serve basic status"""
        try:
            status = {
                'status': 'running',
                'uptime': 'Unknown',
                'last_update': time.time()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error getting status: {e}")
    
    def serve_static_file(self):
        """Serve static files (CSS, JS, images)"""
        try:
            # Remove /static/ prefix and get the file path
            file_path = self.path[8:]  # Remove '/static/'
            
            # Security check - only allow files in static directory
            if '..' in file_path or file_path.startswith('/'):
                self.send_error(403, "Forbidden")
                return
            
            # Determine content type based on file extension
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.endswith('.gif'):
                content_type = 'image/gif'
            else:
                content_type = 'application/octet-stream'
            
            with open(f'static/{file_path}', 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Error serving static file: {e}")

def start_server(port=8080):
    """Start the HTTP server"""
    try:
        with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
            print("🚀 Jetson Dashboard Server démarré!")
            print(f"📊 Dashboard disponible à: http://localhost:{port}")
            print(f"🌐 Accès réseau: http://[IP_DE_VOTRE_JETSON]:{port}")
            print("⏹️  Appuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
    except Exception as e:
        print(f"❌ Erreur du serveur: {e}")

if __name__ == "__main__":
    start_server()
