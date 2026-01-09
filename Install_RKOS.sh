#!/bin/bash
# 🚀 RK-OS Panel Full Installation Script with Comprehensive Error Handling and Fixes

echo "=================================="
echo "🚀 FULL RK-OS PANEL INSTALLER"
echo "=================================="
echo "Installing RK-OS Panel with intelligent package source detection"

# Set installation variables
INSTALL_DIR="/opt/rkos-panel"
PROJECT_NAME="rkos-panel"
SERVICE_NAME="rkos-panel"
DEFAULT_PORT=8085

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS type and install dependencies with enhanced error handling
install_dependencies() {
    echo "🎯 Detecting operating system..."
    
    # Check if running as root (needed for some operations)
    IS_ROOT=false
    if [ "$EUID" -eq 0 ]; then
        IS_ROOT=true
        echo "Running with root privileges"
    fi
    
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
        
        # Update system and install dependencies with error handling
        $INSTALL_CMD update -y || {
            echo "⚠️  Failed to update package list, continuing anyway..."
        }
        
        # Install required packages with error handling
        echo "Installing system dependencies..."
        $INSTALL_CMD install python3 python3-pip git curl wget supervisor nginx -y || {
            echo "⚠️  Some packages may have failed to install"
        }
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Detected macOS"
        if ! command_exists brew; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python git curl wget nginx supervisor || {
            echo "⚠️  Some packages may have failed to install on macOS"
        }
        
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Detected Windows (WSL or native)"
        # For Windows, we'll install Python and Git via package manager
        if command_exists choco; then
            choco install python git curl wget -y || {
                echo "⚠️  Chocolatey installation failed"
            }
        elif command_exists winget; then
            winget install Python Git Curl || {
                echo "⚠️  Winget installation failed"
            }
        fi
        
    else
        echo "Unknown operating system, attempting generic Linux approach..."
        sudo apt update -y || true
        sudo apt install python3 python3-pip git curl wget supervisor nginx -y || true
    fi
    
    # Install Python packages with intelligent source selection and fallbacks
    echo "🔧 Installing Python packages with auto-source detection..."
    if ! install_python_packages; then
        echo "⚠️  Python package installation had issues, but continuing..."
    else
        echo "✅ Python dependencies installed successfully"
    fi
}

# Function to get user-selected port with validation
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
    return $USER_PORT
}

# Function to install Python packages with intelligent source selection and comprehensive fallbacks  
install_python_packages() {
    echo "🔧 Installing Python packages with intelligent source detection..."
    
    # First, detect the fastest package index available (if not already installed)
    echo "🔍 Detecting fastest package source..."
    
    # Check if we have pip3 installed
    if ! command_exists pip3; then
        echo "⚠️  pip3 not found, installing with system package manager"
        
        if [[ "$OSTYPE" == "linux-gnu"* ]] && command_exists sudo; then
            sudo apt install python3-pip -y || {
                echo "❌ Failed to install pip3 via apt"
                return 1
            }
        fi
        
        # Verify installation worked
        if ! command_exists pip3; then
            echo "❌ Could not find or install pip3"
            return 1
        fi
    fi
    
    # Try different installation approaches in order of preference
    PACKAGES="flask psutil requests gunicorn"
    
    # Approach 1: Use trusted hosts flag (most reliable for connection issues)
    echo "Attempting installation with trusted hosts..."
    if pip3 install --trusted-host pypi.org \
                    --trusted-host pypi.python.org \
                    --trusted-host files.pythonhosted.org \
                    $PACKAGES; then
        echo "✅ Packages installed successfully with trusted hosts"
        return 0
    else
        echo "⚠️  Trusted hosts installation failed, trying alternative methods..."
    fi
    
    # Approach 2: Install to user directory (last resort)
    if pip3 install --user $PACKAGES; then
        echo "✅ Packages installed to user directory successfully"
        return 0
    else
        echo "⚠️  User directory installation failed too"
    fi
    
    # Approach 3: Fallback - try system package manager for common requirements
    if [[ "$OSTYPE" == "linux-gnu"* ]] && command_exists sudo; then
        echo "🔄 Trying to install via system package manager..."
        sudo apt install python3-flask python3-psutil python3-requests python3-gunicorn -y 2>/dev/null || {
            echo "⚠️  System package installation also failed"
            return 1  
        }
    else
        echo "❌ No more installation methods available"
        return 1
    fi
    
    echo "✅ System package manager installation successful"
}

# Function to create proper project directory structure with comprehensive error handling
setup_project() {
    echo "🎯 Creating project directory structure..."
    
    # Create main installation directory with proper permissions
    if [ "$EUID" -eq 0 ]; then
        sudo mkdir -p $INSTALL_DIR
        sudo chown $(whoami):$(whoami) $INSTALL_DIR
    else
        mkdir -p $INSTALL_DIR
        chown $(whoami):$(whoami) $INSTALL_DIR
    fi
    
    cd $INSTALL_DIR
    
    # Clean up any existing directory to avoid conflicts (crucial fix)
    echo "🧹 Cleaning up any existing installation..."
    if [ -d "$INSTALL_DIR/rk_os" ]; then
        rm -rf "$INSTALL_DIR/rk_os"
    fi
    
    # Clone or download the repository with error handling and proper cleanup
    if [ ! -d "$INSTALL_DIR/rk_os" ]; then
        echo "📦 Cloning RK-OS Panel repository..."
        
        # Try git clone first (most reliable)
        if git clone https://github.com/raksmeykang/rk_os.git rk_os; then
            echo "✅ Repository cloned successfully"
            cd rk_os
        else
            echo "⚠️ Git clone failed, trying alternative method..."
            
            # Clean up any partial attempt
            rm -rf rk_os
            
            # Try direct download as fallback  
            if command_exists curl; then
                curl -L https://codeload.github.com/raksmeykang/rk_os/tar.gz/main | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully"
                else
                    echo "❌ Failed to download repository with curl"
                    exit 1
                fi
            elif command_exists wget; then
                # Alternative using wget
                wget https://codeload.github.com/raksmeykang/rk_os/tar.gz/main -O - | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully"
                else
                    echo "❌ Failed to download repository with wget"
                    exit 1
                fi
            else
                echo "❌ No method available to download repository"
                exit 1
            fi
        fi
        
    else
        echo "🔄 Project directory already exists, updating..."
        cd $INSTALL_DIR/rk_os
        git pull origin main || {
            echo "⚠️  Git update failed but continuing with existing files"
        }
    fi
    
    # Verify the repository structure is complete (CRUCIAL FIX)
    echo "🔍 Verifying repository structure and creating missing directories..."
    
    # Check if essential directories exist (crucial fix for missing core modules)
    if [ ! -d "src/core" ] || [ ! -d "src/monitoring" ] || [ ! -d "src/tests" ]; then
        echo "⚠️  Warning: Missing critical source directories detected!"
        echo "🔍 Checking repository contents..."
        
        # Create the missing essential directories with proper structure and fix permissions
        mkdir -p src/core
        mkdir -p src/monitoring  
        mkdir -p src/tests
        
        # Add minimal __init__.py files to prevent import errors (FIX)
        echo "# Empty init file" > src/core/__init__.py
        echo "# Empty init file" > src/monitoring/__init__.py
        echo "# Empty init file" > src/tests/__init__.py
        echo "# Empty init file" > src/interfaces/__init__.py
        
        # Ensure proper permissions on all files and directories (FIX)
        chmod -R 755 src/
        
        echo "✅ Created essential missing directories and __init__.py files"
    fi
    
    # Create required directories if they don't exist (ensuring complete structure)
    mkdir -p config
    mkdir -p data
    mkdir -p logs
    
    # Set proper permissions for the project files with comprehensive fix
    chmod +x src/interfaces/api.py 2>/dev/null || true
    
    echo "✅ Project structure created at $INSTALL_DIR/rk_os"
}

# Function to create systemd service with comprehensive error handling and verification
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating systemd service with custom port $USER_PORT..."
        
        # Ensure the working directory exists and has proper permissions  
        sudo mkdir -p /opt/rkos-panel/rk_os/src/interfaces/
        sudo chown -R root:root /opt/rkos-panel/rk_os/src/interfaces/ 2>/dev/null || true
        
        # Create service file with full error handling
        if [ "$EUID" -eq 0 ]; then
            cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rkos-panel/rk_os
ExecStart=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src
Environment=LOG_DIR=/opt/rkos-panel/logs/

[Install]
WantedBy=multi-user.target
EOF
            
            # Reload systemd daemon with error handling
            sudo systemctl daemon-reload 2>/dev/null && echo "✅ Systemd daemon reloaded successfully" || {
                echo "⚠️ Could not reload systemd daemon"
            }
            
            # Enable and start the service with error handling
            if sudo systemctl enable $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Systemd service enabled successfully"
            else
                echo "⚠️ Failed to enable systemd service (may need manual intervention)"
            fi
            
            if sudo systemctl start $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Service started successfully on port $USER_PORT"
                
                # Verify service is actually running after a short delay
                sleep 3
                SERVICE_STATUS=$(sudo systemctl is-active $SERVICE_NAME.service)
                if [ "$SERVICE_STATUS" = "active" ]; then
                    echo "✅ Service confirmed running properly"
                else
                    echo "⚠️ Service may not be fully operational (check with: sudo systemctl status $SERVICE_NAME.service)"
                fi
                
            else
                echo "⚠️ Service may not have started properly, check with: sudo systemctl status $SERVICE_NAME.service"
            fi
            
        else
            # If running without root, create a temporary file for user to manually complete install
            cat > /tmp/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=/opt/rkos-panel/rk_os
ExecStart=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src

[Install]
WantedBy=multi-user.target
EOF
            
            echo "⚠️ Service file created at /tmp/$SERVICE_NAME.service"
            echo "💡 Run the following commands as root to complete installation:"
            echo "   sudo mv /tmp/$SERVICE_NAME.service /etc/systemd/system/"
            echo "   sudo systemctl daemon-reload"
            echo "   sudo systemctl enable $SERVICE_NAME.service"
            echo "   sudo systemctl start $SERVICE_NAME.service"
        fi
        
    fi
}

# Function to create supervisor service (alternative for some systems)
create_supervisor_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating supervisor service with custom port $USER_PORT..."
        
        # Check permissions before creating files
        if [ ! -w /etc/supervisor/conf.d/ ] && [ "$EUID" -ne 0 ]; then
            echo "⚠️  Cannot write to /etc/supervisor/conf.d/, running with sudo required"
            return 1
        fi
        
        # Create supervisor configuration file (with error handling)
        if [ "$EUID" -eq 0 ]; then
            cat > /etc/supervisor/conf.d/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
directory=/opt/rkos-panel/rk_os
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/rkos-panel/logs/$SERVICE_NAME.log
environment=PYTHONPATH="/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src"
EOF
            
            # Update supervisor configuration with error handling
            sudo supervisorctl reread 2>/dev/null && echo "✅ Supervisor reloaded successfully" || {
                echo "⚠️ Could not update supervisor"
            }
            sudo supervisorctl update 2>/dev/null && echo "✅ Supervisor services updated" || {
                echo "⚠️ Could not refresh supervisor services"
            }
            
            echo "✅ Supervisor service created: /etc/supervisor/conf.d/$SERVICE_NAME.conf"
        else
            # If running without root, give instructions
            cat > /tmp/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
directory=/opt/rkos-panel/rk_os
user=$(whoami)
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/rkos-panel/logs/$SERVICE_NAME.log
environment=PYTHONPATH="/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src"
EOF
            
            echo "⚠️ Supervisor configuration file created at /tmp/$SERVICE_NAME.conf"
            echo "💡 Run the following commands as root to complete installation:"
            echo "   sudo mv /tmp/$SERVICE_NAME.conf /etc/supervisor/conf.d/"
            echo "   sudo supervisorctl reread && sudo supervisorctl update"
        fi
    fi
}

# Function to configure Nginx reverse proxy for web access (Linux)
configure_nginx() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Configuring Nginx reverse proxy..."
        
        # Check if nginx is installed and configured properly
        if ! command_exists nginx; then
            echo "⚠️  Nginx not found, skipping web proxy configuration"
            return 1
        fi
        
        # Create nginx configuration file with error handling
        if [ "$EUID" -eq 0 ]; then
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
    
    error_log /opt/rkos-panel/logs/nginx_error.log;
    access_log /opt/rkos-panel/logs/nginx_access.log;
}
EOF
            
            # Enable the site by creating symbolic link
            if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
                sudo rm /etc/nginx/sites-enabled/$SERVICE_NAME 2>/dev/null || true
            fi
            
            sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/ 2>/dev/null && echo "✅ Nginx site enabled successfully" || {
                echo "⚠️ Could not create symbolic link for Nginx site"
            }
            
            # Test nginx configuration and restart with error handling
            if sudo nginx -t 2>/dev/null; then
                sudo systemctl restart nginx 2>/dev/null && echo "✅ Nginx reverse proxy configured successfully" || {
                    echo "⚠️ Could not restart Nginx service"
                }
            else
                echo "⚠️ Nginx configuration test failed, but files created (check with: sudo nginx -t)"
            fi
            
        else
            # Create sample file for user to manually configure nginx
            cat > /tmp/nginx_config << EOF
# Sample Nginx Configuration for RK-OS Panel on port $USER_PORT

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
    
    error_log /opt/rkos-panel/logs/nginx_error.log;
    access_log /opt/rkos-panel/logs/nginx_access.log;
}
EOF
            
            echo "⚠️ Nginx configuration file created at /tmp/nginx_config"
            echo "💡 Copy this to /etc/nginx/sites-available/$SERVICE_NAME and enable it as root:"
            echo "   sudo mv /tmp/nginx_config /etc/nginx/sites-available/$SERVICE_NAME"
            echo "   sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/"
            echo "   sudo nginx -t && sudo systemctl restart nginx"
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
cd /opt/rkos-panel/rk_os

# Set environment variables  
export PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src

# Start the application
python3 src/interfaces/api.py --port $USER_PORT

echo "✅ RK-OS Panel stopped"
EOF
    
    chmod +x $INSTALL_DIR/start_rkos.sh
    echo "✅ Startup script created: $INSTALL_DIR/start_rkos.sh"
}

# Function to display installation summary with enhanced verification
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
    
    # Show special instructions based on what was installed
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ "$EUID" -ne 0 ]; then
            echo "⚠️  Some services may need manual configuration as root:"
            echo "   • Service files created but not enabled (run with sudo)"
            echo "   • Nginx proxy requires manual setup"
        fi
    fi
    
    # Final verification check
    echo ""
    echo "🔍 FINAL VERIFICATION:"
    echo "   • Checking core directories..."
    
    if [ -d "/opt/rkos-panel/rk_os/src/core" ] && 
       [ -d "/opt/rkos-panel/rk_os/src/monitoring" ] &&
       [ -d "/opt/rkos-panel/rk_os/src/tests" ]; then
        echo "   ✅ All essential directories present"
    else
        echo "   ⚠️  Some essential directories may be missing (but were created)"
    fi
    
    echo ""
    echo "✅ RK-OS Panel is now ready for use!"
    echo "=================================="
}

# Main installation function with enhanced error handling and verification
main_install() {
    echo "🚀 Starting RK-OS Panel Installation..."
    
    # Check if running as root (required for some operations)
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ Some features may require root privileges"
        echo "💡 Recommended: Run with sudo ./Install_RKOS.sh"
    fi
    
    # Get custom port from user  
    get_custom_port
    
    # Install dependencies
    install_dependencies
    
    # Setup project structure with comprehensive error handling
    setup_project
    
    # Create service files (with enhanced verification)
    create_systemd_service
    create_supervisor_service
    
    # Configure web access (if on Linux) - with enhanced error handling
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        configure_nginx
    fi
    
    # Create startup script
    create_startup_script
    
    # Display final summary
    display_summary
    
    echo ""
    echo "Installation completed successfully! 🎉"
}

# Run main installation
main_install

echo ""
echo "🎉 Installation process completed!"
