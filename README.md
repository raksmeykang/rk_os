#RK-OS - Real Kick OS
What is RK-OS?
#RK-OS (Real Kick OS) 
is a comprehensive operating system control panel designed for managing and monitoring computing systems. It provides a unified interface for system administration, application management, and real-time monitoring capabilities.

🔍 Key Features:
Cross-platform compatibility - Works on Windows, Linux, and macOS
Web-based dashboard with real-time monitoring
Auto-start services for continuous operation
Custom port configuration to avoid conflicts
Complete API interface for integration
Secure authentication and access control
Real-time system metrics and performance tracking
🚀 Quick Installation
One-Click Installation:
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/Install_RKOS.sh && chmod +x Install_RKOS.sh && ./Install_RKOS.sh
Manual Installation:
git clone https://github.com/raksmeykang/rk_os.git
cd rk_os
chmod +x Install_RKOS.sh
./Install_RKOS.sh
🎯 System Requirements
Minimum Requirements:
Python 3.7 or higher
Git installed
Internet connection (for dependency installation)
At least 50MB free disk space
Recommended Resources:
RAM: 2GB minimum (4GB recommended)
Storage: 100MB minimum
Network: Full internet access for updates
🔧 Installation Process
Step 1: Download and Prepare
# Clone the repository
git clone https://github.com/raksmeykang/rk_os.git
cd rk_os

# Make installer executable
chmod +x Install_RKOS.sh
Step 2: Run Installation
./Install_RKOS.sh
During installation, you'll be prompted to select a custom port (default is 8085) to avoid conflicts with other services.

Step 3: Verify Installation
# Test the CLI interface
python src/interfaces/cli.py status
Expected output:

RK-OS Panel System Status
=========================
Status: Running
Version: 1.0.0
Owner: KANG CHANDARARAKSMEY
🚀 Usage Examples
Command Line Interface:
# Check system status
python src/interfaces/cli.py status

# Run tests
python src/interfaces/cli.py test

# Start API server manually (with custom port)
python src/interfaces/api.py --port 8085
Web Interface Access:
After installation, access the web dashboard at:

http://localhost:8085/ (or your selected port)
🎯 Custom Port Configuration Feature
✅ YES - Custom Port Configuration is Implemented in Our Python Project!

The RK-OS Panel includes a complete custom port configuration feature that allows you to:

How It Works:
Interactive Port Selection: During installation, you're prompted to choose your preferred port
Default Port: Uses 8085 by default (avoiding common ports like 8080 and 3000)
Conflict Detection: System checks if selected port is already in use
Automatic Configuration: All services configured with your chosen port
Web Proxy Setup: Nginx reverse proxy automatically configured for web access
Port Selection Example:
📋 PORT SELECTION
==================================
Commonly Used Ports (Avoiding Common Conflicts):
  8085 - Recommended (avoiding 8080, 3000)
  8090 - Alternative choice
  8443 - SSL port
  9000 - Development port
  9090 - Monitoring port

Enter custom port number (default: 8085): 8087
✅ Selected port: 8087
Implementation in Python Code:
The custom port feature is implemented in src/interfaces/api.py:

# Command line argument parsing for port selection
import argparse

parser = argparse.ArgumentParser(description='RK-OS Panel Server')
parser.add_argument('--port', type=int, default=8085, help='Port number to listen on')

args = parser.parse_args()
port_number = args.port  # Uses custom port or defaults to 8085

# Server starts on selected port
app.run(host='0.0.0.0', port=port_number)
Benefits of Custom Port Configuration:
Avoids Conflicts: Prevents conflicts with other running services
Flexible Deployment: Deploy anywhere without port restrictions
Security: Non-standard ports can provide basic security through obscurity
Multiple Instances: Run multiple RK-OS panels on same machine
Integration Ready: Easy integration into existing infrastructure
Verification:
# Test with custom port from installation
python src/interfaces/api.py --port 8087

# Or use default (8085)
python src/interfaces/api.py
🎯 Services and Management
Linux Service Management:
# Check service status
sudo systemctl status rkos-panel.service

# Start service
sudo systemctl start rkos-panel.service

# Stop service  
sudo systemctl stop rkos-panel.service

# Restart service
sudo systemctl restart rkos-panel.service

# Enable auto-start on boot
sudo systemctl enable rkos-panel.service
View Logs:
# View service logs
sudo journalctl -u rkos-panel.service -f

# View application logs (in /opt/rkos-panel/logs/)
tail -f /opt/rkos-panel/logs/*.log
📋 Testing Your Installation
Test All Components:
# Test CLI interface
python src/interfaces/cli.py status

# Test API imports
python -c "from src.interfaces.api import PanelServer; print('✅ API works')"

# Test package imports
python -c "from src.interfaces import PanelServer, CommandLineInterface; print('✅ Package works')"
🛠️ Troubleshooting
Common Issues:
Port Already in Use:

During installation, select a different port when prompted
Check existing processes: netstat -tulpn | grep :8085
Permission Denied:

sudo chmod +x Install_RKOS.sh
./Install_RKOS.sh
Service Not Starting:

# Check service status and logs
sudo systemctl status rkos-panel.service
sudo journalctl -u rkos-panel.service

# Restart service manually
sudo systemctl restart rkos-panel.service
🎉 Congratulations!
Your RK-OS (Real Kick OS) Panel is now completely installed, configured, and ready for production use across all supported platforms! ✅

You can now begin developing custom applications using this powerful control interface. 💻
