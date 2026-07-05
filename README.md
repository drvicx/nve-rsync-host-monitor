# nve-rsync-host-monitor

Monitoring web service for rsync directory synchronization between Source and Target servers.

## Features
- REST API for receiving data from Source and Target servers
- Web interface with table view showing directory comparison
- Interactive charts for historical data visualization
- Auto-cleanup of old data
- Logging of sync events

## Installation

```bash
# Configure system user and permissions
- see "configs/sudoers.d/deployer" for example

# Connect to your server with ssh and login by configured user
- check: whoami && id $(whoami) && sudo cat /etc/sudoers.d/$(whoami)

# Goto apps directory
cd /opt/apps

# Clone repository and goin repo directory
git clone https://github.com/drvicx/nve-rsync-host-monitor.git
cd nve-rsync-host-monitor

# Execute install script
./scripts/deploy_install.sh

# Check REST Service status locally with "curl" and "jq" tools
curl -s 127.0.0.1:8010/api/status | jq '.'

# Check Service status response
{
  "status": "running",
  "status_code": 200,
  "total_records": 0,
  "last_update_s": null,
  "last_update_d": null,
  "debugMessage": "test_20260704_1",
  "serverDateTime": "2026-07-05T10:39:48.962264"
}

# Execute uninstall script
./scripts/deploy_uninstall.sh

```
