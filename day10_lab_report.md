
Day 10 – Privilege Escalation (Cron Jobs & Password Enumeration)

## 1. Environment

Attacker Machine:
- Kali Linux

Target Machine: 
- Metasploitable2

Network Configuration: 
- Adapter 1: NAT (Internet access for Kali) 
- Adapter 2: Host-Only / Isolated Network 
- Communication between Kali and Metasploitable confirmed


## 2. Initial Access

Initial access to the target system was obtained through a vulnerable web service exposed on the Metasploitable2 machine. 
Using a WebDAV misconfiguration, a PHP web shell was successfully uploaded and executed.

The initial shell was obtained with the following privileges:

whoami
www-data

## 3. Privilege Escalation – Method A: Cron Job Abuse

3.1 Cron Enumeration

The system was checked for scheduled cron jobs that are executed with elevated privileges:  

ls -la /etc/cron*        

The following directories were analyzed in detail:

/etc/cron.d

/etc/cron.daily

/etc/cron.hourly

During enumeration, a cron script was identified that was executed by the root user and had insecure file permissions.

3.2 Vulnerability Identified

A cron script located in 

/etc/cron.daily 

was found to be world-writable or writable by a non-root user.

This allowed modification of the script contents without administrative privileges.

This is a critical misconfiguration, as any command added to this script will be executed automatically by the system with root privileges.

3.3 Exploitation

A malicious command was appended to the vulnerable cron script:

echo "chmod u+s /bin/bash" >> /etc/cron.daily/backup.sh 

This command sets the SUID bit on /bin/bash, allowing it to be executed with root privileges by any user. 

3.4 Privilege Escalation Result

After waiting for the cron job to execute, the permissions of /bin/bash were verified: 

ls -l /bin/bash  

Output confirmed the SUID bit was set:  

-rwsr-xr-x  

A root shell was then obtained:  /bin/bash -p 

Verification: whoami
root  id
uid=0(root) gid=0(root) groups=0(root)      

## 4. Privilege Escalation – Method B: Password Enumeration

4.1 passwd File Review

The /etc/passwd file was reviewed for misconfigurations such as:

Accounts without passwords

Suspicious UID 0 assignments   

cat /etc/passwd  

No immediate passwordless root account was identified, but this step confirmed system user structure.

4.2 Credential Hunting

The system was searched for hardcoded credentials in commonly misconfigured locations:

grep -Ri "password" /var/www 2>/dev/null
grep -Ri "pass" / 2>/dev/null


This method targets:

Web application configuration files

Backup files

Legacy scripts

Credential reuse or plaintext password storage could potentially allow privilege escalation via su or ssh.

## 5. Proof of Compromise

Non-Privileged User

whoami

www-data

Root User

whoami

root

id

uid=0(root) gid=0(root)


This confirms a successful escalation from a low-privileged web user to full system administrator (root).

## 6. Security Impact

The identified vulnerabilities allow:

Full system compromise

Persistence via cron jobs

Execution of arbitrary commands as root

Complete loss of system integrity and confidentiality

The attack required no credentials and relied entirely on misconfigurations.

## 7. Recommendations

Ensure all cron jobs are owned by root and not writable by non-privileged users

Regularly audit /etc/cron* directories

Remove unnecessary services and legacy scripts

Implement file integrity monitoring

Restrict WebDAV write permissions or disable WebDAV if not required

## 8. Conclusion

This lab demonstrated a full privilege escalation attack path using classic Linux misconfigurations.

By combining proper enumeration with insecure cron job permissions, root access was achieved without exploiting a kernel vulnerability.

This scenario reflects real-world privilege escalation techniques commonly observed during internal penetration tests.
