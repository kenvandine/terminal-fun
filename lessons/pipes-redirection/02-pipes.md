---
title: Pipes and Chaining Commands
description: Master the pipe operator to chain commands together
order: 2
---

## Instructions

Pipes are one of the most powerful concepts in Linux. They let you take the output of one command and use it as input for another, creating powerful command chains.

### The Pipe Operator |

The `|` (pipe) symbol connects commands:

```bash
command1 | command2
```

The output of `command1` becomes the input of `command2`.

### Common Pipe Patterns

**Count lines in output:**

```bash
ls -l | wc -l
```

This lists files and counts how many lines (files) there are.

**Search output:**

```bash
ps aux | grep firefox
```

This lists all processes and searches for "firefox".

**Sort output:**

```bash
cat names.txt | sort
```

**Remove duplicates:**

```bash
cat file.txt | sort | uniq
```

**Page through long output:**

```bash
ls -lR /etc | less
```

### Useful Commands for Pipes

- **`wc`**: Count words, lines, or characters
  - `wc -l`: count lines
  - `wc -w`: count words
  - `wc -c`: count characters

- **`sort`**: Sort lines alphabetically
  - `sort -r`: reverse sort
  - `sort -n`: numeric sort

- **`uniq`**: Remove duplicate adjacent lines (use after `sort`)
  - `uniq -c`: show count of occurrences

- **`head`**: Show first N lines
  - `head -n 10`: first 10 lines

- **`tail`**: Show last N lines
  - `tail -n 10`: last 10 lines
  - `tail -f`: follow file (watch it grow)

- **`cut`**: Extract columns
  - `cut -d: -f1`: extract first field with `:` delimiter

- **`tr`**: Translate characters
  - `tr 'a-z' 'A-Z'`: convert to uppercase

### Complex Examples

Find the 5 largest files:

```bash
ls -lS | head -n 6
```

Count unique users logged in:

```bash
who | cut -d' ' -f1 | sort | uniq | wc -l
```

Show processes using most memory:

```bash
ps aux | sort -nk 4 | tail -n 5
```

## Exercise 1: Count Files

Use `ls` and `wc -l` with a pipe to count how many items are in your home directory.

**Command:** `ls ~ | wc -l`

**Verify:**
```yaml
type: command_output
command: ls ~ | wc -l
```

## Exercise 2: Search and Sort

Create a file with names, then use pipes to sort them. Create the file and display it sorted.

**Command:** `echo -e "zebra\napple\nmango\nbanana" > fruits.txt && cat fruits.txt | sort`

**Verify:**
```yaml
type: command_output
command: cat fruits.txt | sort
contains: apple
```

## Exercise 3: Chain Multiple Commands

Create a file with duplicate lines, then sort and remove duplicates.

**Command:** `echo -e "cat\ndog\ncat\nbird\ndog" > animals.txt && cat animals.txt | sort | uniq`

**Verify:**
```yaml
type: command_output
command: cat animals.txt | sort | uniq
contains: bird
```

## Exercise 4: Filter with grep

Use `ls` with `grep` to find only `.txt` files in your current directory.

**Command:** `ls | grep ".txt"`

**Verify:**
```yaml
type: command_output
command: ls | grep ".txt"
```

Amazing! You've learned to:
- Use the pipe `|` operator
- Chain multiple commands together
- Work with `wc`, `sort`, `uniq`, `head`, and `tail`
- Build complex command pipelines

Pipes are the key to Unix philosophy: small tools that do one thing well, combined to solve complex problems!
