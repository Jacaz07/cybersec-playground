# Day 20 – SQL Injection (Blind) & Command Injection Analysis

## Target

- IP: 192.168.56.106
- Application: Remote System Administration Login
- Technology:
- OS: Linux CentOS 4
- Web Server: Apache 2.0.52
- Backend: PHP 4.3.9
- Database: MySQL < 5.0.12

## Objectives

- Bypass authentication
- Identify SQL Injection
- Verify command injection via ping functionality
- Attempt data extraction

## Step 1 – Authentication Bypass (SQL Injection)

The login form was vulnerable to SQL Injection in the uname parameter.

 Payload:

admin' OR '1'='1

Result:

Successful authentication bypass

Access to administrative panel

## Step 2 – SQL Injection Verification (sqlmap)

Tool: sqlmap

Findings:

Parameter uname is injectable

Injection types:

Boolean-based blind

Time-based blind (BENCHMARK)

Database identified:

MySQL < 5.0.12

Current database: webapp

Limitations:

Unable to enumerate tables

Time-based blind extraction unstable

## Step 3 – Command Injection Testing (pingit.php)

The application allows users to submit an IP address to be pinged.

Tested payloads:

127.0.0.1;id

127.0.0.1 && id

127.0.0.1 | id

id

$(id)

## Observations:

Most operators were sanitized or echoed

Command substitution via $() executed locally

Output reflected client-side execution, not server-side

## Conclusion:

No confirmed server-side OS command execution

Application reflects input without proper validation

Potential false-positive command injection

## Impact

Authentication bypass allows unauthorized admin access

SQL Injection confirmed (blind)

No verified RCE on server

## Recommendations

Use prepared statements (PDO / MySQLi)

Sanitize and validate user input

Disable command execution functions

Implement proper session handling
