---
title: Creating and Editing Files
description: Learn to create files with touch, echo, and basic text editors
order: 1
---

## Instructions

Now that you can navigate directories, let's learn how to create and work with files. Files are where you store your data, code, and documents.

### Creating Empty Files with touch

The `touch` command creates an empty file or updates the timestamp of an existing file:

```bash
touch myfile.txt
```

You can create multiple files at once:

```bash
touch file1.txt file2.txt file3.txt
```

### Writing Content with echo

The `echo` command prints text to the screen, but you can redirect it to a file using `>`:

```bash
echo "Hello, World!" > greeting.txt
```

**Important:** Using `>` will overwrite the file if it exists. To append instead, use `>>`:

```bash
echo "Another line" >> greeting.txt
```

### Viewing File Contents

Use `cat` to display file contents:

```bash
cat greeting.txt
```

For longer files, use `less` for scrollable viewing:

```bash
less longfile.txt
```

(Press `q` to quit less)

### Basic Text Editors

**nano** - Beginner-friendly terminal editor:

```bash
nano myfile.txt
```

Controls shown at bottom: `Ctrl+O` to save, `Ctrl+X` to exit.

## Exercise 1: Create Your First File

Create an empty file called `test.txt` using the touch command.

**Command:** `touch test.txt`

**Verify:**
```yaml
type: file_exists
path: ~/test.txt
```

## Exercise 2: Write Content to a File

Use echo to write "My first file" to a file called `first.txt`.

**Command:** `echo "My first file" > first.txt`

**Verify:**
```yaml
type: file_exists
path: ~/first.txt
```

## Exercise 3: Append to a File

Add a second line "Line 2" to your `first.txt` file using `>>`.

**Command:** `echo "Line 2" >> first.txt`

**Verify:**
```yaml
type: command_output
command: cat first.txt
contains: Line 2
```

## Exercise 4: View File Contents

Use `cat` to display the contents of `first.txt` and verify both lines are there.

**Command:** `cat first.txt`

**Verify:**
```yaml
type: command_output
command: cat first.txt
```

Excellent! You now know how to:
- Create files with `touch`
- Write content with `echo` and `>`
- Append content with `>>`
- View files with `cat` and `less`
- Edit files with `nano`
