---
title: Getting Started with the Terminal
description: Learn the basics of opening and using the terminal
order: 1
---

## Instructions

Welcome to your first lesson! The terminal (also called command line, shell, or console) is a powerful way to interact with your computer using text commands instead of clicking with a mouse.

### What is a Terminal?

Think of the terminal as a text-based interface to your computer. Instead of clicking on folders and files, you type commands to navigate, create, modify, and delete things.

### Opening the Terminal

To open the terminal:
- **Linux**: Press `Ctrl + Alt + T` or search for "Terminal" in your applications
- **Windows**: Use WSL (Windows Subsystem for Linux) or Git Bash

When you open the terminal, you'll see a prompt that usually looks something like:
```
username@computername:~$
```

The `~` symbol represents your home directory - this is where you start when you open a new terminal window.

### Terminal Tips: Copy and Paste

Unlike regular applications, the terminal uses different keyboard shortcuts for copying and pasting:

- **Copy**: Select text with your mouse, then press **`Ctrl+Shift+C`**
- **Paste**: Press **`Ctrl+Shift+V`**

**Why the Shift key?** Regular `Ctrl+C` is used to stop (interrupt) running programs in the terminal, so we need `Ctrl+Shift+C` for copying instead.

**Pro Tip:** You can usually paste into the terminal by middle-clicking your mouse or touchpad (if you have a middle button or can click with three fingers).

### Your First Command

The most basic command is `pwd`, which stands for "Print Working Directory". It tells you where you are in your file system right now.

## Exercise 1: Find Your Location

Try running the `pwd` command to see where you are in the file system.

**Command:** `pwd`

**Verify:**
```yaml
type: command_output
command: pwd
contains: /
```

## Exercise 2: List Files

Now that you know where you are, let's see what's in your current directory. Use the `ls` command (short for "list") to see all files and folders.

**Command:** `ls`

**Verify:**
```yaml
type: command_output
command: ls
```

Congrats! You've completed your first lesson. You've learned:
- What a terminal is
- How to find your current location with `pwd`
- How to list files with `ls`

Ready for more? Let's learn about navigation next!

