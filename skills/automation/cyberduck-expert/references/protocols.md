# Protocol Reference Guide

Detailed specifications and configuration for all protocols supported by CyberDuck and duck CLI.

## FTP (File Transfer Protocol)

### Connection Format
```
ftp://username:password@hostname:port/path
```

### Default Port
- Port 21 (standard)
- Port 990 (implicit TLS)

### Connection Modes

**Passive Mode (Default)**
- Client initiates both control and data connections
- Recommended for NAT/firewall environments
- Used by default in duck CLI

**Active Mode**
- Server initiates data connection back to client
- Requires firewall configuration
- Enable with: `--active`

### Transfer Modes

**Binary Mode (Default)**
- Used for all file types by default
- Preserves exact file content

**ASCII Mode**
- Text file line-ending conversion
- Rarely needed in modern systems
- Enable with: `--transfer-mode ascii`

### TLS/SSL Support

**Explicit TLS (FTPS - AUTH TLS)**
```
ftps://user:pass@host/path
```
- Upgrades plain FTP to encrypted
- Port 21 by default
- Recommended for security

**Implicit TLS**
```
ftps://user:pass@host:990/path
```
- Encrypted from connection start
- Port 990 by default
- Legacy method

### Authentication
- Username/password (basic auth)
- Anonymous: `ftp://anonymous@host/path`

---

## SFTP (SSH File Transfer Protocol)

### Connection Format
```
sftp://username@hostname:port/path
```

### Default Port
- Port 22 (SSH standard)

### Authentication Methods

**SSH Key (Recommended)**
```bash
# Default key location
duck --upload sftp://user@host/path /local/file

# Custom key
duck --upload sftp://user@host/path /local/file -i ~/.ssh/custom_key

# Key with passphrase (will prompt)
duck --upload sftp://user@host/path /local/file -i ~/.ssh/encrypted_key
```

**Password**
```bash
# Inline password (not recommended for scripts)
duck --upload sftp://user:password@host/path /local/file

# Interactive prompt (recommended)
duck --upload sftp://user@host/path /local/file
# Will prompt for password
```

**SSH Agent**
- Automatically uses ssh-agent if available
- No additional configuration needed

### SSH Key Setup

Generate key pair:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Copy public key to server:
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname
```

Set correct permissions:
```bash
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### Host Key Verification

**First connection**: Duck will ask to verify host key fingerprint

**Skip verification (not recommended)**:
```bash
duck --upload sftp://user@host/path /local/file --trust-all-certificates
```

### Known Hosts
- Stored in: `~/.ssh/known_hosts`
- Automatic management by duck CLI

---

## Amazon S3 and S3-Compatible Storage

### Connection Format
```
s3://bucket-name/prefix/path/
```

### Authentication

**AWS Credentials File** (Recommended)
Location: `~/.aws/credentials`
```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[production]
aws_access_key_id = AKIAI...
aws_secret_access_key = wJal...
```

Use specific profile:
```bash
duck --upload s3://bucket/path /local/file --profile production
```

**Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"
```

**IAM Instance Profile**
- Automatic for EC2 instances with IAM role
- No credential configuration needed

### Storage Classes

Specify on upload:
```bash
--storage-class STANDARD         # Default, frequent access
--storage-class STANDARD_IA      # Infrequent access, lower cost
--storage-class ONEZONE_IA       # Single AZ, lowest cost
--storage-class INTELLIGENT_TIERING  # Auto-optimization
--storage-class GLACIER          # Archive, minutes-hours retrieval
--storage-class DEEP_ARCHIVE     # Long-term archive, 12h retrieval
```

### Encryption

**Server-Side Encryption (SSE)**
```bash
--encryption AES256              # S3-managed keys (SSE-S3)
--encryption aws:kms             # KMS-managed keys (SSE-KMS)
--encryption aws:kms --kms-key-id arn:aws:kms:...  # Specific KMS key
```

**Client-Side Encryption**
Not directly supported by duck CLI. Encrypt files before upload.

### Access Control

**ACL (Access Control List)**
```bash
--acl private                    # Owner only (default)
--acl public-read                # Public read access
--acl public-read-write          # Public read/write (not recommended)
--acl authenticated-read         # Authenticated AWS users
--acl bucket-owner-read          # Bucket owner has read access
--acl bucket-owner-full-control  # Bucket owner has full control
```

**Bucket Policies and IAM Roles** (preferred over ACLs)
- Configure via AWS Console or CLI
- More granular control
- Better security practices

### Regions

Specify region:
```bash
duck --upload s3://bucket/path /local/file --region us-west-2
```

Common regions:
- `us-east-1` - US East (N. Virginia)
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-southeast-1` - Asia Pacific (Singapore)

### S3-Compatible Services

**Wasabi**
```bash
duck --upload s3://bucket/path /local/file \
  --endpoint s3.wasabisys.com \
  --region us-east-1
```

**DigitalOcean Spaces**
```bash
duck --upload s3://bucket/path /local/file \
  --endpoint nyc3.digitaloceanspaces.com \
  --region nyc3
```

**MinIO**
```bash
duck --upload s3://bucket/path /local/file \
  --endpoint minio.example.com:9000 \
  --region us-east-1
```

### CloudFront CDN Integration

Invalidate cached content:
```bash
duck --invalidate s3://bucket/path/file.txt \
  --distribution-id E1234567890ABC
```

Wildcard invalidation:
```bash
duck --invalidate s3://bucket/path/* \
  --distribution-id E1234567890ABC
```

---

## Google Drive

### Connection Format
```
googledrive://email@gmail.com/folder-id-or-name/
```

### Authentication

**OAuth 2.0** (Required)
First connection opens browser for authorization:
```bash
duck --list googledrive://user@gmail.com/
```

Credentials stored in:
- macOS: Keychain
- Windows: Credential Manager
- Linux: Secret Service or file

### Folder Navigation

**By Folder ID** (Recommended)
```bash
googledrive://user@gmail.com/1a2b3c4d5e6f7g8h9i0j/
```

Get folder ID from URL:
```
https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
                                          ^^^^^^^^^^^^^^^^^^^^
```

**By Folder Name**
```bash
googledrive://user@gmail.com/My%20Documents/
```
- Space = `%20` in URL encoding
- Not unique - may match multiple folders

### Shared Drives (Team Drives)

Access shared drive:
```bash
googledrive://user@gmail.com/shared-drive-name/
```

### File Limitations

- Max file size: 5 TB
- Daily upload quota: ~750 GB per user
- API rate limits apply

---

## Microsoft OneDrive and SharePoint

### Connection Format

**OneDrive Personal**
```
onedrive://user@outlook.com/path/
```

**OneDrive for Business**
```
onedrive://user@company.com/path/
```

**SharePoint**
```
sharepoint://tenant.sharepoint.com/sites/sitename/path/
```

### Authentication

OAuth 2.0 required. Browser opens for authorization on first use.

### Limitations

- Max file size: 100 GB (OneDrive), 15 GB (SharePoint)
- Path length limits apply
- Special characters in filenames may cause issues

---

## Dropbox

### Connection Format
```
dropbox://user@email.com/path/
```

### Authentication

OAuth 2.0 required. Browser authorization on first connection.

### File Versions

Dropbox maintains file versions automatically. Duck CLI doesn't directly manage versions.

### Limitations

- Max file size: 350 GB (via upload API)
- Rate limits: 200 API calls per user per hour

---

## Azure Blob Storage

### Connection Format
```
azure://accountname.blob.core.windows.net/container/path/
```

### Authentication

**Shared Key (Account Key)**
```bash
duck --upload azure://account.blob.core.windows.net/container/path /local/file \
  --username accountname \
  --password "account-access-key"
```

**SAS Token (Shared Access Signature)**
```bash
duck --upload "azure://account.blob.core.windows.net/container/path?sv=2020-08-04&ss=b&srt=sco&sp=rwdlacx&se=..." /local/file
```

### Blob Types

- **Block Blob** (default) - Optimized for streaming, documents
- **Page Blob** - Optimized for random read/write (VHDs)
- **Append Blob** - Optimized for append operations (logs)

Duck CLI uses block blobs by default.

### Access Tiers

```bash
--storage-class Hot              # Frequent access
--storage-class Cool             # Infrequent access, 30-day minimum
--storage-class Archive          # Rare access, 180-day minimum
```

---

## WebDAV

### Connection Format
```
dav://username:password@hostname/path
davs://username:password@hostname/path  # HTTPS
```

### Default Ports
- HTTP: 80
- HTTPS: 443

### Common WebDAV Servers

**Nextcloud/ownCloud**
```bash
davs://username@cloud.example.com/remote.php/dav/files/username/
```

**Box.com**
```bash
davs://username@dav.box.com/dav/
```

### Authentication

Basic authentication (username/password) is standard. Some servers support OAuth.

---

## Backblaze B2

### Connection Format
```
b2://bucket-name/path/
```

### Authentication

Requires Application Key:
```bash
duck --upload b2://bucket/path /local/file \
  --username keyID \
  --password applicationKey
```

Generate keys in Backblaze web console.

### Storage Classes

B2 has single storage class with automatic lifecycle transitions available.

### Cost Optimization

- First 10 GB storage free
- First 1 GB download free per day
- Transaction costs apply

---

## OpenStack Swift

### Connection Format
```
swift://container/path/
```

### Authentication

Requires OpenStack credentials:
```bash
duck --upload swift://container/path /local/file \
  --username tenant:user \
  --password password \
  --identity-url https://auth.example.com:5000/v3
```

### Regions

Specify region if using multi-region deployment:
```bash
--region RegionOne
```

---

## Google Cloud Storage

### Connection Format
```
gs://bucket-name/path/
```

### Authentication

**Service Account Key** (Recommended)
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
duck --upload gs://bucket/path /local/file
```

**OAuth 2.0**
Browser-based authorization similar to Google Drive.

### Storage Classes

```bash
--storage-class STANDARD         # Frequent access
--storage-class NEARLINE         # Infrequent (once/month)
--storage-class COLDLINE         # Rare (once/quarter)
--storage-class ARCHIVE          # Long-term archive (once/year)
```

### Regional vs Multi-Regional

Specified at bucket creation, not per-file.

---

## Protocol Selection Guide

Choose protocol based on use case:

**General File Transfer**
- SFTP - Best for Linux/Unix servers (secure, efficient)
- FTP - Legacy systems only (insecure unless FTPS)

**Cloud Storage**
- S3 - AWS infrastructure, CDN integration
- Google Drive - User-friendly, collaboration
- Dropbox - Simple sharing, sync
- Azure Blob - Microsoft ecosystem

**Web/CMS Integration**
- WebDAV - Nextcloud, ownCloud, SharePoint

**Backup/Archive**
- S3 Glacier - Long-term AWS storage
- Backblaze B2 - Cost-effective alternative
- Azure Archive - Microsoft ecosystem

**Performance Priorities**
- SFTP - Best for direct server access
- S3 - Best for cloud-native applications
- HTTP/HTTPS - Best for public distribution
