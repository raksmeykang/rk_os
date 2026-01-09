# 🖥️ RK-OS (Real Kick OS) - Comprehensive Documentation

**RK-OS (Real Kick OS)** is a comprehensive operating system control panel designed for managing and monitoring computing systems. It provides a unified interface for system administration, application management, and real-time monitoring capabilities.

### 🔍 CORE FEATURES & REQUIREMENTS
* **Compatibility:** Works on Windows, Linux, and macOS.
* **Monitoring:** Web-based Dashboard with real-time metrics and performance tracking.
* **Configuration:** Auto-start services, custom port configuration, and secure authentication.
* **Minimum Specs:** Python 3.7+, Git, 50MB Disk Space, 2GB RAM (4GB recommended).

### 🚀 INSTALLATION & SETUP

1. `git clone https://github.com/raksmeykang/rk_os.git`
2. `cd rk_os`
3. `chmod +x Install_RKOS.sh`
4. `sudo ./Install_RKOS.sh` (You will be prompted to select a custom port, default is 8085).

**Verification:** Run `python src/interfaces/cli.py status` to confirm the system is running. Expected output shows Status: Running, Version: 1.0.0, and Owner: KANG CHANDARARAKSMEY.

### 💻 USAGE & COMMANDS
* **CLI Status:** `python src/interfaces/cli.py status`
* **Run Tests:** `python src/interfaces/cli.py test`
* **Start API Manually:** `python src/interfaces/api.py --port 8085`
* **Web Access:** Open `http://localhost:8085/` in your browser.

### ⚙️ SERVICE MANAGEMENT (LINUX)
Manage the background service using systemctl:
* **Status:** `sudo systemctl status rkos-panel.service`
* **Start/Stop/Restart:** Use `start`, `stop`, or `restart` with the service name above.
* **Logs:** `sudo journalctl -u rkos-panel.service -f` or `tail -f /opt/rkos-panel/logs/*.log`.

### 🎯 PORT CUSTOMIZATION & TROUBLESHOOTING
The RK-OS Panel includes an interactive port selection during setup to avoid conflicts (e.g., avoiding 8080 or 3000). It uses Python's `argparse` to listen on your chosen port: `app.run(host='0.0.0.0', port=args.port)`. 

**Troubleshooting:**
* If the port is in use, check processes with `netstat -tulpn | grep :8085`.
* If you see "Permission Denied," ensure you used `sudo chmod +x` on the installer.
* If the service fails to start, check `systemctl status` for error logs.

---
**Author:** [KANG CHANDARARAKSMEY](https://github.com/raksmeykang) | ✅ RK-OS is ready for production use.


