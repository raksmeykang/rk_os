#!/bin/bash

echo "Installing RK-OS 1.0 Logical Operating System on Raspberry Pi 5"
echo "================================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  echo "Warning: Running as root. This may cause permission issues."
fi

# Update package list and fix any broken packages first
echo "Fixing system package management..."
sudo dpkg --configure -a
sudo apt clean
sudo apt update

# Install required dependencies for Raspberry Pi 5
echo "Installing dependencies for Raspberry Pi 5..."
sudo apt install python3-pip python3-dev git build-essential libssl-dev libffi-dev python3-venv -y

# Upgrade pip
echo "Upgrading pip..."
pip3 install --upgrade pip

# Create virtual environment for RK-OS (to avoid system conflicts)
echo "Creating virtual environment..."
mkdir -p /opt/rkos
cd /opt/rkos
python3 -m venv rkos_env
source rkos_env/bin/activate

# Install Python requirements in virtual environment
echo "Installing Python requirements in virtual environment..."
if [ -f "/home/raksmeykang/rk_os/requirements.txt" ]; then
    cd /home/raksmeykang/rk_os
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Installing basic dependencies."
    pip install flask psutil
fi

# Copy source files to opt directory (system location)
echo "Copying source files to system directories..."
sudo mkdir -p /opt/rkos/src
sudo cp -r /home/raksmeykang/rk_os/src/* /opt/rkos/src/

# Make scripts executable in system location
echo "Making scripts executable..."
sudo chmod +x /opt/rkos/*.sh
sudo chmod +x /opt/rkos/src/interfaces/cli.py
sudo chmod +x /opt/rkos/src/interfaces/gui.py
sudo chmod +x /opt/rkos/src/interfaces/api.py

# Create systemd service file for Raspberry Pi 5
echo "Creating systemd service file for Raspberry Pi 5..."
sudo cat > /etc/systemd/system/rkos.service << EOF
[Unit]
Description=RK-OS 1.0 Logical Operating System for Raspberry Pi 5
After=network.target

[Service]
Type=simple
User=raksmeykang
WorkingDirectory=/opt/rkos
ExecStart=/opt/rkos/rkos_env/bin/python3 -m src.interfaces.api
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable service to start on boot
echo "Enabling RK-OS service..."
sudo systemctl enable rkos.service

echo ""
echo "RK-OS 1.0 Installation Complete for Raspberry Pi 5!"
echo "================================================"
echo "Installation Details:"
echo "- System location: /opt/rkos/"
echo "- Virtual environment: /opt/rkos/rkos_env/"
echo "- Service file: /etc/systemd/system/rkos.service"
echo ""
echo "To start the system:"
echo "  sudo systemctl start rkos.service"
echo "  or"
echo "  source /opt/rkos/rkos_env/bin/activate && python3 -m src.interfaces.cli start"
echo ""
echo "To check status:"
echo "  sudo systemctl status rkos.service"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u rkos.service"
echo ""
echo "To test installation:"
echo "  source /opt/rkos/rkos_env/bin/activate && python3 -m src.interfaces.cli test"
echo ""
echo "Owner: KANG CHANDARARAKSMEY"
echo "License: MIT License"
