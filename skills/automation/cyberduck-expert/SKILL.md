---
name: cyberduck-expert
description: Expert guidance for CyberDuck and duck CLI for file transfer operations. Use this skill when working with FTP, SFTP, S3, Google Drive, Dropbox, Azure, or other cloud storage protocols. Handles upload, download, synchronization, and management of remote files and directories using both the GUI application and command-line interface.
---

# CyberDuck Expert

## Overview

Provide expert assistance with CyberDuck (GUI) and duck CLI for file transfer and cloud storage operations. Cover all major protocols (FTP, SFTP, S3, WebDAV, Google Drive, Dropbox, Azure, Backblaze B2) and operations (upload, download, sync, list, delete, permissions).

## When to Use This Skill

Trigger this skill when the user needs to:
- Transfer files to/from remote servers or cloud storage
- Work with FTP, SFTP, FTPS, or WebDAV protocols
- Manage S3, Google Cloud Storage, Azure Blob, or Backblaze B2 buckets
- Synchronize local and remote directories
- Automate file transfer operations via CLI
- Configure connection profiles or bookmarks
- Handle batch operations on remote files
- Work with CDN configurations (CloudFront, Akamai, Fastly)

## Core Concepts

### Duck CLI vs CyberDuck GUI

**duck CLI**: Command-line interface for automation and scripting. Installed via:
- macOS: `brew install duck`
- Windows: Download from https://duck.sh/
- Linux: Download from https://duck.sh/

**CyberDuck GUI**: Desktop application for interactive file management. Download from https://cyberduck.io/

### Connection URL Format

Duck CLI uses URL-based connections with the format:
```
protocol://username:password@hostname/path
```

Examples:
- FTP: `ftp://user:pass@ftp.example.com/remote/path`
- SFTP: `sftp://user@example.com/home/user/files`
- S3: `s3://bucket-name/prefix/`
- Google Drive: `googledrive://user@gmail.com/folder-id`

### Authentication Methods

1. **Password in URL**: `protocol://user:pass@host/path`
2. **SSH Key**: `sftp://user@host/path` (uses ~/.ssh/id_rsa by default)
3. **AWS Credentials**: Uses `~/.aws/credentials` for S3
4. **OAuth**: Required for Google Drive, Dropbox, OneDrive
5. **Bookmark/Profile**: `--username profile-name`

## Common Operations

### Upload Files

Upload single file:
```bash
duck --upload protocol://host/remote/path /local/file.txt
```

Upload directory recursively:
```bash
duck --upload protocol://host/remote/path/ /local/directory/
```

Upload with specific permissions:
```bash
duck --upload protocol://host/remote/path /local/file.txt --permissions 644
```

### Download Files

Download single file:
```bash
duck --download protocol://host/remote/file.txt /local/destination/
```

Download directory recursively:
```bash
duck --download protocol://host/remote/directory/ /local/destination/
```

### Synchronization

Sync local to remote (mirror mode):
```bash
duck --synchronize protocol://host/remote/path/ /local/directory/
```

Sync with delete (exact mirror):
```bash
duck --synchronize protocol://host/remote/path/ /local/directory/ --delete
```

### List and Browse

List directory contents:
```bash
duck --list protocol://host/remote/path/
```

List with long format (permissions, size, date):
```bash
duck --list protocol://host/remote/path/ --long
```

### Delete Operations

Delete single file:
```bash
duck --delete protocol://host/remote/file.txt
```

Delete directory recursively:
```bash
duck --delete protocol://host/remote/directory/
```

### Create Directories

```bash
duck --mkdir protocol://host/remote/new-directory/
```

### Copy and Move

Copy within same protocol:
```bash
duck --copy protocol://host/source/file.txt protocol://host/destination/
```

Move/rename:
```bash
duck --move protocol://host/old-name.txt protocol://host/new-name.txt
```

## Protocol-Specific Guidance

### S3 and S3-Compatible Storage

S3 bucket URL format:
```bash
s3://bucket-name/prefix/path/
```

Set storage class:
```bash
duck --upload s3://bucket/path/ /local/file --storage-class STANDARD_IA
```

Enable server-side encryption:
```bash
duck --upload s3://bucket/path/ /local/file --encryption AES256
```

Set ACL:
```bash
duck --upload s3://bucket/path/ /local/file --acl public-read
```

Invalidate CloudFront distribution:
```bash
duck --invalidate s3://bucket/path/file.txt --distribution-id E1234567890ABC
```

### SFTP/SSH

Use specific SSH key:
```bash
duck --upload sftp://user@host/path/ /local/file -i ~/.ssh/custom_key
```

Specify port:
```bash
duck --upload sftp://user@host:2222/path/ /local/file
```

### FTP/FTPS

Explicit TLS (FTPS):
```bash
duck --upload ftps://user:pass@host/path/ /local/file
```

Passive mode (default):
```bash
duck --upload ftp://user:pass@host/path/ /local/file
```

Active mode:
```bash
duck --upload ftp://user:pass@host/path/ /local/file --active
```

### Google Drive

First-time OAuth (opens browser):
```bash
duck --list googledrive://user@gmail.com/
```

Specify folder by ID:
```bash
duck --upload googledrive://user@gmail.com/1a2b3c4d5e6f/ /local/file
```

### Azure Blob Storage

```bash
duck --upload azure://account.blob.core.windows.net/container/path/ /local/file
```

### Backblaze B2

```bash
duck --upload b2://bucket-name/path/ /local/file
```

## Advanced Options

### Bandwidth Throttling

Limit upload speed to 1 MB/s:
```bash
duck --upload protocol://host/path/ /local/file --throttle 1048576
```

### Resume Transfers

Enable resume for interrupted transfers:
```bash
duck --upload protocol://host/path/ /local/file --resume
```

### Parallel Transfers

Set number of parallel connections:
```bash
duck --upload protocol://host/path/ /local/directory/ --parallel 5
```

### Retry Logic

Set retry attempts and delay:
```bash
duck --upload protocol://host/path/ /local/file --retry 3 --retry-delay 5
```

### Verbose Output

Enable detailed logging:
```bash
duck --upload protocol://host/path/ /local/file --verbose
```

Quiet mode (suppress output):
```bash
duck --upload protocol://host/path/ /local/file --quiet
```

### Timestamp Preservation

Preserve modification times:
```bash
duck --upload protocol://host/path/ /local/file --preserve
```

## Bookmarks and Profiles

### Save Connection Profile

Create bookmark from command line:
```bash
duck --bookmark protocol://user@host/path/ --nickname "My Server"
```

### Use Saved Profile

List available bookmarks:
```bash
duck --list-bookmarks
```

Use bookmark by name:
```bash
duck --upload "My Server" /local/file
```

## Scripting Best Practices

### Error Handling

Check exit codes:
```bash
duck --upload sftp://host/path/ /local/file
if [ $? -eq 0 ]; then
    echo "Upload successful"
else
    echo "Upload failed"
    exit 1
fi
```

### Batch Operations

Upload multiple files with loop:
```bash
for file in /local/directory/*.txt; do
    duck --upload protocol://host/remote/ "$file"
done
```

### Logging

Redirect output to log file:
```bash
duck --upload protocol://host/path/ /local/file --verbose > transfer.log 2>&1
```

### Credentials Management

Use environment variables:
```bash
export DUCK_USERNAME="myuser"
export DUCK_PASSWORD="mypass"
duck --upload ftp://$DUCK_USERNAME:$DUCK_PASSWORD@host/path/ /local/file
```

Store in secure credential manager instead of scripts.

## Common Issues and Solutions

### Permission Denied

- Verify credentials are correct
- Check SSH key permissions (should be 600)
- Ensure target directory has write permissions
- For S3, verify IAM permissions

### Connection Timeout

- Check firewall rules
- Verify hostname/IP is reachable
- For FTP, try switching between active/passive modes
- Increase timeout: `--timeout 300`

### Transfer Interrupted

- Use `--resume` flag to continue
- Check network stability
- Consider bandwidth throttling if network is unstable

### Character Encoding Issues

Specify encoding:
```bash
duck --upload protocol://host/path/ /local/file --encoding UTF-8
```

## Quick Reference Commands

```bash
# Upload
duck --upload REMOTE LOCAL

# Download
duck --download REMOTE LOCAL

# List
duck --list REMOTE

# Delete
duck --delete REMOTE

# Sync
duck --synchronize REMOTE LOCAL

# Create directory
duck --mkdir REMOTE

# Copy
duck --copy SOURCE DESTINATION

# Move
duck --move SOURCE DESTINATION

# Edit remote file
duck --edit REMOTE

# Get file info
duck --info REMOTE
```

## Additional Resources

For detailed reference documentation on specific protocols and advanced features, load:
- `references/protocols.md` - Detailed protocol specifications and authentication
- `references/cli_options.md` - Complete CLI options reference
- `references/troubleshooting.md` - Detailed troubleshooting guide

For example scripts and automation templates, see:
- `scripts/backup_script.sh` - Example backup automation
- `scripts/batch_upload.py` - Python wrapper for batch operations
