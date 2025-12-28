# Terminal Fun 🎯

An interactive, challenge-based terminal application for learning Linux command line basics. Designed for complete beginners, Terminal Fun guides you through mastering essential command line skills with hands-on practice and progress tracking.

## Features

- 🎓 **Beginner-Friendly**: Assumes no prior Linux/terminal experience
- 📚 **Structured Lessons**: Organized into logical categories (navigation, file operations, etc.)
- ✅ **Progress Tracking**: Save your progress and resume where you left off
- 🎮 **Interactive Learning**: Learn by doing with hands-on exercises
- 🎨 **Beautiful Terminal UI**: Colorful, engaging interface
- 📝 **Markdown-Based Content**: Lesson materials stored in easy-to-edit markdown files

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd terminal-fun
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

## Usage

When you run Terminal Fun, you'll see:

1. **Welcome Screen**: An introduction to the app and what you'll learn
2. **Main Menu**: Options to continue learning, view progress, select lessons, or exit
3. **Interactive Lessons**: Follow along with instructions and complete exercises
4. **Progress Tracking**: Your progress is automatically saved to `.terminal_fun_progress.json`

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
- **Exercises**: Hands-on practice with commands and verification

## Current Lessons

### Navigation Category
- **Getting Started**: Introduction to the terminal, `pwd`, and `ls`
- **Changing Directories**: Learn `cd` and navigation basics
- **Creating Directories**: Master `mkdir` for creating folders
- **Listing Files (Advanced)**: Explore `ls` options and flags

## Creating Your Own Lessons

To create a new lesson:

1. Create a markdown file in the appropriate category directory
2. Add YAML frontmatter with title, description, and order
3. Write instructions in markdown
4. Add exercises with the format:

```markdown
## Exercise 1: Title

Description of what to do.

**Command:** `command-to-run`

**Verify:**
```yaml
type: directory_exists
path: /path/to/check
```
```

## Progress File

Your progress is stored in `.terminal_fun_progress.json` in the project root. This file tracks:
- Which lessons you've completed
- Which exercises you've finished
- When you last worked on lessons

You can safely delete this file to reset your progress and start over.

## Requirements

- Python 3.7+
- PyYAML
- markdown

## Contributing

Feel free to add more lessons! The markdown format makes it easy to extend the curriculum. Just follow the existing lesson structure and add files to the appropriate category directories.

## License

[Add your license here]

## Future Enhancements

Potential additions:
- More lesson categories (file manipulation, text processing, permissions, etc.)
- Achievement system
- Practice mode for reviewing completed lessons
- More sophisticated exercise verification
- Integration with shell history for better verification

---

**Ready to become a terminal wizard? Run `python main.py` and let the adventure begin!** 🚀

