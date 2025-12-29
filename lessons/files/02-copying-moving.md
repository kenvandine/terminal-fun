---
title: Copying and Moving Files
description: Master cp and mv commands for file management
order: 2
---

## Instructions

File management is essential in the terminal. You'll frequently need to copy, move, and rename files.

### Copying Files with cp

The `cp` command copies files from one location to another:

```bash
cp source.txt destination.txt
```

Copy a file to a directory:

```bash
cp file.txt /path/to/directory/
```

Copy multiple files to a directory:

```bash
cp file1.txt file2.txt file3.txt /destination/
```

**Copy directories:** Use the `-r` (recursive) flag:

```bash
cp -r source_directory/ destination_directory/
```

### Moving and Renaming with mv

The `mv` command moves files or renames them:

```bash
mv oldname.txt newname.txt
```

Move a file to another directory:

```bash
mv file.txt /path/to/directory/
```

Move multiple files:

```bash
mv file1.txt file2.txt file3.txt /destination/
```

**Note:** Unlike `cp`, `mv` doesn't need `-r` for directories.

### Useful Options

- **`cp -i`** or **`mv -i`**: Interactive mode (asks before overwriting)
- **`cp -v`** or **`mv -v`**: Verbose mode (shows what's being done)
- **`cp -u`**: Copy only newer files (update)

## Exercise 1: Copy a File

First create a test file, then copy it to a new name. Create `original.txt` with some content, then copy it to `copy.txt`.

**Command:** `echo "test content" > original.txt && cp original.txt copy.txt`

**Verify:**
```yaml
type: file_exists
path: ~/copy.txt
```

## Exercise 2: Move (Rename) a File

Rename `copy.txt` to `renamed.txt` using the mv command.

**Command:** `mv copy.txt renamed.txt`

**Verify:**
```yaml
type: file_exists
path: ~/renamed.txt
```

## Exercise 3: Copy to a Directory

Create a directory called `backups` and copy `original.txt` into it.

**Command:** `mkdir backups && cp original.txt backups/`

**Verify:**
```yaml
type: file_exists
path: ~/backups/original.txt
```

## Exercise 4: Copy a Directory

Create a directory with files, then copy the entire directory. Create `test_dir` with a file, then copy it to `test_dir_copy`.

**Command:** `mkdir test_dir && touch test_dir/file.txt && cp -r test_dir test_dir_copy`

**Verify:**
```yaml
type: directory_exists
path: ~/test_dir_copy
```

Great work! You can now:
- Copy files with `cp`
- Move and rename files with `mv`
- Copy entire directories with `cp -r`
- Use options like `-i` and `-v` for safety and feedback
