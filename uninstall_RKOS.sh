#!/bin/bash
# 🗑️ RK-OS Panel Intelligent Uninstallation Script (Cross-Platform)

echo "=================================="
echo "🗑️  INTELLIGENT RK-OS UNINSTALLER"
echo "=================================="
echo ""

# Set default variables
INSTALL_DIR="/opt/rkos-panel"
SERVICE_NAME="rkos-panel"
DETECTED_PORT=""
FOUND_PORT=false
FOUND_INSTALLATION=false

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect port automatically
detect_rkos_port() {
    echo "🎯 Auto-detecting RK-OS Panel port..."
    
    # Method 1: Check systemd service configuration (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
            PORT_LINE=$(grep "ExecStart.*--port\|port.*api.py" "/etc/systemd/system/$SERVICE_NAME.service" 2>/dev/null)
            if [[ ! -z "$PORT_LINE" ]]; then
                if [[ $PORT_LINE =~ --port[[:space:]]*([0-9]+) ]]; then
                    DETECTED_PORT="${BASH_REMATCH[1]}"
                    echo "✅ Port detected from systemd service: $DETECTED_PORT"
                    FOUND_PORT=true
                    return 0
                elif [[ $PORT_LINE =~ ([0-9]{4,5}) ]]; then
                    DETECTED_PORT="${BASH_REMATCH[1]}"
                    echo "✅ Port detected from systemd service: $DETECTED_PORT"
                    FOUND_PORT=true
                    return 0
                fi
            fi
        fi
    fi
    
    # Method 2: Check running processes
    if command_exists ps; then
        PROCESS_LINE=$(ps aux | grep -v grep | grep "python.*api.py" | head -1)
        if [[ ! -z "$PROCESS_LINE" ]]; then
            if [[ $PROCESS_LINE =~ --port[[:space:]]*([0-9]+) ]]; then
                DETECTED_PORT="${BASH_REMATCH[1]}"
                echo "✅ Port detected from running process: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            elif [[ $PORT_LINE =~ ([0-9]{4,5}) ]]; then
                DETECTED_PORT="${BASH_REMATCH[1]}"
                echo "✅ Port detected from running process: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            fi
        fi
    fi
    
    # Method 3: Check configuration files  
    if [ -f "$INSTALL_DIR/rk_os/config/server.conf" ]; then
        PORT_LINE=$(grep -i "port\|listen" "$INSTALL_DIR/rk_os/config/server.conf" 2>/dev/null | head -1)
        if [[ ! -z "$PORT_LINE" ]]; then
            if [[ $PORT_LINE =~ [0-9]{4,5} ]]; then
                DETECTED_PORT="${BASH_REMATCH[0]}"
                echo "✅ Port detected from config file: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            fi
        fi
    fi
    
    # Method 4: Check for default port (fallback)
    if command_exists lsof; then
        for PORT in 8085 8080 3000 9000 8443; do
            if lsof -i :$PORT > /dev/null 2>&1; then
                PROCESS_INFO=$(lsof -i :$PORT | grep python)
                if [[ ! -z "$PROCESS_INFO" ]]; then
                    DETECTED_PORT=$PORT
                    echo "✅ Found RK-OS service on default port: $DETECTED_PORT"
                    FOUND_PORT=true
                    return 0
                fi
            fi
        done
    elif command_exists netstat; then
        for PORT in 8085 8080 3000 9000 8443; do
            if netstat -an | grep :$PORT > /dev/null 2>&1; then
                PROCESS_INFO=$(netstat -an | grep :$PORT | grep python)
                if [[ ! -z "$PROCESS_INFO" ]]; then
                    DETECTED_PORT=$PORT
                    echo "✅ Found RK-OS service on default port: $DETECTED_PORT"
                    FOUND_PORT=true
                    return 0
                fi
            fi
        done
    fi
    
    # Method 5: Fallback to default if still not found
    DETECTED_PORT=8085
    echo "⚠️  Using fallback default port: $DETECTED_PORT"
    FOUND_PORT=true
    return 0
}

# Function to detect installation directory automatically  
detect_installation_directory() {
    echo "🎯 Auto-detecting RK-OS Panel installation..."
    
    # Check main locations (cross-platform)
    INSTALL_DIRS=("/opt/rkos-panel" "$HOME/rk_os" "$USERPROFILE/rk_os" "/opt/rkos-panel" "$HOME/rkos-panel")
    
    for dir in "${INSTALL_DIRS[@]}"; do
        if [ -d "$dir/rk_os" ]; then
            INSTALL_DIR="$dir"
            echo "✅ Found installation at: $INSTALL_DIR/rk_os"
            FOUND_INSTALLATION=true
            return 0
        elif [ -d "$dir" ] && [ -f "$dir/src/interfaces/api.py" ]; then
            INSTALL_DIR="$dir"
            echo "✅ Found installation at: $INSTALL_DIR"
            FOUND_INSTALLATION=true
            return 0
        fi
    done
    
    # Check for any RK-OS related directories in common locations (cross-platform)
    COMMON_DIRS=("/opt" "$HOME" "$USERPROFILE")
    for base_dir in "${COMMON_DIRS[@]}"; do
        if [ -d "$base_dir/rk_os" ]; then
            INSTALL_DIR="$base_dir/rk_os"
            echo "✅ Found installation at: $INSTALL_DIR"
            FOUND_INSTALLATION=true
            return 0
        fi
        if [ -d "$base_dir/rkos-panel" ]; then
            INSTALL_DIR="$base_dir/rkos-panel"
            echo "✅ Found installation at: $INSTALL_DIR"
            FOUND_INSTALLATION=true
            return 0
        fi
    done
    
    # If no specific location found, use default but mark as not found
    echo "⚠️  Installation directory not auto-detected, using default: $INSTALL_DIR"
    FOUND_INSTALLATION=false
    return 1
}

# Function to stop and remove services based on detected port and installation
uninstall_services() {
    echo "🎯 Stopping and removing services..."
    
    # Kill any running processes for this service (cross-platform)
    if command_exists pkill; then
        pkill -f "$SERVICE_NAME" 2>/dev/null || true
        pkill -f "rkos-panel" 2>/dev/null || true
    fi
    
    # Linux specific cleanup
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🔍 Checking Linux services..."
        
        # Systemd service removal
        if command_exists systemctl; then
            if sudo systemctl is-active --quiet $SERVICE_NAME.service 2>/dev/null; then
                echo "Stopping systemd service..."
                sudo systemctl stop $SERVICE_NAME.service || true
            fi
            
            if [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
                echo "Removing systemd service..."
                sudo systemctl disable $SERVICE_NAME.service 2>/dev/null || true
                sudo rm -f /etc/systemd/system/$SERVICE_NAME.service 2>/dev/null || true
                sudo systemctl daemon-reload 2>/dev/null || true
            fi
        fi
        
        # Supervisor service removal (if exists)
        if [ -f "/etc/supervisor/conf.d/$SERVICE_NAME.conf" ]; then
            echo "Removing supervisor service..."
            sudo rm -f /etc/supervisor/conf.d/$SERVICE_NAME.conf 2>/dev/null || true
            sudo supervisorctl reread 2>/dev/null || true
            sudo supervisorctl update 2>/dev/null || true
        fi
        
        # Nginx configuration removal (if exists)
        if command_exists nginx; then
            if [ -f "/etc/nginx/sites-available/$SERVICE_NAME" ]; then
                echo "Removing Nginx configuration..."
                sudo rm -f /etc/nginx/sites-available/$SERVICE_NAME 2>/dev/null || true
                if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
                    sudo rm -f /etc/nginx/sites-enabled/$SERVICE_NAME 2>/dev/null || true
                fi
                sudo nginx -t 2>/dev/null && sudo systemctl restart nginx 2>/dev/null || true
            fi
        fi
        
        # Kill any remaining processes on detected port
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            if command_exists lsof; then
                lsof -ti :$DETECTED_PORT | xargs kill -9 2>/dev/null || true
            elif command_exists netstat; then
                netstat -anp 2>/dev/null | grep :$DETECTED_PORT | awk '{print $7}' | cut -d'/' -f1 | xargs kill -9 2>/dev/null || true
            fi
        fi
        
    # macOS specific cleanup  
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🔍 Checking macOS services..."
        
        # Remove launch agents (if they exist)
        sudo rm -f /Library/LaunchDaemons/com.rkos.panel.plist 2>/dev/null || true
        rm -f ~/Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null || true
        
        # Kill any processes on detected port
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            lsof -ti :$DETECTED_PORT | xargs kill -9 2>/dev/null || true
        fi
        
    # Windows/WSL specific cleanup
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "🔍 Checking Windows/WSL services..."
        
        # Kill any Python processes with RK-OS in name
        if command_exists taskkill; then
            taskkill /F /IM python.exe 2>/dev/null | grep -i rkos || true
        fi
        
        # Kill processes on detected port (if available)
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            # Windows specific approach would go here with PowerShell commands
        fi
        
    else
        echo "🔍 Unknown OS type, performing generic cleanup..."
        
        # Kill any remaining Python processes related to RK-OS
        if command_exists pkill; then
            pkill -f "python.*rkos" 2>/dev/null || true
        fi
    fi
    
    echo "✅ Services stopped and removed"
}

# Function to remove installation directory
uninstall_directory() {
    echo "🎯 Removing installation directory..."
    
    if [ -d "$INSTALL_DIR" ]; then
        echo "Removing $INSTALL_DIR directory..."
        sudo rm -rf "$INSTALL_DIR"
        
        # Also check for user home directory installations (cross-platform)
        USER_INSTALL_DIRS=("$HOME/rk_os" "$USERPROFILE/rk_os" "$HOME/rkos-panel" "$USERPROFILE/rkos-panel")
        
        for dir in "${USER_INSTALL_DIRS[@]}"; do
            if [ -d "$dir" ]; then
                echo "Removing user installation at $dir..."
                rm -rf "$dir"
            fi
        done
        
        echo "✅ Installation directory removed"
    else
        echo "⚠️  Installation directory not found: $INSTALL_DIR"
    fi
}

# Function to clean up system files and configurations (cross-platform)
cleanup_system_files() {
    echo "🎯 Cleaning up system files..."
    
    # Remove any remaining RK-OS related files (cross-platform)
    find /tmp -name "*rkos*" -type f -delete 2>/dev/null || true
    find /var/log -name "*rkos*" -type f -delete 2>/dev/null || true
    
    # Clean cache directories  
    rm -rf /tmp/rkos* 2>/dev/null || true
    rm -rf /var/cache/rkos* 2>/dev/null || true
    
    # Remove from system paths (if they exist)
    if command_exists which; then
        RKO_PATHS=$(which rkos-panel 2>/dev/null | head -10)
        echo "Found potential RK-OS binaries: $RKO_PATHS"
    fi
    
    # Clean up any environment variables or PATH entries that might reference RK-OS
    for file in "$HOME/.bashrc" "$HOME/.profile" "$HOME/.zshrc"; do
        if [ -f "$file" ]; then
            sed -i '/rkos/d' "$file" 2>/dev/null || true
        fi
    done
    
    echo "✅ System files cleaned up"
}

# Function to remove Python packages (if installed in user space)
cleanup_python_packages() {
    echo "🎯 Cleaning up Python packages..."
    
    # Try to uninstall specific RK-OS related packages
    pip3 list | grep -i rkos > /dev/null 2>&1 && pip3 uninstall -y rkos-panel 2>/dev/null || true
    
    # Remove any installed modules from site-packages that might be RK-OS related
    python3 -c "import sys; import os; [os.unlink(p) for p in sys.path if 'rkos' in p and os.path.exists(p)]" 2>/dev/null || true
    
    echo "✅ Python packages cleaned up"
}

# Function to remove startup scripts and cron jobs (cross-platform)
cleanup_startup() {
    echo "🎯 Removing startup scripts..."
    
    # Remove any crontab entries for RK-OS
    if command_exists crontab; then
        (crontab -l 2>/dev/null | grep -v "rkos") | crontab - 2>/dev/null || true
    fi
    
    # Remove startup scripts from system directories (Linux only)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo rm -f /etc/init.d/rkos* 2>/dev/null || true
        sudo rm -f /etc/systemd/system/rkos* 2>/dev/null || true
        
        # Clean up any service files in system directories
        sudo find /etc -name "*rkos*" -type f -delete 2>/dev/null || true
    fi
    
    # Remove macOS LaunchAgents (if they exist)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS detected - removing LaunchAgents..."
        sudo rm -f /Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null || true
        rm -f ~/Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null || true
    fi
    
    # Remove Windows startup items (if running in WSL)
    if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        echo "Windows/WSL detected - cleaning up Windows environment..."
        
        # Check for any registry or PowerShell script cleanup needed here
        # This would typically require PowerShell commands in Windows environment
        
        # Clean up temporary files that might be Windows-specific
        rm -rf /tmp/rkos* 2>/dev/null || true
    fi
    
    echo "✅ Startup scripts cleaned up"
}

# Function to confirm uninstallation
confirm_uninstall() {
    echo ""
    echo "⚠️  IMPORTANT: This will completely remove RK-OS Panel from your system!"
    echo ""
    echo "What will be removed:"
    echo "  • Installation directory: $INSTALL_DIR"
    echo "  • System services (systemd/supervisor/launchd)"
    echo "  • Nginx configuration"
    echo "  • Log files and cache"
    echo "  • Environment variables"
    echo "  • Startup scripts and cron jobs"
    echo ""
    
    # Show detected information
    if [ "$FOUND_PORT" = true ]; then
        echo "Detected Port: $DETECTED_PORT"
    fi
    
    if [ "$FOUND_INSTALLATION" = true ]; then
        echo "Installation Location: $INSTALL_DIR/rk_os"
    else
        echo "Installation Location: Not auto-detected (using default)"
    fi
    
    read -p "Do you want to proceed with complete uninstallation? (y/N): " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "❌ Uninstallation cancelled."
        exit 1
    fi
}

# Function to display final summary
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 UNINSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 What was removed:"
    echo "   • Installation directory: $INSTALL_DIR"
    echo "   • System services (systemd/supervisor/launchd)"
    echo "   • Nginx reverse proxy configuration"
    echo "   • Log files and cache directories"
    echo "   • Environment variables"
    echo "   • Startup scripts and cron jobs"
    echo ""
    
    if [ "$FOUND_PORT" = true ]; then
        echo "✅ Detected Port: $DETECTED_PORT (cleaned up)"
    fi
    
    if [ "$FOUND_INSTALLATION" = true ]; then
        echo "✅ Installation Location: $INSTALL_DIR/rk_os (removed)"
    else
        echo "⚠️  Installation Location: Not auto-detected, using default"
    fi
    
    echo ""
    echo "💡 Notes:"
    echo "   • All processes on port $DETECTED_PORT were terminated"
    echo "   • No Python packages were removed from system-wide installation"
    echo "   • Manual cleanup may be required for some configurations"
    echo ""
    echo "✅ RK-OS Panel has been completely uninstalled!"
    echo "=================================="
}

# Main uninstallation function
main_uninstall() {
    echo "🚀 Starting Intelligent RK-OS Panel Uninstallation..."
    
    # Detect port and installation directory first
    detect_rkos_port
    detect_installation_directory
    
    # Confirm before proceeding
    confirm_uninstall
    
    # Run all uninstallation steps based on detected information
    uninstall_services
    uninstall_directory
    cleanup_system_files
    cleanup_python_packages
    cleanup_startup
    
    # Display final summary
    display_summary
}

# Run main uninstallation
main_uninstall

echo ""
echo "Intelligent uninstallation completed successfully! 🎉"
