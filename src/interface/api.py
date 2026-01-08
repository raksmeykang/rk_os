"""
api.py - REST API server for RK-OS system management and control
"""

import json
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class APIServer:
    """
    RESTful API server for RK-OS system operations and monitoring
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        """Initialize the API server"""
        self.host = host
        self.port = port
        
        # Create Flask app 
        self.app = Flask(__name__)
        
        # Initialize routes
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
                        'success': True,
                        'data': metrics
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to get system status: {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            
            # Logical operations endpoint
            @self.app.route('/logic/evaluate', methods=['POST'])
            def evaluate_logic():
                try:
                    data = request.get_json()
                    
                    if not data or 'operation' not in data:
                        return jsonify({
                            'success': False,
                            'error': 'Missing operation parameter'
                        }), 400
                    
                    from src.core.engine import initialize_rkos
                    
                    rkos_engine = initialize_rkos() 
                    result = rkos_engine.process_logic_operation(
                        data['operation'], **data.get('params', {})
                    )
                    
                    return jsonify({
                        'success': True,
                        'result': result
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to evaluate logic: {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            
            # Metrics endpoint
            @self.app.route('/metrics', methods=['GET'])
            def get_metrics():
                try:
                    from src.core.engine import initialize_rkos
                    from src.monitoring.logger import PerformanceLogger
                    
                    rkos_engine = initialize_rkos()
                    metrics = rkos_engine.get_system_metrics() 
                    
                    return jsonify({
                        'success': True,
                        'data': metrics
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to get metrics: {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            
            # Configuration endpoint  
            @self.app.route('/config', methods=['GET', 'POST'])
            def configuration():
                if request.method == 'GET':
                    # Return current config
                    return jsonify({
                        'success': True,
                        'data': {
                            'version': '1.0.0',
                            'host': self.host,
                            'port': self.port
                        }
                    })
                
                elif request.method == 'POST':
                    try:
                        data = request.get_json()
                        
                        # Update config (simplified for demo)
                        logger.info(f"Configuration updated: {data}")
                        
                        return jsonify({
                            'success': True,
                            'message': 'Configuration updated'
                        })
                        
                    except Exception as e:
                        logger.error(f"Failed to update configuration: {str(e)}")
                        return jsonify({
                            'success': False,
                            'error': str(e)
                        }), 500
            
            # Test endpoint
            @self.app.route('/test', methods=['GET'])
            def run_tests():
                try:
                    from src.tests.test_logic_system import run_tests
                    
                    test_results = run_tests()
                    
                    return jsonify({
                        'success': True,
                        'results': test_results
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to run tests: {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 500
            
            # Version endpoint
            @self.app.route('/version', methods=['GET'])
            def get_version():
                return jsonify({
                    'success': True,
                    'version': '1.0.0',
                    'service': 'rkos-api'
                })
                
        except Exception as e:
            logger.error(f"Failed to setup routes: {str(e)}")
            raise
    
    def start(self):
        """Start the API server"""
        try:
            # Run in debug mode for development
            self.app.run(
                host=self.host,
                port=self.port,
                debug=True,
                use_reloader=False  # Prevents issues with multiple threads
            )
            
        except Exception as e:
            logger.error(f"Failed to start API server: {str(e)}")
            raise
    
    def stop(self):
        """Stop the API server"""
        try:
            logger.info("API Server stopped")
            
        except Exception as e:
            logger.error(f"Error stopping API server: {str(e)}")

# Main API instance
api_server = APIServer()

def main():
    """Main function for API execution""" 
    try:
        print("Starting RK-OS API Server...")
        print(f"Server will be available at http://{api_server.host}:{api_server.port}")
        
        # Start the server (blocking call)
        api_server.start()
        
    except Exception as e:
        logger.error(f"Failed to start API server: {str(e)}")
        print(f"Error starting API server: {str(e)}")

if __name__ == "__main__":
    main()
