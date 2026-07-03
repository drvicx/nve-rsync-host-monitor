#!/bin/bash

set -e

echo "============================================"
echo "Installing RSync Monitoring Service (prod).."
echo "============================================"

# Set Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_NAME="nve-rsync-monitor-prod"
SERVICE_NAME_CFG="nve-rsync-monitor-prod.service"

cd "$PROJECT_DIR"

#echo "0. Installing System Packages..."
sudo apt update
sudo apt install -y sqlite3
sqlite3 --version

echo "1. Creating Python Virtual Environment (venv)..."
python3 -m venv venv

echo "2. Activating venv..."
source venv/bin/activate

echo "3. Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "4. Creating necessary directories.."
mkdir -p data logs

echo "5. Setting execution flag to scripts..."
chmod +x scripts/run.sh

echo "6. Configuring and Starting app as systemd service..."
# Copy service configuration file to systemd directory
sudo cp configs/systemd/$SERVICE_NAME_CFG /etc/systemd/system/
sudo systemctl daemon-reload
# Enable and Start python app as a system service
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "============================================"
echo "Install complete!"
echo "To launch the application, run the following commands:"
echo "  sudo systemctl enable $SERVICE_NAME"
echo "  sudo systemctl start $SERVICE_NAME"
echo ""
echo "Or execute startup script manually:"
echo "  ./scripts/run.sh"
echo "============================================"
