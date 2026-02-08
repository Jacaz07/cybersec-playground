Day 12 — Privilege Escalation via SUID Binaries

## Environment
- Attacker machine: Kali Linux
- Target machine: Metasploitable2
- Network: Isolated lab environment
- Initial access: WebDAV PHP webshell
- Initial user: www-data

## Objective
The goal of this lab was to identify misconfigured SUID binaries on the target
system and exploit them to escalate privileges to root without using automated
tools or internet access.

## Enumeration
After obtaining a low-privileged shell, SUID binaries were enumerated using the
following command:

find / -perm -4000 -type f 2>/dev/null

This command lists all files with the SUID permission bit set, suppressing error
messages for inaccessible directories.

## Exploitation
During enumeration, the binary /usr/bin/find was identified as having the SUID
bit set and owned by root.

The find binary allows execution of arbitrary commands using the -exec
parameter. This behavior was abused to spawn a root shell using:

/usr/bin/find . -exec /bin/sh \; -quit

Because the binary runs with root privileges, the spawned shell also executed
as root.

## Result
Privilege escalation was successful.

- Initial user: www-data
- Escalated user: root

Root access was confirmed using:
- whoami
- id
- Read access to /etc/shadow

## Impact
Misconfigured SUID binaries represent a critical security risk. Any local user
who can execute such binaries may gain full control over the system.

## Lessons Learned
- Manual enumeration is effective even without automated tools.
- SUID binaries should be carefully audited and restricted.
- Knowledge of common exploitable binaries is essential for both attackers
  and defenders.
