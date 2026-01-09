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
