---
title: Input Redirection
description: Learn to redirect input from files to commands
order: 3
---

## Instructions

Just as you can redirect output TO files, you can also redirect input FROM files. This is less common but still useful.

### Redirecting Input with <

The `<` operator redirects a file's contents as input to a command:

```bash
command < inputfile.txt
```

### Practical Examples

**Sort a file:**

```bash
sort < unsorted.txt
```

This is equivalent to `cat unsorted.txt | sort` but slightly more efficient.

**Count words in a file:**

```bash
wc -w < document.txt
```

**Mail content from a file:**

```bash
mail user@example.com < message.txt
```

### Here Documents (<<)

A "here document" lets you provide multi-line input inline:

```bash
cat << EOF
This is line 1
This is line 2
This is line 3
EOF
```

This is useful in scripts when you want to write multiple lines to a file:

```bash
cat << EOF > config.txt
Setting1=value1
Setting2=value2
Setting3=value3
EOF
```

### Here Strings (<<<)

A "here string" passes a string as input:

```bash
bc <<< "5 + 3"
```

This is equivalent to:

```bash
echo "5 + 3" | bc
```

### Combining Input and Output Redirection

You can use both at once:

```bash
sort < unsorted.txt > sorted.txt
```

This reads from `unsorted.txt` and writes to `sorted.txt`.

### When to Use Input Redirection

Input redirection is most useful:
- In scripts where you want explicit data flow
- When a command doesn't accept filenames as arguments
- For feeding test data to programs
- With here documents for inline configuration

## Exercise 1: Sort with Input Redirection

Create a file with unsorted numbers, then sort it using input redirection.

**Command:** `echo -e "5\n2\n8\n1\n9" > numbers.txt && sort -n < numbers.txt`

**Verify:**
```yaml
type: command_output
command: sort -n < numbers.txt
contains: 1
```

## Exercise 2: Count Words from File

Create a file with text and use `wc -w` with input redirection to count words.

**Command:** `echo "hello world from terminal" > words.txt && wc -w < words.txt`

**Verify:**
```yaml
type: command_output
command: wc -w < words.txt
```

## Exercise 3: Use a Here Document

Use a here document to create a file with multiple lines.

**Command:** `cat << EOF > poem.txt
Roses are red
Violets are blue
Linux is fun
And so are you
EOF`

**Verify:**
```yaml
type: file_exists
path: ~/poem.txt
```

## Exercise 4: Combine Input and Output

Sort a file and save the result using both input and output redirection.

**Command:** `echo -e "dog\napple\ncat" > unsorted.txt && sort < unsorted.txt > sorted.txt`

**Verify:**
```yaml
type: file_exists
path: ~/sorted.txt
```

Perfect! You've mastered:
- Input redirection with `<`
- Here documents with `<<`
- Here strings with `<<<`
- Combining input and output redirection

Now you have complete control over data flow in the shell!
