---
title: Viewing Processes
description: Learn to view and monitor running processes with ps, top, and htop
order: 1
---

## Instructions

Everything running on your Linux system is a process - programs, services, background tasks. Learning to view and manage processes is essential for system administration.

### What is a Process?

A process is a running instance of a program. Each process has:
- A unique **PID** (Process ID)
- An **owner** (user who started it)
- **Memory** and **CPU** usage
- A **parent process** that started it

### Viewing Processes with ps

The `ps` command shows running processes:

```bash
ps
```

This shows only your processes in the current terminal.

**Show all processes:**

```bash
ps aux
```

- `a`: show processes from all users
- `u`: show user-oriented format
- `x`: show processes not attached to a terminal

**Find specific processes:**

```bash
ps aux | grep firefox
```

### Understanding ps Output

```
USER  PID  %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
john  1234  2.5  1.2 234567 12345 ?     Sl   10:30   0:05 firefox
```

- **USER**: Who owns the process
- **PID**: Process ID
- **%CPU**: CPU usage percentage
- **%MEM**: Memory usage percentage
- **STAT**: Process state (R=running, S=sleeping, Z=zombie)
- **COMMAND**: The program name

### Interactive Process Viewer: top

The `top` command shows processes in real-time:

```bash
top
```

Useful keys in top:
- `q`: quit
- `k`: kill a process (asks for PID)
- `M`: sort by memory usage
- `P`: sort by CPU usage
- `h`: help

### Better Alternative: htop

If available, `htop` is a more user-friendly version:

```bash
htop
```

Features:
- Color-coded display
- Mouse support
- Tree view of processes
- Easy sorting and filtering

### Viewing Process Tree

See process relationships:

```bash
ps auxf
```

Or use `pstree`:

```bash
pstree
```

## Exercise 1: View Your Processes

Use `ps` to see processes running in your current terminal.

**Command:** `ps`

**Verify:**
```yaml
type: command_output
command: ps
contains: PID
```

## Exercise 2: View All Processes

Use `ps aux` to see all processes on the system. Pipe to `head` to see just the first 10.

**Command:** `ps aux | head -n 10`

**Verify:**
```yaml
type: command_output
command: ps aux | head -n 10
contains: USER
```

## Exercise 3: Find Specific Processes

Use `ps aux` with `grep` to find all bash processes.

**Command:** `ps aux | grep bash`

**Verify:**
```yaml
type: command_output
command: ps aux | grep bash
contains: bash
```

## Exercise 4: Check Process Count

Count how many processes are running on your system.

**Command:** `ps aux | wc -l`

**Verify:**
```yaml
type: command_output
command: ps aux | wc -l
```

Excellent work! You can now:
- View processes with `ps`
- Monitor processes in real-time with `top`
- Find specific processes with `grep`
- Understand process information (PID, CPU, memory)

Next, you'll learn how to manage these processes!
