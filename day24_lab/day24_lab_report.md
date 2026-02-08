# Day 24 – CUPS 1.1 Remote Command Execution → Root  

## Lab Report

### Objective

The goal of Day 24 was to gain root access through the Remote Command Execution vulnerability in CUPS 1.1 and learn how to correctly analyze the feasibility of an exploit depending on the system configuration.

### Target Information

- IP: 192.168.56.106
- OS: CentOS (legacy)
- Web Server: Apache/2.0.52
- Services observed:
  - HTTP (80)
  - HTTPS (443)
  - CUPS (631 – filtered / restricted)

### Enumeration Summary

#### Web Application

- HTTPS application available at /index.php
- Login panel: "Remote System Administration Login"
- No visible error messages
- No SQL injection confirmed during basic testing
- Apache manual fully exposed under /manual/

#### CUPS

- Service reachable but restricted
- All administrative and enumeration endpoints return 403 Forbidden
- Remote access to CUPS denied
- No ability to trigger printer/job-based command execution

### Exploitation Attempts

#### CUPS 1.1 RCE

- Attempted enumeration using:
  - lpstat
  - lpinfo
- Remote interaction denied
- Injection attempts rejected by input validation
- Required conditions for exploit not met:
  - No local access
  - No administrative CUPS privileges
  - Restricted configuration

#### Web-based Attacks

- Directory brute-force revealed only default Apache documentation
- No custom administrative endpoints discovered
- Login form resistant to trivial SQL injection attempts

### Key Findings

- Presence of a vulnerable version (CUPS 1.1) does not guarantee exploitability
- Service configuration and access scope are critical factors
- CUPS RCE requires local or privileged interaction in this environment
- The lab intentionally presents a false-positive exploit path

### Conclusion

The CUPS 1.1 Remote Command Execution vulnerability is not exploitable remotely
on this system due to restrictive configuration and access controls.

The true purpose of Day 24 is to:
- Train recognition of dead-end exploit paths
- Avoid tunnel vision based on version numbers alone
- Practice disciplined enumeration and decision-making

The correct outcome of this lab is analysis and rejection of the exploit path,
not forced exploitation.

### Lessons Learned

- Enumeration > exploitation
- Configuration matters more than CVE presence
- Abandoning an exploit is a valid and professional decision
- Real-world pentesting involves rejecting most initial hypotheses

### Status

- Initial Access: Not achieved
- Root Access: Not applicable
- Lab Objective (Analytical): Achieved
