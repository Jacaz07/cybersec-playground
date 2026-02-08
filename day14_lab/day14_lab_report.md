Day 14 – Privilege Escalation via SUDO & PATH Hijacking

## Environment
- Attacker: Kali Linux
- Target: Metasploitable2
- Access: SSH (msfadmin)

## Initial Access
User logged in via SSH as msfadmin.

## Enumeration
Command used:
sudo -l

Result:
User msfadmin may run (ALL) ALL.

## Exploitation
Privilege escalation achieved by executing:
sudo su

Alternative method:
sudo bash

## Result
Root shell obtained successfully.

## Lessons Learned
- Always check sudo permissions
- Misconfigured sudo is a critical vulnerability
- PATH hijacking is possible when full paths are not used
