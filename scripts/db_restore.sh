#!/bin/bash
# db_restore.sh - Restore SQLite DB from archive

# ============================================
# Settings
# ============================================
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_PATH="$PROJECT_DIR/data/monitor.db"
BACKUP_DIR="$PROJECT_DIR/data/backups"
LOG_FILE="$PROJECT_DIR/logs/db_restore.log"

# ============================================
# Functions
# ============================================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

show_help() {
    cat << EOF
Using: $0 [options]

Options:
  --archive=FILE    Restore DB from selected archive file
  --list            Show available archives list
  --help            Show this help

If archive file not set, restore DB from latest available archive file

Examples:
  $0                                             # Restore DB from latest archive
  $0 --archive=monitorDB_20260703_155040.tar.gz  # Restore DB from selected archive
  $0 --list                                      # Show all available archives
EOF
}

# ============================================
# Parse arguments
# ============================================
ARCHIVE=""
LIST_ONLY=false

for arg in "$@"; do
    case $arg in
        --archive=*)
            ARCHIVE="${arg#*=}"
            ;;
        --list)
            LIST_ONLY=true
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "❌ Unknown argument: $arg"
            echo "Use --help for command description"
            exit 1
            ;;
    esac
done

# ============================================
# Main logic
# ============================================

# 1. Check is backup directory is exists
if [ ! -d "$BACKUP_DIR" ]; then
    log "ERROR: Backup directory NOT found: $BACKUP_DIR"
    exit 1
fi

# 2. If --list argument is used, show archives list and exit
if [ "$LIST_ONLY" = true ]; then
    echo "=== Available archives ==="
    echo ""
    cd "$BACKUP_DIR"
    ls -lh monitorDB_*.tar.gz 2>/dev/null || echo "  (no archives)"
    echo ""
    exit 0
fi

# 3. Define archive for restore
cd "$BACKUP_DIR"

if [ -z "$ARCHIVE" ]; then
    # If archive file not set, use latest by datetime in timestamp
    ARCHIVE=$(ls -t monitorDB_*.tar.gz 2>/dev/null | head -1)
    if [ -z "$ARCHIVE" ]; then
        log "ERROR: No available archives in $BACKUP_DIR"
        exit 1
    fi
    log "Archive not set. Using latest from list: $ARCHIVE"
else
    # Check, is selected archive available
    if [ ! -f "$ARCHIVE" ]; then
        log "ERROR: Selected archive not found: $ARCHIVE"
        echo ""
        echo "Available archives:"
        ls -lh monitorDB_*.tar.gz 2>/dev/null || echo "  (нет архивов)"
        exit 1
    fi
fi

# 4. Check archive integrity
log "Checking archive integrity: $ARCHIVE"
if ! tar -tzf "$ARCHIVE" >/dev/null 2>&1; then
    log "ERROR: Archive broken or not tar.gz"
    exit 1
fi

# 5. Create additional backup from current database (just in case)
if [ -f "$DB_PATH" ]; then
    CURRENT_BACKUP="monitorDB_before_restore_$(date +"%Y%m%d_%H%M%S").db"
    log "Creating backup from current database: $CURRENT_BACKUP"
    cp "$DB_PATH" "$BACKUP_DIR/$CURRENT_BACKUP"
fi

# 6. Restore database from archive file
log "Restoring database file from archive: $ARCHIVE"

# Get db file name from inside archive (for ex: monitor_YYYYMMDD_HHMMSS.db)
TEMP_DIR=$(mktemp -d)
tar -xzf "$ARCHIVE" -C "$TEMP_DIR"

# Locate extracted .db file
EXTRACTED_DB=$(find "$TEMP_DIR" -name "*.db" -type f | head -1)

if [ -z "$EXTRACTED_DB" ] || [ ! -f "$EXTRACTED_DB" ]; then
    log "ERROR: No .db file in archive found!"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 7. Stop monitor service (if running)
if systemctl is-active --quiet nve-rsync-monitor-prod 2>/dev/null; then
    log "Stopping monitoring service..."
    sudo systemctl stop nve-rsync-monitor-prod
    SERVICE_STOPPED=true
else
    SERVICE_STOPPED=false
fi

# 8. Restore database
log "Restoring database..."
cp "$EXTRACTED_DB" "$DB_PATH"

# Check is database restored
if [ -f "$DB_PATH" ]; then
    DB_SIZE=$(du -h "$DB_PATH" | cut -f1)
    log "✅ Database restored SUCCESSFULLY: $DB_PATH (size: $DB_SIZE)"
else
    log "❌ ERROR restoring database!"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 9. Check restored database integrity
log "Checking database integrity..."
if sqlite3 "$DB_PATH" "PRAGMA integrity_check;" | grep -q "ok"; then
    log "✅ Integrity check complete SUCCESSFULLY"
else
    log "⚠️ WARN: Integrity check FAILED!"
fi

# 10. Start monitoring service (if stopped)
if [ "$SERVICE_STOPPED" = true ]; then
    log "Starting monitoring service..."
    sudo systemctl start nve-rsync-monitor-prod
    sudo systemctl status nve-rsync-monitor-prod --no-pager || true
fi

# 11. Clearing
rm -rf "$TEMP_DIR"

# 12. Print final message
echo ""
echo "============================================"
echo "✅ Restore COMPLETE!"
echo "============================================"
echo "📦 Archive.: $ARCHIVE"
echo "📁 Database: $DB_PATH"
echo "📊 Size....: $DB_SIZE"
echo ""
echo "Check database data:"
echo "  sqlite3 $DB_PATH 'SELECT COUNT(*) FROM directory_stats;'"
echo ""
if [ "$SERVICE_STOPPED" = true ]; then
    echo "Service restarted. Check it:"
    echo "  sudo systemctl status nve-rsync-monitor-prod"
    echo "  curl http://localhost:8010/api/status"
fi
echo "============================================"

log "✅ Restore complete from archive file: $ARCHIVE"
exit 0
