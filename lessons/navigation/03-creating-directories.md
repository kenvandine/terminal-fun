---
title: Creating Directories with mkdir
description: Learn how to create new folders using mkdir
order: 3
---

## Instructions

Now that you can navigate the file system, let's learn how to create your own directories (folders) using the `mkdir` command.

### The mkdir Command

`mkdir` stands for "make directory". It creates new folders in your file system.

### Basic Usage

The simplest form is:
```bash
mkdir directory_name
```

This creates a new directory in your current location.

### Creating Multiple Directories

You can create multiple directories at once:
```bash
mkdir dir1 dir2 dir3
```

### Creating Nested Directories

Sometimes you want to create a directory structure with subdirectories. Use the `-p` flag (which stands for "parents") to create all necessary parent directories:

```bash
mkdir -p parent/child/grandchild
```

This creates the entire path, creating parent directories if they don't exist.

### Important Notes

- Directory names are case-sensitive: `MyDir` and `mydir` are different
- You can't create a directory if one with the same name already exists (unless you use special flags)
- Avoid spaces in directory names, or use quotes: `mkdir "my folder"`

## Exercise 1: Create Your First Directory

Create a directory called `terminal-practice` in your current location (your home directory).

**Command:** `mkdir terminal-practice`

**Verify:**
```yaml
type: directory_exists
path: ~/terminal-practice
```

## Exercise 2: Navigate Into Your New Directory

Use `cd` to move into the directory you just created.

**Command:** `cd terminal-practice`

**Verify:**
```yaml
type: current_directory
path: ~/terminal-practice
```

## Exercise 3: Create Nested Directories

Create a nested directory structure: `projects/my-first-project`. Use the `-p` flag to create both directories at once.

**Command:** `mkdir -p projects/my-first-project`

**Verify:**
```yaml
type: directory_exists
path: ~/terminal-practice/projects/my-first-project
```

## Exercise 4: Create Multiple Directories

Create three directories at once: `notes`, `scripts`, and `data`.

**Command:** `mkdir notes scripts data`

**Verify:**
```yaml
type: directory_exists
path: ~/terminal-practice/notes
```

Excellent! You now know how to:
- Create single directories with `mkdir`
- Create multiple directories at once
- Create nested directory structures with `mkdir -p`

In the next lesson, we'll learn how to create files and write content to them!

