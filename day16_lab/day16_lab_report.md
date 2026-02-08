Day 16 — Local Privilege Escalation via Multiple Vectors

## Environment

- Attacker machine: Kali Linux
- Target machine: Metasploitable2
- Network: Isolated lab environment
- Initial access: SSH
- Initial user: msfadmin

## Objective

The goal of this lab was to perform local privilege escalation using manual
enumeration techniques, documenting both failed and successful exploitation
paths.

## Enumeration

After gaining access as the msfadmin user, multiple privilege escalation
vectors were investigated, including PATH hijacking, cron job abuse, and sudo
misconfiguration.

## Attempt 1 — PATH Hijacking (Failed)

The script /usr/local/bin/backup.sh was identified and analyzed. It appeared
to execute system commands that could potentially be hijacked via PATH
manipulation.

A malicious tar binary was created in /tmp, and the PATH variable was
modified to prioritize this directory.

Despite executing the script with sudo, privilege escalation was not achieved.

### Reason for Failure

The execution context and script behavior did not allow PATH hijacking in this
case. This highlights the importance of validating assumptions during
exploitation.

## Attempt 2 — Cron Job Abuse (Failed)

System-wide cron jobs were reviewed via /etc/crontab. While several jobs were
executed as root, no writable scripts or directories were identified that could
be abused for privilege escalation.

### Reason for Failure

No misconfigured cron-executed files were writable by the current user.

## Successful Exploitation — Sudo Misconfiguration

Further enumeration revealed a critical sudoers misconfiguration:

sudo -l
The output indicated that the msfadmin user could execute any command as any
user, including root.

Privilege escalation was achieved by executing:

sudo -i
An alternative method using:

sudo su -
was also successful.

## Result

Privilege escalation was successful.

Initial user: msfadmin

Escalated user: root

Root access was verified using:

whoami

id

## Impact

An unrestricted sudo configuration completely compromises system security.
Any local user can gain full administrative access without exploiting
software vulnerabilities.

Lessons Learned
Failed exploitation attempts are valuable for understanding system behavior.

Manual enumeration is critical.

Sudo permissions should always be reviewed early.

Configuration issues are often more dangerous than software bugs.

## Mitigation

Remove (ALL) ALL entries from sudoers unless strictly required.

Apply the principle of least privilege.

Regularly audit sudo configurations.

Monitor and restrict script execution paths.
