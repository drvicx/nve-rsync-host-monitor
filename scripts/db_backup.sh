#!/bin/bash
# backupDB.sh - SQLite Backup script used .backup mode
#               please install "sqlite3" with "sudo apt install -y sqlite3"

PROJECT_DIR="/opt/apps/nve-rsync-host-monitor"
DB_PATH="$PROJECT_DIR/data/monitor.db"
BACKUP_DIR="$PROJECT_DIR/data/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="monitorDB_${TIMESTAMP}.tar.gz"
LOG_FILE="$PROJECT_DIR/logs/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check DB file
if [ ! -f "$DB_PATH" ]; then
    log "ERROR: Database file NOT found!"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

log "Backup started..."

# Create a temp DB copy using .backup (ensures integrity)
TEMP_DB="$BACKUP_DIR/monitor_${TIMESTAMP}.db"
sqlite3 "$DB_PATH" ".backup '$TEMP_DB'"

if [ -f "$TEMP_DB" ]; then
    # Archive temp DB file
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$BACKUP_DIR" "$(basename "$TEMP_DB")"
    rm -f "$TEMP_DB"
    
    log "✅ Backup created: $BACKUP_NAME"
else
    log "❌ Error creating backup"
    exit 1
fi

# Remove old backup files (keep last 10 files)
cd "$BACKUP_DIR"
ls -t monitorDB_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f

log "✅ DONE. The latest 10 backup files have been kept"
