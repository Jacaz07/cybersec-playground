Day 19 – Kioptrix Level 1

## Target

- Name: Kioptrix Level 1
- IP: 192.168.56.105
- OS: Linux Kernel 2.4.x
- Difficulty: Easy
- Source: VulnHub

## Attacker

- OS: Kali Linux
- IP: 192.168.56.101
- Network: Host-only

## Objective

Gain root access on Kioptrix Level 1 through enumeration, exploitation and privilege escalation.

---

## Enumeration

### Network Discovery

Target identified via ARP scan in host-only network.

### Port Scanning

Nmap scan revealed multiple outdated services including Apache, OpenSSL, Samba and RPC.

Key findings:
- Apache 1.3.20
- OpenSSL 0.9.6b
- mod_ssl 2.8.4
- Linux kernel 2.4.x

---

## Initial Access

HTTPS service on port 443 was vulnerable to OpenSSL/mod_ssl remote buffer overflow.

Exploit used:
- OpenFuck v3.0.4

Result:
- Remote shell obtained as user apache

---

## Post-Exploitation

Confirmed limited privileges:
- User: apache
- No access to /etc/shadow
- Kernel version vulnerable to known local privilege escalation exploits

---

## Privilege Escalation

Used local ptrace kernel exploit compatible with Linux kernel 2.4.x.

Exploit was transferred to the target, compiled locally and executed.

Result:
- Root shell obtained

---

## Proof of Compromise

- whoami → root
- id → uid=0(root)

---

## Conclusion

The system was fully compromised due to:
- Outdated OpenSSL and Apache
- Lack of patching
- Vulnerable kernel

Root access achieved successfully.
