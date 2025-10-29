#!/usr/bin/env python3
"""
Jetson Dashboard Web Server
Simple Flask server to serve the dashboard
"""

from flask import Flask, render_template, jsonify
import json
import threading
import time
from data_collector import JetsonDataCollector

app = Flask(__name__)

# Global data storage
current_data = {}
system_info = {}
data_collector = JetsonDataCollector()

def update_data():
    """Background thread to continuously update data"""
    global current_data, system_info
    while True:
        try:
            current_data = data_collector.get_tegrastats_data()
            system_info = data_collector.get_system_info()
            time.sleep(2)  # Update every 2 seconds
        except Exception as e:
            print(f"Error updating data: {e}")
            time.sleep(5)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    """API endpoint for system data"""
    return jsonify({
        'data': current_data,
        'system': system_info,
        'timestamp': time.time()
    })

@app.route('/api/status')
def api_status():
    """API endpoint for basic status"""
    return jsonify({
        'status': 'running',
        'uptime': system_info.get('uptime', 'Unknown'),
        'last_update': current_data.get('timestamp', 'Never')
    })

if __name__ == '__main__':
    # Start background data collection
    data_thread = threading.Thread(target=update_data, daemon=True)
    data_thread.start()
    
    # Wait a moment for initial data
    time.sleep(1)
    
    print("🚀 Starting Jetson Dashboard Server...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🔧 API endpoint: http://localhost:5000/api/data")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
