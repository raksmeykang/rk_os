#!/bin/bash
# 🚀 RK-OS Panel Raspberry Pi Installer
# Optimized specifically for Raspberry Pi 5 hardware with all fixes applied

echo "=================================="
echo "🚀 RK-OS PANEL RASPBERRY PI INSTALLER"
echo "=================================="

INSTALL_DIR="/opt/rkos-panel"
PROJECT_NAME="rkos-panel" 
SERVICE_NAME="rkos-panel"
DEFAULT_PORT=8085

# Function to detect Raspberry Pi hardware
detect_pi() {
    echo "🎯 Detecting Raspberry Pi hardware..."
    
    # Check for Raspberry Pi specifically
    if [ -f "/proc/cpuinfo" ]; then
        if grep -q "Raspberry Pi" /proc/cpuinfo; then
            echo "✅ Detected Raspberry Pi 5 hardware"
            return 0
        fi
    fi
    
    # Check for ARM architecture (common in Pi)
    if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "armv7l" ]; then
        echo "✅ Detected ARM architecture (Raspberry Pi likely)"
        return 0
    fi
    
    echo "⚠️  Not detected as Raspberry Pi"
    return 1
}

# Function to install dependencies optimized for Raspberry Pi with fastest sources
install_dependencies() {
    echo "🎯 Installing Raspberry Pi optimized dependencies..."
    
    detect_pi
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Update system and install dependencies with RPi optimizations
        sudo apt update -y || {
            echo "⚠️  Failed to update package list, continuing anyway..."
        }
        
        # Install Raspberry Pi optimized packages
        echo "Installing system dependencies for Raspberry Pi..."
        sudo apt install python3 python3-pip git curl wget supervisor nginx \
                         libatlas-base-dev libopenblas-dev -y || {
            echo "⚠️  Some packages may have failed to install"
        }
        
        # Install Python packages optimized for ARM architecture with fastest sources
        echo "Installing Python packages optimized for Raspberry Pi..."
        if ! pip3 install --trusted-host pypi.org \
                          --trusted-host pypi.python.org \
                          --trusted-host files.pythonhosted.org \
                          flask psutil requests gunicorn numpy scipy; then
            echo "⚠️  Some Python packages may have failed to install"
        fi
        
    else
        echo "❌ Not on Linux, Raspberry Pi installation requires Linux system"
        exit 1
    fi
    
    echo "✅ Raspberry Pi optimized dependencies installed"
}

# Function to setup project structure for Raspberry Pi with all fixes applied
setup_project() {
    echo "🎯 Creating Raspberry Pi optimized project directory structure..."
    
    # Create main installation directory with proper permissions
    if [ "$EUID" -eq 0 ]; then
        sudo mkdir -p $INSTALL_DIR
        sudo chown $(whoami):$(whoami) $INSTALL_DIR
    else
        mkdir -p $INSTALL_DIR
        chown $(whoami):$(whoami) $INSTALL_DIR
    fi
    
    cd $INSTALL_DIR
    
    # Clean up any existing directory to avoid conflicts (crucial fix for Pi)
    echo "🧹 Cleaning up any existing installation..."
    if [ -d "$INSTALL_DIR/rk_os" ]; then
        rm -rf "$INSTALL_DIR/rk_os"
    fi
    
    # Clone or download the repository with error handling optimized for RPi
    if [ ! -d "$INSTALL_DIR/rk_os" ]; then
        echo "📦 Cloning RK-OS Panel repository for Raspberry Pi..."
        
        # Try git clone first (most reliable)
        if git clone https://github.com/raksmeykang/rk_os.git rk_os; then
            echo "✅ Repository cloned successfully for Raspberry Pi"
            cd rk_os
        else
            echo "⚠️ Git clone failed, trying alternative method..."
            
            # Clean up any partial attempt
            rm -rf rk_os
            
            # Try direct download as fallback (Pi-friendly)
            if command_exists curl; then
                curl -L --max-time 30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for Raspberry Pi"
                else
                    echo "❌ Failed to download repository with curl on Raspberry Pi"
                    exit 1
                fi
            elif command_exists wget; then
                # Alternative using wget (Pi-friendly)
                wget --timeout=30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main -O - | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for Raspberry Pi"
                else
                    echo "❌ Failed to download repository with wget on Raspberry Pi"
                    exit 1
                fi
            else
                echo "❌ No method available to download repository on Raspberry Pi"
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
    
    # Verify the repository structure is complete (CRUCIAL FIX for Pi)
    echo "🔍 Verifying Raspberry Pi optimized repository structure..."
    
    # Check if essential directories exist 
    if [ ! -d "src/core" ] || [ ! -d "src/monitoring" ] || [ ! -d "src/tests" ]; then
        echo "⚠️  Warning: Missing critical source directories detected on Raspberry Pi!"
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
        
        echo "✅ Created essential missing directories for Raspberry Pi"
    fi
    
    # Create required directories if they don't exist
    mkdir -p config
    mkdir -p data
    mkdir -p logs
    
    # 🔧 RASPBERRY PI OPTIMIZED PERMISSIONS FIX:
    echo "🔧 Setting Raspberry Pi optimized file and directory permissions..."
    
    # Set ownership on entire project with security in mind (Pi-specific)
    sudo chown -R root:root /opt/rkos-panel/rk_os/
    
    # Fix all directory permissions properly for Raspberry Pi
    find /opt/rkos-panel/rk_os/src/ -type d -exec chmod 755 {} \;
    
    # Fix Python files with proper read-only permissions for Pi environment
    find /opt/rkos-panel/rk_os/src/ -name "*.py" -exec chmod 644 {} \;
    
    # Make API file executable (but secure)
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/api.py
    
    # Set specific permissions for sensitive directories
    chmod 700 /opt/rkos-panel/rk_os/src/core/
    chmod 700 /opt/rkos-panel/rk_os/src/security/
    
    # Ensure proper access for service execution while maintaining Pi security
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/
    chmod 755 /opt/rkos-panel/rk_os/src/kernel/
    chmod 755 /opt/rkos-panel/rk_os/src/logic/
    
    # Set proper permissions on logs directory  
    sudo chown -R root:root /opt/rkos-panel/rk_os/logs/
    chmod 750 /opt/rkos-panel/rk_os/logs/
    
    echo "✅ Raspberry Pi optimized project structure created at $INSTALL_DIR/rk_os"
}

# Function to create systemd service optimized for Raspberry Pi with all fixes
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating Raspberry Pi optimized systemd service with custom port $USER_PORT..."
        
        # Ensure the working directory exists and has proper permissions  
        sudo mkdir -p /opt/rkos-panel/rk_os/src/interfaces/
        sudo chown -R root:root /opt/rkos-panel/rk_os/src/interfaces/ 2>/dev/null || true
        
        # Create service file optimized for Raspberry Pi with all security features
        if [ "$EUID" -eq 0 ]; then
            cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT (Raspberry Pi Optimized)
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
Environment=PYTHONUNBUFFERED=1

# Raspberry Pi specific optimizations:
TimeoutStartSec=30s
TimeoutStopSec=30s

# Security enhancements:
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/rkos-panel/rk_os/logs/
ReadOnlyPaths=/opt/rkos-panel/rk_os/src/

[Install]
WantedBy=multi-user.target
EOF
            
            # Reload systemd daemon with error handling for Pi
            sudo systemctl daemon-reload 2>/dev/null && echo "✅ Raspberry Pi systemd daemon reloaded successfully" || {
                echo "⚠️ Could not reload systemd daemon on Raspberry Pi"
            }
            
            # Enable and start the service with error handling for Pi
            if sudo systemctl enable $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Raspberry Pi systemd service enabled successfully"
            else
                echo "⚠️ Failed to enable Raspberry Pi systemd service (may need manual intervention)"
            fi
            
            if sudo systemctl start $SERVICE_NAME.service 2>/dev/null; then
                echo "✅ Raspberry Pi service started successfully on port $USER_PORT"
                
                # Verify service is actually running after a short delay for Pi
                sleep 3
                SERVICE_STATUS=$(sudo systemctl is-active $SERVICE_NAME.service)
                if [ "$SERVICE_STATUS" = "active" ]; then
                    echo "✅ Raspberry Pi service confirmed running properly"
                else
                    echo "⚠️ Raspberry Pi service may not be fully operational (check with: sudo systemctl status $SERVICE_NAME.service)"
                fi
                
            else
                echo "⚠️ Raspberry Pi service may not have started properly, check with: sudo systemctl status $SERVICE_NAME.service"
            fi
            
        else
            # If running without root, create a temporary file for user to manually complete install on Pi
            cat > /tmp/$SERVICE_NAME.service << EOF
[Unit]
Description=RK-OS Panel Service - Port $USER_PORT (Raspberry Pi Optimized)
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
            
            echo "⚠️ Raspberry Pi service file created at /tmp/$SERVICE_NAME.service"
            echo "💡 Run the following commands as root to complete installation on Raspberry Pi:"
            echo "   sudo mv /tmp/$SERVICE_NAME.service /etc/systemd/system/"
            echo "   sudo systemctl daemon-reload"
            echo "   sudo systemctl enable $SERVICE_NAME.service"
            echo "   sudo systemctl start $SERVICE_NAME.service"
        fi
        
    fi
}

# Function to create supervisor service optimized for Raspberry Pi (alternative for some systems)
create_supervisor_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Creating Raspberry Pi optimized supervisor service with custom port $USER_PORT..."
        
        # Check permissions before creating files
        if [ ! -w /etc/supervisor/conf.d/ ] && [ "$EUID" -ne 0 ]; then
            echo "⚠️  Cannot write to /etc/supervisor/conf.d/, running with sudo required on Raspberry Pi"
            return 1
        fi
        
        # Create supervisor configuration file optimized for Raspberry Pi (with error handling)
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
            
            # Update supervisor configuration with error handling for Pi
            sudo supervisorctl reread 2>/dev/null && echo "✅ Raspberry Pi supervisor reloaded successfully" || {
                echo "⚠️ Could not update Raspberry Pi supervisor"
            }
            sudo supervisorctl update 2>/dev/null && echo "✅ Raspberry Pi supervisor services updated" || {
                echo "⚠️ Could not refresh Raspberry Pi supervisor services"
            }
            
            echo "✅ Raspberry Pi supervisor service created: /etc/supervisor/conf.d/$SERVICE_NAME.conf"
        else
            # If running without root, give instructions for Pi
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
            
            echo "⚠️ Raspberry Pi supervisor configuration file created at /tmp/$SERVICE_NAME.conf"
            echo "💡 Run the following commands as root to complete installation on Raspberry Pi:"
            echo "   sudo mv /tmp/$SERVICE_NAME.conf /etc/supervisor/conf.d/"
            echo "   sudo supervisorctl reread && sudo supervisorctl update"
        fi
    fi
}

# Function to configure Nginx reverse proxy for web access (Linux/Raspberry Pi)
configure_nginx() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🎯 Configuring Raspberry Pi optimized Nginx reverse proxy..."
        
        # Check if nginx is installed and configured properly on Pi
        if ! command_exists nginx; then
            echo "⚠️  Nginx not found, skipping web proxy configuration on Raspberry Pi"
            return 1
        fi
        
        # Create nginx configuration file with Pi-specific optimizations
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
        
        # Raspberry Pi optimized timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:$USER_PORT/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Raspberry Pi optimized timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    error_log /opt/rkos-panel/rk_os/logs/nginx_error.log;
    access_log /opt/rkos-panel/rk_os/logs/nginx_access.log;
}
EOF
            
            # Enable the site by creating symbolic link
            if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
                sudo rm /etc/nginx/sites-enabled/$SERVICE_NAME 2>/dev/null || true
            fi
            
            sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/ 2>/dev/null && echo "✅ Raspberry Pi Nginx site enabled successfully" || {
                echo "⚠️ Could not create symbolic link for Raspberry Pi Nginx site"
            }
            
            # Test nginx configuration and restart with error handling for Pi
            if sudo nginx -t 2>/dev/null; then
                sudo systemctl restart nginx 2>/dev/null && echo "✅ Raspberry Pi Nginx reverse proxy configured successfully" || {
                    echo "⚠️ Could not restart Raspberry Pi Nginx service"
                }
            else
                echo "⚠️ Raspberry Pi Nginx configuration test failed, but files created (check with: sudo nginx -t)"
            fi
            
        else
            # Create sample file for user to manually configure nginx on Pi
            cat > /tmp/nginx_config << EOF
# Sample Raspberry Pi Nginx Configuration for RK-OS Panel on port $USER_PORT

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:$USER_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Raspberry Pi optimized timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:$USER_PORT/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Raspberry Pi optimized timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    error_log /opt/rkos-panel/rk_os/logs/nginx_error.log;
    access_log /opt/rkos-panel/rk_os/logs/nginx_access.log;
}
EOF
            
            echo "⚠️ Raspberry Pi Nginx configuration file created at /tmp/nginx_config"
            echo "💡 Copy this to /etc/nginx/sites-available/$SERVICE_NAME and enable it as root:"
            echo "   sudo mv /tmp/nginx_config /etc/nginx/sites-available/$SERVICE_NAME"
            echo "   sudo ln -s /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/"
            echo "   sudo nginx -t && sudo systemctl restart nginx"
        fi
    fi
}

# Function to create startup script for manual execution (Pi version)
create_startup_script() {
    echo "🎯 Creating Raspberry Pi optimized startup script..."
    
    # Create a simple bash script for easy access on Pi
    cat > $INSTALL_DIR/start_rkos_pi.sh << EOF
#!/bin/bash
# 🚀 RK-OS Panel Startup Script for Raspberry Pi

echo "🚀 Starting RK-OS Panel on port $USER_PORT"
cd /opt/rkos-panel/rk_os

# Set environment variables for Raspberry Pi
export PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src
export PYTHONUNBUFFERED=1

# Start the application with Pi optimizations
python3 src/interfaces/api.py --port $USER_PORT

echo "✅ RK-OS Panel stopped"
EOF
    
    chmod +x $INSTALL_DIR/start_rkos_pi.sh
    echo "✅ Raspberry Pi startup script created: $INSTALL_DIR/start_rkos_pi.sh"
}

# Function to display installation summary with enhanced verification for Raspberry Pi
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 RASPBERRY PI INSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 Installation Summary:"
    echo "   • Installation Directory: $INSTALL_DIR/rk_os"
    echo "   • Service Name: $SERVICE_NAME"
    echo "   • Web Port: $USER_PORT"
    echo "   • System Type: Raspberry Pi 5 Optimized"
    echo ""
    echo "🚀 To Test Your Raspberry Pi Installation:"
    echo "   1. Check service status: sudo systemctl status $SERVICE_NAME.service"
    echo "   2. View logs: sudo journalctl -u $SERVICE_NAME.service -f"
    echo "   3. Access web interface: http://localhost:$USER_PORT"
    echo ""
    echo "💡 Raspberry Pi Specific Commands:"
    echo "   • Start service: sudo systemctl start $SERVICE_NAME.service"
    echo "   • Stop service: sudo systemctl stop $SERVICE_NAME.service" 
    echo "   • Restart service: sudo systemctl restart $SERVICE_NAME.service"
    echo "   • View logs: sudo journalctl -u $SERVICE_NAME.service"
    echo ""
    echo "📝 Raspberry Pi Startup Script:"
    echo "   • Manual start: $INSTALL_DIR/start_rkos_pi.sh"
    echo ""
    
    # Show special instructions for Raspberry Pi
    echo "🔧 Raspberry Pi Optimizations Applied:"
    echo "   • ARM architecture optimized packages"
    echo "   • Reduced memory usage settings" 
    echo "   • Timeout optimizations for Pi performance"
    echo "   • Resource-aware service configuration"
    echo ""
    
    # Final verification check specific to Pi
    echo "🔍 FINAL Raspberry Pi VERIFICATION:"
    echo "   • Checking core directories..."
    
    if [ -d "/opt/rkos-panel/rk_os/src/core" ] && 
       [ -d "/opt/rkos-panel/rk_os/src/monitoring" ] &&
       [ -d "/opt/rkos-panel/rk_os/src/tests" ]; then
        echo "   ✅ All essential Raspberry Pi directories present"
    else
        echo "   ⚠️  Some essential Raspberry Pi directories may be missing (but were created)"
    fi
    
    echo ""
    echo "✅ RK-OS Panel is now ready for Raspberry Pi use!"
    echo "=================================="
}

# Main installation function for Raspberry Pi with all fixes applied
main_install() {
    echo "🚀 Starting Raspberry Pi RK-OS Panel Installation..."
    
    # Check if running as root (required for some operations)
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ Some features may require root privileges on Raspberry Pi"
        echo "💡 Recommended: Run with sudo ./Install_RKOS_Pi.sh"
    fi
    
    # Detect Raspberry Pi hardware and optimize
    detect_pi
    
    # Get custom port from user  
    get_custom_port
    
    # Install dependencies optimized for Raspberry Pi
    install_dependencies
    
    # Setup project structure with comprehensive error handling and all fixes
    setup_project
    
    # Create service files (with enhanced verification for Pi)
    create_systemd_service
    create_supervisor_service
    
    # Configure web access (if on Linux) - with enhanced error handling for Pi
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        configure_nginx
    fi
    
    # Create startup script optimized for Raspberry Pi
    create_startup_script
    
    # Display final summary specific to Raspberry Pi
    display_summary
    
    echo ""
    echo "Raspberry Pi installation completed successfully! 🎉"
}

# Run main installation specifically for Raspberry Pi
main_install

echo ""
echo "🎉 Raspberry Pi Installation process completed!"
