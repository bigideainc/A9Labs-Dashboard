import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class DataGenerator:
    def __init__(self):
        self.start_time = datetime.now()
        self.anomaly_probability = 0.1
        self.node_names = ["Alpha9-Node1", "Alpha9-Node2", "Alpha9-Node3", "YoGPT-Node1", "YoGPT-Node2"]
        self.validator = None
        
    def get_progress(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        percentage = min(100, 12.39 + (elapsed / 3600))
        tokens = int(123_936_697_600 + (elapsed * 41_700))
        return {
            'percentage': round(percentage, 2),
            'tokens': tokens
        }
    
    def get_loss_data(self):
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(99, -1, -1)]
        base_loss = 2 + np.exp(-np.linspace(1, 17000, 100)/1000) * 10
        if random.random() < self.anomaly_probability:
            base_loss[-1] += random.uniform(2, 5)
        return {'x': timestamps, 'y': base_loss}
    
    def get_perplexity_data(self):
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(99, -1, -1)]
        base_perplexity = 7 + np.exp(-np.linspace(1, 17000, 100)/1000) * 393
        
        if random.random() < self.anomaly_probability:
            base_perplexity[-1] *= random.uniform(1.5, 2.0)
            
        return {'x': timestamps, 'y': base_perplexity}
    
    def get_tps_data(self):
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(99, -1, -1)]
        base_tps = 41700 + np.random.normal(0, 1000, 100)
        if random.random() < self.anomaly_probability:
            base_tps[-1] *= random.uniform(0.7, 0.9)
        return {'x': timestamps, 'y': base_tps}
    
    def get_lr_data(self):
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(99, -1, -1)]
        base_lr = [7.5e-5] * 100
        
        if random.random() < self.anomaly_probability/2:
            base_lr[-1] = 7.5e-5 * random.uniform(0.8, 1.2)
            
        return {'x': timestamps, 'y': base_lr}
    
    def get_node_locations(self):
        return {
            'lat': [59.3293, 60.1699, 59.9139],
            'lon': [18.0686, 24.9384, 10.7522],
            'location': ['Stockholm', 'Helsinki', 'Oslo']
        }
    
    def get_leaderboard_data(self):
        try:
            # If validator is not available, return demo data
            demo_data = []
            for i in range(1, 11):
                demo_data.append({
                    "position": i,
                    "miner_uid": f"miner_{i}",
                    "final_loss": f"{random.uniform(0.1, 5.0):.4f}"
                })
            return demo_data
        except Exception as e:
            print(f"Error generating leaderboard data: {e}")
            return []
    
    def get_node_stats(self):
        now = datetime.now()
        time_points = [now - timedelta(minutes=i) for i in range(60, -1, -1)]
        
        nodes = []
        for node_name in self.node_names:
            base_response_time = random.uniform(50, 150)
            base_network_score = random.uniform(0.7, 0.95)
            
            response_time_history = {
                'x': time_points,
                'y': [base_response_time + random.uniform(-10, 10) for _ in range(61)]
            }
            
            network_score_history = {
                'x': time_points,
                'y': [base_network_score + random.uniform(-0.05, 0.05) for _ in range(61)]
            }
            
            response_time_change = response_time_history['y'][-1] - response_time_history['y'][-2]
            network_score_change = network_score_history['y'][-1] - network_score_history['y'][-2]
            
            node = {
                'name': node_name,
                'cpu_usage': random.uniform(20, 80),
                'memory_usage': random.uniform(30, 90),
                'gpu_usage': random.uniform(40, 95),
                'response_time': response_time_history['y'][-1],
                'response_time_change': response_time_change,
                'uptime': random.uniform(98, 100),
                'uptime_change': random.uniform(-0.5, 0.5),
                'success_rate': random.uniform(95, 99.9),
                'success_rate_change': random.uniform(-1, 1),
                'network_score': network_score_history['y'][-1],
                'network_score_change': network_score_change,
                'response_time_history': response_time_history,
                'network_score_history': network_score_history
            }
            nodes.append(node)
        
        return nodes