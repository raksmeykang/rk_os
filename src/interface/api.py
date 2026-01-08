#!/usr/bin/env python3
"""
RK-OS API Server - Logical Operating System
Provides RESTful API endpoints for RK-OS functionality
"""

import sys
import os
import time
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from typing import Dict, Any, Optional

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class RKOServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self.host = host
        self.port = port
        self.start_time = time.time()
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['JSON_SORT_KEYS'] = False
        
        # Setup routes and start server
        self._setup_routes()
        
        logger.info(f"API Server initialized on {host}:{port}")
    
    def _setup_routes(self):
        """Setup API endpoints"""
        try:
            # Health check endpoint
            @self.app.route('/health', methods=['GET'])
            def health_check():
                return jsonify({
                    'status': 'healthy',
                    'service': 'rkos-api'
                })

            # System status endpoint
            @self.app.route('/status', methods=['GET'])
            def system_status():
                try:
                    from src.core.engine import initialize_rkos

                    rkos_engine = initialize_rkos()
                    metrics = rkos_engine.get_system_metrics()

                    return jsonify({
                        'data': {
                            'system_status': 'RUNNING',
                            'metrics': metrics,
                            'timestamp': time.time(),
                            'uptime_seconds': time.time() - self.start_time
                        },
                        'success': True
                    })
                except Exception as e:
                    logger.error(f"Error in system status: {e}")
                    return jsonify({
                        'error': str(e),
                        'success': False
                    }), 500

            # Version endpoint  
            @self.app.route('/version', methods=['GET'])
            def version():
                return jsonify({
                    'service': 'rkos-api',
                    'version': '1.0.0',
                    'success': True
                })

            # Logic evaluation endpoint
            @self.app.route('/logic/evaluate', methods=['POST'])
            def evaluate_logic():
                try:
                    data = request.get_json()
                    if not data:
                        return jsonify({'error': 'No JSON data provided'}), 400
                    
                    from src.logic.propositional import PropositionalLogic
                    logic_engine = PropositionalLogic()
                    
                    result = logic_engine.evaluate_expression(
                        data.get('expression'),
                        data.get('variables', {})
                    )
                    
                    return jsonify({
                        'result': result,
                        'success': True
                    })
                except Exception as e:
                    logger.error(f"Error in logic evaluation: {e}")
                    return jsonify({
                        'error': str(e),
                        'success': False
                    }), 500

            # Metrics endpoint - FIXED VERSION
            @self.app.route('/metrics', methods=['GET'])
            def get_metrics():
                try:
                    # Try to import the system metrics properly
                    from src.monitoring.metrics import get_system_stats
                    
                    system_stats = get_system_stats()
                    return jsonify({
                        'data': {
                            'system_stats': system_stats,
                            'timestamp': time.time(),
                            'uptime_seconds': time.time() - self.start_time
                        },
                        'success': True
                    })
                except ImportError as e:
                    # If direct import fails, fallback to basic metrics  
                    logger.warning(f"Metrics import failed: {e}")
                    return jsonify({
                        'data': {
                            'system_stats': {
                                'errors_count': 0,
                                'warnings_count': 0,
                                'start_time': self.start_time
                            },
                            'timestamp': time.time(),
                            'uptime_seconds': time.time() - self.start_time
                        },
                        'success': True,
                        'warning': f'Metrics fallback due to import error: {str(e)}'
                    })
                except Exception as e:
                    # Handle any other errors in metrics processing
                    logger.error(f"Error getting metrics: {e}")
                    return jsonify({
                        'error': str(e),
                        'success': False
                    }), 500

            # Configuration endpoint  
            @self.app.route('/config', methods=['GET', 'POST'])
            def configuration():
                try:
                    if request.method == 'GET':
                        from src.core.engine import initialize_rkos
                        rkos_engine = initialize_rkos()
                        config = rkos_engine.get_configuration()
                        
                        return jsonify({
                            'data': config,
                            'success': True
                        })
                    elif request.method == 'POST':
                        data = request.get_json()
                        if not data:
                            return jsonify({'error': 'No JSON data provided'}), 400
                        
                        from src.core.engine import initialize_rkos
                        rkos_engine = initialize_rkos()
                        success = rkos_engine.update_configuration(data)
                        
                        return jsonify({
                            'success': success,
                            'message': 'Configuration updated successfully' if success else 'Failed to update configuration'
                        })
                except Exception as e:
                    logger.error(f"Error in config endpoint: {e}")
                    return jsonify({
                        'error': str(e),
                        'success': False
                    }), 500

            # Test endpoint
            @self.app.route('/test', methods=['GET'])
            def test_endpoint():
                try:
                    from src.tests.test_logic_system import run_all_tests
                    
                    results = run_all_tests()
                    return jsonify({
                        'data': results,
                        'success': True
                    })
                except Exception as e:
                    logger.error(f"Error in test endpoint: {e}")
                    return jsonify({
                        'error': str(e),
                        'success': False
                    }), 500

            # Dashboard route - THIS IS THE MISSING PIECE WE ADDED!
            @self.app.route('/')
            def dashboard():
                """Serve the main dashboard page"""
                return '''
                <html>
                <head><title>RK-OS 1.0 Dashboard</title></head>
                <body style="font-family: Arial, sans-serif; margin: 20px;">
                    <h1>🚀 RK-OS 1.0 System Dashboard</h1>
                    <p><strong>Status:</strong> <span style="color: green;">RUNNING</span></p>
                    <p><strong>Version:</strong> 1.0.0</p>
                    <p><strong>Owner:</strong> KANG CHANDARARAKSMEY</p>
                    
                    <hr>
                    <h2>📊 System Endpoints:</h2>
                    <ul>
                        <li><a href="/status" target="_blank">/status</a> - Current system status and metrics</li>
                        <li><a href="/health" target="_blank">/health</a> - Health check and service status</li>
                        <li><a href="/version" target="_blank">/version</a> - System version information</li>
                        <li><a href="/metrics" target="_blank">/metrics</a> - Performance metrics</li>
                        <li><a href="/test" target="_blank">/test</a> - Test suite execution</li>
                    </ul>
                    
                    <hr>
                    <h2>🔧 Quick Actions:</h2>
                    <button onclick="location.href='/test'">Run Test Suite</button>
                </body>
                </html>
                '''

        except Exception as e:
            logger.error(f"Error setting up routes: {e}")
    
    def start(self):
        """Start the API server"""
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise

if __name__ == '__main__':
    # Parse command line arguments for host and port
    import argparse
    
    parser = argparse.ArgumentParser(description='RK-OS API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port number to listen on')
    
    args = parser.parse_args()
    
    # Create and start server
    try:
        server = RKOServer(host=args.host, port=args.port)
        print(f"Starting RK-OS API Server on {args.host}:{args.port}")
        print("Server will be available at http://0.0.0.0:8080")
        server.start()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
