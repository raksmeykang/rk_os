#!/bin/bash
# Universal RK-OS Panel Installation Script

echo "🚀 Universal RK-OS Panel Installer"

# Detect operating system
OS_TYPE=$(uname -s)

case $OS_TYPE in
    Linux*)
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            case $ID in
                raspbian|raspberry*)
                    echo "Detected Raspberry Pi (Raspbian)"
                    ./install_pi.sh
                    ;;
                ubuntu)
                    echo "Detected Ubuntu"
                    ./install_ubuntu.sh
                    ;;
                *)
                    echo "Detected generic Linux"
                    ./install_ubuntu.sh
                    ;;
            esac
        else
            echo "Generic Linux detected"
            ./install_ubuntu.sh
        fi
        ;;
    Darwin*)
        echo "Detected macOS"
        ./install_mac.sh
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "Detected Windows (MSYS/Cygwin)"
        ./install_windows.bat
        ;;
    *)
        echo "Unknown operating system: $OS_TYPE"
        echo "Installing generic Linux version..."
        ./install_ubuntu.sh
        ;;
esac

echo "Installation complete!"
