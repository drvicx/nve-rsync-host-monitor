#!/bin/bash

set -e

echo "============================================"
echo "Removing RSync Monitoring Service (prod)..  "
echo "============================================"

# Set Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_NAME="nve-rsync-monitor-prod"
SERVICE_NAME_CFG="nve-rsync-monitor-prod.service"

cd "$PROJECT_DIR"

# Stop & Remove Service
sudo systemctl stop $SERVICE_NAME
sudo systemctl reset-failed $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo rm /etc/systemd/system/$SERVICE_NAME_CFG
sudo systemctl daemon-reload

# Deactivate Pyton venv
#deactivate

# Remove Project files
cd ..
rm -rf $PROJECT_DIR

# Check Project Directory
ls -1X /opt/apps

# Print Final Message
echo "============================================"
echo "DONE!"
echo "============================================"
