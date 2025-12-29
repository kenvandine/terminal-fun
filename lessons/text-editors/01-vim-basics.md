---
title: Vim Basics
description: Learn the essential commands for using Vim, the powerful terminal text editor
order: 1
---

## Instructions

Vim (Vi Improved) is a powerful text editor that's available on virtually every Unix system. While it has a steep learning curve, mastering even the basics makes you much more efficient at editing files from the command line.

### Why Learn Vim?

- **Universally Available** - Found on every Linux/Unix system
- **Works Over SSH** - Edit files on remote servers with no GUI
- **Incredibly Powerful** - Once you learn it, you'll be faster than any other editor
- **Modal Editing** - Different modes for different tasks (the secret to its power)

### Vim's Modes

Vim is a **modal editor**, meaning it has different modes for different tasks:

**Normal Mode** - Navigate and manipulate text (default when you open vim)
- Press `Esc` to return to Normal mode from any other mode

**Insert Mode** - Type and edit text like a regular editor
- Press `i` to enter Insert mode
- Press `a` to enter Insert mode after the cursor
- Press `o` to create a new line below and enter Insert mode

**Command Mode** - Execute commands (save, quit, search, etc.)
- Press `:` from Normal mode to enter Command mode

**Visual Mode** - Select text
- Press `v` to enter Visual mode (character selection)
- Press `V` to enter Visual Line mode (line selection)

### Essential Vim Commands

**Opening and Quitting:**
```
vim filename     - Open a file in vim
:q               - Quit (only works if no changes)
:q!              - Quit without saving changes
:w               - Write (save) the file
:wq              - Write and quit
:x               - Save and quit (only writes if changes were made)
ZZ               - Save and quit (faster than :wq)
```

**Switching Modes:**
```
Esc              - Return to Normal mode
i                - Insert mode (before cursor)
a                - Insert mode (after cursor)
o                - Insert mode (new line below)
O                - Insert mode (new line above)
```

**Navigation in Normal Mode:**
```
h                - Move left
j                - Move down
k                - Move up
l                - Move right
w                - Move forward one word
b                - Move backward one word
0                - Move to beginning of line
$                - Move to end of line
gg               - Move to beginning of file
G                - Move to end of file
:n               - Go to line n (e.g., :42 goes to line 42)
```

**Editing in Normal Mode:**
```
x                - Delete character under cursor
dd               - Delete current line
yy               - Copy (yank) current line
p                - Paste after cursor
P                - Paste before cursor
u                - Undo
Ctrl+r           - Redo
```

**Searching:**
```
/pattern         - Search forward for pattern
?pattern         - Search backward for pattern
n                - Go to next search result
N                - Go to previous search result
```

### The Vim Learning Curve

Don't try to learn everything at once! Start with these basics:

1. **Opening and Quitting** - `vim file`, `:wq`, `:q!`
2. **Insert Mode** - `i` to type, `Esc` to exit
3. **Basic Navigation** - `h`, `j`, `k`, `l` or arrow keys
4. **Save and Quit** - `:w` and `:q`

Once comfortable, add:
- **Better navigation** - `w`, `b`, `0`, `$`, `gg`, `G`
- **Editing** - `dd`, `yy`, `p`, `u`
- **Searching** - `/pattern`

### Vim Tips

**If you get stuck:**
- Press `Esc` multiple times to return to Normal mode
- Type `:q!` to quit without saving

**Enable syntax highlighting:**
Your Terminal Fun environment has syntax highlighting enabled by default! Try opening a Python or JavaScript file to see colors.

**Learn more:**
- Type `vimtutor` in the terminal for an interactive tutorial
- Practice makes perfect - the more you use vim, the faster you'll get

## Exercise 1: Create and Edit a File with Vim

Create a new file called `hello.txt` using vim.

**Command:** `vim hello.txt`

**Verify:**
```yaml
type: command_output
command: ls hello.txt
contains: hello.txt
```

## Exercise 2: Write and Save Content

While in vim (from Exercise 1):
1. Press `i` to enter Insert mode
2. Type: "Hello from Vim!"
3. Press `Esc` to return to Normal mode
4. Type `:wq` and press Enter to save and quit

Then verify the file was saved with the content.

**Command:** `cat hello.txt`

**Verify:**
```yaml
type: command_output
command: cat hello.txt
contains: Hello from Vim
```

## Exercise 3: Edit an Existing File

Open the `hello.txt` file again and add more content.

**Command:** `vim hello.txt`

**After opening:**
1. Press `G` to go to the end of the file
2. Press `o` to create a new line and enter Insert mode
3. Type: "Vim is powerful!"
4. Press `Esc`, then type `:wq` to save and quit

**Verify:**
```yaml
type: command_output
command: cat hello.txt
contains: Vim is powerful
```

## Exercise 4: Test Syntax Highlighting with Python

Create a Python file to see syntax highlighting in action.

**Command:** `vim test.py`

**In vim:**
1. Press `i` to enter Insert mode
2. Type:
   ```
   def hello():
       print("Hello, World!")
   ```
3. Press `Esc`, then `:wq` to save and quit

**Verify:**
```yaml
type: command_output
command: cat test.py
contains: def hello
```

## Exercise 5: Practice Basic Navigation

Open the Python file and practice navigation.

**Command:** `vim test.py`

**Try these in Normal mode:**
- Press `gg` to go to the top
- Press `G` to go to the bottom
- Press `0` to go to the beginning of a line
- Press `$` to go to the end of a line
- Press `:q!` to quit without saving when done

**Verify:**
```yaml
type: command_output
command: echo "Navigation practice complete"
contains: complete
```

Excellent work! You've learned the essentials of Vim:
- How to open and quit vim (`:wq`, `:q!`)
- The difference between Normal and Insert modes
- Basic navigation (`h`, `j`, `k`, `l`, `gg`, `G`)
- How to enter Insert mode (`i`, `a`, `o`)
- How to save files (`:w`)

**Next Steps:**
- Practice these basics until they feel natural
- Try `vimtutor` for an interactive tutorial
- Gradually learn more advanced commands
- Remember: Press `Esc` if you get stuck!

**Pro Tip:** Set up a `.vimrc` file in your home directory to customize vim's behavior. Your Terminal Fun environment already has one configured with syntax highlighting!
