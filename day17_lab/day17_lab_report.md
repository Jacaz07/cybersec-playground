Day 17 — Local Privilege Escalation via SUDO Misconfiguration

## Objective

The goal of this lab was to identify and exploit a local privilege escalation
vector on the Metasploitable2 system after obtaining a low-privileged shell
as the msfadmin user.

The objective was to enumerate the system, test multiple realistic LPE vectors,
and finally achieve full root access.

##  Enumeration

whoami

Result:

msfadmin

Writable files and directories (initial checks)

Attempts to find writable files in /etc and system-wide writable files:

find /etc -type f -writable 2>/dev/null

find / -type f -writable 2>/dev/null

➡️ No output returned — no directly writable critical system files.

World-writable directories

find / -type d -perm -o+w 2>/dev/null

Interesting results:

/tmp

/var/tmp

/dev/shm

/var/www/dav

multiple TWiki directories under /var/www/twiki

Web directory analysis

ls -la /var/www/dav

Result:

drwxrwxrwt  2 root root     4096 .

-rw-r--r--  1 www-data www-data shell.php

This directory is world-writable and web-accessible but not used by cron or
executed by root, making it unsuitable for direct privilege escalation.

Cron jobs inspection

cat /etc/crontab

No writable cron entries found.

However, a custom cron script was discovered:

ls -l /etc/cron.daily/backup.sh

cat /etc/cron.daily/backup.sh

Content:

chmod u+s /bin/bash

chmod u+s /bin/bash

Despite the script being owned by root, it was not writable and could not
be modified by msfadmin.

Manual execution using run-parts failed due to insufficient privileges,
confirming this vector was not exploitable at this stage.

PATH hijacking attempt (FAILED)

An attempt was made to hijack the tar binary by placing a fake executable
in /tmp and modifying $PATH.

export PATH=/tmp:$PATH

sudo ./backup.sh

Result:

Command executed without errors

No privilege escalation occurred

whoami still returned msfadmin

Reason:

Script was not executed in a privileged cron context

PATH hijacking did not affect root-owned execution

##  Exploitation — SUDO Misconfiguration

Enumerating sudo permissions

sudo -l

Result:

User msfadmin may run the following commands on this host:
    (ALL) ALL

This indicates a critical misconfiguration where the user msfadmin
can execute any command as any user, including root.

Privilege escalation

sudo -i

or:

sudo su -

Verification

whoami

id

Result:

uid=0(root) gid=0(root) groups=0(root)

Full root access achieved.

Why It Worked

The /etc/sudoers configuration allowed unrestricted access:

(ALL) ALL means any command can be run as any user

No command restrictions were applied

Password requirement does not mitigate risk if credentials are known

This is a configuration-based privilege escalation, not a binary exploit.

##  Impact

Complete system compromise

Ability to:

Read /etc/shadow

Modify system services

Install persistence mechanisms (cron, SUID, users)

Disable logging and security controls

##  Mitigation

Apply the principle of least privilege

Restrict sudo access to specific commands

Use NOPASSWD sparingly and only where required

Regularly audit /etc/sudoers

Monitor sudo usage logs

##  Key Takeaways

Not all writable directories lead to privilege escalation

Cron jobs must be both writable and executed as root

PATH hijacking only works when executed in a privileged context

SUDO misconfiguration remains one of the most dangerous real-world LPE vectors
