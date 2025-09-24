# TryHackMe - Alfred

**Platform:** TryHackMe  
**Category:** Web Application Security  
**Difficulty:** Easy  
**Author:** TryHackMe

## Challenge Description

Alfred is a vulnerable web application that demonstrates common web security flaws. This challenge focuses on gaining initial access through web vulnerabilities and escalating privileges on a Windows system.

## Target Information

- **Target IP:** 10.10.x.x (assigned by TryHackMe)
- **Services:** HTTP (Port 80), Jenkins (Port 8080)
- **OS:** Windows Server

## Reconnaissance

### Port Scanning
```bash
nmap -sC -sV -oA alfred 10.10.x.x
```

**Key Findings:**
- Port 80: HTTP (IIS)
- Port 8080: Jenkins CI/CD Server
- Port 3389: RDP (filtered)

### Web Enumeration

#### Main Web Application (Port 80)
- Static website with potential email harvesting
- No obvious vulnerabilities on main site

#### Jenkins Server (Port 8080)
- Default Jenkins installation
- No authentication required
- Administrative access available

## Exploitation

### Initial Access - Jenkins Code Execution

1. **Access Jenkins Dashboard**
   - Navigate to `http://10.10.x.x:8080`
   - No authentication required

2. **Create Malicious Build Job**
   - Click "New Item"
   - Create "Freestyle project"
   - Configure build to execute system commands

3. **Reverse Shell Payload**
   - Use Windows PowerShell reverse shell
   - Configure listener on attacking machine

### Privilege Escalation

#### Method 1: Token Impersonation
- Check current privileges with `whoami /priv`
- Look for `SeImpersonatePrivilege`
- Use token impersonation techniques

#### Method 2: Service Exploitation
- Enumerate running services
- Check for unquoted service paths
- Look for weak service permissions

## Tools Used

- **nmap:** Port scanning and service enumeration
- **Jenkins:** Code execution platform
- **PowerShell:** Reverse shell and enumeration
- **Metasploit:** Privilege escalation modules
- **nc/netcat:** Listener for reverse shells

## Key Vulnerabilities

1. **Unauthenticated Jenkins Access**
   - No authentication required for administrative functions
   - Allows arbitrary code execution

2. **Weak Windows Privileges**
   - Service account with excessive privileges
   - Token impersonation possible

3. **Insecure Service Configuration**
   - Services running with SYSTEM privileges
   - Exploitable through various methods

## Lessons Learned

### Security Misconfigurations
- **Jenkins Security:** Always enable authentication and authorization
- **Service Hardening:** Run services with minimal required privileges
- **Network Segmentation:** Isolate CI/CD systems from production

### Detection and Prevention
- Monitor for unusual Jenkins activity
- Implement proper access controls
- Regular security audits of CI/CD pipelines
- Use least privilege principle

## Remediation

### Immediate Actions
1. Enable Jenkins authentication
2. Configure proper authorization matrix
3. Update Jenkins to latest version
4. Review service account privileges

### Long-term Security
1. Implement network segmentation
2. Regular vulnerability assessments
3. Security awareness training
4. Incident response procedures

## References

- [TryHackMe Alfred Room](https://tryhackme.com/room/alfred)
- [Jenkins Security Documentation](https://www.jenkins.io/doc/book/security/)
- [Windows Privilege Escalation Guide](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
- [PowerShell Reverse Shells](https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3)

## Disclaimer

⚠️ **Educational Purpose Only**

This writeup is for educational and ethical hacking purposes only. Only use these techniques on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.

---

*Last Updated: September 2025*
*Challenge Completed: TryHackMe Alfred Room*
