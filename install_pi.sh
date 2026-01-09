#!/bin/bash
# RK-OS Panel Installation Script for Raspberry Pi

echo "🚀 Installing RK-OS Panel on Raspberry Pi..."

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "Installing Python and required packages..."
sudo apt install python3 python3-pip git curl -y

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

echo "✅ RK-OS Panel installed successfully on Raspberry Pi!"
echo "💡 Run: python3 src/interfaces/cli.py status to test"
