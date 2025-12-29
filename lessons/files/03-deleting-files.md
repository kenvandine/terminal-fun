---
title: Deleting Files and Directories
description: Learn to safely remove files with rm and rmdir
order: 3
---

## Instructions

Deleting files and directories is a powerful but dangerous operation. Unlike graphical file managers, the terminal doesn't have a "Recycle Bin" - deleted files are gone forever!

### Removing Files with rm

The `rm` command removes (deletes) files:

```bash
rm filename.txt
```

Remove multiple files:

```bash
rm file1.txt file2.txt file3.txt
```

Remove files matching a pattern:

```bash
rm *.txt
```

### Removing Directories

Remove an **empty** directory with `rmdir`:

```bash
rmdir empty_directory
```

Remove a directory and all its contents with `rm -r`:

```bash
rm -r directory_name
```

**⚠️ Warning:** `rm -r` is very dangerous! It recursively deletes everything.

### Safe Deletion Options

Always use these flags for safety:

- **`rm -i`**: Interactive mode (asks for confirmation for each file)
- **`rm -I`**: Prompts once before removing more than 3 files
- **`rm -v`**: Verbose mode (shows what's being deleted)

**Never use `rm -rf` unless you're absolutely certain!** This force-removes everything without asking.

### Best Practices

1. Always double-check before using `rm`
2. Use `ls` first to verify what you're deleting
3. Start with `rm -i` until you're confident
4. Be extra careful with wildcards like `*`
5. Never run `rm -rf /` or `rm -rf /*` (can destroy your system!)

## Exercise 1: Create and Delete a File

Create a test file and then delete it safely.

**Command:** `touch deleteme.txt && rm deleteme.txt`

**Verify:**
```yaml
type: command_output
command: ls deleteme.txt 2>&1
contains: cannot access
```

## Exercise 2: Delete Multiple Files

Create three files, then delete them all at once.

**Command:** `touch file1.txt file2.txt file3.txt && rm file1.txt file2.txt file3.txt`

**Verify:**
```yaml
type: command_output
command: ls file1.txt 2>&1
contains: cannot access
```

## Exercise 3: Remove an Empty Directory

Create an empty directory and remove it with `rmdir`.

**Command:** `mkdir empty_dir && rmdir empty_dir`

**Verify:**
```yaml
type: command_output
command: ls -d empty_dir 2>&1
contains: cannot access
```

## Exercise 4: Remove a Directory with Contents

Create a directory with files, then remove it with `rm -r`.

**Command:** `mkdir test_removal && touch test_removal/file.txt && rm -r test_removal`

**Verify:**
```yaml
type: command_output
command: ls -d test_removal 2>&1
contains: cannot access
```

Excellent! You now understand:
- How to remove files with `rm`
- The difference between `rmdir` and `rm -r`
- Important safety options like `-i`
- Why you must be careful with deletion commands

Remember: With great power comes great responsibility! Always think twice before deleting.
