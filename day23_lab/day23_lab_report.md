# Day 23 – Service Enumeration and Attack Surface Analysis

## Target

- Host: 192.168.56.106
- Environment: Internal lab (Kioptrix-like VM)
- Attacker: Kali Linux

## Objective

The goal of Day 23 was to perform full network and service enumeration in order to identify viable attack vectors and eliminate false positives before exploitation.

## Network Discovery

The target was confirmed alive using ARP and TCP SYN scans.

## Port and Service Enumeration

A full TCP scan with service detection revealed the following open services:

- SSH (22/tcp) – OpenSSH 3.9p1
- HTTP (80/tcp) – Apache 2.0.52 with PHP 4.3.9
- HTTPS (443/tcp) – Apache 2.0.52
- RPC (111/tcp)
- CUPS (631/tcp)
- RPC Status (632/tcp)
- MySQL (3306/tcp) – Unauthorized access

The operating system appears to be a legacy CentOS-based distribution.

## Web Application Enumeration

### HTTP Analysis

- Supported methods: GET, POST, HEAD, OPTIONS
- Server: Apache/2.0.52 (CentOS)
- PHP version: 4.3.9

### Directory Enumeration

Discovered directories:

- /index.php (login page)
- /manual/
- /icons/

No upload functionality or dangerous endpoints were discovered.

## Web Vulnerability Testing

### Local File Inclusion (LFI)

Tested directory traversal via GET parameters:

- Attempted inclusion of /etc/passwd
- No file inclusion occurred
- LFI ruled out

### CGI / Shellshock

- /cgi-bin/ directory inaccessible (403)
- No CGI scripts discovered
- Shellshock attack surface ruled out

## SSH Analysis

SSH service uses deprecated cryptographic algorithms:

- diffie-hellman-group1-sha1
- diffie-hellman-group14-sha1

However:

- No credentials available
- No pre-authentication RCE
- SSH brute-force considered out of scope

## MySQL Service

- MySQL service detected
- Remote connections denied
- No authentication bypass observed

## RPC and CUPS Analysis (Key Finding)

The system exposes:

- rpcbind (111/tcp)
- CUPS 1.1 on port 631/tcp

This version of CUPS is known to contain remote command execution vulnerabilities when combined with RPC services on legacy Linux systems.

## Attack Surface Decision

After eliminating non-viable vectors:

- Web RCE: Not possible
- LFI/RFI: Not possible
- CGI/Shellshock: Not applicable
- SSH: Requires credentials
- MySQL: Access denied

The only viable exploitation path identified:

- CUPS 1.1 Remote Command Execution via RPC

## Conclusion

Day 23 successfully narrowed the attack surface to a single, reliable exploitation vector. The system is vulnerable to a known CUPS-related RCE which will be targeted in the next phase.

## Next Steps

- Exploit CUPS 1.1
- Obtain remote shell
- Escalate privileges (expected root access)

Day 24 will focus on exploitation.
