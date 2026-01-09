#!/bin/bash
# 🚀 Cross-Platform RK-OS Panel Installer
# Automatically detects OS and runs appropriate installer with all fixes applied

echo "=================================="
echo "🚀 RK-OS PANEL CROSS-PLATFORM INSTALLER"
echo "=================================="

# Detect operating system
case "$(uname -s)" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*|MINGW32*|MSYS*) machine=Windows;;
    *)          machine="UNKNOWN:$OSTYPE"
esac

echo "Detected OS: $machine"

# Function to check if required commands exist
check_requirements() {
    echo "🔧 Checking system requirements..."
    
    # Check for git
    if ! command -v git &> /dev/null; then
        echo "❌ Git is not installed. Please install git first."
        exit 1
    fi
    
    # Check for python3
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    echo "✅ All requirements met"
}

# Function to detect Raspberry Pi specifically
detect_raspberry_pi() {
    if [ -f "/proc/cpuinfo" ]; then
        if grep -q "Raspberry Pi" /proc/cpuinfo; then
            return 0  # Is Raspberry Pi
        fi
    fi
    
    # Check for ARM architecture (common in Pi)
    if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "armv7l" ]; then
        return 0  # Likely Raspberry Pi
    fi
    
    return 1  # Not Raspberry Pi
}

# Function to auto detect and choose port
auto_detect_port() {
    echo "🔍 Auto-detecting available ports..."
    
    # Try common ports in order of preference
    COMMON_PORTS=(8085 8090 8443 9000 9090)
    
    for port in "${COMMON_PORTS[@]}"; do
        if ! command_exists lsof; then
            # Fallback method without lsof
            if ! netstat -an | grep -q ":$port "; then
                echo "✅ Found available port: $port"
                echo "Selected port: $port"
                return 0
            fi
        else
            # Use lsof to check port availability
            if ! lsof -i :$port > /dev/null 2>&1; then
                echo "✅ Found available port: $port"
                echo "Selected port: $port"
                return 0
            fi
        fi
    done
    
    # If all common ports are taken, use a random high port
    RANDOM_PORT=$((RANDOM % 15000 + 49152))
    echo "⚠️ All common ports in use. Using random available port: $RANDOM_PORT"
    echo "Selected port: $RANDOM_PORT"
}

# Function to get user-selected port with validation
get_custom_port() {
    echo ""
    echo "📋 PORT SELECTION"
    echo "=================================="
    
    # Show commonly used ports based on OS type
    case "$machine" in
        Linux)
            echo "Commonly Used Ports (Linux optimized):"
            echo "  8085 - Recommended (avoiding common conflicts)"
            echo "  8090 - Alternative choice"  
            echo "  8443 - SSL port"
            echo "  9000 - Development port"
            echo "  9090 - Monitoring port"
            ;;
        Mac)
            echo "Commonly Used Ports (macOS optimized):"
            echo "  8085 - Recommended (avoiding common conflicts)"
            echo "  8090 - Alternative choice"  
            echo "  8443 - SSL port"
            echo "  9000 - Development port"
            echo "  9090 - Monitoring port"
            ;;
        Windows)
            echo "Commonly Used Ports (Windows optimized):"
            echo "  8085 - Recommended (avoiding common conflicts)"
            echo "  8090 - Alternative choice"  
            echo "  8443 - SSL port"
            echo "  9000 - Development port"
            echo "  9090 - Monitoring port"
            ;;
    esac
    
    read -p "Enter custom port number (or press Enter for auto-detect): " USER_PORT
    
    # Use auto-detection if empty
    if [ -z "$USER_PORT" ]; then
        auto_detect_port
        return 0
    fi
    
    # Validate port number
    if ! [[ "$USER_PORT" =~ ^[0-9]+$ ]] || [ "$USER_PORT" -lt 1 ] || [ "$USER_PORT" -gt 65535 ]; then
        echo "❌ Invalid port number. Using auto-detection..."
        auto_detect_port
        return 0
    else
        echo "✅ Selected port: $USER_PORT"
    fi
    
    # Check if port is already in use (with better error handling)
    if command_exists lsof; then
        if lsof -i :$USER_PORT > /dev/null 2>&1; then
            echo ""
            echo "⚠️ WARNING: Port $USER_PORT appears to be in use!"
            read -p "Continue anyway? (y/n): " CONTINUE
            if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
                echo "Installation cancelled."
                exit 1
            fi
        fi
    elif command_exists netstat; then
        if netstat -an | grep :$USER_PORT > /dev/null 2>&1; then
            echo ""
            echo "⚠️ WARNING: Port $USER_PORT appears to be in use!"
            read -p "Continue anyway? (y/n): " CONTINUE
            if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
                echo "Installation cancelled."
                exit 1
            fi
        fi
    fi
    
    echo ""
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run appropriate installer based on OS and hardware
run_installer() {
    # Check if this is a Raspberry Pi first
    if detect_raspberry_pi; then
        echo "🎯 Detected Raspberry Pi hardware - running Pi installation with all fixes..."
        if [ -f "./Install_RKOS_Pi.sh" ]; then
            chmod +x ./Install_RKOS_Pi.sh
            ./Install_RKOS_Pi.sh
        else
            echo "❌ Raspberry Pi installer not found!"
            exit 1
        fi
    else
        # Handle regular OS types
        case "$machine" in
            Linux)
                echo "🎯 Running Linux installation with all fixes..."
                if [ -f "./Install_RKOS_Linux.sh" ]; then
                    chmod +x ./Install_RKOS_Linux.sh
                    ./Install_RKOS_Linux.sh
                elif [ -f "/opt/rkos-panel/Install_RKOS_Linux.sh" ]; then
                    cd /opt/rkos-panel/
                    ./Install_RKOS_Linux.sh
                else
                    echo "❌ Linux installer not found!"
                    exit 1
                fi
                ;;
            Mac)
                echo "🎯 Running macOS installation with all fixes..."
                if [ -f "./Install_RKOS_Mac.sh" ]; then
                    chmod +x ./Install_RKOS_Mac.sh
                    ./Install_RKOS_Mac.sh
                else
                    echo "❌ macOS installer not found!"
                    exit 1
                fi
                ;;
            Windows)
                echo "🎯 Running Windows installation with all fixes..."
                if [ -f "./Install_RKOS_Windows.bat" ]; then
                    ./Install_RKOS_Windows.bat
                else
                    echo "❌ Windows installer not found!"
                    exit 1
                fi
                ;;
            *)
                echo "❌ Unsupported operating system: $machine"
                exit 1
                ;;
        esac
    fi
}

# Main execution flow
check_requirements
get_custom_port
run_installer

echo ""
echo "🎉 Installation completed successfully!"
