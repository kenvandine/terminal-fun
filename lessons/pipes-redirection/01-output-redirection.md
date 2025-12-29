---
title: Output Redirection
description: Learn to redirect command output to files
order: 1
---

## Instructions

One of the most powerful features of the Linux shell is the ability to redirect output. Instead of printing to the screen, you can send it to files.

### Understanding Standard Output (stdout)

By default, commands print their output to the terminal screen. This is called "standard output" or stdout.

### Redirecting Output with >

The `>` operator redirects output to a file, **overwriting** it if it exists:

```bash
ls -l > filelist.txt
```

This saves the output of `ls -l` to `filelist.txt` instead of showing it on screen.

### Appending Output with >>

The `>>` operator **appends** output to a file without overwriting:

```bash
echo "New line" >> existing.txt
```

### Redirecting Error Messages (stderr)

Commands can also produce error messages. These go to "standard error" (stderr) and appear on screen even if you redirect stdout.

Redirect errors to a file:

```bash
command 2> errors.txt
```

Redirect both stdout and stderr:

```bash
command > output.txt 2>&1
```

Or use the simpler syntax:

```bash
command &> output.txt
```

### Discarding Output

Send output to `/dev/null` to discard it completely:

```bash
command > /dev/null 2>&1
```

This is useful for commands you want to run silently.

### Practical Examples

Save a directory listing:

```bash
ls -la > directory_contents.txt
```

Save system information:

```bash
uname -a > system_info.txt
date >> system_info.txt
```

Run a command silently:

```bash
some_noisy_command > /dev/null 2>&1
```

## Exercise 1: Redirect Basic Output

Use `echo` to write "Terminal Fun" to a file called `output.txt`.

**Command:** `echo "Terminal Fun" > output.txt`

**Verify:**
```yaml
type: file_exists
path: ~/output.txt
```

## Exercise 2: Append to a File

Add another line "Learning Linux" to `output.txt` using append redirection.

**Command:** `echo "Learning Linux" >> output.txt`

**Verify:**
```yaml
type: command_output
command: cat output.txt
contains: Learning Linux
```

## Exercise 3: Save Command Output

Save the output of `ls -l` to a file called `listing.txt`.

**Command:** `ls -l > listing.txt`

**Verify:**
```yaml
type: file_exists
path: ~/listing.txt
```

## Exercise 4: Redirect Both Output and Errors

Try to list a non-existent directory and redirect both output and errors to `combined.txt`.

**Command:** `ls /nonexistent 2>&1 > combined.txt`

**Verify:**
```yaml
type: file_exists
path: ~/combined.txt
```

Excellent! You now know how to:
- Redirect output with `>`
- Append output with `>>`
- Redirect errors with `2>`
- Combine output and errors with `2>&1` or `&>`
- Discard output with `/dev/null`

This is foundational knowledge for shell scripting!
