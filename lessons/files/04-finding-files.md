---
title: Finding Files
description: Search for files using find and locate commands
order: 4
---

## Instructions

When working with many files, you need tools to find what you're looking for. Linux provides powerful search commands.

### Finding Files with find

The `find` command searches for files in a directory hierarchy:

```bash
find /path/to/search -name "filename"
```

Find files in the current directory:

```bash
find . -name "*.txt"
```

The `.` means "current directory" and `*.txt` finds all files ending in `.txt`.

### Common find Options

**Search by name** (case-insensitive):

```bash
find . -iname "readme*"
```

**Search by type:**

```bash
find . -type f    # files only
find . -type d    # directories only
```

**Search by size:**

```bash
find . -size +10M    # files larger than 10 MB
find . -size -1k     # files smaller than 1 KB
```

**Search by modification time:**

```bash
find . -mtime -7     # modified in last 7 days
find . -mtime +30    # modified more than 30 days ago
```

**Execute commands on results:**

```bash
find . -name "*.log" -delete    # delete all .log files
find . -name "*.txt" -exec cat {} \;    # cat each .txt file
```

### Using grep to Search File Contents

`grep` searches for text within files:

```bash
grep "search term" filename.txt
```

Search all files in current directory:

```bash
grep "error" *.log
```

Search recursively:

```bash
grep -r "TODO" .
```

Useful grep options:
- `-i`: Case-insensitive search
- `-n`: Show line numbers
- `-v`: Invert match (show lines that DON'T match)
- `-c`: Count matches

## Exercise 1: Find Files by Name

Create some test files, then use find to locate all `.txt` files in your current directory.

**Command:** `touch file1.txt file2.txt data.csv && find . -name "*.txt"`

**Verify:**
```yaml
type: command_output
command: find . -name "*.txt"
contains: .txt
```

## Exercise 2: Find Files by Type

Use find to list only directories in your home directory (limit depth to avoid too much output).

**Command:** `find ~ -maxdepth 1 -type d`

**Verify:**
```yaml
type: command_output
command: find ~ -maxdepth 1 -type d
```

## Exercise 3: Search File Contents with grep

Create a file with content, then search for a word inside it.

**Command:** `echo "Hello World" > greetings.txt && grep "Hello" greetings.txt`

**Verify:**
```yaml
type: command_output
command: grep "Hello" greetings.txt
contains: Hello
```

## Exercise 4: Recursive Search

Create a directory structure with files, then search recursively for a pattern.

**Command:** `mkdir -p search_test/sub && echo "test" > search_test/file.txt && echo "test" > search_test/sub/file.txt && grep -r "test" search_test/`

**Verify:**
```yaml
type: command_output
command: grep -r "test" search_test/
contains: test
```

Perfect! You've learned to:
- Find files by name with `find`
- Search by file type, size, and date
- Search file contents with `grep`
- Use recursive search options

These skills are essential for managing large file systems!
