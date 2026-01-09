# 🚀 RK-OS Panel

**RK-OS Panel** is a cross-platform system management interface with automated installation for Raspberry Pi, Linux, macOS, and Windows.

## 📋 Table of Contents
1. [Features](#features)
2. [Supported Platforms](#supported-platforms)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

## 🔧 Features

- **Cross-Platform Support**: Works on Raspberry Pi 5, Ubuntu/Debian Linux, macOS, and Windows
- **Automated Installation**: One-click installation with all fixes applied
- **Auto Port Detection**: Automatically finds available ports or lets you choose
- **Security Optimized**: All security features properly configured for each platform
- **Service Management**: Auto-start services at boot time
- **Dashboard Interface**: Complete web-based control panel

## 🖥️ Supported Platforms

| Platform | Status |
|----------|--------|
| Raspberry Pi 5 | ✅ Fully Supported |
| Ubuntu/Debian Linux | ✅ Fully Supported |
| macOS | ✅ Fully Supported |
| Windows | ✅ Fully Supported |

## 🚀 Installation

### Method 1: One-Click Cross-Platform Installer (Recommended)

```bash
# Download and run the cross-platform installer
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/install.sh -O install.sh
chmod +x install.sh
./install.sh
```
### Method 2: Platform-Specific Installers
### Raspberry Pi 5:
```
# Download and run Raspberry Pi installer
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/Install_RKOS_Pi.sh -O Install_RKOS_Pi.sh
chmod +x Install_RKOS_Pi.sh
sudo ./Install_RKOS_Pi.sh
```
### Linux (Ubuntu/Debian):
```
# Download and run Linux installer
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/Install_RKOS_Linux.sh -O Install_RKOS_Linux.sh
chmod +x Install_RKOS_Linux.sh
sudo ./Install_RKOS_Linux.sh
```
### macOS:
```
# Download and run macOS installer
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/Install_RKOS_Mac.sh -O Install_RKOS_Mac.sh
chmod +x Install_RKOS_Mac.sh
sudo ./Install_RKOS_Mac.sh
```
### Windows:
```
# Download and run Windows installer (run as Administrator)
curl https://raw.githubusercontent.com/raksmeykang/rk_os/main/Install_RKOS_Windows.bat -o Install_RKOS_Windows.bat
Install_RKOS_Windows.bat
```
## Usage
### Raspberry Pi: 
```
sudo systemctl start rkos-panel.service
sudo systemctl enable rkos-panel.service
```
### Linux:
```
sudo systemctl start rkos-panel.service
sudo systemctl enable rkos-panel.service
```
### macOS:
```
sudo launchctl load /Library/LaunchDaemons/com.rkos.panel.plist
```
### Windows
Run the startup script or use Task Scheduler to auto-start.

## Accessing the Dashboard
```
http://localhost:8085
```
```
http://[your-server-ip]:8085
```

## Configuration
### Port Selection
The installer will automatically detect available ports or let you choose:

Default port: 8085 (recommended)
Alternative ports: 8090, 8443, 9000, 9090
To specify a custom port during installation:
```
./install.sh
```
When prompted, enter your desired port number
### Service Configuration
Services are automatically configured with security features:
- NoNewPrivileges: true
- PrivateTmp: true
- ProtectSystem: strict
- ReadWritePaths: /opt/rkos-panel/rk_os/logs/
- ReadOnlyPaths: /opt/rkos-panel/rk_os/src/

## Troubleshooting
Common Issues and Solutions
1. Permission Denied Errors
```
# Fix permissions for your user
sudo chown -R $USER:$USER /opt/rkos-panel
```
2. Port Already in Use
The installer will automatically detect available ports or prompt you to choose a different one.

3. Python Import Errors
Ensure all dependencies are installed:
```
pip install --trusted-host pypi.org flask psutil requests gunicorn numpy scipy
```
4. Service Not Starting
Check service status:
```
# Linux/Raspberry Pi
sudo systemctl status rkos-panel.service

# macOS
sudo launchctl list | grep com.rkos.panel
```
## Directory
```
/opt/rkos-panel/
├── rk_os/                  # Main application files
│   ├── src/                # Source code
│   │   ├── core/           # Core functionality
│   │   ├── interfaces/     # API and UI interfaces  
│   │   ├── kernel/         # System core
│   │   ├── logic/          # Business logic
│   │   └── monitoring/     # Monitoring components
│   ├── config/             # Configuration files
│   ├── data/               # Data storage
│   └── logs/               # Log files
├── start_rkos_*.sh         # Platform-specific startup scripts
└── install.sh              # Main cross-platform installer
```
## Security Features
All Platforms Include:
- Secure File Permissions: Proper ownership and access controls
- Service Isolation: Restricted service environments
- Path Protection: Read-only paths for system files
- Memory Management: Optimized memory usage for each platform
Platform-Specific Security:
- Raspberry Pi: ARM architecture optimized security
- Linux: systemd security enhancements
- macOS: launchd service protection
- Windows: Windows ACL integration

## Performance
Raspberry Pi 5:
- ARM architecture optimized packages
- Reduced memory usage settings
- Timeout optimizations for Pi performance
- Resource-aware service configuration
Linux:
- Systemd timeout configurations
- Memory-efficient service management
- Optimized package installations
macOS:
- Launchd service optimization
- macOS-specific path handling
Windows:
- Windows Service integration
- Batch file optimization


