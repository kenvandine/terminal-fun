---
title: File Permissions
description: Understand and manage file permissions with chmod and chown
order: 5
---

## Instructions

Linux is a multi-user system where security matters. File permissions control who can read, write, or execute files and directories. Understanding permissions is essential for managing your system safely.

### Understanding Permission Structure

When you run `ls -l`, you see permissions like this:

```
-rw-r--r-- 1 user group 1234 Dec 28 10:30 file.txt
drwxr-xr-x 2 user group 4096 Dec 28 10:30 mydir
```

Let's break down the permissions: `-rw-r--r--`

```
-  rw-  r--  r--
│   │    │    │
│   │    │    └─ Others (everyone else)
│   │    └────── Group (users in the file's group)
│   └─────────── Owner (the file's owner)
└─────────────── File type (- = file, d = directory, l = link)
```

### The Three Permission Types

Each position can have one of these permissions:

- **`r`** (read) - Can view the file's contents or list directory contents
- **`w`** (write) - Can modify the file or add/remove files in directory
- **`x`** (execute) - Can run the file as a program or enter the directory

A dash `-` means that permission is not granted.

### Permission Examples

```
-rw-r--r--  # File: owner can read/write, group and others can only read
-rwxr-xr-x  # File: owner can read/write/execute, others can read/execute
drwxr-xr-x  # Directory: owner full access, others can read and enter
-rw-------  # File: only owner can read/write, others have no access
```

### Changing Permissions with chmod

The `chmod` command changes file permissions. There are two ways to use it:

**Symbolic Mode** (easier to read):

```bash
chmod u+x file.txt      # Add execute permission for user (owner)
chmod g-w file.txt      # Remove write permission for group
chmod o+r file.txt      # Add read permission for others
chmod a+x file.txt      # Add execute for all (a = all)
```

Breakdown:
- **Who**: `u` (user/owner), `g` (group), `o` (others), `a` (all)
- **Operation**: `+` (add), `-` (remove), `=` (set exactly)
- **Permission**: `r` (read), `w` (write), `x` (execute)

**Numeric Mode** (faster for experts):

Each permission has a number:
- `r` (read) = 4
- `w` (write) = 2
- `x` (execute) = 1

Add them together for each group:

```bash
chmod 755 file.txt  # rwxr-xr-x (4+2+1, 4+1, 4+1)
chmod 644 file.txt  # rw-r--r-- (4+2, 4, 4)
chmod 600 file.txt  # rw------- (4+2, 0, 0)
chmod 777 file.txt  # rwxrwxrwx (4+2+1, 4+2+1, 4+2+1)
```

Common permission numbers:
- **755** - Standard for directories and executables
- **644** - Standard for regular files
- **600** - Private file (only owner can read/write)
- **700** - Private directory (only owner has access)

### Changing File Ownership

The `chown` command changes who owns a file:

```bash
sudo chown newuser file.txt              # Change owner
sudo chown newuser:newgroup file.txt     # Change owner and group
sudo chown :newgroup file.txt            # Change only group
```

**Note:** You usually need `sudo` to change ownership (unless you own the file and are changing to yourself).

The `chgrp` command changes only the group:

```bash
sudo chgrp newgroup file.txt
```

### Recursive Changes

Use `-R` to change permissions or ownership for a directory and everything inside:

```bash
chmod -R 755 mydir/     # Apply to directory and all contents
chown -R user:group mydir/
```

### Why Permissions Matter

Proper permissions are crucial for:
- **Security** - Prevent unauthorized access to sensitive files
- **Safety** - Prevent accidental deletion or modification
- **Multi-user systems** - Control what other users can see/modify
- **Executables** - Files need `x` permission to run as programs

### Common Permission Scenarios

**Make a script executable:**
```bash
chmod +x script.sh
```

**Make a file private (only you can access):**
```bash
chmod 600 sensitive.txt
```

**Share a directory with your group:**
```bash
chmod 775 shared_folder/
```

**Create a read-only file:**
```bash
chmod 444 important.txt
```

## Exercise 1: View File Permissions

Create a test file and view its permissions using `ls -l`.

**Command:** `touch testfile.txt && ls -l testfile.txt`

**Verify:**
```yaml
type: command_output
command: touch testfile.txt && ls -l testfile.txt
contains: testfile.txt
```

## Exercise 2: Add Execute Permission

Make the test file executable using symbolic mode.

**Command:** `chmod +x testfile.txt && ls -l testfile.txt`

**Verify:**
```yaml
type: command_output
command: chmod +x testfile.txt && ls -l testfile.txt
contains: x
```

## Exercise 3: Remove Write Permission for Group and Others

Remove write permission for group and others using symbolic mode.

**Command:** `chmod go-w testfile.txt && ls -l testfile.txt`

**Verify:**
```yaml
type: command_output
command: chmod go-w testfile.txt && ls -l testfile.txt
```

## Exercise 4: Set Permissions with Numeric Mode

Use numeric mode to set permissions to `644` (rw-r--r--).

**Command:** `chmod 644 testfile.txt && ls -l testfile.txt`

**Verify:**
```yaml
type: command_output
command: chmod 644 testfile.txt && ls -l testfile.txt
contains: rw-r--r--
```

## Exercise 5: Create a Private File

Create a new file and set it to `600` (readable/writable only by you).

**Command:** `touch private.txt && chmod 600 private.txt && ls -l private.txt`

**Verify:**
```yaml
type: command_output
command: touch private.txt && chmod 600 private.txt && ls -l private.txt
contains: rw-------
```

## Exercise 6: Check Directory Permissions

Create a directory and view its default permissions.

**Command:** `mkdir testdir && ls -ld testdir`

**Verify:**
```yaml
type: command_output
command: mkdir testdir && ls -ld testdir
contains: testdir
```

Excellent work! You've learned:
- How to read permission strings like `rwxr-xr-x`
- The three permission types: read, write, execute
- How to change permissions with `chmod` (both symbolic and numeric)
- How to change ownership with `chown` and `chgrp`
- Why permissions are crucial for security
- Common permission patterns (644, 755, 600, 700)

**Security Best Practices:**
- Never use `chmod 777` (gives everyone full access - dangerous!)
- Keep sensitive files at `600` or `400`
- Keep directories at `755` or `700`
- Only give `x` permission to files that need to be executed
- Be careful with `sudo chown` - it's hard to undo
- Use `chmod -R` carefully - it affects everything inside

**Pro Tip:** When in doubt, use `ls -l` to check current permissions before changing them!
