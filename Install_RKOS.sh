#!/bin/bash
# 🚀 RK-OS Panel Full Installation Script with Custom Port Selection

echo "=================================="
echo "🚀 FULL RK-OS PANEL INSTALLER"
echo "=================================="
echo "Installing RK-OS Panel with custom port selection, auto-start services, and web access"

# Set installation variables
INSTALL_DIR="/opt/rkos-panel"
PROJECT_NAME="rkos-panel"
SERVICE_NAME="rkos-panel"
DEFAULT_PORT=8085  # Default custom port to avoid conflicts

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get user-selected port
get_custom_port() {
    echo ""
    echo "📋 PORT SELECTION"
    echo "=================================="
    
    # Show commonly used ports that are less likely to conflict
    echo "Commonly Used Ports (Avoiding Common Conflicts):"
    echo "  8085 - Recommended (avoiding 8080, 3000)"
    echo "  8090 - Alternative choice"
    echo "  8443 - SSL port"
    echo "  9000 - Development port"
    echo "  9090 - Monitoring port"
    echo ""
    
    read -p "Enter custom port number (default: $DEFAULT_PORT): " USER_PORT
    
    # Use default if empty
    if [ -z "$USER_PORT" ]; then
        USER_PORT=$DEFAULT_PORT
        echo "Using default port: $USER_PORT"
    else
        # Validate port number
        if ! [[ "$USER_PORT" =~ ^[0-9]+$ ]] || [ "$USER_PORT" -lt 1 ] || [ "$USER_PORT" -gt 65535 ]; then
            echo "❌ Invalid port number. Using default: $DEFAULT_PORT"
            USER_PORT=$DEFAULT_PORT
        else
            echo "✅ Selected port: $USER_PORT"
        fi
    fi
    
    # Check if port is already in use
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
    return $USER_PORT
}

# Function to detect OS type and install dependencies
install_dependencies() {
    echo "🎯 Detecting operating system..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux detection
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            case $ID in
                raspbian|raspberry*)
                    echo "Detected Raspberry Pi (Raspbian)"
                    INSTALL_CMD="sudo apt"
                    PKG_MANAGER="apt"
                    ;;
                ubuntu)
                    echo "Detected Ubuntu"
                    INSTALL_CMD="sudo apt"
                    PKG_MANAGER="apt"
                    ;;
                debian)
                    echo "Detected Debian"
                    INSTALL_CMD="sudo apt"
                    PKG_MANAGER="apt"
                    ;;
                fedora)
                    echo "Detected Fedora"
                    INSTALL_CMD="sudo dnf"
                    PKG_MANAGER="dnf"
                    ;;
                centos|rhel)
                    echo "Detected CentOS/RHEL"
                    INSTALL_CMD="sudo yum"
                    PKG_MANAGER="yum"
                    ;;
                *)
                    echo "Generic Linux detected"
                    INSTALL_CMD="sudo apt"
                    PKG_MANAGER="apt"
                    ;;
            esac
        else
            echo "Generic Linux detected"
            INSTALL_CMD="sudo apt"
            PKG_MANAGER="apt"
        fi
        
        # Install system dependencies
        $INSTALL_CMD update -y
        $INSTALL_CMD install python3 python3-pip git curl wget supervisor nginx -y
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Detected macOS"
        if ! command_exists brew; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python git curl wget nginx supervisor
        
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Detected Windows (assuming WSL or native)"
        # For Windows, we'll install Python and Git via package manager
        if command_exists choco; then
            choco install python git curl wget -y
        elif command_exists winget; then
            winget install Python Git Curl
        fi
        
    else
        echo "Unknown operating system"
        exit 1
    fi
    
    # Install Python packages
    echo "🔧 Installing Python packages..."
    pip3 install flask psutil requests gunicorn
}

# Function to create project directory structure
setup_project() {
    echo "🎯 Creating project directory structure..."
    
    # Create main installation directory with proper permissions
    sudo mkdir -p $INSTALL_DIR
    sudo chown $(whoami):$(whoami) $INSTALL_DIR
    
    cd $INSTALL_DIR
    
    # Clone or download the repository
    if [ ! -d "$INSTALL_DIR/rk_os" ]; then
        echo "📦 Cloning RK-OS Panel repository..."
        git clone https://github.com/raksmeykang/rk_os.git .
        
        # If cloning fails, try direct download
        if [ $? -ne 0 ]; then
            echo "⚠️ Clone failed, trying alternative method..."
            curl -L https://codeload.github.com/raksmeykang/rk_os/tar.gz/main | tar xz
            mv rk_os-main/* .
            rm -rf rk_os-main
        fi
    else
        echo "🔄 Project directory already exists"
        cd $INSTALL_DIR/rk_os
    fi
    
    # Create required directories
    mkdir -p logs
    mkdir -p config
    mkdir -p data
    
    # Set proper permissions for the project files
    chmod +x src/interfaces/cli.py
    chmod +x src/interfaces/api.py
    
    echo "✅ Project structure created at $INSTALL_DIR/rk_os"
}

# Function to create systemd service (Linux)
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating systemd service with custom port $USER_PORT..."
        
        cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$INSTALL_DIR/rk_os
ExecStart=/usr/bin/python3 $INSTALL_DIR/rk_os/src/interfaces/api.py --port $USER_PORT
Restart=always
RestartSec=10
Environment=PYTHONPATH=$INSTALL_DIR/rk_os

[Install]
WantedBy=multi-user.target
EOF

        # Enable and start the service
        sudo systemctl daemon-reload
        sudo systemctl enable $SERVICE_NAME.service
        
        # Start the service immediately
        if sudo systemctl start $SERVICE_NAME.service; then
            echo "✅ Systemd service created: /etc/systemd/system/$SERVICE_NAME.service"
            echo "✅ Service started successfully on port $USER_PORT"
        else
            echo "❌ Failed to start service, but service file created"
        fi
        
    fi
}

# Function to create supervisor service (alternative for some systems)
create_supervisor_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating supervisor service with custom port $USER_PORT..."
        
        cat > /etc/supervisor/conf.d/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 $INSTALL_DIR/rk_os/src/interfaces/api.py --port $USER_PORT
directory=$INSTALL_DIR/rk_os
user=$(whoami)
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$INSTALL_DIR/logs/$SERVICE_NAME.log
environment=PYTHONPATH="$INSTALL_DIR/rk_os"
EOF

        # Update supervisor configuration
        sudo supervisorctl reread
        sudo supervisorctl update
        
        echo "✅ Supervisor service created: /etc/supervisor/conf.d/$SERVICE_NAME.conf"
    fi
}

# Function to configure Nginx reverse proxy for web access (Linux)
configure_nginx() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Configuring Nginx reverse proxy..."
        
        # Create nginx configuration file
        cat > /etc/nginx/sites-available/$SERVICE_NAME << EOF
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:$USER_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:$USER_PORT/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    error_log $INSTALL_DIR/logs/nginx_error.log;
    access_log $INSTALL_DIR/logs/nginx_access.log;
}
EOF

        # Enable the site
        if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
            sudo rm /etc/nginx/sites-enabled/$SERVICE_NAME
        fi
        
        sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
        
        # Test nginx configuration and restart
        if sudo nginx -t; then
            sudo systemctl restart nginx
            echo "✅ Nginx reverse proxy configured for port $USER_PORT"
        else
            echo "⚠️ Nginx configuration test failed, but service files created"
        fi
        
    fi
}

# Function to create startup script for manual execution (Windows/macOS)
create_startup_script() {
    echo "🎯 Creating startup script..."
    
    # Create a simple bash script for easy access
    cat > $INSTALL_DIR/start_rkos.sh << EOF
#!/bin/bash
# 🚀 RK-OS Panel Startup Script

echo "🚀 Starting RK-OS Panel on port $USER_PORT"
cd $INSTALL_DIR/rk_os

# Set environment variables
export PYTHONPATH=$INSTALL_DIR/rk_os

# Start the application
python3 src/interfaces/api.py --port $USER_PORT

echo "✅ RK-OS Panel stopped"
EOF
    
    chmod +x $INSTALL_DIR/start_rkos.sh
    echo "✅ Startup script created: $INSTALL_DIR/start_rkos.sh"
}

# Function to create systemd service (Linux)
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating systemd service with custom port $USER_PORT..."
        
        cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$INSTALL_DIR/rk_os
ExecStart=/usr/bin/python3 $INSTALL_DIR/rk_os/src/interfaces/api.py --port $USER_PORT
Restart=always
RestartSec=10
Environment=PYTHONPATH=$INSTALL_DIR/rk_os

[Install]
WantedBy=multi-user.target
EOF

        # Enable and start the service
        sudo systemctl daemon-reload
        sudo systemctl enable $SERVICE_NAME.service
        
        # Start the service immediately
        if sudo systemctl start $SERVICE_NAME.service; then
            echo "✅ Systemd service created: /etc/systemd/system/$SERVICE_NAME.service"
            echo "✅ Service started successfully on port $USER_PORT"
        else
            echo "❌ Failed to start service, but service file created"
        fi
        
    fi
}

# Function to display installation summary
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 INSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 Installation Summary:"
    echo "   • Installation Directory: $INSTALL_DIR/rk_os"
    echo "   • Service Name: $SERVICE_NAME"
    echo "   • Web Port: $USER_PORT"
    echo "   • System Type: $(uname -s)"
    echo ""
    echo "🚀 To Test Your Installation:"
    echo "   1. Check service status: sudo systemctl status $SERVICE_NAME.service"
    echo "   2. View logs: sudo journalctl -u $SERVICE_NAME.service -f"
    echo "   3. Access web interface: http://localhost:$USER_PORT"
    echo ""
    echo "💡 Useful Commands:"
    echo "   • Start service: sudo systemctl start $SERVICE_NAME.service"
    echo "   • Stop service: sudo systemctl stop $SERVICE_NAME.service" 
    echo "   • Restart service: sudo systemctl restart $SERVICE_NAME.service"
    echo "   • View logs: sudo journalctl -u $SERVICE_NAME.service"
    echo ""
    echo "📝 Startup Script:"
    echo "   • Manual start: $INSTALL_DIR/start_rkos.sh"
    echo ""
    echo "✅ RK-OS Panel is now ready for use!"
    echo "=================================="
}

# Main installation function
main_install() {
    echo "🚀 Starting RK-OS Panel Installation..."
    
    # Get custom port from user
    get_custom_port
    
    # Install dependencies
    install_dependencies
    
    # Setup project structure
    setup_project
    
    # Create service files
    create_systemd_service
    create_supervisor_service
    
    # Configure web access (if on Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        configure_nginx
    fi
    
    # Create startup script
    create_startup_script
    
    # Display final summary
    display_summary
}

# Run main installation
main_install

echo ""
echo "Installation completed successfully! 🎉"
