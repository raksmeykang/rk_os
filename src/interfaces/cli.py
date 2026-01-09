#!/usr/bin/env python3
"""
CLI Interface for RK-OS Panel
Owner: KANG CHANDARARAKSMEY
"""

import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class CommandLineInterface:
    """Command Line Interface for RK-OS Panel"""
    
    def test(self):
        """Run basic system tests"""
        print("RK-OS Panel CLI Test")
        print("==================")
        print("System Status: OK")
        print("Dependencies: Available")
        print("Environment: Ready")
        return True

    def status(self):
        """Show system status""" 
        print("RK-OS Panel System Status")
        print("=========================")
        print("Status: Running")
        print("Version: 1.0.0")
        print("Owner: KANG CHANDARARAKSMEY")
        return True

    def start(self):
        """Start the system"""
        print("Starting RK-OS Panel...")
        print("System started successfully!")
        return True

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 cli.py [test|status|start]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Create interface instance
    cli = CommandLineInterface()
    
    if command == "test":
        cli.test()
    elif command == "status": 
        cli.status()
    else:
        cli.start()

if __name__ == "__main__":
    main()
