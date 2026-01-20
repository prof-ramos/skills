# Duck CLI Options Reference

Complete reference of all command-line options and flags for duck CLI.

## Command Syntax

```bash
duck [OPTIONS] [COMMAND] [ARGUMENTS]
```

## Global Options

Options that apply to all commands.

### Connection Options

**`--username <username>`**
- Username for authentication
- Can also specify in URL: `protocol://username@host/path`

**`--password <password>`**
- Password for authentication
- **Not recommended**: Use keychain, credential manager, or interactive prompt
- Can also specify in URL (insecure): `protocol://username:password@host/path`

**`-i <identity>`, `--identity <identity>`**
- Path to private key file for SSH/SFTP authentication
- Example: `-i ~/.ssh/id_rsa`

**`--profile <name>`**
- Use saved bookmark/profile by name
- Example: `--profile "Production Server"`

**`--endpoint <url>`**
- Custom endpoint for S3-compatible storage
- Example: `--endpoint s3.wasabisys.com`

**`--region <region>`**
- AWS/S3 region
- Example: `--region us-west-2`

**`--port <port>`**
- Override default port
- Example: `--port 2222`

### Authentication & Security

**`--trust-all-certificates`**
- Skip SSL/TLS certificate verification
- **Not recommended**: Use only for testing/development

**`--trust-certificate <fingerprint>`**
- Trust specific SSL/TLS certificate by fingerprint

**`--nokeychain`**
- Don't use system keychain for password storage
- Useful for testing or automation

### Output & Logging

**`-v`, `--verbose`**
- Enable verbose output
- Shows detailed connection and transfer information

**`-q`, `--quiet`**
- Suppress all output except errors
- Useful for scripts and cron jobs

**`--json`**
- Output in JSON format (for `--list` and `--info` commands)
- Enables machine-readable output parsing

**`--log <file>`**
- Write log to specified file
- Example: `--log /var/log/duck-transfer.log`

### Performance Options

**`--throttle <bytes/sec>`**
- Limit bandwidth usage
- Value in bytes per second
- Example: `--throttle 1048576` (1 MB/s)

**`--parallel <count>`**
- Number of parallel connections/transfers
- Default: 5
- Range: 1-20
- Example: `--parallel 10`

**`--retry <count>`**
- Number of retry attempts on failure
- Default: 0
- Example: `--retry 3`

**`--retry-delay <seconds>`**
- Delay between retry attempts
- Default: 1
- Example: `--retry-delay 5`

**`--timeout <seconds>`**
- Connection timeout in seconds
- Default: 30
- Example: `--timeout 60`

**`--chunk-size <bytes>`**
- Chunk size for multipart uploads
- Relevant for S3 and large files
- Example: `--chunk-size 10485760` (10 MB)

## Command-Specific Options

### Upload Command

**Syntax**: `duck --upload <remote> <local> [OPTIONS]`

**`--resume`**
- Resume interrupted upload
- Only works if server supports resume

**`--preserve`**
- Preserve file modification timestamps

**`--permissions <mode>`**
- Set file permissions (Unix octal notation)
- Example: `--permissions 644`

**`--storage-class <class>`**
- S3 storage class (STANDARD, STANDARD_IA, GLACIER, etc.)
- Azure access tier (Hot, Cool, Archive)

**`--encryption <type>`**
- Server-side encryption
- Values: `AES256`, `aws:kms`

**`--acl <acl>`**
- S3 Access Control List
- Values: `private`, `public-read`, `public-read-write`, etc.

**`--kms-key-id <key-arn>`**
- AWS KMS key ARN for SSE-KMS encryption

**`--metadata <key=value>`**
- Set custom metadata (can be used multiple times)
- Example: `--metadata "Author=John Doe" --metadata "Version=1.0"`

**`--no-checksum`**
- Skip checksum verification
- Faster but less safe

### Download Command

**Syntax**: `duck --download <remote> <local> [OPTIONS]`

**`--resume`**
- Resume interrupted download

**`--preserve`**
- Preserve file modification timestamps

**`--overwrite`**
- Overwrite existing files without prompting

**`--skip-existing`**
- Skip files that already exist locally

### Synchronize Command

**Syntax**: `duck --synchronize <remote> <local> [OPTIONS]`

**`--delete`**
- Delete files in destination not present in source
- Creates exact mirror

**`--preserve`**
- Preserve timestamps

**`--upload`**
- Sync direction: local to remote (default)

**`--download`**
- Sync direction: remote to local

**`--mirror`**
- Bidirectional sync (not recommended without careful testing)

**`--checksum`**
- Use checksum instead of size/date for comparison
- More accurate but slower

**`--exclude <pattern>`**
- Exclude files matching pattern
- Example: `--exclude "*.tmp"`
- Can be used multiple times

**`--include <pattern>`**
- Include only files matching pattern
- Example: `--include "*.pdf"`

### List Command

**Syntax**: `duck --list <remote> [OPTIONS]`

**`-L`, `--long`**
- Long format with permissions, size, date
- Similar to `ls -l`

**`-R`, `--recursive`**
- List recursively

**`--json`**
- Output in JSON format

### Delete Command

**Syntax**: `duck --delete <remote> [OPTIONS]`

**`--recursive`**
- Delete directories recursively

**`--force`**
- Don't prompt for confirmation

### Copy/Move Commands

**Copy Syntax**: `duck --copy <source> <destination> [OPTIONS]`
**Move Syntax**: `duck --move <source> <destination> [OPTIONS]`

**`--overwrite`**
- Overwrite existing files

### Info Command

**Syntax**: `duck --info <remote> [OPTIONS]`

Returns file/folder metadata: size, modification date, permissions, checksum.

**`--json`**
- Output in JSON format

### Edit Command

**Syntax**: `duck --edit <remote> [OPTIONS]`

**`--editor <command>`**
- Specify editor command
- Default: uses $EDITOR environment variable

Opens remote file in local editor, uploads changes on save.

### Bookmark Commands

**Create**: `duck --bookmark <url> [OPTIONS]`

**`--nickname <name>`**
- Friendly name for bookmark

**List**: `duck --list-bookmarks`

**Delete**: `duck --delete-bookmark <name>`

## Transfer Mode Options

**`--transfer-mode <mode>`**
- Transfer mode for FTP
- Values: `binary` (default), `ascii`

**`--active`**
- Use active FTP mode instead of passive

**`--encoding <charset>`**
- Character encoding for filenames
- Example: `--encoding UTF-8`

## CDN/Cache Options

**`--invalidate`**
- Invalidate CDN cache (CloudFront, Akamai)
- Requires `--distribution-id`

**`--distribution-id <id>`**
- CDN distribution ID for invalidation

## Debug & Advanced Options

**`--trace`**
- Enable protocol trace logging
- Very verbose, for debugging only

**`--no-progress`**
- Disable progress indicators
- Useful for redirecting output

**`--version`**
- Display version information

**`--help`**
- Display help message

**`--license`**
- Display license information

**`--default-protocol <protocol>`**
- Set default protocol for URLs without scheme
- Example: `--default-protocol sftp`

## Exit Codes

Duck CLI returns standard exit codes:

- **0**: Success
- **1**: General error
- **2**: Connection failed
- **3**: Authentication failed
- **4**: File not found
- **5**: Permission denied
- **6**: Transfer interrupted
- **7**: Disk full

Use in scripts:
```bash
duck --upload sftp://host/path /local/file
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed with code $?"
fi
```

## Environment Variables

Duck CLI respects these environment variables:

**AWS Credentials**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- `AWS_DEFAULT_REGION`

**Google Cloud**
- `GOOGLE_APPLICATION_CREDENTIALS`

**SSH**
- `SSH_AUTH_SOCK` (for ssh-agent)

**Editor**
- `EDITOR` (for `--edit` command)

**Locale**
- `LANG`, `LC_ALL` (for character encoding)

**Proxy**
- `HTTP_PROXY`, `HTTPS_PROXY`
- `NO_PROXY`

## Configuration Files

**Bookmarks Location**
- macOS: `~/Library/Group Containers/G69SCX94XU.duck/Library/Application Support/duck/Bookmarks/`
- Windows: `%AppData%\Cyberduck\Bookmarks\`
- Linux: `~/.duck/bookmarks/`

**Credentials Storage**
- macOS: Keychain
- Windows: Credential Manager
- Linux: Secret Service API or plaintext (insecure)

## Common Option Combinations

**Secure upload with verification**
```bash
duck --upload sftp://host/path /local/file \
  --verbose \
  --retry 3 \
  --preserve \
  --permissions 644
```

**High-performance S3 upload**
```bash
duck --upload s3://bucket/path /local/large-file \
  --parallel 10 \
  --chunk-size 10485760 \
  --storage-class INTELLIGENT_TIERING \
  --quiet
```

**Bandwidth-limited sync**
```bash
duck --synchronize sftp://host/path /local/dir \
  --throttle 524288 \
  --preserve \
  --exclude "*.tmp" \
  --verbose
```

**Production backup script**
```bash
duck --upload s3://backups/$(date +%Y%m%d)/ /data/ \
  --recursive \
  --preserve \
  --storage-class GLACIER \
  --retry 5 \
  --retry-delay 10 \
  --log /var/log/backup.log \
  --quiet
```

## Best Practices

1. **Never hardcode passwords** - Use keychain, bookmarks, or interactive prompts
2. **Use --verbose for debugging** - Essential for troubleshooting
3. **Set appropriate --retry values** - Network issues are common
4. **Use --preserve for backups** - Maintains timestamps
5. **Enable --throttle on production** - Prevents bandwidth saturation
6. **Use --quiet in cron jobs** - Only log errors
7. **Check exit codes in scripts** - Detect failures reliably
8. **Use --json for parsing** - Machine-readable output
9. **Test with --dry-run** - Preview operations (if supported)
10. **Log to files in automation** - Debug issues after the fact
