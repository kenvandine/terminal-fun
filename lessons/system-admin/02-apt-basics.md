---
title: Package Management with apt
description: Learn to install and manage software with apt on Debian/Ubuntu
order: 2
---

## Instructions

On Debian-based systems (Ubuntu, Linux Mint, etc.), `apt` is the primary tool for installing and managing software packages.

### What is apt?

`apt` (Advanced Package Tool) is a package manager that:
- Installs software from repositories
- Handles dependencies automatically
- Updates installed software
- Removes unwanted software

### Updating Package Lists

Always update before installing:

```bash
sudo apt update
```

This fetches the latest package information from repositories. It doesn't install anything, just updates the list of available packages.

### Upgrading Packages

**Upgrade all installed packages:**

```bash
sudo apt upgrade
```

**Full upgrade (handles dependencies better):**

```bash
sudo apt full-upgrade
```

**Upgrade + clean up:**

```bash
sudo apt update && sudo apt upgrade -y
```

The `-y` flag automatically answers "yes" to prompts.

### Installing Packages

**Install a package:**

```bash
sudo apt install package-name
```

**Install multiple packages:**

```bash
sudo apt install package1 package2 package3
```

**Install without prompts:**

```bash
sudo apt install -y package-name
```

**Common packages to try:**

```bash
sudo apt install curl
sudo apt install git
sudo apt install htop
sudo apt install tree
```

### Removing Packages

**Remove a package (keep config files):**

```bash
sudo apt remove package-name
```

**Remove package and config files:**

```bash
sudo apt purge package-name
```

**Remove unused dependencies:**

```bash
sudo apt autoremove
```

### Searching for Packages

**Search for a package:**

```bash
apt search keyword
```

**Show package details:**

```bash
apt show package-name
```

**List all installed packages:**

```bash
apt list --installed
```

**List upgradeable packages:**

```bash
apt list --upgradeable
```

### Cleaning Up

**Remove cached package files:**

```bash
sudo apt clean
```

**Remove old cached packages:**

```bash
sudo apt autoclean
```

**Full cleanup:**

```bash
sudo apt autoremove && sudo apt autoclean
```

### Common Workflows

**Install new software:**

```bash
sudo apt update
sudo apt install package-name
```

**Update your system:**

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

**Remove software completely:**

```bash
sudo apt purge package-name
sudo apt autoremove
```

### Best Practices

1. **Always `apt update` before installing** to get latest versions
2. **Regularly upgrade** to get security updates
3. **Use `autoremove`** periodically to clean up unused packages
4. **Be careful with purge** - config files are deleted
5. **Read what apt wants to do** before confirming

## Exercise 1: Update Package Lists

Update your package lists using apt update.

**Command:** `sudo apt update`

**Verify:**
```yaml
type: command_output
command: echo "Update completed"
contains: completed
```

## Exercise 2: Search for a Package

Search for packages related to "curl".

**Command:** `apt search curl | head -n 10`

**Verify:**
```yaml
type: command_output
command: apt search curl | head -n 10
```

## Exercise 3: Show Package Information

Get detailed information about the `curl` package.

**Command:** `apt show curl`

**Verify:**
```yaml
type: command_output
command: apt show curl
contains: Package
```

## Exercise 4: List Installed Packages

List all installed packages and count them.

**Command:** `apt list --installed | wc -l`

**Verify:**
```yaml
type: command_output
command: apt list --installed | wc -l
```

Excellent work! You've learned:
- How to update package lists with `apt update`
- Installing packages with `apt install`
- Upgrading with `apt upgrade`
- Removing software with `apt remove` and `apt purge`
- Searching and showing package info
- Cleaning up with `autoremove` and `autoclean`

You can now manage software on Debian/Ubuntu systems!
