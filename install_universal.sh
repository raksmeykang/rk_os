mkdir -p install_scripts
cd install_scripts

# Save all independent scripts here
cat > install_universal.sh << 'EOF'
#!/bin/bash
# 🚀 RK-OS Panel Universal Installation Script (Independent Version)

echo "=================================="
echo "🚀 RK-OS PANEL UNIVERSAL INSTALLER"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS type
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux detection
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            case $ID in
                raspbian|raspberry*)
                    echo "raspberry_pi"
                    ;;
                ubuntu)
                    echo "ubuntu"
                    ;;
                debian)
                    echo "debian"
                    ;;
                fedora)
                    echo "fedora"
                    ;;
                centos|rhel)
                    echo "centos"
                    ;;
                *)
                    echo "linux_generic"
                    ;;
            esac
        else
            echo "linux_generic"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS detection
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows detection (WSL or native)
        if command_exists wslpath; then
            echo "wsl"
        else
            echo "windows"
        fi
    else
        echo "unknown"
    fi
}

# Function to install on Raspberry Pi
install_raspberry_pi() {
    echo "🎯 Installing on Raspberry Pi..."
    
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install required packages
    sudo apt install python3 python3-pip git curl wget -y
    
    # Create project directory
    cd ~/
    mkdir -p rk_os_project
    cd rk_os_project
    
    # Clone repository
    echo "📦 Cloning RK-OS Panel repository..."
    if ! git clone https://github.com/raksmeykang/rk_os.git; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    cd rk_os
    
    # Install Python dependencies
    echo "🔧 Installing Python dependencies..."
    pip3 install flask psutil requests
    
    # Test installation
    echo "✅ Testing installation..."
    if python3 src/interfaces/cli.py status; then
        echo "🎉 Raspberry Pi installation complete!"
        return 0
    else
        echo "❌ Installation test failed"
        return 1
    fi
}

# Function to install on Ubuntu/Debian
install_ubuntu() {
    echo "🎯 Installing on Ubuntu/Debian..."
    
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install required packages
    sudo apt install python3 python3-pip git curl wget -y
    
    # Create project directory
    cd ~/
    mkdir -p rk_os_project
    cd rk_os_project
    
    # Clone repository
    echo "📦 Cloning RK-OS Panel repository..."
    if ! git clone https://github.com/raksmeykang/rk_os.git; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    cd rk_os
    
    # Install Python dependencies
    echo "🔧 Installing Python dependencies..."
    pip3 install flask psutil requests
    
    # Test installation
    echo "✅ Testing installation..."
    if python3 src/interfaces/cli.py status; then
        echo "🎉 Ubuntu/Debian installation complete!"
        return 0
    else
        echo "❌ Installation test failed"
        return 1
    fi
}

# Function to install on macOS
install_macos() {
    echo "🎯 Installing on macOS..."
    
    # Check if Homebrew is installed
    if ! command_exists brew; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install required packages
    brew install python git curl wget
    
    # Create project directory
    cd ~/
    mkdir -p rk_os_project
    cd rk_os_project
    
    # Clone repository
    echo "📦 Cloning RK-OS Panel repository..."
    if ! git clone https://github.com/raksmeykang/rk_os.git; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    cd rk_os
    
    # Install Python dependencies
    echo "🔧 Installing Python dependencies..."
    pip3 install flask psutil requests
    
    # Test installation
    echo "✅ Testing installation..."
    if python3 src/interfaces/cli.py status; then
        echo "🎉 macOS installation complete!"
        return 0
    else
        echo "❌ Installation test failed"
        return 1
    fi
}

# Function to install on Windows (native)
install_windows() {
    echo "🎯 Installing on Windows..."
    
    # Check if Git is installed
    if ! command_exists git; then
        echo "⚠️ Git not found. Please install Git from https://git-scm.com/"
        read -p "Press Enter after installing Git to continue..."
    fi
    
    # Check if Python is installed  
    if ! command_exists python; then
        echo "⚠️ Python not found. Please install Python 3.x from https://python.org"
        read -p "Press Enter after installing Python to continue..."
    fi
    
    # Create project directory
    cd %USERPROFILE%
    mkdir rk_os_project
    cd rk_os_project
    
    # Clone repository
    echo "📦 Cloning RK-OS Panel repository..."
    if ! git clone https://github.com/raksmeykang/rk_os.git; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    cd rk_os
    
    # Install Python dependencies
    echo "🔧 Installing Python dependencies..."
    pip install flask psutil requests
    
    # Test installation
    echo "✅ Testing installation..."
    if python src/interfaces/cli.py status; then
        echo "🎉 Windows installation complete!"
        return 0
    else
        echo "❌ Installation test failed"
        return 1
    fi
}

# Function to install on WSL (Windows Subsystem for Linux)
install_wsl() {
    echo "🎯 Installing on WSL..."
    
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install required packages
    sudo apt install python3 python3-pip git curl wget -y
    
    # Create project directory
    cd ~/
    mkdir -p rk_os_project
    cd rk_os_project
    
    # Clone repository
    echo "📦 Cloning RK-OS Panel repository..."
    if ! git clone https://github.com/raksmeykang/rk_os.git; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    cd rk_os
    
    # Install Python dependencies
    echo "🔧 Installing Python dependencies..."
    pip3 install flask psutil requests
    
    # Test installation
    echo "✅ Testing installation..."
    if python3 src/interfaces/cli.py status; then
        echo "🎉 WSL installation complete!"
        return 0
    else
        echo "❌ Installation test failed"
        return 1
    fi
}

# Main installation function
main_install() {
    OS_TYPE=$(detect_os)
    echo " detected operating system: $OS_TYPE"
    
    case $OS_TYPE in
        raspberry_pi)
            install_raspberry_pi
            ;;
        ubuntu|debian|linux_generic)
            install_ubuntu
            ;;
        macos)
            install_macos
            ;;
        windows)
            install_windows
            ;;
        wsl)
            install_wsl
            ;;
        *)
            echo "⚠️ Unknown operating system detected. Installing generic Linux version..."
            install_ubuntu
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================="
        echo "🎉 INSTALLATION SUCCESSFUL!"
        echo "=================================="
        echo "📍 To test your installation:"
        echo "   cd ~/rk_os_project/rk_os"
        echo "   python3 src/interfaces/cli.py status"
        echo ""
        echo "💡 For API server (port 8080):"
        echo "   python3 src/interfaces/api.py --port 8080"
        echo "=================================="
    else
        echo ""
        echo "=================================="
        echo "❌ INSTALLATION FAILED!"
        echo "=================================="
        exit 1
    fi
}

# Run main installation
main_install

echo ""
echo "🚀 Installation process completed!"
EOF

# Make it executable
chmod +x install_universal.sh

# Create a simple usage guide
cat > USAGE.md << 'EOF'
# 📋 RK-OS Panel Universal Installer Usage Guide

## ✅ Quick Start

### Linux/macOS:
```bash
wget https://raw.githubusercontent.com/raksmeykang/rk_os/main/install_scripts/install_universal.sh
chmod +x install_universal.sh
./install_universal.sh
