"""
cli.py - Command-line interface for RK-OS system control
"""

import sys
import argparse
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class CommandLineInterface:
    """
    Command-line interface for RK-OS management and operations
    """
    
    def __init__(self):
        """Initialize the CLI"""
        self.parser = self._create_parser()
        
        logger.info("Command Line Interface initialized")
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create command-line argument parser
        
        Returns:
            ArgumentParser: Configured parser
        """
        parser = argparse.ArgumentParser(
            prog='rkos',
            description='RK-OS - Logical Operating System',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  rkos --help                    # Show this help message  
  rkos start                     # Start the system
  rkos status                    # Check system status
  rkos test                      # Run system tests
  rkos metrics                   # View performance metrics
  rkos config --set debug=true   # Set configuration options
            """
        )
        
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Start command  
        start_parser = subparsers.add_parser('start', help='Start RK-OS system')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Check system status') 
        
        # Test command
        test_parser = subparsers.add_parser('test', help='Run system tests')
        
        # Metrics command
        metrics_parser = subparsers.add_parser('metrics', help='View performance metrics')
        
        # Config command  
        config_parser = subparsers.add_parser('config', help='Configuration management')
        config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'),
                                  help='Set configuration key-value pair')
        config_parser.add_argument('--get', metavar='KEY',
                                  help='Get configuration value by key')
        
        # Version command
        subparsers.add_parser('version', help='Show version information')
        
        return parser
    
    def parse_args(self, args: list = None) -> Dict[str, Any]:
        """
        Parse command-line arguments
        
        Args:
            args (list): Arguments to parse (or sys.argv if None)
            
        Returns:
            dict: Parsed arguments
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Convert namespace to dictionary for easier handling
            result = {
                'command': parsed_args.command,
                'verbose': parsed_args.verbose
            }
            
            # Add command-specific arguments  
            if hasattr(parsed_args, 'set') and parsed_args.set:
                result['config_set'] = parsed_args.set
                
            if hasattr(parsed_args, 'get') and parsed_args.get:
                result['config_get'] = parsed_args.get
            
            return result
            
        except SystemExit as e:
            # argparse calls sys.exit() on error - we want to handle gracefully
            logger.error(f"Failed to parse arguments: {str(e)}")
            raise
    
    def run_command(self, args: list = None) -> int:
        """
        Execute command based on parsed arguments
        
        Args:
            args (list): Arguments to execute
            
        Returns:
            int: Exit code
        """
        try:
            parsed_args = self.parse_args(args)
            
            if parsed_args['verbose']:
                logger.setLevel(logging.DEBUG)
                
            # Handle commands  
            command = parsed_args.get('command', '')
            
            if not command or command == 'help':
                print(self.parser.format_help())
                return 0
                
            elif command == 'start':
                self._handle_start_command()
                return 0
                
            elif command == 'status':
                self._handle_status_command()  
                return 0
                
            elif command == 'test':
                self._handle_test_command()
                return 0
                
            elif command == 'metrics':
                self._handle_metrics_command()
                return 0
                
            elif command == 'config':
                self._handle_config_command(parsed_args)
                return 0
                
            elif command == 'version':
                print("RK-OS Version: 1.0.0")
                return 0
                
            else:
                logger.error(f"Unknown command: {command}")
                print(self.parser.format_usage())
                return 1
                
        except Exception as e:
            logger.error(f"Failed to execute command: {str(e)}")
            return 1
    
    def _handle_start_command(self):
        """Handle start command"""
        try:
            from src.core.engine import initialize_rkos
            
            print("Starting RK-OS system...")
            
            # Initialize the main engine
            rkos_engine = initialize_rkos()
            
            if rkos_engine:
                print("RK-OS started successfully!")
                print(f"System status: {rkos_engine.system_status}")
                
                # For demonstration, run a quick test  
                try:
                    result = rkos_engine.process_logical_operation('AND', operand1=True, operand2=False)
                    print(f"Test operation result: {result}")
                except Exception as e:
                    logger.warning(f"Test operation failed: {str(e)}")
                    
            else:
                print("Failed to initialize RK-OS system")
                
        except Exception as e:
            logger.error(f"Failed to start system: {str(e)}")
            print(f"Error starting system: {str(e)}")
    
    def _handle_status_command(self):
        """Handle status command"""
        try:
            from src.core.engine import initialize_rkos
            
            print("Checking RK-OS system status...")
            
            # Initialize the main engine
            rkos_engine = initialize_rkos()
            
            if rkos_engine:
                metrics = rkos_engine.get_system_metrics()
                
                print(f"System Status: {metrics['system_status']}")
                print(f"Uptime: {metrics['uptime_seconds']:.2f} seconds")
                
                # Display some system information
                if 'metrics' in metrics and 'system_stats' in metrics['metrics']:
                    stats = metrics['metrics']['system_stats']
                    print(f"Total Operations: {stats.get('total_operations', 0)}")
                    print(f"Errors Count: {stats.get('errors_count', 0)}")
                    
            else:
                print("System not initialized")
                
        except Exception as e:
            logger.error(f"Failed to check status: {str(e)}")
            print(f"Error checking status: {str(e)}")
    
    def _handle_test_command(self):
        """Handle test command"""
        try:
            from src.tests.test_logic_system import run_tests
            from src.tests.test_kernel_integration import run_tests as kernel_tests  
            
            print("Running RK-OS system tests...")
            
            # Run logic tests
            logic_results = run_tests()
            print(f"Logic tests: {logic_results}")
            
            # Run kernel tests 
            kernel_results = kernel_tests()
            print(f"Kernel tests: {kernel_results}")
            
        except Exception as e:
            logger.error(f"Failed to run tests: {str(e)}")
            print(f"Error running tests: {str(e)}")
    
    def _handle_metrics_command(self):
        """Handle metrics command"""
        try:
            from src.core.engine import initialize_rkos
            from src.monitoring.logger import PerformanceLogger
            
            print("Retrieving system performance metrics...")
            
            # Initialize the main engine
            rkos_engine = initialize_rkos()
            
            if rkos_engine:
                # Get and display metrics  
                metrics = rkos_engine.get_system_metrics()
                
                print(f"System Status: {metrics['system_status']}")
                print(f"Uptime: {metrics['uptime_seconds']:.2f} seconds")
                
                if 'metrics' in metrics:
                    perf_metrics = metrics['metrics']
                    
                    # Display system statistics  
                    if 'system_stats' in perf_metrics:
                        stats = perf_metrics['system_stats']
                        print("\nSystem Statistics:")
                        for key, value in stats.items():
                            print(f"  {key}: {value}")
                            
                    # Display recent operations
                    if 'recent_operations' in perf_metrics and perf_metrics['recent_operations']:
                        print("\nRecent Operations:")
                        for op in perf_metrics['recent_operations'][:5]:  # Show last 5
                            print(f"  {op.get('operation', 'unknown')}: "
                                  f"{op.get('duration', 0):.4f}s")
                            
            else:
                print("System not initialized")
                
        except Exception as e:
            logger.error(f"Failed to retrieve metrics: {str(e)}")
            print(f"Error retrieving metrics: {str(e)}")
    
    def _handle_config_command(self, parsed_args):
        """Handle config command"""
        try:
            if 'config_set' in parsed_args and parsed_args['config_set']:
                key, value = parsed_args['config_set']
                print(f"Setting configuration: {key} = {value}")
                
            elif 'config_get' in parsed_args and parsed_args['config_get']:
                key = parsed_args['config_get']
                print(f"Getting configuration for: {key}")
                
            else:
                print("Configuration command requires --set or --get options")
                
        except Exception as e:
            logger.error(f"Failed to handle config command: {str(e)}")
            print(f"Error handling configuration: {str(e)}")

# Main CLI instance
cli = CommandLineInterface()

def main():
    """Main function for CLI execution"""
    exit_code = cli.run_command()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
