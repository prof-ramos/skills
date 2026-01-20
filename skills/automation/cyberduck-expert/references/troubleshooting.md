# CyberDuck/Duck CLI Troubleshooting Guide

Comprehensive troubleshooting guide for common issues and errors.

## Connection Issues

### "Connection Refused" or "Connection Timeout"

**Symptoms**
- Cannot connect to server
- Timeout after several seconds

**Possible Causes & Solutions**

1. **Firewall blocking connection**
   - Check local firewall settings
   - Verify server firewall allows incoming connections
   - For FTP: Ensure both port 21 (control) and passive ports are open
   - Test with: `telnet hostname port`

2. **Wrong hostname or port**
   - Verify hostname/IP is correct
   - Check if custom port is needed
   - Test DNS resolution: `nslookup hostname`

3. **Server is down**
   - Verify server is running
   - Check server logs for errors
   - Try connecting from another client

4. **Network issues**
   - Test basic connectivity: `ping hostname`
   - Check for VPN/proxy interference
   - Try from different network

**Quick Fixes**
```bash
# Increase timeout
duck --upload sftp://host/path /local/file --timeout 60

# Try different port
duck --upload sftp://host:2222/path /local/file

# Use IP instead of hostname
duck --upload sftp://192.168.1.100/path /local/file
```

---

### "Authentication Failed" or "Permission Denied"

**Symptoms**
- Connection establishes but login fails
- "Invalid credentials" error

**Possible Causes & Solutions**

**For Password Authentication:**
1. Wrong username/password
2. Account disabled or locked
3. Password expired
4. Special characters in password need escaping

**For SSH Key Authentication:**
1. Wrong key being used
2. Key not authorized on server
3. Wrong permissions on key file
4. Passphrase required but not provided

**Solutions:**

Test credentials:
```bash
# For SFTP
ssh user@hostname

# For FTP
ftp hostname
```

Check SSH key:
```bash
# Verify key permissions (must be 600)
chmod 600 ~/.ssh/id_rsa

# Test specific key
ssh -i ~/.ssh/id_rsa user@hostname

# Use correct key with duck
duck --upload sftp://user@host/path /local/file -i ~/.ssh/custom_key
```

Verify key is authorized:
```bash
# On server, check ~/.ssh/authorized_keys
# Public key must be present
cat ~/.ssh/id_rsa.pub | ssh user@host 'cat >> ~/.ssh/authorized_keys'
```

---

### "Host Key Verification Failed"

**Symptoms**
- SSH/SFTP connection fails with host key error
- "Host key has changed" warning

**Causes**
- First connection to new server
- Server reinstalled/changed
- Man-in-the-middle attack (rare)

**Solutions:**

Trust certificate (first connection):
```bash
# Duck will prompt - answer 'yes'
duck --list sftp://user@host/path
```

Skip verification (not recommended):
```bash
duck --upload sftp://user@host/path /local/file --trust-all-certificates
```

Reset known host:
```bash
# Remove old host key
ssh-keygen -R hostname

# Reconnect
duck --list sftp://user@host/path
```

---

## Transfer Issues

### "Transfer Interrupted" or "Connection Lost"

**Symptoms**
- Transfer starts but stops mid-way
- "Connection reset by peer"

**Causes**
- Network instability
- Server timeout
- Bandwidth limits exceeded
- Large file transfer

**Solutions:**

Enable resume:
```bash
duck --upload sftp://host/path /local/file --resume
```

Increase timeout and retries:
```bash
duck --upload sftp://host/path /local/file \
  --timeout 300 \
  --retry 5 \
  --retry-delay 10
```

Throttle bandwidth:
```bash
# Limit to 1 MB/s
duck --upload sftp://host/path /local/file --throttle 1048576
```

Split large files:
```bash
# On Linux/Mac
split -b 100M large-file.zip part-

# Upload parts separately
for part in part-*; do
    duck --upload sftp://host/path/ "$part"
done
```

---

### Slow Transfer Speeds

**Symptoms**
- Transfer much slower than expected
- Progress bar barely moving

**Causes & Solutions**

1. **Network bandwidth limit**
   - Check network speed: `speedtest-cli`
   - Verify ISP bandwidth limits
   - Consider time of day (peak hours)

2. **Server bandwidth limit**
   - Check server resources
   - Verify no rate limiting
   - Try different time

3. **Too few parallel connections**
   ```bash
   # Increase parallel transfers
   duck --upload s3://bucket/path /local/dir --parallel 10
   ```

4. **Small chunk size (S3)**
   ```bash
   # Increase chunk size for large files
   duck --upload s3://bucket/path /local/file --chunk-size 10485760
   ```

5. **CPU bottleneck (encryption)**
   - Check CPU usage
   - Use faster machine
   - Consider disabling compression (if applicable)

6. **Disk I/O bottleneck**
   - Check disk usage: `iostat`
   - Use faster storage (SSD)
   - Reduce parallel transfers

---

### "Permission Denied" During Upload

**Symptoms**
- Connection successful
- Upload fails with permission error

**Causes & Solutions**

1. **No write permission on target directory**
   ```bash
   # Check permissions via SFTP
   sftp user@host
   sftp> ls -la /target/directory
   
   # On server, fix permissions
   chmod 755 /target/directory
   chown user:group /target/directory
   ```

2. **Disk full**
   ```bash
   # Check disk space on server
   df -h /target/directory
   ```

3. **Quota exceeded**
   ```bash
   # Check quota
   quota -s
   ```

4. **Wrong user/group**
   ```bash
   # Verify you're uploading as correct user
   whoami
   
   # Switch user if needed
   sudo -u targetuser duck --upload ...
   ```

---

## Protocol-Specific Issues

### FTP: "Entering Passive Mode" Fails

**Symptoms**
- Connection hangs after "Entering Passive Mode"
- Data transfer never starts

**Causes**
- NAT/firewall blocking passive ports
- Server passive port range not accessible

**Solutions:**

Try active mode:
```bash
duck --upload ftp://host/path /local/file --active
```

Configure firewall for passive ports:
```bash
# On server, configure passive port range
# Usually 50000-51000
# Open these ports in firewall
```

Use FTPS instead:
```bash
duck --upload ftps://host/path /local/file
```

---

### S3: "Access Denied"

**Symptoms**
- Authentication works
- Cannot list/upload/download files

**Causes & Solutions**

1. **Insufficient IAM permissions**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:ListBucket",
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject"
         ],
         "Resource": [
           "arn:aws:s3:::bucket-name",
           "arn:aws:s3:::bucket-name/*"
         ]
       }
     ]
   }
   ```

2. **Bucket policy denying access**
   - Check bucket policy in AWS Console
   - Verify no explicit DENY statements

3. **Wrong region**
   ```bash
   # Specify correct region
   duck --upload s3://bucket/path /local/file --region us-west-2
   ```

4. **Bucket doesn't exist**
   ```bash
   # List buckets to verify
   aws s3 ls
   ```

---

### S3: "Signature Does Not Match"

**Symptoms**
- Authentication error with signature mismatch

**Causes**
- Wrong AWS credentials
- Clock skew (time difference between client and AWS)
- Special characters in credentials

**Solutions:**

Verify credentials:
```bash
# Check credentials file
cat ~/.aws/credentials

# Test with AWS CLI
aws s3 ls s3://bucket-name
```

Fix clock skew:
```bash
# Sync system time
sudo ntpdate pool.ntp.org

# Or on systemd systems
sudo timedatectl set-ntp true
```

---

### SFTP: "Received Too Large Packet"

**Symptoms**
- SFTP connection fails with "packet too large" error

**Causes**
- Banner or message in server's shell startup
- Server sending non-SFTP data

**Solutions:**

1. **Disable shell banner**
   ```bash
   # On server, comment out banner in /etc/ssh/sshd_config
   # Banner none
   ```

2. **Clean shell startup files**
   ```bash
   # On server, check ~/.bashrc, ~/.bash_profile
   # Remove any echo/print statements
   # Move them inside: if [ -z "$PS1" ]; then return; fi
   ```

---

## File/Directory Issues

### "File Not Found" or "No Such File"

**Causes & Solutions**

1. **Wrong path**
   - Verify exact path
   - Check for typos
   - Use absolute paths

2. **Case sensitivity**
   - Unix/Linux is case-sensitive
   - "File.txt" ≠ "file.txt"

3. **Hidden files**
   ```bash
   # List with hidden files
   duck --list sftp://host/path/ --all
   ```

4. **Permissions**
   ```bash
   # May not have read permission
   # Check on server
   ls -la /path/to/file
   ```

---

### Filename Encoding Issues

**Symptoms**
- Files with special characters don't transfer
- Filenames appear garbled

**Solutions:**

Specify encoding:
```bash
duck --upload sftp://host/path /local/file --encoding UTF-8
```

Rename files to ASCII:
```bash
# Before transfer, rename problematic files
for f in *; do
    mv "$f" "$(echo $f | iconv -f utf8 -t ascii//TRANSLIT)"
done
```

---

### "Disk Full" or "No Space Left"

**On Server:**
```bash
# Check disk space
df -h

# Find large files
du -sh /* | sort -h

# Clean up
# - Remove old logs
# - Clear temp files
# - Archive old data
```

**On Client:**
```bash
# Check local disk space
df -h .

# Free up space before download
```

---

## Performance Optimization Issues

### High CPU Usage

**Causes:**
- Encryption overhead (SSH/TLS)
- Compression enabled
- Multiple parallel transfers

**Solutions:**
```bash
# Reduce parallel connections
duck --upload sftp://host/path /local/dir --parallel 2

# Use less CPU-intensive cipher (if supported)
# Configure in ~/.ssh/config:
# Ciphers aes128-ctr,aes192-ctr,aes256-ctr
```

---

### High Memory Usage

**Causes:**
- Large buffer sizes
- Too many parallel transfers
- Large files in memory

**Solutions:**
```bash
# Reduce parallel transfers
duck --upload s3://bucket/path /local/dir --parallel 3

# Use smaller chunk sizes
duck --upload s3://bucket/path /local/file --chunk-size 5242880
```

---

## Debugging Techniques

### Enable Verbose Logging

```bash
# Verbose output
duck --upload sftp://host/path /local/file --verbose

# Protocol trace (very detailed)
duck --upload sftp://host/path /local/file --trace

# Log to file
duck --upload sftp://host/path /local/file \
  --verbose \
  --log /tmp/duck-debug.log 2>&1
```

### Test with Alternative Clients

**SFTP:**
```bash
# Native sftp client
sftp user@host
sftp> put /local/file /remote/path

# rsync
rsync -avz -e ssh /local/file user@host:/remote/path
```

**FTP:**
```bash
# Native ftp client
ftp hostname

# lftp (better FTP client)
lftp ftp://user:pass@host
```

**S3:**
```bash
# AWS CLI
aws s3 cp /local/file s3://bucket/path/
```

### Network Diagnostics

```bash
# Test connectivity
ping hostname

# Test port
telnet hostname port
nc -zv hostname port

# Trace route
traceroute hostname

# Check DNS
nslookup hostname
dig hostname
```

### Server-Side Logs

Check server logs for errors:
```bash
# SFTP/SSH logs
tail -f /var/log/auth.log
tail -f /var/log/secure

# FTP logs (vsftpd)
tail -f /var/log/vsftpd.log

# Apache/nginx (WebDAV)
tail -f /var/log/apache2/error.log
tail -f /var/log/nginx/error.log
```

---

## Getting Help

### Collect Debug Information

Before requesting help, gather:

1. **Exact error message**
2. **Full command used** (redact credentials)
3. **Duck version**: `duck --version`
4. **Operating system**: `uname -a`
5. **Debug logs**: `duck --verbose --log debug.log ...`
6. **Network test results**: `ping`, `telnet`

### Community Resources

- **GitHub Issues**: https://github.com/iterate-ch/cyberduck/issues
- **Documentation**: https://docs.cyberduck.io/
- **Forums**: https://cyberduck.io/help/
- **Stack Overflow**: Tag `[cyberduck]`

### Commercial Support

For professional support:
- **Cyberduck Support**: support@cyberduck.io
- Available for enterprise users
- Includes priority bug fixes and feature requests
