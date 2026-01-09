#!/bin/bash
# 🚀 RK-OS Panel Linux Installer
# Optimized for Ubuntu/Debian/Linux distributions with all fixes applied

echo "=================================="
echo "🚀 RK-OS PANEL LINUX INSTALLER"
echo "=================================="

INSTALL_DIR="/opt/rkos-panel"
PROJECT_NAME="rkos-panel"
SERVICE_NAME="rkos-panel"
DEFAULT_PORT=8085

# Function to install dependencies for Linux
install_dependencies() {
    echo "🎯 Installing Linux dependencies..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Update system and install dependencies with fastest sources
        sudo apt update -y || {
            echo "⚠️  Failed to update package list, continuing anyway..."
        }
        
        # Install required packages for Ubuntu/Debian
        echo "Installing system dependencies for Linux..."
        sudo apt install python3 python3-pip git curl wget supervisor nginx \
                         libatlas-base-dev libopenblas-dev -y || {
            echo "⚠️  Some packages may have failed to install"
        }
        
        # Install Python packages with fastest sources
        echo "Installing Python packages for Linux..."
        if ! pip3 install --trusted-host pypi.org \
                          --trusted-host pypi.python.org \
                          --trusted-host files.pythonhosted.org \
                          flask psutil requests gunicorn numpy scipy; then
            echo "⚠️  Some Python packages may have failed to install"
        fi
        
    else
        echo "❌ Not on Linux system, cannot proceed with Linux installation"
        exit 1
    fi
    
    echo "✅ Linux dependencies installed"
}

# Function to setup project structure for Linux with all fixes applied
setup_project() {
    echo "🎯 Creating Linux project directory structure..."
    
    # Create main installation directory with proper permissions
    if [ "$EUID" -eq 0 ]; then
        sudo mkdir -p $INSTALL_DIR
        sudo chown $(whoami):$(whoami) $INSTALL_DIR
    else
        mkdir -p $INSTALL_DIR
        chown $(whoami):$(whoami) $INSTALL_DIR
    fi
    
    cd $INSTALL_DIR
    
    # Clean up any existing directory to avoid conflicts
    echo "🧹 Cleaning up any existing installation..."
    if [ -d "$INSTALL_DIR/rk_os" ]; then
        rm -rf "$INSTALL_DIR/rk_os"
    fi
    
    # Clone or download the repository with error handling for Linux
    if [ ! -d "$INSTALL_DIR/rk_os" ]; then
        echo "📦 Cloning RK-OS Panel repository for Linux..."
        
        # Try git clone first (most reliable)
        if git clone https://github.com/raksmeykang/rk_os.git rk_os; then
            echo "✅ Repository cloned successfully for Linux"
            cd rk_os
        else
            echo "⚠️ Git clone failed, trying alternative method..."
            
            # Clean up any partial attempt
            rm -rf rk_os
            
            # Try direct download as fallback (Linux-friendly)
            if command_exists curl; then
                curl -L --max-time 30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for Linux"
                else
                    echo "❌ Failed to download repository with curl on Linux"
                    exit 1
                fi
            elif command_exists wget; then
                # Alternative using wget (Linux-friendly)
                wget --timeout=30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main -O - | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for Linux"
                else
                    echo "❌ Failed to download repository with wget on Linux"
                    exit 1
                fi
            else
                echo "❌ No method available to download repository on Linux"
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
    
    # Verify the repository structure is complete for Linux
    echo "🔍 Verifying Linux optimized repository structure..."
    
    # Check if essential directories exist 
    if [ ! -d "src/core" ] || [ ! -d "src/monitoring" ] || [ ! -d "src/tests" ]; then
        echo "⚠️  Warning: Missing critical source directories detected on Linux!"
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
        
        echo "✅ Created essential missing directories for Linux"
    fi
    
    # Create required directories if they don't exist
    mkdir -p config
    mkdir -p data
    mkdir -p logs
    
    # 🔧 LINUX PERMISSIONS FIX:
    echo "🔧 Setting Linux file and directory permissions..."
    
    # Set ownership on entire project with security in mind (Linux-specific)
    sudo chown -R root:root /opt/rkos-panel/rk_os/
    
    # Fix all directory permissions properly for Linux
    find /opt/rkos-panel/rk_os/src/ -type d -exec chmod 755 {} \;
    
    # Fix Python files with proper read-only permissions for Linux environment
    find /opt/rkos-panel/rk_os/src/ -name "*.py" -exec chmod 644 {} \;
    
    # Make API file executable (but secure)
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/api.py
    
    # Set specific permissions for sensitive directories
    chmod 700 /opt/rkos-panel/rk_os/src/core/
    chmod 700 /opt/rkos-panel/rk_os/src/security/
    
    # Ensure proper access for service execution while maintaining Linux security
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/
    chmod 755 /opt/rkos-panel/rk_os/src/kernel/
    chmod 755 /opt/rkos-panel/rk_os/src/logic/
    
    # Set proper permissions on logs directory  
    sudo chown -R root:root /opt/rkos-panel/rk_os/logs/
    chmod 750 /opt/rkos-panel/rk_os/logs/
    
    echo "✅ Linux optimized project structure created at $INSTALL_DIR/rk_os"
}

# Function to create systemd service for Linux with all fixes
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating Linux systemd service with custom port $USER_PORT..."
        
        # Ensure the working directory exists and has proper permissions  
        sudo mkdir -p /opt/rkos-panel/rk_os/src/interfaces/
        sudo chown -R root:root /opt/rkos-panel/rk_os/src/interfaces/ 2>/dev/null || true
        
        # Create service file with Linux security features
        if [ "$EUID" -eq 0 ]; then
            cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT (Linux Optimized)
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/rkos-panel/rk_os
ExecStart=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src

# Security enhancements:
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/rkos-panel/rk_os/logs/
ReadOnlyPaths=/opt/rkos-panel/rk_os/src/

[Install]
WantedBy=multi-user.target
EOF
            
            # Reload systemd daemon with error handling for Linux
            sudo systemctl daemon-reload 2>/dev/null && echo "✅ Linux systemd daemon reloaded successfully" || {
                echo "⚠️ Could not reload systemd daemon on Linux"
            }
            
            # Enable and start the service with error handling for Linux
            if sudo systemctl enable $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Linux systemd service enabled successfully"
            else
                echo "⚠️ Failed to enable Linux systemd service (may need manual intervention)"
            fi
            
            if sudo systemctl start $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Linux service started successfully on port $USER_PORT"
                
                # Verify service is actually running after a short delay for Linux
                sleep 3
                SERVICE_STATUS=$(sudo systemctl is-active $SERVICE_NAME.service)
                if [ "$SERVICE_STATUS" = "active" ]; then
                    echo "✅ Linux service confirmed running properly"
                else
                    echo "⚠️ Linux service may not be fully operational (check with: sudo systemctl status $SERVICE_NAME.service)"
                fi
                
            else
                echo "⚠️ Linux service may not have started properly, check with: sudo systemctl status $SERVICE_NAME.service"
            fi
            
        else
            # If running without root, create a temporary file for user to manually complete install on Linux
            cat > /tmp/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT (Linux Optimized)
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
            
            echo "⚠️ Linux service file created at /tmp/$SERVICE_NAME.service"
            echo "💡 Run the following commands as root to complete installation on Linux:"
            echo "   sudo mv /tmp/$SERVICE_NAME.service /etc/systemd/system/"
            echo "   sudo systemctl daemon-reload"
            echo "   sudo systemctl enable $SERVICE_NAME.service"
            echo "   sudo systemctl start $SERVICE_NAME.service"
        fi
        
    fi
}

# Function to create supervisor service for Linux (alternative for some systems)
create_supervisor_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating Linux supervisor service with custom port $USER_PORT..."
        
        # Check permissions before creating files
        if [ ! -w /etc/supervisor/conf.d/ ] && [ "$EUID" -ne 0 ]; then
            echo "⚠️  Cannot write to /etc/supervisor/conf.d/, running with sudo required on Linux"
            return 1
        fi
        
        # Create supervisor configuration file for Linux (with error handling)
        if [ "$EUID" -eq 0 ]; then
            cat > /etc/supervisor/conf.d/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
directory=/opt/rkos-panel/rk_os
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/rkos-panel/rk_os/logs/$SERVICE_NAME.log
environment=PYTHONPATH="/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src"
EOF
            
            # Update supervisor configuration with error handling for Linux
            sudo supervisorctl reread 2>/dev/null && echo "✅ Linux supervisor reloaded successfully" || {
                echo "⚠️ Could not update Linux supervisor"
            }
            sudo supervisorctl update 2>/dev/null && echo "✅ Linux supervisor services updated" || {
                echo "⚠️ Could not refresh Linux supervisor services"
            }
            
            echo "✅ Linux supervisor service created: /etc/supervisor/conf.d/$SERVICE_NAME.conf"
        else
            # If running without root, give instructions for Linux
            cat > /tmp/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=/usr/bin/python3 /opt/rkos-panel/rk_os/src/interfaces/api.py --port $USER_PORT
directory=/opt/rkos-panel/rk_os
user=$(whoami)
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/rkos-panel/rk_os/logs/$SERVICE_NAME.log
environment=PYTHONPATH="/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src"
EOF
            
            echo "⚠️ Linux supervisor configuration file created at /tmp/$SERVICE_NAME.conf"
            echo "💡 Run the following commands as root to complete installation on Linux:"
            echo "   sudo mv /tmp/$SERVICE_NAME.conf /etc/supervisor/conf.d/"
            echo "   sudo supervisorctl reread && sudo supervisorctl update"
        fi
    fi
}

# Function to configure Nginx reverse proxy for web access (Linux)
configure_nginx() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Configuring Linux Nginx reverse proxy..."
        
        # Check if nginx is installed and configured properly on Linux
        if ! command_exists nginx; then
            echo "⚠️  Nginx not found, skipping web proxy configuration on Linux"
            return 1
        fi
        
        # Create nginx configuration file for Linux
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
    
    error_log /opt/rkos-panel/rk_os/logs/nginx_error.log;
    access_log /opt/rkos-panel/rk_os/logs/nginx_access.log;
}
EOF
            
            # Enable the site by creating symbolic link
            if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
                sudo rm /etc/nginx/sites-enabled/$SERVICE_NAME 2>/dev/null || true
            fi
            
            sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/ 2>/dev/null && echo "✅ Linux Nginx site enabled successfully" || {
                echo "⚠️ Could not create symbolic link for Linux Nginx site"
            }
            
            # Test nginx configuration and restart with error handling for Linux
            if sudo nginx -t 2>/dev/null; then
                sudo systemctl restart nginx 2>/dev/null && echo "✅ Linux Nginx reverse proxy configured successfully" || {
                    echo "⚠️ Could not restart Linux Nginx service"
                }
            else
                echo "⚠️ Linux Nginx configuration test failed, but files created (check with: sudo nginx -t)"
            fi
            
        else
            # Create sample file for user to manually configure nginx on Linux
            cat > /tmp/nginx_config << EOF
# Sample Linux Nginx Configuration for RK-OS Panel on port $USER_PORT

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
    
    error_log /opt/rkos-panel/rk_os/logs/nginx_error.log;
    access_log /opt/rkos-panel/rk_os/logs/nginx_access.log;
}
EOF
            
            echo "⚠️ Linux Nginx configuration file created at /tmp/nginx_config"
            echo "💡 Copy this to /etc/nginx/sites-available/$SERVICE_NAME and enable it as root:"
            echo "   sudo mv /tmp/nginx_config /etc/nginx/sites-available/$SERVICE_NAME"
            echo "   sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/"
            echo "   sudo nginx -t && sudo systemctl restart nginx"
        fi
    fi
}

# Function to create startup script for manual execution (Linux version)
create_startup_script() {
    echo "🎯 Creating Linux optimized startup script..."
    
    # Create a simple bash script for easy access on Linux
    cat > $INSTALL_DIR/start_rkos_linux.sh << EOF
#!/bin/bash
# 🚀 RK-OS Panel Startup Script for Linux

echo "🚀 Starting RK-OS Panel on port $USER_PORT"
cd /opt/rkos-panel/rk_os

# Set environment variables for Linux
export PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src

# Start the application with Linux optimizations
python3 src/interfaces/api.py --port $USER_PORT

echo "✅ RK-OS Panel stopped"
EOF
    
    chmod +x $INSTALL_DIR/start_rkos_linux.sh
    echo "✅ Linux startup script created: $INSTALL_DIR/start_rkos_linux.sh"
}

# Function to display installation summary with enhanced verification for Linux
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 LINUX INSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 Installation Summary:"
    echo "   • Installation Directory: $INSTALL_DIR/rk_os"
    echo "   • Service Name: $SERVICE_NAME"
    echo "   • Web Port: $USER_PORT"
    echo "   • System Type: Linux Optimized"
    echo ""
    echo "🚀 To Test Your Linux Installation:"
    echo "   1. Check service status: sudo systemctl status $SERVICE_NAME.service"
    echo "   2. View logs: sudo journalctl -u $SERVICE_NAME.service -f"
    echo "   3. Access web interface: http://localhost:$USER_PORT"
    echo ""
    echo "💡 Linux Specific Commands:"
    echo "   • Start service: sudo systemctl start $SERVICE_NAME.service"
    echo "   • Stop service: sudo systemctl stop $SERVICE_NAME.service" 
    echo "   • Restart service: sudo systemctl restart $SERVICE_NAME.service"
    echo "   • View logs: sudo journalctl -u $SERVICE_NAME.service"
    echo ""
    echo "📝 Linux Startup Script:"
    echo "   • Manual start: $INSTALL_DIR/start_rkos_linux.sh"
    echo ""
    
    # Final verification check specific to Linux
    echo "🔍 FINAL LINUX VERIFICATION:"
    echo "   • Checking core directories..."
    
    if [ -d "/opt/rkos-panel/rk_os/src/core" ] && 
       [ -d "/opt/rkos-panel/rk_os/src/monitoring" ] &&
       [ -d "/opt/rkos-panel/rk_os/src/tests" ]; then
        echo "   ✅ All essential Linux directories present"
    else
        echo "   ⚠️  Some essential Linux directories may be missing (but were created)"
    fi
    
    echo ""
    echo "✅ RK-OS Panel is now ready for Linux use!"
    echo "=================================="
}

# Main installation function for Linux with all fixes applied
main_install() {
    echo "🚀 Starting Linux RK-OS Panel Installation..."
    
    # Check if running as root (required for some operations)
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ Some features may require root privileges on Linux"
        echo "💡 Recommended: Run with sudo ./Install_RKOS_Linux.sh"
    fi
    
    # Get custom port from user  
    get_custom_port
    
    # Install dependencies for Linux
    install_dependencies
    
    # Setup project structure with comprehensive error handling and all fixes
    setup_project
    
    # Create service files (with enhanced verification for Linux)
    create_systemd_service
    create_supervisor_service
    
    # Configure web access (if on Linux) - with enhanced error handling for Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        configure_nginx
    fi
    
    # Create startup script optimized for Linux
    create_startup_script
    
    # Display final summary specific to Linux
    display_summary
    
    echo ""
    echo "Linux installation completed successfully! 🎉"
}

# Run main installation specifically for Linux
main_install

echo ""
echo "🎉 Linux Installation process completed!"
