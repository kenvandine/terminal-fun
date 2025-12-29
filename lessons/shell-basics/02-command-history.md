---
title: Command History
description: Master command history to work faster and smarter in the terminal
order: 2
---

## Instructions

The bash shell remembers every command you type. This history feature is incredibly powerful and can save you tons of time by letting you quickly rerun or edit previous commands.

### Viewing Your Command History

The `history` command shows all commands you've run in your current and previous sessions:

```bash
history
```

Each command is numbered. By default, bash stores the last 1000 commands.

### Navigating History with Arrow Keys

The easiest way to access previous commands:
- **Up Arrow** - Go back through previous commands
- **Down Arrow** - Go forward through command history
- Press **Enter** to run the selected command

### Quick History Shortcuts

Bash provides powerful shortcuts for reusing commands:

- **`!!`** - Repeat the last command
  ```bash
  sudo !!  # Run the previous command with sudo
  ```

- **`!n`** - Run command number n from history
  ```bash
  !42  # Run command #42 from your history
  ```

- **`!string`** - Run the most recent command starting with "string"
  ```bash
  !cd  # Run the most recent cd command
  ```

- **`!?string`** - Run the most recent command containing "string"
  ```bash
  !?test  # Run the most recent command containing "test"
  ```

### Searching History Interactively

The most powerful history feature is **reverse search** with `Ctrl+R`:

1. Press **`Ctrl+R`**
2. Start typing part of a command
3. Bash shows the most recent matching command
4. Press **`Ctrl+R`** again to see older matches
5. Press **Enter** to run it, or **Right Arrow** to edit it

This is invaluable for finding complex commands you ran days ago!

### Editing History

You can edit the last command before running it:

```bash
^old^new  # Replace "old" with "new" in the previous command
```

For example, if you typed `cat file.txt` and want to run `cat file.log`:
```bash
^txt^log
```

### Clearing History

Sometimes you want to clear your command history:

```bash
history -c  # Clear the current session's history
```

To delete a specific entry:
```bash
history -d 42  # Delete command #42
```

### History Environment Variables

Several variables control history behavior:

- **`HISTSIZE`** - Number of commands to remember (default: 1000)
- **`HISTFILE`** - Where history is saved (`~/.bash_history`)
- **`HISTCONTROL`** - Controls what's saved (ignore duplicates, etc.)

## Exercise 1: View Your Command History

Display your command history to see what commands you've been running.

**Command:** `history`

**Verify:**
```yaml
type: command_output
command: history
```

## Exercise 2: Use the Last Command

First, run `echo "First command"`. Then use `!!` to repeat the echo command.

**Command:** `echo "First command" && !!`

**Verify:**
```yaml
type: command_output
command: echo "First command" && !!
contains: First command
```

## Exercise 3: Find a Previous Command

Run a few test commands, then use the `!` operator to run the most recent `echo` command.

**Command:** `echo "Test 1" && ls && echo "Test 2" && !echo`

**Verify:**
```yaml
type: command_output
command: echo "Test 1" && ls && echo "Test 2" && !echo
contains: Test
```

## Exercise 4: Check History Size

Display how many commands your shell remembers by checking the `HISTSIZE` variable.

**Command:** `echo $HISTSIZE`

**Verify:**
```yaml
type: command_output
command: echo $HISTSIZE
```

## Exercise 5: Add a Command to History

Type any command you like, then use `history | tail -5` to see the last 5 commands in your history (including the history command itself).

**Command:** `echo "Adding to history" && history | tail -5`

**Verify:**
```yaml
type: command_output
command: echo "Adding to history" && history | tail -5
contains: history
```

Excellent! You've learned:
- How to view your command history with `history`
- Quick shortcuts like `!!`, `!n`, and `!string`
- How to use `Ctrl+R` for interactive searching (try this manually!)
- How history makes you more efficient

**Pro Tip:** Start using `Ctrl+R` in your daily work. It's one of the most valuable terminal skills - once you get used to it, you'll wonder how you ever worked without it!
