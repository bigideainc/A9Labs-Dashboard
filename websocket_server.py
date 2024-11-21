import sys
import os
from pathlib import Path

# Add the project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import asyncio
import websockets
import json
import logging
from neurons.validator import TrainingValidator

class MetricsWebSocketServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.validator = TrainingValidator(repo_name="Tobius/yogpt_test")
        
    async def handle_client(self, websocket, path):
        """Handle individual client connections"""
        try:
            while True:
                # Fetch metrics using validator methods
                commits = self.validator.read_commits()
                job_groups = self.validator.group_commits(commits)
                metrics_data = []
                
                for job_id, commits in job_groups.items():
                    metrics_data.extend(self.validator.extract_metrics_by_job_id(job_id, commits))
                
                # Send metrics to client
                await websocket.send(json.dumps({
                    "metrics": metrics_data,
                    "timestamp": asyncio.get_event_loop().time()
                }))
                
                await asyncio.sleep(5)  # Update interval
                
        except websockets.exceptions.ConnectionClosed:
            logging.info("Client disconnected")
        except Exception as e:
            logging.error(f"Error in handle_client: {str(e)}")

    async def start_server(self):
        """Start the WebSocket server"""
        async with websockets.serve(self.handle_client, self.host, self.port) as server:
            logging.info(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

def run_server():
    """Entry point to start the server"""
    server = MetricsWebSocketServer()
    asyncio.run(server.start_server())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_server() 