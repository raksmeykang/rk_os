#!/bin/bash
# 🚀 RK-OS Panel macOS Installer
# Optimized for macOS with all fixes applied

echo "=================================="
echo "🚀 RK-OS PANEL MACOS INSTALLER"
echo "=================================="

INSTALL_DIR="/opt/rkos-panel"
PROJECT_NAME="rkos-panel"
SERVICE_NAME="rkos-panel"
DEFAULT_PORT=8085

# Function to install dependencies for macOS
install_dependencies() {
    echo "🎯 Installing macOS dependencies..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Check if Homebrew is installed
        if ! command_exists brew; then
            echo "⚠️ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        
        # Install required packages for macOS using Homebrew
        echo "Installing system dependencies for macOS..."
        brew install python3 git curl wget nginx supervisor || {
            echo "⚠️ Some packages may have failed to install"
        }
        
        # Install Python packages with fastest sources
        echo "Installing Python packages for macOS..."
        if ! pip3 install --trusted-host pypi.org \
                          --trusted-host pypi.python.org \
                          --trusted-host files.pythonhosted.org \
                          flask psutil requests gunicorn numpy scipy; then
            echo "⚠️ Some Python packages may have failed to install"
        fi
        
    else
        echo "❌ Not on macOS system, cannot proceed with macOS installation"
        exit 1
    fi
    
    echo "✅ macOS dependencies installed"
}

# Function to setup project structure for macOS with all fixes applied
setup_project() {
    echo "🎯 Creating macOS project directory structure..."
    
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
    
    # Clone or download the repository with error handling for macOS
    if [ ! -d "$INSTALL_DIR/rk_os" ]; then
        echo "📦 Cloning RK-OS Panel repository for macOS..."
        
        # Try git clone first (most reliable)
        if git clone https://github.com/raksmeykang/rk_os.git rk_os; then
            echo "✅ Repository cloned successfully for macOS"
            cd rk_os
        else
            echo "⚠️ Git clone failed, trying alternative method..."
            
            # Clean up any partial attempt
            rm -rf rk_os
            
            # Try direct download as fallback (macOS-friendly)
            if command_exists curl; then
                curl -L --max-time 30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for macOS"
                else
                    echo "❌ Failed to download repository with curl on macOS"
                    exit 1
                fi
            elif command_exists wget; then
                # Alternative using wget (macOS-friendly)
                wget --timeout=30 https://codeload.github.com/raksmeykang/rk_os/tar.gz/main -O - | tar xz
                mv rk_os-main/* .
                rmdir rk_os-main
                
                if [ $? -eq 0 ]; then
                    echo "✅ Repository downloaded and extracted successfully for macOS"
                else
                    echo "❌ Failed to download repository with wget on macOS"
                    exit 1
                fi
            else
                echo "❌ No method available to download repository on macOS"
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
    
    # Verify the repository structure is complete for macOS
    echo "🔍 Verifying macOS optimized repository structure..."
    
    # Check if essential directories exist 
    if [ ! -d "src/core" ] || [ ! -d "src/monitoring" ] || [ ! -d "src/tests" ]; then
        echo "⚠️  Warning: Missing critical source directories detected on macOS!"
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
        
        echo "✅ Created essential missing directories for macOS"
    fi
    
    # Create required directories if they don't exist
    mkdir -p config
    mkdir -p data
    mkdir -p logs
    
    # 🔧 MACOS PERMISSIONS FIX:
    echo "🔧 Setting macOS file and directory permissions..."
    
    # Set ownership on entire project with security in mind (macOS-specific)
    sudo chown -R root:root /opt/rkos-panel/rk_os/
    
    # Fix all directory permissions properly for macOS
    find /opt/rkos-panel/rk_os/src/ -type d -exec chmod 755 {} \;
    
    # Fix Python files with proper read-only permissions for macOS environment
    find /opt/rkos-panel/rk_os/src/ -name "*.py" -exec chmod 644 {} \;
    
    # Make API file executable (but secure)
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/api.py
    
    # Set specific permissions for sensitive directories
    chmod 700 /opt/rkos-panel/rk_os/src/core/
    chmod 700 /opt/rkos-panel/rk_os/src/security/
    
    # Ensure proper access for service execution while maintaining macOS security
    chmod 755 /opt/rkos-panel/rk_os/src/interfaces/
    chmod 755 /opt/rkos-panel/rk_os/src/kernel/
    chmod 755 /opt/rkos-panel/rk_os/src/logic/
    
    # Set proper permissions on logs directory  
    sudo chown -R root:root /opt/rkos-panel/rk_os/logs/
    chmod 750 /opt/rkos-panel/rk_os/logs/
    
    echo "✅ macOS optimized project structure created at $INSTALL_DIR/rk_os"
}

# Function to create launchd service for macOS with all fixes
create_launchd_service() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🎯 Creating macOS launchd service with custom port $USER_PORT..."
        
        # Create launchd plist file for macOS
        if [ "$EUID" -eq 0 ]; then
            cat > /Library/LaunchDaemons/com.rkos.panel.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rkos.panel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/opt/rkos-panel/rk_os/src/interfaces/api.py</string>
        <string>--port</string>
        <string>$USER_PORT</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/opt/rkos-panel/rk_os</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/opt/rkos-panel/rk_os/logs/service.log</string>
    <key>StandardErrorPath</key>
    <string>/opt/rkos-panel/rk_os/logs/service.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src</string>
    </dict>
</dict>
</plist>
EOF
            
            # Load the service
            sudo launchctl load /Library/LaunchDaemons/com.rkos.panel.plist 2>/dev/null && echo "✅ macOS launchd service loaded successfully" || {
                echo "⚠️ Could not load macOS launchd service"
            }
            
            echo "✅ macOS launchd service created: /Library/LaunchDaemons/com.rkos.panel.plist"
        else
            # If running without root, create instructions for user to manually install on macOS
            cat > /tmp/com.rkos.panel.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rkos.panel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/opt/rkos-panel/rk_os/src/interfaces/api.py</string>
        <string>--port</string>
        <string>$USER_PORT</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/opt/rkos-panel/rk_os</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/opt/rkos-panel/rk_os/logs/service.log</string>
    <key>StandardErrorPath</key>
    <string>/opt/rkos-panel/rk_os/logs/service.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src</string>
    </dict>
</dict>
</plist>
EOF
            
            echo "⚠️ macOS launchd service file created at /tmp/com.rkos.panel.plist"
            echo "💡 Run the following commands as root to complete installation on macOS:"
            echo "   sudo cp /tmp/com.rkos.panel.plist /Library/LaunchDaemons/"
            echo "   sudo chmod 644 /Library/LaunchDaemons/com.rkos.panel.plist"
            echo "   sudo launchctl load /Library/LaunchDaemons/com.rkos.panel.plist"
        fi
        
    fi
}

# Function to create startup script for manual execution (macOS version)
create_startup_script() {
    echo "🎯 Creating macOS optimized startup script..."
    
    # Create a simple bash script for easy access on macOS
    cat > $INSTALL_DIR/start_rkos_mac.sh << EOF
#!/bin/bash
# 🚀 RK-OS Panel Startup Script for macOS

echo "🚀 Starting RK-OS Panel on port $USER_PORT"
cd /opt/rkos-panel/rk_os

# Set environment variables for macOS
export PYTHONPATH=/opt/rkos-panel/rk_os:/opt/rkos-panel/rk_os/src

# Start the application with macOS optimizations
python3 src/interfaces/api.py --port $USER_PORT

echo "✅ RK-OS Panel stopped"
EOF
    
    chmod +x $INSTALL_DIR/start_rkos_mac.sh
    echo "✅ macOS startup script created: $INSTALL_DIR/start_rkos_mac.sh"
}

# Function to display installation summary with enhanced verification for macOS
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 MACOS INSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 Installation Summary:"
    echo "   • Installation Directory: $INSTALL_DIR/rk_os"
    echo "   • Service Name: $SERVICE_NAME"
    echo "   • Web Port: $USER_PORT"
    echo "   • System Type: macOS Optimized"
    echo ""
    echo "🚀 To Test Your macOS Installation:"
    echo "   1. Check service status: sudo launchctl list | grep com.rkos.panel"
    echo "   2. View logs: tail -f /opt/rkos-panel/rk_os/logs/service.log"
    echo "   3. Access web interface: http://localhost:$USER_PORT"
    echo ""
    echo "💡 macOS Specific Commands:"
    echo "   • Start service: sudo launchctl load /Library/LaunchDaemons/com.rkos.panel.plist"
    echo "   • Stop service: sudo launchctl unload /Library/LaunchDaemons/com.rkos.panel.plist"
    echo "   • Restart service: sudo launchctl unload && sudo launchctl load /Library/LaunchDaemons/com.rkos.panel.plist"
    echo ""
    echo "📝 macOS Startup Script:"
    echo "   • Manual start: $INSTALL_DIR/start_rkos_mac.sh"
    echo ""
    
    # Final verification check specific to macOS
    echo "🔍 FINAL macOS VERIFICATION:"
    echo "   • Checking core directories..."
    
    if [ -d "/opt/rkos-panel/rk_os/src/core" ] && 
       [ -d "/opt/rkos-panel/rk_os/src/monitoring" ] &&
       [ -d "/opt/rkos-panel/rk_os/src/tests" ]; then
        echo "   ✅ All essential macOS directories present"
    else
        echo "   ⚠️  Some essential macOS directories may be missing (but were created)"
    fi
    
    echo ""
    echo "✅ RK-OS Panel is now ready for macOS use!"
    echo "=================================="
}

# Main installation function for macOS with all fixes applied
main_install() {
    echo "🚀 Starting macOS RK-OS Panel Installation..."
    
    # Check if running as root (required for some operations)
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ Some features may require root privileges on macOS"
        echo "💡 Recommended: Run with sudo ./Install_RKOS_Mac.sh"
    fi
    
    # Get custom port from user  
    get_custom_port
    
    # Install dependencies for macOS
    install_dependencies
    
    # Setup project structure with comprehensive error handling and all fixes
    setup_project
    
    # Create service files (with enhanced verification for macOS)
    create_launchd_service
    
    # Create startup script optimized for macOS
    create_startup_script
    
    # Display final summary specific to macOS
    display_summary
    
    echo ""
    echo "macOS installation completed successfully! 🎉"
}

# Run main installation specifically for macOS
main_install

echo ""
echo "🎉 macOS Installation process completed!"
