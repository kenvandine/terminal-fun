---
title: Environment Variables
description: Learn about environment variables and how they control shell behavior
order: 1
---

## Instructions

Environment variables are named values that affect how programs and the shell behave. Think of them as settings that programs can read to change their behavior.

### What are Environment Variables?

Environment variables store information like:
- Where to find programs (`PATH`)
- Your home directory location (`HOME`)
- Your username (`USER`)
- Which shell you're using (`SHELL`)

They're called "environment" variables because they define the environment in which your programs run.

### Viewing Environment Variables

The `env` command shows all current environment variables:

```bash
env
```

To see a specific variable, use `echo` with a `$` before the variable name:

```bash
echo $HOME
echo $USER
echo $PATH
```

### Understanding PATH

The `PATH` variable is one of the most important. It tells the shell where to look for commands. When you type a command like `ls`, the shell searches each directory in `PATH` to find the `ls` program.

`PATH` contains multiple directories separated by colons (`:`):

```bash
/usr/local/bin:/usr/bin:/bin:/usr/games
```

### Creating Your Own Variables

You can create variables for temporary use in your current shell session:

```bash
MY_VAR="Hello World"
echo $MY_VAR
```

To make a variable available to programs you run (export it to the environment):

```bash
export MY_VAR="Hello World"
```

### Common Environment Variables

- **`HOME`** - Your home directory path
- **`USER`** - Your username
- **`SHELL`** - Your current shell (usually `/bin/bash`)
- **`PATH`** - Directories to search for commands
- **`PWD`** - Current working directory
- **`LANG`** - Your language and locale settings

## Exercise 1: View Your Environment

Use the `env` command to see all environment variables currently set in your shell.

**Command:** `env`

**Verify:**
```yaml
type: command_output
command: env
contains: HOME
```

## Exercise 2: Check Your Home Directory

Display your home directory by printing the `HOME` environment variable.

**Command:** `echo $HOME`

**Verify:**
```yaml
type: command_output
command: echo $HOME
contains: /home/
```

## Exercise 3: View Your PATH

Display your `PATH` variable to see where the shell looks for commands.

**Command:** `echo $PATH`

**Verify:**
```yaml
type: command_output
command: echo $PATH
contains: /bin
```

## Exercise 4: Find Where a Command Lives

Use the `which` command to find where the `ls` command is located. The shell finds it by searching directories in your `PATH`.

**Command:** `which ls`

**Verify:**
```yaml
type: command_output
command: which ls
contains: /bin/ls
```

## Exercise 5: Create a Custom Variable

Create your own environment variable called `GREETING` with the value "Hello Terminal" and then display it.

**Command:** `export GREETING="Hello Terminal" && echo $GREETING`

**Verify:**
```yaml
type: command_output
command: export GREETING="Hello Terminal" && echo $GREETING
contains: Hello Terminal
```

Great job! You now understand:
- What environment variables are and why they matter
- How to view variables with `env` and `echo $VARIABLE`
- The importance of the `PATH` variable
- How to create and export your own variables

Remember: Variables you create with `export` only last for your current terminal session. In the next lesson, you'll learn how to make them permanent!
