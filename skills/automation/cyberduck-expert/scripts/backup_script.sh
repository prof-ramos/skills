#!/bin/bash
#
# CyberDuck/Duck CLI Backup Script
# Automated backup to remote storage with rotation and logging
#
# Usage: ./backup_script.sh [config-file]
#

set -euo pipefail

# Default configuration
BACKUP_NAME="${BACKUP_NAME:-backup}"
SOURCE_DIR="${SOURCE_DIR:-/data}"
REMOTE_URL="${REMOTE_URL:-s3://my-backup-bucket/backups/}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
LOG_DIR="${LOG_DIR:-/var/log/backups}"
COMPRESSION="${COMPRESSION:-true}"
STORAGE_CLASS="${STORAGE_CLASS:-STANDARD_IA}"
PARALLEL="${PARALLEL:-5}"
THROTTLE="${THROTTLE:-0}"  # 0 = no limit, otherwise bytes/sec

# Load custom config if provided
if [ $# -ge 1 ] && [ -f "$1" ]; then
    # shellcheck source=/dev/null
    source "$1"
fi

# Create log directory
mkdir -p "$LOG_DIR"

# Generate timestamp and log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_DIR=$(date +%Y%m%d)
LOG_FILE="$LOG_DIR/backup_${TIMESTAMP}.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check if duck is installed
if ! command -v duck &> /dev/null; then
    error_exit "duck CLI not found. Install from https://duck.sh/"
fi

log "=== Backup Started ==="
log "Source: $SOURCE_DIR"
log "Destination: $REMOTE_URL"
log "Date: $DATE_DIR"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    error_exit "Source directory not found: $SOURCE_DIR"
fi

# Build remote path with date
REMOTE_PATH="${REMOTE_URL%/}/${DATE_DIR}/"

# Build duck command
DUCK_CMD=(
    duck
    --upload "$REMOTE_PATH" "$SOURCE_DIR"
    --verbose
    --parallel "$PARALLEL"
    --retry 3
    --retry-delay 5
    --preserve
)

# Add storage class for S3
if [[ $REMOTE_URL == s3://* ]]; then
    DUCK_CMD+=(--storage-class "$STORAGE_CLASS")
fi

# Add throttle if specified
if [ "$THROTTLE" -gt 0 ]; then
    DUCK_CMD+=(--throttle "$THROTTLE")
    log "Bandwidth limit: $THROTTLE bytes/sec"
fi

cutoff_date() {
    if date -v-"$RETENTION_DAYS"d +%Y%m%d >/dev/null 2>&1; then
        date -v-"$RETENTION_DAYS"d +%Y%m%d
    else
        date -d "$RETENTION_DAYS days ago" +%Y%m%d
    fi
}

# Compression (create tar.gz first if enabled)
if [ "$COMPRESSION" = true ]; then
    log "Creating compressed archive..."
    ARCHIVE_NAME="${BACKUP_NAME}_${TIMESTAMP}.tar.gz"
    TEMP_ARCHIVE="/tmp/$ARCHIVE_NAME"
    
    tar -czf "$TEMP_ARCHIVE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        log "Archive created: $TEMP_ARCHIVE"
        log "Archive size: $(du -h "$TEMP_ARCHIVE" | cut -f1)"
        
        # Upload archive
        log "Uploading archive..."
        REMOTE_ARCHIVE="${REMOTE_PATH%/}/$ARCHIVE_NAME"

        ARCHIVE_UPLOAD_CMD=(
            duck
            --upload "$REMOTE_ARCHIVE" "$TEMP_ARCHIVE"
            --verbose
            --retry 3
            --retry-delay 5
        )
        if [ "$THROTTLE" -gt 0 ]; then
            ARCHIVE_UPLOAD_CMD+=(--throttle "$THROTTLE")
        fi
        if [[ $REMOTE_URL == s3://* ]]; then
            ARCHIVE_UPLOAD_CMD+=(--storage-class "$STORAGE_CLASS")
        fi

        "${ARCHIVE_UPLOAD_CMD[@]}" 2>&1 | tee -a "$LOG_FILE"
        
        UPLOAD_STATUS=${PIPESTATUS[0]}
        
        # Clean up temp archive
        rm -f "$TEMP_ARCHIVE"
        log "Temporary archive removed"
    else
        error_exit "Failed to create archive"
    fi
else
    # Direct upload without compression
    log "Uploading files..."
    "${DUCK_CMD[@]}" 2>&1 | tee -a "$LOG_FILE"
    UPLOAD_STATUS=${PIPESTATUS[0]}
fi

# Check upload status
if [ $UPLOAD_STATUS -eq 0 ]; then
    log "Upload completed successfully"
else
    error_exit "Upload failed with exit code $UPLOAD_STATUS"
fi

# Backup rotation - delete old backups
if [ "$RETENTION_DAYS" -gt 0 ]; then
    log "Cleaning up backups older than $RETENTION_DAYS days..."
    
    # Calculate cutoff date
    CUTOFF_DATE=$(cutoff_date)
    
    # List all backup directories
    log "Listing remote backups..."
    REMOTE_LIST=$(duck --list "${REMOTE_URL}" --json 2>> "$LOG_FILE")
    
    if [ $? -eq 0 ]; then
        # Parse JSON and delete old backups
        echo "$REMOTE_LIST" | jq -r '.[] | select(.type == "directory") | .path' | while read -r backup_dir; do
            # Extract date from path (assumes format YYYYMMDD)
            backup_date=$(basename "$backup_dir" | grep -oE '[0-9]{8}' || echo "")
            
            if [ -n "$backup_date" ] && [ "$backup_date" -lt "$CUTOFF_DATE" ]; then
                log "Deleting old backup: $backup_dir (date: $backup_date)"
                duck --delete "${REMOTE_URL%/}/$backup_dir" --recursive 2>&1 | tee -a "$LOG_FILE"
                
                if [ $? -eq 0 ]; then
                    log "Deleted: $backup_dir"
                else
                    log "WARNING: Failed to delete $backup_dir"
                fi
            fi
        done
    else
        log "WARNING: Could not list remote backups for cleanup"
    fi
fi

# Calculate backup statistics
log "=== Backup Statistics ==="
log "Start time: $(head -n1 "$LOG_FILE" | cut -d']' -f1 | tr -d '[')"
log "End time: $(date '+%Y-%m-%d %H:%M:%S')"

if [ "$COMPRESSION" = true ]; then
    log "Backup type: Compressed archive"
else
    log "Backup type: Direct file upload"
fi

# Verify backup
log "Verifying backup..."
VERIFY_OUTPUT=$(duck --list "$REMOTE_PATH" 2>> "$LOG_FILE")
if [ $? -eq 0 ]; then
    log "Backup verified successfully"
    log "Remote location: $REMOTE_PATH"
else
    log "WARNING: Could not verify backup"
fi

log "=== Backup Completed Successfully ==="

# Optional: Send notification (email, webhook, etc.)
# Uncomment and configure as needed
# send_notification "Backup completed: $BACKUP_NAME"

exit 0
