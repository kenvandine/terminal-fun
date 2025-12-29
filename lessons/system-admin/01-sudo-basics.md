---
title: Understanding sudo
description: Learn to run commands with administrator privileges
order: 1
---

## Instructions

Many system operations require administrator (root) privileges. The `sudo` command lets you run commands as the superuser safely.

### What is sudo?

`sudo` stands for "**s**uper**u**ser **do**". It allows permitted users to run commands as root (administrator) or another user.

### Why Use sudo Instead of Root?

**Benefits of sudo:**
1. **Accountability**: Commands are logged with the user who ran them
2. **Safety**: You must explicitly use sudo for each command
3. **Limited scope**: Only specific commands need elevated privileges
4. **Temporary**: Privileges aren't permanent

**Danger of root:** Logging in as root gives unlimited power - one mistake can destroy your system!

### Basic sudo Usage

Run a single command as root:

```bash
sudo command
```

**Example:** Update package lists:

```bash
sudo apt update
```

You'll be prompted for **your password** (not root's password).

### Common sudo Patterns

**Install software:**

```bash
sudo apt install package-name
```

**Edit system files:**

```bash
sudo nano /etc/hosts
```

**Restart services:**

```bash
sudo systemctl restart nginx
```

**View system logs:**

```bash
sudo cat /var/log/syslog
```

### sudo Options

**Run as different user:**

```bash
sudo -u username command
```

**Open a root shell (be careful!):**

```bash
sudo -i
# or
sudo su
```

**Run previous command with sudo:**

```bash
sudo !!
```

This is useful when you forget to add sudo!

**Check if you have sudo access:**

```bash
sudo -v
```

**List your sudo privileges:**

```bash
sudo -l
```

### The sudo Password Cache

After entering your password, sudo remembers it for **15 minutes** (default). This prevents constant password prompts.

**Clear the password cache:**

```bash
sudo -k
```

### Best Practices

1. **Think before using sudo** - you're working with elevated privileges
2. **Never run untrusted scripts with sudo**
3. **Don't use sudo to fix permission problems** if not needed
4. **Avoid `sudo rm -rf`** without triple-checking
5. **Don't stay logged in as root** - use sudo for individual commands
6. **Review commands** before pressing Enter with sudo

### Common Mistakes to Avoid

**❌ Don't do this:**

```bash
sudo chmod 777 /
```

**❌ Or this:**

```bash
sudo rm -rf / --no-preserve-root
```

**❌ Or this:**

```bash
sudo cat /dev/random > /dev/sda
```

These commands can destroy your system!

## Exercise 1: Check sudo Access

Verify you have sudo access by running a simple command.

**Command:** `sudo -v`

**Verify:**
```yaml
type: command_output
command: echo "sudo access verified"
contains: verified
```

## Exercise 2: List sudo Privileges

Check what sudo privileges you have using `sudo -l`.

**Command:** `sudo -l`

**Verify:**
```yaml
type: command_output
command: sudo -l
```

## Exercise 3: Run a Command with sudo

Use sudo to view a file that typically requires root access (if it exists).

**Command:** `sudo cat /etc/sudoers | head -n 5`

**Verify:**
```yaml
type: command_output
command: sudo cat /etc/sudoers | head -n 5
```

## Exercise 4: Create a System Directory

Create a directory in `/tmp` with sudo (for practice - /tmp usually doesn't require sudo).

**Command:** `sudo mkdir /tmp/test_sudo_dir`

**Verify:**
```yaml
type: directory_exists
path: /tmp/test_sudo_dir
```

Perfect! You now understand:
- What sudo is and why it's important
- How to run commands with sudo
- Common sudo patterns and options
- Best practices for safe sudo usage
- Common mistakes to avoid

Remember: With great power comes great responsibility!
