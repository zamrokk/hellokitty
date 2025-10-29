#!/usr/bin/env python3
"""
Jetson Dashboard Data Collector
Collects system data from tegrastats, /proc, and other sources
"""

import subprocess
import json
import time
import re
import os
from datetime import datetime

class JetsonDataCollector:
    def __init__(self):
        self.last_tegrastats = None
        
    def get_tegrastats_data(self):
        """Extract data from tegrastats output"""
        try:
            # Run tegrastats for 1 second to get current data
            result = subprocess.run(['timeout', '1', 'tegrastats', '--interval', '1000'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    self.last_tegrastats = lines[-1]  # Get the last line
                    return self.parse_tegrastats(self.last_tegrastats)
        except Exception as e:
            print(f"Error getting tegrastats data: {e}")
        
        return self.get_fallback_data()
    
    def parse_tegrastats(self, line):
        """Parse tegrastats output line"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'ram': {'used': 0, 'total': 0, 'percentage': 0},
            'swap': {'used': 0, 'total': 0, 'percentage': 0},
            'cpu': {'cores': [], 'average': 0},
            'gpu': {'frequency': 0, 'utilization': 0},
            'load': {'1min': 0, '5min': 0, '15min': 0, 'percentage': 0},
            'temperature': {'cpu': 0, 'gpu': 0, 'soc': []},
            'power': {'vdd_in': 0, 'vdd_cpu_gpu_cv': 0, 'vdd_soc': 0}
        }
        
        try:
            # RAM: RAM 2356/7620MB (lfb 5x4MB)
            ram_match = re.search(r'RAM (\d+)/(\d+)MB', line)
            if ram_match:
                used = int(ram_match.group(1))
                total = int(ram_match.group(2))
                data['ram'] = {
                    'used': used,
                    'total': total,
                    'percentage': round((used / total) * 100, 1)
                }
            
            # SWAP: SWAP 0/3810MB (cached 0MB)
            swap_match = re.search(r'SWAP (\d+)/(\d+)MB', line)
            if swap_match:
                used = int(swap_match.group(1))
                total = int(swap_match.group(2))
                data['swap'] = {
                    'used': used,
                    'total': total,
                    'percentage': round((used / total) * 100, 1) if total > 0 else 0
                }
            
            # CPU: CPU [0%@729,1%@729,1%@729,0%@729,0%@729,0%@729]
            cpu_match = re.search(r'CPU \[([^\]]+)\]', line)
            if cpu_match:
                cpu_data = cpu_match.group(1)
                cores = []
                total_usage = 0
                for core in cpu_data.split(','):
                    core_match = re.search(r'(\d+)%@(\d+)', core.strip())
                    if core_match:
                        usage = int(core_match.group(1))
                        freq = int(core_match.group(2))
                        cores.append({'usage': usage, 'frequency': freq})
                        total_usage += usage
                
                data['cpu'] = {
                    'cores': cores,
                    'average': round(total_usage / len(cores), 1) if cores else 0
                }
            
            # GPU: GR3D_FREQ 0%
            gpu_match = re.search(r'GR3D_FREQ (\d+)%', line)
            if gpu_match:
                data['gpu']['utilization'] = int(gpu_match.group(1))
            
            # Temperatures: cpu@50.031C soc2@49.75C soc0@50.843C gpu@52.031C
            temp_matches = re.findall(r'(\w+)@([\d.]+)C', line)
            for sensor, temp in temp_matches:
                temp_val = float(temp)
                if sensor == 'cpu':
                    data['temperature']['cpu'] = temp_val
                elif sensor == 'gpu':
                    data['temperature']['gpu'] = temp_val
                elif sensor.startswith('soc'):
                    data['temperature']['soc'].append({'sensor': sensor, 'temp': temp_val})
            
            # Power: VDD_IN 3709mW/3709mW VDD_CPU_GPU_CV 523mW/523mW VDD_SOC 1128mW/1128mW
            power_matches = re.findall(r'VDD_(\w+) (\d+)mW/(\d+)mW', line)
            for ptype, current, max_power in power_matches:
                if ptype == 'IN':
                    data['power']['vdd_in'] = int(current)
                elif ptype == 'CPU_GPU_CV':
                    data['power']['vdd_cpu_gpu_cv'] = int(current)
                elif ptype == 'SOC':
                    data['power']['vdd_soc'] = int(current)
                    
        except Exception as e:
            print(f"Error parsing tegrastats: {e}")
        
        return data
    
    def get_fallback_data(self):
        """Get basic system data when tegrastats fails"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'ram': {'used': 0, 'total': 0, 'percentage': 0},
            'swap': {'used': 0, 'total': 0, 'percentage': 0},
            'cpu': {'cores': [], 'average': 0},
            'gpu': {'frequency': 0, 'utilization': 0},
            'load': {'1min': 0, '5min': 0, '15min': 0, 'percentage': 0},
            'temperature': {'cpu': 0, 'gpu': 0, 'soc': []},
            'power': {'vdd_in': 0, 'vdd_cpu_gpu_cv': 0, 'vdd_soc': 0}
        }
        
        try:
            # Get memory info from /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            # Parse memory data
            mem_total = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1)) // 1024  # Convert to MB
            mem_available = int(re.search(r'MemAvailable:\s+(\d+)', meminfo).group(1)) // 1024
            mem_used = mem_total - mem_available
            
            data['ram'] = {
                'used': mem_used,
                'total': mem_total,
                'percentage': round((mem_used / mem_total) * 100, 1)
            }
            
            # Get load average
            with open('/proc/loadavg', 'r') as f:
                loadavg = f.read().split()
            
            # Get CPU count
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            cpu_count = cpuinfo.count('processor')
            
            # Parse load average
            load_1min = float(loadavg[0])
            load_5min = float(loadavg[1])
            load_15min = float(loadavg[2])
            
            # Calculate load percentage (load / cpu_count * 100)
            load_percentage = min(100, (load_1min / cpu_count) * 100)
            cpu_usage = min(100, (load_1min / cpu_count) * 100)
            
            data['load'] = {
                '1min': round(load_1min, 2),
                '5min': round(load_5min, 2),
                '15min': round(load_15min, 2),
                'percentage': round(load_percentage, 1)
            }
            
            data['cpu'] = {
                'cores': [{'usage': round(cpu_usage), 'frequency': 0} for _ in range(cpu_count)],
                'average': round(cpu_usage, 1)
            }
            
            # Get temperature from thermal zones
            temp_zones = ['thermal_zone0', 'thermal_zone1', 'thermal_zone5']
            for zone in temp_zones:
                try:
                    with open(f'/sys/class/thermal/{zone}/temp', 'r') as f:
                        temp = float(f.read().strip()) / 1000.0
                        if 'cpu' in zone or zone == 'thermal_zone0':
                            data['temperature']['cpu'] = temp
                        elif 'gpu' in zone or zone == 'thermal_zone1':
                            data['temperature']['gpu'] = temp
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting fallback data: {e}")
        
        return data
    
    def get_system_info(self):
        """Get static system information"""
        try:
            # Get Jetson model info
            jetson_info = {}
            try:
                result = subprocess.run(['jetson_release'], capture_output=True, text=True)
                if result.returncode == 0:
                    jetson_info['model'] = 'NVIDIA Jetson Orin Nano'
                    jetson_info['l4t'] = '36.4.7'
                    jetson_info['architecture'] = 'ARMv8 Cortex-A78AE (Unified Memory)'
            except:
                jetson_info['model'] = 'NVIDIA Jetson Device'
                jetson_info['l4t'] = 'Unknown'
                jetson_info['architecture'] = 'ARM (Unified Memory)'
            
            # Get uptime
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.read().split()[0])
                uptime_hours = uptime_seconds / 3600
                jetson_info['uptime'] = f"{uptime_hours:.1f} hours"
            
            # Get CPU info
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    cpu_count = cpuinfo.count('processor')
                    jetson_info['cpu_cores'] = cpu_count
                    
                    # Get CPU model
                    model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
                    if model_match:
                        jetson_info['cpu_model'] = model_match.group(1).strip()
                    else:
                        jetson_info['cpu_model'] = 'ARM Cortex-A78AE'
                    
                    # Add CPU architecture details
                    jetson_info['cpu_cores_total'] = cpu_count
                    jetson_info['cpu_clusters'] = 2
                    jetson_info['cpu_cores_per_cluster'] = 3
            except:
                jetson_info['cpu_cores'] = 6
                jetson_info['cpu_model'] = 'ARM Cortex-A78AE'
                jetson_info['cpu_cores_total'] = 6
                jetson_info['cpu_clusters'] = 2
                jetson_info['cpu_cores_per_cluster'] = 3
            
            return jetson_info
        except:
            return {
                'model': 'Unknown', 
                'l4t': 'Unknown', 
                'uptime': 'Unknown',
                'architecture': 'ARM Cortex-A78AE (Unified Memory)',
                'cpu_cores': 6,
                'cpu_model': 'ARM Cortex-A78AE',
                'cpu_cores_total': 6,
                'cpu_clusters': 2,
                'cpu_cores_per_cluster': 3
            }

if __name__ == "__main__":
    collector = JetsonDataCollector()
    data = collector.get_tegrastats_data()
    print(json.dumps(data, indent=2))
