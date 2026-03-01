# Day 25 – Kioptrix 2 Enumeration & Legacy Exploitation Analysis

## 1. Lab Overview

The objective of this lab was to perform full enumeration of the Kioptrix 2 target
and identify potential attack vectors leading to system compromise.

Environment:
- Attacker: Kali Linux
- Target: Kioptrix 2
- Target IP: 192.168.56.106
- Network Type: Host-only

---

## 2. Initial Reconnaissance

### 2.1 Port Scanning

The following ports were identified as open:

- 22/tcp  – SSH
- 80/tcp  – HTTP
- 111/tcp – RPCBind
- 443/tcp – HTTPS
- 631/tcp – IPP (CUPS)
- 3306/tcp – MySQL

The host is alive and responding on all listed services.

---

## 3. Service Enumeration

### 3.1 SSH (Port 22)

- Version: OpenSSH 3.9p1
- SSHv1 supported
- Authentication methods:
  - publickey
  - gssapi-with-mic
  - password

Issue identified:
Modern Kali Linux clients no longer support SSHv1,
which prevents exploitation of legacy protocol weaknesses.

---

### 3.2 HTTP (Port 80)

- Apache 2.0.52 (CentOS)
- No page title detected
- Web application includes a login form

LFI attempts were unsuccessful.
No confirmed SQL Injection during this session.

---

### 3.3 HTTPS (Port 443)

- SSLv2 enabled
- SSLv3 and TLS 1.0 supported
- Certificate expired (2009–2010)
- MD5 signature algorithm used
- Export-grade cipher suites supported

ssl-enum-ciphers results indicate:

- RC4 (deprecated)
- DES/3DES (vulnerable to SWEET32)
- Export ciphers
- CBC-mode in SSLv3 (CVE-2014-3566)

Heartbleed test returned negative.

The cryptographic configuration is critically weak,
however no direct remote code execution vector was obtained.

---

### 3.4 MySQL (Port 3306)

- Service active
- Error: Host not allowed to connect

Conclusion:
MySQL accepts connections only from localhost.
A local shell would be required to leverage this service.

---

### 3.5 RPCBind (Port 111)

- No NFS exports available
- showmount returned: "Program not registered"

Service not exploitable in current configuration.

---

### 3.6 CUPS (Port 631)

- PUT method detected
- Upload attempt returned HTTP 403 Forbidden

No successful file upload possible.

---

## 4. Exploitation Attempts

The following attempts were performed:

- SSHv1 connection attempts (blocked by modern client)
- File upload via CUPS
- SSL exploitation checks
- Legacy OpenSSL mod_ssl exploit attempt
- RPC/NFS enumeration
- Remote MySQL access attempts

None of the attempts resulted in shell access.

---

## 5. Observations

- The system is extremely outdated (circa 2009).
- Supports deprecated cryptographic protocols.
- Requires legacy exploitation environment.
- Modern tools face compatibility limitations.

---

## 6. Conclusion

The target system remains uncompromised during this session.

Successful exploitation likely requires:

- Older attacker environment (e.g., legacy Kali or BackTrack)
- Web-based SQL injection vector
- Local shell access followed by privilege escalation

Lab concluded with successful enumeration but without full system compromise.
