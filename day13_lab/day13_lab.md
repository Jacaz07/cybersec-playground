Day 13 – Privilege Escalation (sudo & PATH hijacking)

## Environment
- Attacker: Kali Linux
- Target: Metasploitable2
- Access level: low-privilege user

## Technique 1 – Sudo Misconfiguration
Using sudo -l a NOPASSWD entry was discovered.
Allowed binary: vim.
Root shell obtained via vim escape.

## Technique 2 – PATH Hijacking
Writable directory present in PATH.
Script executed command without absolute path.
Malicious binary injected resulting in root shell.

## Impact
Full system compromise.

## Mitigation
- Avoid NOPASSWD
- Use absolute paths
- Restrict PATH
- Regular audits
