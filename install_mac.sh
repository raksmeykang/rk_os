#!/bin/bash
# RK-OS Panel Installation Script for macOS

echo "🚀 Installing RK-OS Panel on macOS..."

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python and dependencies
echo "Installing required packages..."
brew install python git

# Create project directory
echo "Creating project directory..."
cd ~/
mkdir rk_os_project
cd rk_os_project

# Clone repository
echo "Cloning RK-OS Panel repository..."
git clone https://github.com/raksmeykang/rk_os.git
cd rk_os

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install flask psutil requests

# Test installation
echo "Testing installation..."
python3 src/interfaces/cli.py status

echo "✅ RK-OS Panel installed successfully on macOS!"
echo "💡 Run: python3 src/interfaces/cli.py status to test"
