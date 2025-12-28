"""
Terminal UI for Terminal Fun.
Provides colored output and interactive prompts.
"""

import sys
from typing import Optional
from progress_tracker import ProgressTracker


class TerminalUI:
    """Handles all terminal output and input."""
    
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    
    def __init__(self):
        self.use_colors = sys.stdout.isatty()
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_colors:
            return f"{color}{text}{self.RESET}"
        return text
    
    def print(self, text: str = ""):
        """Print text normally."""
        print(text)
    
    def print_header(self, text: str):
        """Print a section header."""
        print(self._colorize(f"\n{'=' * 60}", self.CYAN))
        print(self._colorize(f"{text:^60}", self.BOLD + self.CYAN))
        print(self._colorize(f"{'=' * 60}\n", self.CYAN))
    
    def print_subheader(self, text: str):
        """Print a subsection header."""
        print(self._colorize(f"\n{text}", self.BOLD + self.BLUE))
        print(self._colorize("-" * len(text), self.BLUE))
    
    def print_section(self, text: str):
        """Print a section marker."""
        print(self._colorize(f"\n{text}", self.BOLD + self.MAGENTA))
    
    def print_success(self, text: str):
        """Print success message."""
        print(self._colorize(text, self.GREEN))
    
    def print_error(self, text: str):
        """Print error message."""
        print(self._colorize(text, self.RED))
    
    def print_warning(self, text: str):
        """Print warning message."""
        print(self._colorize(text, self.YELLOW))
    
    def print_info(self, text: str):
        """Print info message."""
        print(self._colorize(text, self.CYAN))
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input."""
        try:
            return input(self._colorize(prompt, self.YELLOW))
        except (EOFError, KeyboardInterrupt):
            raise
    
    def show_welcome(self):
        """Show the welcome screen."""
        welcome_text = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            🎯 TERMINAL FUN - COMMAND LINE ADVENTURE 🎯        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Welcome, brave adventurer! 

You stand at the threshold of a great journey. Before you lies the
mysterious realm of the Linux command line - a world of untold power
where wizards (that's you!) control computers with mere words.

But fear not! You are not alone in this quest. I shall be your guide
through this terminal wilderness, teaching you the ancient arts of:
  
  • Navigating the digital landscape
  • Creating and manipulating files
  • Taming the wild processes
  • And much, much more!

Each lesson will challenge you to learn by doing. You'll type commands,
see results, and slowly transform from a terminal novice into a command
line master.

Your progress will be tracked, so you can always pick up where you left
off. Ready to begin your adventure?

"""
        self.print(self._colorize(welcome_text, self.CYAN))
    
    def show_main_menu(self, progress_tracker: ProgressTracker) -> str:
        """Show the main menu and get user choice."""
        stats = progress_tracker.get_stats()
        
        self.print_header("Main Menu")
        
        menu_text = f"""
  1. Continue Learning
  2. View Progress
  3. Select Lesson
  4. Exit

  Progress: {stats['completed']} completed, {stats['failed']} failed, 
            {stats['not_started']} not started
"""
        self.print(menu_text)
        
        choice = self.get_input("What would you like to do? ")
        return choice.strip()
    
    def show_progress(self, progress_tracker: ProgressTracker):
        """Show detailed progress information."""
        self.print_header("Your Progress")
        
        progress = progress_tracker.get_all_progress()
        stats = progress_tracker.get_stats()
        
        self.print(f"Started: {progress.get('started_at', 'Unknown')}")
        self.print(f"Last Updated: {progress.get('last_updated', 'Unknown')}\n")
        
        self.print(f"Total Lessons: {stats['total']}")
        self.print_success(f"Completed: {stats['completed']}")
        if stats['failed'] > 0:
            self.print_error(f"Failed: {stats['failed']}")
        self.print_info(f"In Progress: {stats['in_progress']}")
        self.print(f"Not Started: {stats['not_started']}\n")
        
        if progress.get('lessons'):
            self.print_subheader("Lesson Details")
            for lesson_key, lesson_data in sorted(progress['lessons'].items()):
                status = lesson_data.get('status', 'not_started')
                status_icon = "✓" if status == "completed" else "✗" if status == "failed" else "○"
                
                if status == "completed":
                    self.print_success(f"  {status_icon} {lesson_key}")
                elif status == "failed":
                    self.print_error(f"  {status_icon} {lesson_key}")
                else:
                    self.print(f"  {status_icon} {lesson_key}")
        
        self.print()
        self.get_input("Press Enter to continue...")
    
    def show_goodbye(self):
        """Show goodbye message."""
        goodbye_text = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    Until Next Time, Adventurer!               ║
║                                                               ║
║         Your progress has been saved. Come back soon!         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        self.print(self._colorize(goodbye_text, self.CYAN))

