# Terminal Fun 🎯

A beautiful GTK4 application for learning Linux command line basics. Terminal Fun provides an interactive, beginner-friendly way to master essential terminal skills with embedded terminal support and structured lessons.

## Features

- 🎓 **Beginner-Friendly**: Assumes no prior Linux/terminal experience
- 📚 **Structured Lessons**: Organized into logical categories (navigation, file operations, etc.)
- ✅ **Progress Tracking**: Save your progress and resume where you left off
- 🎮 **Interactive Learning**: Learn by doing with hands-on exercises
- 🖥️ **GTK4 GUI**: Beautiful native GNOME application with Adwaita styling
- 🔧 **Embedded Terminal**: Full VTE terminal emulator built right into the app
- 📝 **Markdown-Based Content**: Lesson materials stored in easy-to-edit markdown files

## Screenshots

The application features a split-pane interface:
- **Left Pane**: Lesson content with instructions and exercises
- **Right Pane**: Embedded terminal for practicing commands

## Installation

### System Requirements

You'll need GTK4, Adwaita, and VTE development libraries installed:

#### Fedora/RHEL
```bash
sudo dnf install gtk4-devel libadwaita-devel vte291-devel python3-gobject
```

#### Debian/Ubuntu
```bash
sudo apt install libgtk-4-dev libadwaita-1-dev libvte-2.91-dev python3-gi python3-gi-cairo python3-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-vte-3.91
```

#### Arch Linux
```bash
sudo pacman -S gtk4 libadwaita vte3 python-gobject
```

### Python Dependencies

1. Clone this repository:
```bash
git clone <repository-url>
cd terminal-fun
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

## Usage

When you start Terminal Fun, you'll see:

1. **Main Window**: Split into two resizable panes
   - Left: Lesson content with instructions and exercises
   - Right: Embedded terminal for running commands

2. **Navigation**: 
   - Use "Previous" and "Next" buttons to move between lessons
   - Click the progress icon in the header to view your learning statistics

3. **Practice**: 
   - Read the lesson instructions on the left
   - Type commands in the embedded terminal on the right
   - See results immediately as you learn

## Lesson Structure

Lessons are organized in the `lessons/` directory by category:

```
lessons/
  navigation/
    01-getting-started.md
    02-changing-directories.md
    03-creating-directories.md
    04-listing-files-advanced.md
```

Each lesson file contains:
- **Frontmatter** (YAML): Metadata like title, description, and order
- **Instructions**: Markdown content explaining the concepts
- **Exercises**: Hands-on practice with suggested commands

## Current Lessons

### Navigation Category
- **Getting Started**: Introduction to the terminal, `pwd`, and `ls`
- **Changing Directories**: Learn `cd` and navigation basics
- **Creating Directories**: Master `mkdir` for creating folders
- **Listing Files (Advanced)**: Explore `ls` options and flags

## Creating Your Own Lessons

To create a new lesson:

1. Create a markdown file in the appropriate category directory
2. Add YAML frontmatter with title, description, and order:

```markdown
---
title: Your Lesson Title
description: Brief description
order: 5
---

## Instructions

Your lesson content here with **bold** and `code` formatting.

### Subsection

You can use headings, code blocks, and more:

\`\`\`bash
command-example
\`\`\`

## Exercise 1: Title

Description of what to do.

**Command:** `command-to-run`

**Verify:**
\`\`\`yaml
type: directory_exists
path: /path/to/check
\`\`\`
```

See existing lessons in `lessons/navigation/` for more examples.

## Progress Tracking

Your progress is automatically saved to `.terminal_fun_progress.json` in the project root. This file tracks:
- Which lessons you've completed
- Which exercises you've finished
- When you last worked on lessons

You can safely delete this file to reset your progress and start over.

## Requirements

- Python 3.7+
- PyGObject (for GTK4 bindings)
- PyYAML (for lesson parsing)
- GTK4, Libadwaita, and VTE3 system libraries (see Installation above)

## Development

The application consists of:
- `main.py` - GTK4 application entry point
- `lesson_loader.py` - Loads and parses lesson markdown files
- `progress_tracker.py` - Manages user progress
- `lessons/` - Lesson content directory

## Contributing

Feel free to add more lessons! The markdown format makes it easy to extend the curriculum. Just follow the existing lesson structure and add files to the appropriate category directories.

## License

[Add your license here]

## Future Enhancements

Potential additions:
- More lesson categories (file manipulation, text processing, permissions, etc.)
- Achievement system
- Practice mode for reviewing completed lessons
- Command autocompletion suggestions
- Export command history for review

---

**Ready to become a terminal wizard? Run `python3 main.py` and let the adventure begin!** 🚀
