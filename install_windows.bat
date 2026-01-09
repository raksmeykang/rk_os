@echo off
REM RK-OS Panel Installation Script for Windows

echo.
echo 🚀 Installing RK-OS Panel on Windows...
echo.

cd /d %USERPROFILE%

REM Create project directory
echo Creating project directory...
mkdir rk_os_project
cd rk_os_project

REM Clone repository
echo Cloning RK-OS Panel repository...
git clone https://github.com/raksmeykang/rk_os.git
cd rk_os

REM Install Python dependencies
echo Installing Python dependencies...
pip install flask psutil requests

REM Test installation
echo Testing installation...
python src/interfaces/cli.py status

echo.
echo ✅ RK-OS Panel installed successfully on Windows!
echo 💡 Run: python src/interfaces/cli.py status to test
echo.

pause
