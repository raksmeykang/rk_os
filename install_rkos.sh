#!/bin/bash
# RK-OS Installation Script
# This script installs the complete RK-OS system with all dependencies

set -e  # Exit on any error

echo "=================================="
echo "RK-OS Installation Script"
echo "=================================="

# Check if running as root (required for system-wide installation)
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install package based on OS
install_package() {
    local package_name=$1
    
    if command_exists apt-get; then
        # Debian/Ubuntu
        echo "Installing $package_name using apt-get..."
        apt-get update
        apt-get install -y "$package_name"
    elif command_exists yum; then
        # CentOS/RHEL/Fedora  
        echo "Installing $package_name using yum..."
        yum install -y "$package_name"
    elif command_exists dnf; then
        # Fedora
        echo "Installing $package_name using dnf..."
        dnf install -y "$package_name"
    elif command_exists pacman; then
        # Arch Linux
        echo "Installing $package_name using pacman..."
        pacman -S --noconfirm "$package_name"
    else
        echo "Unsupported package manager. Please install $package_name manually."
        return 1
    fi
}

# Check Python version
echo "Checking Python version..."
if ! command_exists python3; then
    echo "Python 3 not found. Installing Python 3..."
    if command_exists apt-get; then
        apt-get update && apt-get install -y python3 python3-pip
    elif command_exists yum || command_exists dnf; then
        yum install -y python3 python3-pip
    else
        echo "Please install Python 3 manually"
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# Install system dependencies
echo "Installing system dependencies..."
SYSTEM_DEPS=("git" "build-essential" "libssl-dev" "libffi-dev" "python3-dev")

for dep in "${SYSTEM_DEPS[@]}"; do
    if ! command_exists "$dep"; then
        echo "Installing $dep..."
        install_package "$dep"
    else
        echo "$dep is already installed."
    fi
done

# Create RK-OS directory structure
echo "Creating RK-OS directory structure..."

RKOS_HOME="/opt/rkos"
mkdir -p "$RKOS_HOME"

# Clone or copy the source code (assuming it's in current directory)
echo "Copying RK-OS source files..."
cp -r ./* "$RKOS_HOME/" 2>/dev/null || {
    echo "Error: Could not copy source files. Please ensure you're running this script from the RK-OS root directory."
    exit 1
}

# Set proper ownership and permissions
chown -R root:root "$RKOS_HOME"
chmod -R 755 "$RKOS_HOME"

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$RKOS_HOME" || exit 1

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Installing basic dependencies..."
    pip3 install psutil python-dateutil
fi

# Create systemd service file for RK-OS (optional)
echo "Creating systemd service file..."

SERVICE_FILE="/etc/systemd/system/rkos.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=RK-OS Logical Operating System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$RKOS_HOME
ExecStart=/usr/bin/python3 $RKOS_HOME/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

chmod 644 "$SERVICE_FILE"

# Enable and start the service (if desired)
echo "Would you like to enable RK-OS as a system service? (y/n)"
read -r response
if [[ $response == [Yy] ]]; then
    echo "Enabling RK-OS service..."
    systemctl daemon-reload
    systemctl enable rkos.service
    echo "RK-OS service enabled. Start with: sudo systemctl start rkos"
fi

# Create environment variables for easy access
echo "Creating environment setup..."

ENV_FILE="/etc/profile.d/rkos.sh"
cat > "$ENV_FILE" << EOF
#!/bin/bash
export RKOS_HOME="$RKOS_HOME"
export PATH="\$PATH:$RKOS_HOME"
EOF

chmod +x "$ENV_FILE"

# Create user-friendly startup script  
echo "Creating user startup script..."

START_SCRIPT="/usr/local/bin/rkos-start"
cat > "$START_SCRIPT" << EOF
#!/bin/bash
cd $RKOS_HOME
/usr/bin/python3 main.py "\$@"
EOF

chmod +x "$START_SCRIPT"

# Display completion message
echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "To use RK-OS:"
echo "  - Run: sudo rkos-start"
echo "  - Or directly: cd $RKOS_HOME && python3 main.py"
echo ""
echo "To manage the service (if enabled):"
echo "  - Start: sudo systemctl start rkos"
echo "  - Stop: sudo systemctl stop rkos"  
echo "  - Status: sudo systemctl status rkos"
echo "  - Restart: sudo systemctl restart rkos"
echo ""
echo "Logs are available in:"
echo "  - $RKOS_HOME/rkos.log"
echo "  - $RKOS_HOME/rkos_monitoring.log"
echo ""
echo "For more information, see the README.md file."
echo "=================================="

exit 0
