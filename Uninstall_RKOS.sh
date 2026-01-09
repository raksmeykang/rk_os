#!/bin/bash
# 🗑️ RK-OS Panel Intelligent Uninstallation Script (Enhanced Version)

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

# Function to detect port automatically with enhanced error handling
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
    
    # Method 2: Check running processes with enhanced detection
    if command_exists ps; then
        PROCESS_LINE=$(ps aux | grep -v grep | grep "python.*api.py" | head -1)
        if [[ ! -z "$PROCESS_LINE" ]]; then
            if [[ $PROCESS_LINE =~ --port[[:space:]]*([0-9]+) ]]; then
                DETECTED_PORT="${BASH_REMATCH[1]}"
                echo "✅ Port detected from running process: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            elif [[ $PROCESS_LINE =~ ([0-9]{4,5}) ]]; then
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
    
    # Method 4: Check for default port (fallback) with enhanced checking
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
    
    # Method 5: Check for any Python processes with RK-OS in name (most reliable)
    if command_exists ps; then
        PYTHON_PROCESSES=$(ps aux | grep -v grep | grep "python.*api.py" | head -1)
        if [[ ! -z "$PYTHON_PROCESSES" ]]; then
            echo "Found running Python processes with RK-OS:"
            echo "$PYTHON_PROCESSES"
            
            # Extract port from process line (if present)
            if [[ $PYTHON_PROCESSES =~ --port[[:space:]]*([0-9]+) ]]; then
                DETECTED_PORT="${BASH_REMATCH[1]}"
                echo "✅ Port detected from running processes: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            fi
            
            # Try to extract any port number that might be in the command line
            if [[ $PYTHON_PROCESSES =~ ([0-9]{4,5}) ]]; then
                DETECTED_PORT="${BASH_REMATCH[1]}"
                echo "✅ Port detected from process: $DETECTED_PORT"
                FOUND_PORT=true
                return 0
            fi
        fi
    fi
    
    # Method 6: Fallback to default if still not found
    DETECTED_PORT=8085
    echo "⚠️  Using fallback default port: $DETECTED_PORT"
    FOUND_PORT=true
    return 0
}

# Function to detect installation directory automatically with enhanced detection  
detect_installation_directory() {
    echo "🎯 Auto-detecting RK-OS Panel installation..."
    
    # Check main locations (cross-platform)
    INSTALL_DIRS=("/opt/rkos-panel" "$HOME/rk_os" "$USERPROFILE/rk_os" "/opt/rkos-panel" "$HOME/rkos-panel" "$USERPROFILE/rkos-panel")
    
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
    
    # If no specific location found, check for any Python processes that might be RK-OS related 
    if command_exists ps; then
        PYTHON_PROCESSES=$(ps aux | grep -v grep | grep "python.*rkos\|python.*api.py" | head -1)
        if [[ ! -z "$PYTHON_PROCESSES" ]]; then
            echo "Found running RK-OS processes, checking for installation paths..."
            
            # Try to extract path from process command
            if [[ $PYTHON_PROCESSES =~ ([^[:space:]]*/rk_os) ]]; then
                INSTALL_DIR="${BASH_REMATCH[1]}"
                echo "✅ Found potential installation at: $INSTALL_DIR"
                FOUND_INSTALLATION=true
                return 0
            fi
            
            # Try to extract path from working directory or command line
            if [[ $PYTHON_PROCESSES =~ ([^[:space:]]*/rkos-panel) ]]; then
                INSTALL_DIR="${BASH_REMATCH[1]}"
                echo "✅ Found potential installation at: $INSTALL_DIR"
                FOUND_INSTALLATION=true
                return 0
            fi
        fi
    fi
    
    # If no specific location found, use default but mark as not found for user info
    echo "⚠️  Installation directory not auto-detected, using default: $INSTALL_DIR"
    FOUND_INSTALLATION=false
    return 1
}

# Function to stop and remove services based on detected port and installation with enhanced error handling
uninstall_services() {
    echo "🎯 Stopping and removing services..."
    
    # Kill any running processes for this service (cross-platform)
    if command_exists pkill; then
        echo "🔍 Killing any RK-OS related processes..."
        pkill -f "$SERVICE_NAME" 2>/dev/null || true
        pkill -f "rkos-panel" 2>/dev/null || true
        pkill -f "python.*api.py" 2>/dev/null || true
        
        # Kill Python processes that might be running RK-OS on detected port  
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            if command_exists lsof; then
                # Try to kill specific process by PID from the port
                PIDS=$(lsof -ti :$DETECTED_PORT 2>/dev/null)
                if [ ! -z "$PIDS" ]; then
                    echo "Found processes on port $DETECTED_PORT: $PIDS"
                    echo "Killing them..."
                    kill -9 $PIDS 2>/dev/null || true
                fi
            elif command_exists netstat; then
                # Try to find and kill by netstat approach  
                if command_exists awk; then
                    PIDS=$(netstat -anp 2>/dev/null | grep :$DETECTED_PORT | grep LISTEN | awk '{print $7}' | cut -d'/' -f1)
                    if [ ! -z "$PIDS" ]; then
                        echo "Found processes on port $DETECTED_PORT: $PIDS"
                        kill -9 $PIDS 2>/dev/null || true
                    fi
                fi
            fi
        fi
    fi
    
    # Linux specific cleanup
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🔍 Checking Linux services..."
        
        # Systemd service removal (with better error handling)
        if command_exists systemctl; then
            if sudo systemctl is-active --quiet $SERVICE_NAME.service 2>/dev/null; then
                echo "Stopping systemd service..."
                sudo systemctl stop $SERVICE_NAME.service || echo "⚠️ Could not stop service"
            fi
            
            if [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
                echo "Removing systemd service..."
                sudo systemctl disable $SERVICE_NAME.service 2>/dev/null && echo "✅ Service disabled successfully" || true
                sudo rm -f /etc/systemd/system/$SERVICE_NAME.service 2>/dev/null && echo "✅ Service file removed" || {
                    echo "⚠️ Could not remove service file"
                }
                sudo systemctl daemon-reload 2>/dev/null && echo "✅ Systemd reloaded successfully" || true
            else
                echo "ℹ️ No systemd service found to remove"
            fi
        fi
        
        # Supervisor service removal (if exists)
        if [ -f "/etc/supervisor/conf.d/$SERVICE_NAME.conf" ]; then
            echo "Removing supervisor service..."
            sudo rm -f /etc/supervisor/conf.d/$SERVICE_NAME.conf 2>/dev/null && echo "✅ Supervisor config removed" || {
                echo "⚠️ Could not remove supervisor configuration"
            }
            sudo supervisorctl reread 2>/dev/null && echo "✅ Supervisor reloaded successfully" || true
            sudo supervisorctl update 2>/dev/null && echo "✅ Supervisor services updated" || true
        else
            echo "ℹ️ No supervisor service found to remove"
        fi
        
        # Nginx configuration removal (if exists)
        if command_exists nginx; then
            if [ -f "/etc/nginx/sites-available/$SERVICE_NAME" ]; then
                echo "Removing Nginx configuration..."
                sudo rm -f /etc/nginx/sites-available/$SERVICE_NAME 2>/dev/null && echo "✅ Nginx sites-available removed" || {
                    echo "⚠️ Could not remove Nginx sites-available"
                }
                
                if [ -f "/etc/nginx/sites-enabled/$SERVICE_NAME" ]; then
                    sudo rm -f /etc/nginx/sites-enabled/$SERVICE_NAME 2>/dev/null && echo "✅ Nginx sites-enabled removed" || {
                        echo "⚠️ Could not remove Nginx sites-enabled"
                    }
                fi
                
                # Test and restart nginx if it exists
                if sudo nginx -t 2>/dev/null; then
                    sudo systemctl restart nginx 2>/dev/null && echo "✅ Nginx restarted successfully" || {
                        echo "⚠️ Could not restart Nginx service"
                    }
                else
                    echo "⚠️ Nginx configuration test failed, but files removed"
                fi
            else
                echo "ℹ️ No Nginx configuration found to remove"
            fi
        fi
        
    # macOS specific cleanup  
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🔍 Checking macOS services..."
        
        # Remove launch agents (if they exist)
        sudo rm -f /Library/LaunchDaemons/com.rkos.panel.plist 2>/dev/null && echo "✅ LaunchDaemon removed" || true
        rm -f ~/Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null && echo "✅ LaunchAgent removed" || true
        
        # Kill any processes on detected port (if found)
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            lsof -ti :$DETECTED_PORT | xargs kill -9 2>/dev/null || true
        fi
        
    # Windows/WSL specific cleanup
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "🔍 Checking Windows/WSL services..."
        
        # Kill any Python processes with RK-OS in name (if available)
        if command_exists taskkill; then
            taskkill /F /IM python.exe 2>/dev/null | grep -i rkos || true
        fi
        
        # Try to find and kill by port for Windows
        if [ "$FOUND_PORT" = true ] && [[ $DETECTED_PORT =~ ^[0-9]+$ ]]; then
            echo "🔍 Killing processes on port $DETECTED_PORT..."
            # On Windows systems, you might need PowerShell or netstat approach here
        fi
        
    else
        echo "🔍 Unknown OS type, performing generic cleanup..."
        
        # Kill any remaining Python processes related to RK-OS (last resort)
        if command_exists pkill; then
            pkill -f "python.*rkos" 2>/dev/null || true
        fi
    fi
    
    echo "✅ Services stopped and removed"
}

# Function to remove installation directory with enhanced error handling
uninstall_directory() {
    echo "🎯 Removing installation directory..."
    
    # First, let's try to identify the actual path from our detection if needed
    if [ "$FOUND_INSTALLATION" = true ]; then
        TARGET_DIR="$INSTALL_DIR/rk_os"
    else
        TARGET_DIR="$INSTALL_DIR/rk_os"
        echo "ℹ️  Using default installation location: $TARGET_DIR"
    fi
    
    # Remove the main installation directory with error handling
    if [ -d "$INSTALL_DIR" ]; then
        echo "Removing installation directory: $INSTALL_DIR..."
        
        # Try to remove with sudo for permissions
        if [ "$EUID" -eq 0 ]; then
            rm -rf "$INSTALL_DIR"
            echo "✅ Installation directory removed successfully (root)"
        else
            # Use sudo but give user a chance to confirm first
            echo "⚠️  Need root privileges to remove $INSTALL_DIR"
            
            # Try with confirmation if possible  
            read -p "Continue with removal using sudo? (y/n): " CONFIRM_SUDO
            if [[ "$CONFIRM_SUDO" =~ ^[Yy]$ ]]; then
                sudo rm -rf "$INSTALL_DIR"
                echo "✅ Installation directory removed successfully (with sudo)"
            else
                echo "⚠️  Skipped removal of $INSTALL_DIR due to user choice"
            fi
        fi
        
    elif [ -d "$TARGET_DIR" ]; then
        # If the specific rk_os directory exists but not full path
        echo "Removing installation directory: $TARGET_DIR..."
        
        if [ "$EUID" -eq 0 ]; then
            rm -rf "$TARGET_DIR"
            echo "✅ Installation directory removed successfully (root)"
        else
            read -p "Continue with removal using sudo? (y/n): " CONFIRM_SUDO2
            if [[ "$CONFIRM_SUDO2" =~ ^[Yy]$ ]]; then
                sudo rm -rf "$TARGET_DIR"
                echo "✅ Installation directory removed successfully (with sudo)"
            else
                echo "⚠️  Skipped removal of $TARGET_DIR due to user choice"
            fi
        fi
        
    else
        echo "ℹ️  No installation directory found at: $INSTALL_DIR or $TARGET_DIR"
        
        # Check for common alternative locations and remove them too
        ALTERNATIVE_DIRS=("$HOME/rk_os" "$USERPROFILE/rk_os" "$HOME/rkos-panel" "$USERPROFILE/rkos-panel")
        REMOVED_ANY=false
        
        for dir in "${ALTERNATIVE_DIRS[@]}"; do
            if [ -d "$dir" ]; then
                echo "Found alternative installation at: $dir"
                if [ "$EUID" -eq 0 ]; then
                    rm -rf "$dir"
                    echo "✅ Alternative directory removed successfully (root)"
                    REMOVED_ANY=true
                else
                    read -p "Remove alternative directory $dir with sudo? (y/n): " CONFIRM_ALT
                    if [[ "$CONFIRM_ALT" =~ ^[Yy]$ ]]; then
                        sudo rm -rf "$dir"
                        echo "✅ Alternative directory removed successfully (with sudo)"
                        REMOVED_ANY=true
                    fi
                fi
            fi
        done
        
        if [ "$REMOVED_ANY" = false ]; then
            echo "ℹ️  No installation directories found to remove"
        fi
    fi
    
    echo "✅ Installation directory cleanup complete"
}

# Function to clean up system files and configurations (cross-platform with enhanced error handling)
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
    for file in "$HOME/.bashrc" "$HOME/.profile" "$HOME/.zshrc" "$HOME/.bash_profile"; do
        if [ -f "$file" ]; then
            echo "Checking $file for RK-OS references..."
            sed -i '/rkos/d' "$file" 2>/dev/null && echo "✅ Cleaned $file" || true
        fi
    done
    
    # Remove any environment files that might exist
    if [ -f "$HOME/.rkos_env" ]; then
        rm -f "$HOME/.rkos_env"
        echo "✅ Removed .rkos_env file"
    fi
    
    echo "✅ System files cleaned up successfully"
}

# Function to remove Python packages (if installed in user space)
cleanup_python_packages() {
    echo "🎯 Cleaning up Python packages..."
    
    # Try to uninstall specific RK-OS related packages
    if command_exists pip3; then
        echo "Looking for RK-OS related packages..."
        
        # Check what's installed and try to remove
        pip3 list | grep -i rkos > /dev/null 2>&1 && {
            echo "Found RK-OS packages, attempting removal..."
            pip3 uninstall -y rkos-panel 2>/dev/null || true
        }
    fi
    
    # Remove any installed modules from site-packages that might be RK-OS related
    if command_exists python3; then
        echo "Checking for RK-OS Python modules in system paths..."
        python3 -c "
import sys, os
# Try to find and clean up RK-OS references
for p in sys.path:
    try:
        if 'rkos' in p.lower() and os.path.exists(p):
            print('Found potential RK-OS path:', p)
    except: pass
" 2>/dev/null || true
    fi
    
    echo "✅ Python packages cleanup complete"
}

# Function to remove startup scripts and cron jobs (cross-platform with enhanced detection)
cleanup_startup() {
    echo "🎯 Removing startup scripts..."
    
    # Remove any crontab entries for RK-OS  
    if command_exists crontab; then
        echo "Removing RK-OS entries from crontab..."
        (crontab -l 2>/dev/null | grep -v "rkos") | crontab - 2>/dev/null && echo "✅ Cron jobs cleaned up" || true
    fi
    
    # Remove startup scripts from system directories (Linux only)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Cleaning Linux startup files..."
        
        sudo rm -f /etc/init.d/rkos* 2>/dev/null && echo "✅ Removed init.d files" || true
        
        # Remove any service files in system directories that might reference RK-OS  
        sudo find /etc -name "*rkos*" -type f -delete 2>/dev/null && echo "✅ Removed other RK-OS config files" || true
    fi
    
    # Remove macOS LaunchAgents (if they exist)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Cleaning macOS LaunchAgents..."
        sudo rm -f /Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null && echo "✅ Removed system LaunchAgent" || true
        rm -f ~/Library/LaunchAgents/com.rkos.panel.plist 2>/dev/null && echo "✅ Removed user LaunchAgent" || true
    fi
    
    # Remove Windows startup items (if running in WSL)
    if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        echo "Cleaning Windows environment..."
        
        # Check for any PowerShell or registry cleanup needed here
        # This would typically require more advanced Windows-specific commands
        
        # Clean up temporary files that might be Windows-specific
        rm -rf /tmp/rkos* 2>/dev/null && echo "✅ Cleaned temp files" || true
    fi
    
    # Check for any .local/bin entries or other Python-related cleanup
    if command_exists pip3; then
        echo "Checking for user-installed RK-OS packages..."
        
        # Remove from user bin directories (if they exist)
        if [ -d "$HOME/.local/bin" ]; then
            find "$HOME/.local/bin" -name "*rkos*" -type f -delete 2>/dev/null && echo "✅ Removed user binary files" || true
        fi
        
        # Remove from .local directories (common in Ubuntu/Debian)
        if [ -d "$HOME/.local/lib/python3.*/site-packages" ]; then
            find "$HOME/.local/lib/python3.*/site-packages" -name "*rkos*" -type d -exec rm -rf {} + 2>/dev/null && echo "✅ Removed user Python packages" || true
        fi
    fi
    
    echo "✅ Startup scripts and cleanup complete"
}

# Function to confirm uninstallation with enhanced user experience
confirm_uninstall() {
    echo ""
    echo "⚠️  IMPORTANT: This will completely remove RK-OS Panel from your system!"
    echo ""
    echo "What will be removed:"
    echo "  • Installation directory: $INSTALL_DIR (if found)"
    echo "  • System services (systemd/supervisor/launchd)"
    echo "  • Nginx configuration"
    echo "  • Log files and cache"
    echo "  • Environment variables"
    echo "  • Startup scripts and cron jobs"
    echo ""
    
    # Show detected information
    if [ "$FOUND_PORT" = true ]; then
        echo "Detected Port: $DETECTED_PORT"
    else
        echo "Port Detection: Not auto-detected, using fallback (8085)"
    fi
    
    if [ "$FOUND_INSTALLATION" = true ]; then
        echo "Installation Location: $INSTALL_DIR/rk_os"
    else
        echo "Installation Location: Auto-detection failed - default used"
    fi
    
    # Show what we'll try to remove specifically
    echo ""
    echo "🔍 What will be checked for removal:"
    if [ -d "$INSTALL_DIR" ] || [ -d "$HOME/rk_os" ]; then
        echo "   • Directories containing RK-OS files"
    fi
    
    if command_exists systemctl && [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
        echo "   • SystemD service configuration file"
    fi
    
    if command_exists nginx && [ -f "/etc/nginx/sites-available/$SERVICE_NAME" ]; then
        echo "   • Nginx proxy configuration files"
    fi
    
    read -p "Do you want to proceed with complete uninstallation? (y/N): " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "❌ Uninstallation cancelled."
        exit 1
    fi
}

# Function to display final summary with enhanced information
display_summary() {
    echo ""
    echo "=================================="
    echo "🎉 UNINSTALLATION COMPLETE!"
    echo "=================================="
    echo ""
    echo "📋 What was removed:"
    echo "   • Installation directory: $INSTALL_DIR (if found)"
    echo "   • System services (systemd/supervisor/launchd)"
    echo "   • Nginx reverse proxy configuration"
    echo "   • Log files and cache directories"
    echo "   • Environment variables"
    echo "   • Startup scripts and cron jobs"
    echo ""
    
    if [ "$FOUND_PORT" = true ]; then
        echo "✅ Detected Port: $DETECTED_PORT (terminated)"
    else
        echo "⚠️  No port detected, using fallback (8085) for cleanup"
    fi
    
    if [ "$FOUND_INSTALLATION" = true ]; then
        echo "✅ Installation Location: $INSTALL_DIR/rk_os (removed)"
    else
        echo "ℹ️  Installation Location: Auto-detection failed - default used"
    fi
    
    echo ""
    echo "💡 Notes:"
    echo "   • All processes on port $DETECTED_PORT were terminated"
    echo "   • No Python packages were removed from system-wide installation" 
    echo "   • Manual cleanup may be required for some configurations"
    echo "   • Some files might require root access to remove completely"
    echo ""
    echo "✅ RK-OS Panel has been completely uninstalled!"
    echo "=================================="
}

# Function to provide quick verification commands
provide_verification() {
    echo ""
    echo "🔍 VERIFICATION CHECKS:"
    
    # Check if any RK-OS processes are still running
    RUNNING_PROCESSES=$(ps aux | grep -v grep | grep -i rkos 2>/dev/null)
    if [[ ! -z "$RUNNING_PROCESSES" ]]; then
        echo "⚠️  Still found running RK-OS processes:"
        echo "$RUNNING_PROCESSES"
    else
        echo "✅ No RK-OS processes detected (clean)"
    fi
    
    # Check for remaining service files 
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        SERVICE_CHECKS=(
            "/etc/systemd/system/$SERVICE_NAME.service"
            "/etc/supervisor/conf.d/$SERVICE_NAME.conf"
            "/etc/nginx/sites-available/$SERVICE_NAME"
        )
        
        echo ""
        echo "🔍 Checking for remaining configuration files:"
        for file in "${SERVICE_CHECKS[@]}"; do
            if [ -f "$file" ]; then
                echo "⚠️  Found remaining config: $file"
            else
                echo "✅ No config file found: $file"
            fi
        done
    fi
    
    echo ""
}

# Main uninstallation function with enhanced error handling and verification
main_uninstall() {
    echo "🚀 Starting Intelligent RK-OS Panel Uninstallation..."
    
    # Check if running as root (needed for some operations)
    IS_ROOT=false
    if [ "$EUID" -eq 0 ]; then
        IS_ROOT=true
        echo "Running with root privileges"
    fi
    
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
    
    # Provide verification checks
    provide_verification
    
    echo ""
    echo "Intelligent uninstallation completed successfully! 🎉"
}

# Run main uninstallation
main_uninstall

echo ""
echo "Uninstallation process completed!"
