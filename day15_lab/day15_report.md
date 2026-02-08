Day 15 – Privilege Escalation via SUID Binary Abuse

## Objective

The objective of this lab was to identify and exploit a misconfigured SUID binary on the target system (Metasploitable2) in order to escalate privileges from a regular user (msfadmin) to root.

The goal was achieved by enumerating SUID binaries and abusing one of them to spawn a privileged shell.

## Enumeration

System access

Initial access was obtained via SSH as a low-privileged user:

user: msfadmin

SUID binary discovery

The following command was used to locate binaries with the SUID bit set:

find / -perm -4000 -type f 2>/dev/null

## Findings

Among the discovered binaries, the following were of particular interest:

/usr/bin/nmap

/usr/bin/passwd

/usr/bin/sudo

The presence of nmap with SUID permissions is especially dangerous, as older versions allow execution of a shell.

## Exploitation

Abusing SUID nmap

The vulnerable binary was executed with interactive mode:

nmap --interactive


Inside the interactive prompt, a shell was spawned:

!sh

Result

The spawned shell inherited root privileges due to the SUID bit on the binary.

Verification:

whoami


Output:

root


Privilege escalation was successfully completed.

## Why it worked (SUID explanation)

SUID (Set User ID) is a special permission that allows a binary to run with the privileges of its owner, not the user executing it.

In this case:

The binary nmap was owned by root

The SUID bit was set

When executed by msfadmin, the process ran with root privileges

Because the installed version of nmap allows shell execution (!sh), this resulted in a full root shell.

This is a classic example of dangerous SUID misconfiguration.

## Impact

If exploited on a real system, this vulnerability would allow an attacker to:

Gain full root access

Read or modify sensitive system files

Install backdoors

Disable security mechanisms

Take complete control of the system

This represents a critical security risk.

## Mitigation

To prevent this type of vulnerability:

Remove SUID bit from non-essential binaries:

chmod -s /usr/bin/nmap


Uninstall unnecessary tools from production systems

Regularly audit SUID binaries:

find / -perm -4000 -type f


Use updated software versions that do not allow shell escapes

Apply the principle of least privilege

## Conclusion

This lab demonstrates how a single misconfigured SUID binary can lead to full system compromise. Proper permission management and regular audits are essential to maintaining system security.
