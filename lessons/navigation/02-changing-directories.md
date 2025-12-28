---
title: Changing Directories with cd
description: Learn how to navigate between folders using the cd command
order: 2
---

## Instructions

Navigation is one of the most fundamental skills in the terminal. Just like clicking on folders in a file manager, you need to know how to move between directories in the terminal.

### The cd Command

`cd` stands for "change directory". It's how you move from one folder to another.

### Basic Navigation

Here are the essential `cd` commands you'll use:

1. **`cd directory_name`** - Move into a specific directory
   ```bash
   cd Documents
   ```

2. **`cd ..`** - Move up one directory (to the parent folder)
   ```bash
   cd ..
   ```

3. **`cd ~` or `cd`** - Go to your home directory
   ```bash
   cd ~
   # or simply
   cd
   ```

4. **`cd /`** - Go to the root directory (the top of the file system)
   ```bash
   cd /
   ```

5. **`cd -`** - Go back to the previous directory you were in
   ```bash
   cd -
   ```

### Pro Tips

- You can use **Tab completion**: Start typing a directory name and press Tab to auto-complete
- You can use **absolute paths** (starting with `/`) or **relative paths** (relative to where you are)
- Use `ls` before `cd` to see what directories are available

## Exercise 1: Navigate to Your Home Directory

First, make sure you're in your home directory using the `cd` command.

**Command:** `cd ~`

**Verify:**
```yaml
type: current_directory
path: ~
```

## Exercise 2: Explore Your File System

Navigate to a common directory. Try going to `/tmp` (a temporary directory that exists on most Linux systems).

**Command:** `cd /tmp`

**Verify:**
```yaml
type: current_directory
path: /tmp
```

## Exercise 3: Go Back Home

Now navigate back to your home directory.

**Command:** `cd ~`

**Verify:**
```yaml
type: current_directory
path: ~
```

## Exercise 4: Navigate Up and Down

1. First, make sure you're in your home directory: `cd ~`
2. List the contents with `ls` to see what directories are available
3. Choose a directory (like `Documents`, `Downloads`, or `Desktop` if they exist) and navigate into it
4. Use `cd ..` to go back up one level

**Command:** `cd Documents` (or another directory you see), then `cd ..`

**Verify:**
```yaml
type: current_directory
path: ~
```

Great work! You're now comfortable navigating the file system. Next, we'll learn how to create your own directories and files.

