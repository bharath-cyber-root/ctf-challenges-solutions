# Easy Linux CTF Challenge - Hidden Permissions

## Challenge Description
A simple Linux CTF challenge focused on file permissions and hidden files. This challenge is designed for beginners to understand basic Linux security concepts.

## Scenario
You've been given access to a Linux server. There's a flag hidden somewhere in the `/home/ctfuser` directory, but it's not immediately visible. Can you find it?

## Challenge Setup
```bash
# Create the challenge environment
mkdir -p /home/ctfuser/.secret
echo "CTF{l1nux_p3rm1ss10ns_m4tt3r}" > /home/ctfuser/.secret/flag.txt
chmod 400 /home/ctfuser/.secret/flag.txt
chmod 500 /home/ctfuser/.secret
```

## Skills Required
- Basic Linux command line navigation
- Understanding of hidden files/directories (files starting with `.`)
- File permission concepts
- Using `ls -la` command

## Solution

### Step 1: List all files including hidden ones
```bash
ls -la /home/ctfuser
```
This will reveal the `.secret` directory.

### Step 2: Navigate to the hidden directory
```bash
cd /home/ctfuser/.secret
```

### Step 3: List files in the hidden directory
```bash
ls -la
```
This reveals `flag.txt`.

### Step 4: Read the flag
```bash
cat flag.txt
```

### Output
```
CTF{l1nux_p3rm1ss10ns_m4tt3r}
```

## Learning Objectives
- Understanding that files/directories starting with `.` are hidden in Linux
- Using `-a` flag with `ls` to show all files including hidden ones
- Using `-l` flag to see detailed file information including permissions
- Understanding basic file permissions (read, write, execute)

## Difficulty Level
**Easy** - Suitable for beginners

## Tags
`linux` `permissions` `hidden-files` `beginner` `enumeration`
