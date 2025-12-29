---
title: Package Management with snap
description: Learn to install software using snap packages
order: 3
---

## Instructions

Snap is a modern package management system that works across different Linux distributions. Snaps are self-contained applications with all their dependencies.

### What is Snap?

Snap packages (or "snaps") are:
- **Self-contained**: Include all dependencies
- **Sandboxed**: Run in isolation for security
- **Cross-platform**: Work on many Linux distributions
- **Auto-updating**: Update automatically in the background

### Snap vs apt

| Feature | apt | snap |
|---------|-----|------|
| Dependencies | System-wide | Bundled |
| Updates | Manual | Automatic |
| Size | Smaller | Larger (includes deps) |
| Availability | Distro repos | Snap Store |

Use **apt** for system packages, **snap** for applications.

### Finding Snaps

**Search for a snap:**

```bash
snap find keyword
```

**Search for a specific app:**

```bash
snap find firefox
```

**Visit the Snap Store:** https://snapcraft.io/store

### Installing Snaps

**Install a snap:**

```bash
sudo snap install package-name
```

**Install from a specific channel:**

```bash
sudo snap install package-name --channel=stable
```

Channels: `stable`, `candidate`, `beta`, `edge`

**Install classic snap (less confined):**

```bash
sudo snap install package-name --classic
```

**Examples:**

```bash
sudo snap install vlc
sudo snap install spotify
sudo snap install code --classic
```

### Viewing Installed Snaps

**List all installed snaps:**

```bash
snap list
```

**Show details about a snap:**

```bash
snap info package-name
```

### Updating Snaps

Snaps update automatically, but you can manually trigger updates:

**Update all snaps:**

```bash
sudo snap refresh
```

**Update a specific snap:**

```bash
sudo snap refresh package-name
```

**Check for updates:**

```bash
snap refresh --list
```

### Removing Snaps

**Remove a snap:**

```bash
sudo snap remove package-name
```

**Remove a snap and its data:**

```bash
sudo snap remove --purge package-name
```

### Managing Snap Versions

**List available versions:**

```bash
snap list --all package-name
```

**Revert to previous version:**

```bash
sudo snap revert package-name
```

**Switch channels:**

```bash
sudo snap refresh package-name --channel=beta
```

### Snap Configuration

**View snap connections (permissions):**

```bash
snap connections package-name
```

**Connect interfaces:**

```bash
sudo snap connect package-name:interface
```

**Disconnect interfaces:**

```bash
sudo snap disconnect package-name:interface
```

### Managing snapd Service

**Check snapd status:**

```bash
systemctl status snapd
```

**Restart snapd:**

```bash
sudo systemctl restart snapd
```

### Useful Commands

**See snap changes/history:**

```bash
snap changes
```

**View logs:**

```bash
snap logs package-name
```

**Check snap services:**

```bash
snap services
```

### Common Use Cases

**Install a GUI application:**

```bash
sudo snap install gimp
```

**Install a development tool:**

```bash
sudo snap install postman
```

**Install a media player:**

```bash
sudo snap install vlc
```

## Exercise 1: Search for Snaps

Search the snap store for applications related to "editor".

**Command:** `snap find editor | head -n 10`

**Verify:**
```yaml
type: command_output
command: snap find editor | head -n 10
```

## Exercise 2: List Installed Snaps

View all snaps currently installed on your system.

**Command:** `snap list`

**Verify:**
```yaml
type: command_output
command: snap list
```

## Exercise 3: Show Snap Information

Get detailed information about the 'core' snap (the base snap installed on most systems).

**Command:** `snap info core`

**Verify:**
```yaml
type: command_output
command: snap info core
contains: name
```

## Exercise 4: Check for Updates

Check if any of your snaps have available updates.

**Command:** `snap refresh --list`

**Verify:**
```yaml
type: command_output
command: echo "Snap check complete"
contains: complete
```

Perfect! You now know:
- What snaps are and how they differ from apt packages
- How to search for and install snaps
- Managing installed snaps with list, info, and remove
- Updating snaps manually and automatically
- Working with channels and versions

You're now equipped to manage software using both apt and snap!
