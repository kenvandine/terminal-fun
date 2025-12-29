#!/usr/bin/env python3
"""
Terminal Fun - GTK4 Application
A graphical learning app for mastering the Linux command line.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Vte', '3.91')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Adw, Vte, GLib, Pango, Gio, GObject, Gdk
import sys
import os
from pathlib import Path
from typing import Optional

from lesson_loader import LessonLoader
from progress_tracker import ProgressTracker


class LessonViewer(Gtk.Box):
    """Widget for displaying lesson content."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_vexpand(True)
        self.set_hexpand(True)

        # Title
        self.title_label = Gtk.Label()
        self.title_label.add_css_class("title-1")
        self.title_label.set_halign(Gtk.Align.START)
        self.title_label.set_wrap(True)
        self.append(self.title_label)

        # Description
        self.description_label = Gtk.Label()
        self.description_label.add_css_class("body")
        self.description_label.set_halign(Gtk.Align.START)
        self.description_label.set_wrap(True)
        self.description_label.set_selectable(True)
        self.append(self.description_label)

        # Instructions section
        instructions_frame = Gtk.Frame()
        instructions_frame.add_css_class("info")
        instructions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        instructions_box.set_margin_start(12)
        instructions_box.set_margin_end(12)
        instructions_box.set_margin_top(12)
        instructions_box.set_margin_bottom(12)

        instructions_label = Gtk.Label(label="📚 Instructions")
        instructions_label.add_css_class("heading")
        instructions_label.set_halign(Gtk.Align.START)
        instructions_box.append(instructions_label)

        self.instructions_label = Gtk.Label()
        self.instructions_label.add_css_class("body")
        self.instructions_label.set_halign(Gtk.Align.START)
        self.instructions_label.set_wrap(True)
        self.instructions_label.set_selectable(True)
        self.instructions_label.set_use_markup(True)
        self.instructions_label.set_text("")
        instructions_box.append(self.instructions_label)

        instructions_frame.set_child(instructions_box)
        self.append(instructions_frame)

        # Exercises section
        exercises_label = Gtk.Label(label="🎯 Exercises")
        exercises_label.add_css_class("heading")
        exercises_label.set_halign(Gtk.Align.START)
        self.append(exercises_label)

        # Exercises container (no scroll window, let parent handle scrolling)
        self.exercises_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.append(self.exercises_box)

    def display_lesson(self, lesson: dict):
        """Display a lesson in the viewer."""
        # Clear previous content
        self.title_label.set_text(lesson.get('title', 'Untitled Lesson'))
        self.description_label.set_text(lesson.get('description', ''))

        # Instructions
        instructions = lesson.get('instructions', '')
        if instructions:
            # Convert markdown-style formatting to pango markup
            try:
                instructions_html = self._markdown_to_pango(instructions)
                # Ensure markup is enabled
                self.instructions_label.set_use_markup(True)
                self.instructions_label.set_markup(instructions_html)
            except Exception as e:
                # If markup parsing fails, fall back to plain text
                self.instructions_label.set_use_markup(False)
                self.instructions_label.set_text(instructions)
        else:
            self.instructions_label.set_use_markup(False)
            self.instructions_label.set_text("")

        # Clear exercises
        while self.exercises_box.get_first_child():
            self.exercises_box.remove(self.exercises_box.get_first_child())

        # Add exercises
        exercises = lesson.get('exercises', [])
        for idx, exercise in enumerate(exercises, 1):
            self._add_exercise(exercise, idx)

    def _add_exercise(self, exercise: dict, number: int):
        """Add an exercise widget."""
        exercise_frame = Gtk.Frame()
        exercise_frame.add_css_class("card")
        exercise_frame.set_margin_bottom(8)
        
        exercise_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        exercise_box.set_margin_start(12)
        exercise_box.set_margin_end(12)
        exercise_box.set_margin_top(12)
        exercise_box.set_margin_bottom(12)

        # Exercise title
        title_label = Gtk.Label(label=f"Exercise {number}: {exercise.get('title', 'Untitled')}")
        title_label.add_css_class("heading")
        title_label.set_halign(Gtk.Align.START)
        exercise_box.append(title_label)

        # Exercise description
        description = exercise.get('description', '')
        if description:
            desc_label = Gtk.Label()
            desc_label.set_text(description)
            desc_label.add_css_class("body")
            desc_label.set_halign(Gtk.Align.START)
            desc_label.set_wrap(True)
            desc_label.set_selectable(True)
            exercise_box.append(desc_label)

        # Suggested command
        command = exercise.get('command')
        if command:
            cmd_frame = Gtk.Frame()
            cmd_frame.add_css_class("code")
            cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            cmd_box.set_margin_start(8)
            cmd_box.set_margin_end(8)
            cmd_box.set_margin_top(4)
            cmd_box.set_margin_bottom(4)

            cmd_label = Gtk.Label(label=f"💡 Try: {command}")
            cmd_label.add_css_class("monospace")
            cmd_label.set_halign(Gtk.Align.START)
            cmd_label.set_selectable(True)
            cmd_box.append(cmd_label)

            cmd_frame.set_child(cmd_box)
            exercise_box.append(cmd_frame)

        exercise_frame.set_child(exercise_box)
        self.exercises_box.append(exercise_frame)

    def _markdown_to_pango(self, text: str) -> str:
        """Convert simple markdown to pango markup."""
        import re

        # Process in stages: handle patterns that contain other patterns first
        # Use placeholders to protect processed content

        # Handle fenced code blocks ```code```
        code_block_placeholders = []
        code_block_idx = 0

        def code_block_replacer(match):
            nonlocal code_block_idx
            # Group 1 is language (optional), group 2 is content
            if match.lastindex >= 2:
                lang = match.group(1) or ''
                code_content = match.group(2)
            else:
                # Fallback if groups don't match as expected
                lang = ''
                code_content = match.group(0)[3:-3]  # Remove ``` from start and end
            # Strip leading/trailing whitespace/newlines from code content
            code_content = code_content.strip()
            placeholder = f"___CODE_BLOCK_{code_block_idx}___"
            # Escape the code content and wrap in monospace
            escaped_code = GLib.markup_escape_text(code_content)
            # Use <tt> for monospace
            code_block_placeholders.append((placeholder, f'<tt>{escaped_code}</tt>'))
            code_block_idx += 1
            return placeholder

        # Match code blocks - pattern: ```lang\ncontent\n```
        # Use a simpler approach: match anything between triple backticks
        def simple_code_block_replacer(m):
            nonlocal code_block_idx
            full_match = m.group(0)
            # Remove the opening ``` and closing ```
            content = full_match[3:-3]
            # Split on first newline to separate language from content
            parts = content.split('\n', 1)
            if len(parts) > 1:
                lang_part = parts[0].strip()
                code_content = parts[1]
            else:
                lang_part = ''
                code_content = parts[0]
            code_content = code_content.strip()
            placeholder = f"___CODE_BLOCK_{code_block_idx}___"
            escaped_code = GLib.markup_escape_text(code_content)
            code_block_placeholders.append((placeholder, f'<tt>{escaped_code}</tt>'))
            code_block_idx += 1
            return placeholder

        text = re.sub(r'```[^`]*?```', simple_code_block_replacer, text, flags=re.DOTALL)

        # Handle headings ### Heading
        heading_placeholders = []
        heading_idx = 0

        def heading_replacer(match):
            nonlocal heading_idx
            level = len(match.group(1))  # Number of # characters
            heading_text = match.group(2).strip()
            placeholder = f"___HEADING_{heading_idx}___"
            escaped_text = GLib.markup_escape_text(heading_text)
            # Use different sizes based on level (### = h3, ## = h2, # = h1)
            if level == 1:
                heading_placeholders.append((placeholder, f'<span size="x-large" weight="bold">{escaped_text}</span>'))
            elif level == 2:
                heading_placeholders.append((placeholder, f'<span size="large" weight="bold">{escaped_text}</span>'))
            else:  # level 3+
                heading_placeholders.append((placeholder, f'<span size="medium" weight="bold">{escaped_text}</span>'))
            heading_idx += 1
            return placeholder
        
        text = re.sub(r'^(#{1,6})\s+(.+)$', heading_replacer, text, flags=re.MULTILINE)

        # Handle **`code`** patterns (bold code) first
        bold_code_placeholders = []
        bold_code_idx = 0

        def bold_code_replacer(match):
            nonlocal bold_code_idx
            code_text = match.group(1)
            placeholder = f"___BOLD_CODE_{bold_code_idx}___"
            escaped_code = GLib.markup_escape_text(code_text)
            bold_code_placeholders.append((placeholder, f'<b><tt>{escaped_code}</tt></b>'))
            bold_code_idx += 1
            return placeholder

        text = re.sub(r'\*\*`([^`\n]+)`\*\*', bold_code_replacer, text)

        # Handle standalone code `code`
        code_placeholders = []
        code_idx = 0

        def code_replacer(match):
            nonlocal code_idx
            code_text = match.group(1)
            placeholder = f"___CODE_{code_idx}___"
            escaped_code = GLib.markup_escape_text(code_text)
            code_placeholders.append((placeholder, f'<tt>{escaped_code}</tt>'))
            code_idx += 1
            return placeholder

        text = re.sub(r'`([^`\n]+)`', code_replacer, text)

        # Handle standalone bold **text** (but not if it contains placeholders)
        bold_placeholders = []
        bold_idx = 0

        def bold_replacer(match):
            nonlocal bold_idx
            bold_text = match.group(1)
            placeholder = f"___BOLD_{bold_idx}___"
            escaped_text = GLib.markup_escape_text(bold_text)
            bold_placeholders.append((placeholder, f'<b>{escaped_text}</b>'))
            bold_idx += 1
            return placeholder

        text = re.sub(r'\*\*([^*\n]+?)\*\*', bold_replacer, text)

        # Escape remaining text (but not placeholders - they're safe)
        text = GLib.markup_escape_text(text)

        # Restore all placeholders with their HTML
        for placeholder, html in (heading_placeholders + code_block_placeholders + bold_code_placeholders + code_placeholders + bold_placeholders):
            text = text.replace(placeholder, html)

        return text


class TerminalFunWindow(Adw.ApplicationWindow):
    """Main application window."""

    def __init__(self, app):
        super().__init__(application=app, title="Terminal Fun")
        self.set_default_size(1200, 800)

        self.lesson_loader = LessonLoader()
        self.progress_tracker = ProgressTracker()
        self.current_category: Optional[str] = None
        self.current_lesson_slug: Optional[str] = None

        # Set up virtual home directory for isolated terminal
        self.virtual_home = self._setup_virtual_home()

        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)

        # Index button (left side)
        self.index_button = Gtk.Button.new_from_icon_name("view-grid-symbolic")
        self.index_button.set_tooltip_text("Lesson Index")
        self.index_button.connect("clicked", self.on_index_clicked)
        header.pack_start(self.index_button)

        # Main box (paned for resizable split)
        main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_paned.set_shrink_start_child(False)
        main_paned.set_shrink_end_child(False)
        main_paned.set_resize_start_child(True)
        main_paned.set_resize_end_child(True)

        # Left pane: Lesson content
        left_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_pane.set_size_request(550, -1)
        left_pane.set_vexpand(True)
        left_pane.set_hexpand(False)

        # Lesson viewer in a scrolled window
        self.lesson_viewer = LessonViewer()

        lesson_scrolled = Gtk.ScrolledWindow()
        lesson_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        lesson_scrolled.set_vexpand(True)
        lesson_scrolled.set_hexpand(True)
        lesson_scrolled.set_child(self.lesson_viewer)

        left_pane.append(lesson_scrolled)

        # Navigation buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        nav_box.set_margin_start(20)
        nav_box.set_margin_end(20)
        nav_box.set_margin_bottom(12)
        nav_box.set_margin_top(8)

        self.prev_button = Gtk.Button(label="← Previous")
        self.prev_button.connect("clicked", self.on_prev_clicked)
        nav_box.append(self.prev_button)

        # Mark complete button (center, expands)
        self.complete_button = Gtk.Button(label="Mark Complete")
        self.complete_button.add_css_class("suggested-action")
        self.complete_button.set_hexpand(True)
        self.complete_button.connect("clicked", self.on_complete_clicked)
        nav_box.append(self.complete_button)

        self.next_button = Gtk.Button(label="Next →")
        self.next_button.connect("clicked", self.on_next_clicked)
        nav_box.append(self.next_button)

        left_pane.append(nav_box)

        # Right pane: Terminal
        right_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        terminal_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        terminal_header.set_margin_start(12)
        terminal_header.set_margin_end(12)
        terminal_header.set_margin_top(12)

        terminal_label = Gtk.Label(label="Terminal")
        terminal_label.add_css_class("heading")
        terminal_label.set_halign(Gtk.Align.START)
        terminal_label.set_hexpand(True)
        terminal_header.append(terminal_label)

        # Clear terminal button
        clear_button = Gtk.Button.new_from_icon_name("edit-clear-symbolic")
        clear_button.set_tooltip_text("Clear Terminal")
        clear_button.connect("clicked", lambda b: self.terminal.reset(True, True))
        terminal_header.append(clear_button)

        right_pane.append(terminal_header)

        # VTE Terminal
        self.terminal = Vte.Terminal()
        # Set font
        font = Pango.FontDescription()
        font.set_family("Monospace")
        font.set_size(12 * Pango.SCALE)
        self.terminal.set_font(font)

        # Add keyboard shortcuts for copy/paste
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_terminal_key_pressed)
        self.terminal.add_controller(key_controller)

        # Spawn shell with isolated environment
        shell = os.environ.get("SHELL", "/bin/bash")

        # Create custom environment for the virtual home
        # Start with current environment and override HOME
        env_dict = dict(os.environ)
        env_dict["HOME"] = self.virtual_home
        env_dict["PWD"] = self.virtual_home

        # Convert to list of "KEY=VALUE" strings for spawn_async
        envv = [f"{key}={value}" for key, value in env_dict.items()]

        # Spawn the shell process using spawn_async
        # For VTE 3.91, spawn_async signature is:
        # spawn_async(pty_flags, working_directory, argv, envv, spawn_flags,
        #             child_setup, child_setup_data, timeout, cancellable, callback, user_data)
        # Callback signature: callback(source_object, result, user_data)
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,  # pty_flags
            self.virtual_home,     # working_directory (start in virtual home)
            [shell],               # argv
            envv,                  # envv (custom environment with virtual HOME)
            GLib.SpawnFlags.DEFAULT,  # spawn_flags
            None,                  # child_setup
            None,                  # child_setup_data
            -1,                    # timeout (-1 = no timeout)
            Gio.Cancellable(),     # cancellable
            None,                  # callback (None = no callback, we'll check status differently)
            None                   # user_data
        )

        terminal_scrolled = Gtk.ScrolledWindow()
        terminal_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        terminal_scrolled.set_child(self.terminal)
        terminal_scrolled.set_hexpand(True)
        terminal_scrolled.set_vexpand(True)
        right_pane.append(terminal_scrolled)

        # Pack panes
        main_paned.set_start_child(left_pane)
        main_paned.set_end_child(right_pane)
        main_paned.set_position(600)  # Initial split position

        # Content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content_box.append(header)
        content_box.append(main_paned)

        self.set_content(content_box)

        # Load first lesson
        GLib.idle_add(self.load_first_lesson)


    def _setup_virtual_home(self) -> str:
        """Set up an isolated virtual home directory for the terminal."""
        # Create virtual home in user's local data directory
        data_dir = Path.home() / ".local" / "share" / "terminal-fun"
        virtual_home = data_dir / "virtual-home"

        # Create the virtual home if it doesn't exist
        virtual_home.mkdir(parents=True, exist_ok=True)

        # Create realistic home directory structure
        common_dirs = [
            "Documents",
            "Downloads",
            "Pictures",
            "Music",
            "Videos",
            "Desktop",
            "workspace",
            "projects"
        ]

        for dir_name in common_dirs:
            (virtual_home / dir_name).mkdir(exist_ok=True)

        # Create a welcome README in the home directory
        readme_path = virtual_home / "README.txt"
        if not readme_path.exists():
            readme_content = """Welcome to Terminal Fun!

This is your practice terminal environment. Everything you do here is isolated
from your real home directory, so feel free to experiment!

Try these commands to get started:
  ls          - List files and directories
  pwd         - Print working directory
  cd Desktop  - Change to Desktop directory
  mkdir test  - Create a new directory

Happy learning!
"""
            readme_path.write_text(readme_content)

        return str(virtual_home)

    def load_first_lesson(self):
        """Load the first available lesson."""
        categories = self.lesson_loader.get_categories()
        if not categories:
            self.show_error("No lessons found!")
            return

        self.current_category = categories[0]
        lessons = self.lesson_loader.get_lessons(self.current_category)
        if lessons:
            self.load_lesson(self.current_category, lessons[0]['slug'])

    def load_lesson(self, category: str, lesson_slug: str):
        """Load and display a lesson."""
        lesson = self.lesson_loader.load_lesson(category, lesson_slug)
        if not lesson:
            self.show_error(f"Lesson not found: {category}/{lesson_slug}")
            return

        self.current_category = category
        self.current_lesson_slug = lesson_slug
        self.lesson_viewer.display_lesson(lesson)
        self.update_navigation_buttons()
        self.update_complete_button()

    def update_navigation_buttons(self):
        """Update prev/next button states."""
        if not self.current_category:
            self.prev_button.set_sensitive(False)
            self.next_button.set_sensitive(False)
            return

        lessons = self.lesson_loader.get_lessons(self.current_category)
        if not lessons:
            self.prev_button.set_sensitive(False)
            self.next_button.set_sensitive(False)
            return

        current_index = next(
            (i for i, l in enumerate(lessons) if l['slug'] == self.current_lesson_slug),
            -1
        )

        self.prev_button.set_sensitive(current_index > 0)
        self.next_button.set_sensitive(current_index < len(lessons) - 1)

    def update_complete_button(self):
        """Update complete button state and text."""
        if not self.current_category or not self.current_lesson_slug:
            self.complete_button.set_sensitive(False)
            return

        status = self.progress_tracker.get_lesson_status(
            self.current_category, 
            self.current_lesson_slug
        )

        if status == 'completed':
            self.complete_button.set_label("✓ Completed")
            self.complete_button.remove_css_class("suggested-action")
            self.complete_button.add_css_class("success")
        else:
            self.complete_button.set_label("Mark Complete")
            self.complete_button.remove_css_class("success")
            self.complete_button.add_css_class("suggested-action")

        self.complete_button.set_sensitive(True)

    def on_complete_clicked(self, button):
        """Toggle lesson completion status."""
        if not self.current_category or not self.current_lesson_slug:
            return

        status = self.progress_tracker.get_lesson_status(
            self.current_category,
            self.current_lesson_slug
        )

        if status == 'completed':
            # Uncomplete it
            self.progress_tracker.uncomplete_lesson(
                self.current_category,
                self.current_lesson_slug
            )
        else:
            # Complete it
            self.progress_tracker.complete_lesson(
                self.current_category,
                self.current_lesson_slug
            )

        self.update_complete_button()

    def on_terminal_key_pressed(self, controller, keyval, keycode, state):
        """Handle keyboard shortcuts in the terminal."""
        # Check for Ctrl+Shift modifier
        ctrl_shift = (state & Gdk.ModifierType.CONTROL_MASK and
                      state & Gdk.ModifierType.SHIFT_MASK)

        if ctrl_shift:
            # Ctrl+Shift+C - Copy
            if keyval == Gdk.keyval_from_name('c') or keyval == Gdk.keyval_from_name('C'):
                self.terminal.copy_clipboard_format(Vte.Format.TEXT)
                return True
            # Ctrl+Shift+V - Paste
            elif keyval == Gdk.keyval_from_name('v') or keyval == Gdk.keyval_from_name('V'):
                self.terminal.paste_clipboard()
                return True

        return False

    def on_prev_clicked(self, button):
        """Load previous lesson."""
        if not self.current_category or not self.current_lesson_slug:
            return

        lessons = self.lesson_loader.get_lessons(self.current_category)
        current_index = next(
            (i for i, l in enumerate(lessons) if l['slug'] == self.current_lesson_slug),
            -1
        )

        if current_index > 0:
            self.load_lesson(self.current_category, lessons[current_index - 1]['slug'])

    def on_next_clicked(self, button):
        """Load next lesson."""
        if not self.current_category or not self.current_lesson_slug:
            return

        lessons = self.lesson_loader.get_lessons(self.current_category)
        current_index = next(
            (i for i, l in enumerate(lessons) if l['slug'] == self.current_lesson_slug),
            -1
        )

        if current_index < len(lessons) - 1:
            self.load_lesson(self.current_category, lessons[current_index + 1]['slug'])

    def on_index_clicked(self, button):
        """Show lesson index dialog."""
        dialog = LessonIndexDialog(self, self.lesson_loader, self.progress_tracker)
        dialog.connect("lesson-selected", self.on_lesson_selected_from_index)
        dialog.present()

    def on_lesson_selected_from_index(self, dialog, category, lesson_slug):
        """Handle lesson selection from index."""
        print(f"DEBUG: Signal received - loading {category}/{lesson_slug}")
        dialog.close()
        self.load_lesson(category, lesson_slug)

    def show_error(self, message: str):
        """Show an error dialog."""
        dialog = Adw.MessageDialog(
            heading="Error",
            body=message,
            transient_for=self
        )
        dialog.add_response("ok", "OK")
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()


class LessonIndexDialog(Adw.Window):
    """Lesson index/navigation dialog."""

    __gsignals__ = {
        'lesson-selected': (GObject.SignalFlags.RUN_FIRST, None, (str, str))
    }
 
    def __init__(self, parent, lesson_loader, progress_tracker):
        super().__init__(transient_for=parent, title="Lesson Index", modal=True)
        self.set_default_size(700, 600)
        self.lesson_loader = lesson_loader
        self.progress_tracker = progress_tracker

        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)

        # Main content box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_vexpand(True)
        main_box.set_hexpand(True)

        # Title and description
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        title_box.set_margin_start(20)
        title_box.set_margin_end(20)
        title_box.set_margin_top(20)
        title_box.set_margin_bottom(12)

        title_label = Gtk.Label(label="Lesson Index")
        title_label.add_css_class("title-2")
        title_label.set_halign(Gtk.Align.START)
        title_box.append(title_label)

        desc_label = Gtk.Label(label="Choose a lesson to jump to")
        desc_label.add_css_class("dim-label")
        desc_label.set_halign(Gtk.Align.START)
        title_box.append(desc_label)

        main_box.append(title_box)

        # Scrolled window for lessons
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        # Content box for all categories
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(20)

        # Add each category
        categories = self.lesson_loader.get_categories()
        for category in categories:
            category_widget = self._create_category_widget(category)
            content_box.append(category_widget)

        scrolled.set_child(content_box)
        main_box.append(scrolled)

        # Wrap everything
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        outer_box.append(header)
        outer_box.append(main_box)

        self.set_content(outer_box)

    def _create_category_widget(self, category: str):
        """Create a widget for a category with its lessons."""
        category_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        # Category header
        category_label = Gtk.Label(label=self.lesson_loader.get_category_display_name(category))
        category_label.add_css_class("title-3")
        category_label.set_halign(Gtk.Align.START)
        category_box.append(category_label)

        # Lessons in this category
        lessons = self.lesson_loader.get_lessons(category)

        if lessons:
            list_box = Gtk.ListBox()
            list_box.add_css_class("boxed-list")
            list_box.set_selection_mode(Gtk.SelectionMode.NONE)

            # Store lesson data on the list_box for the signal handler
            list_box._lessons_data = []

            for lesson in lessons:
                row = self._create_lesson_row(category, lesson)
                # Store the lesson data on the row itself
                row._category = category
                row._lesson_slug = lesson['slug']
                list_box.append(row)
                list_box._lessons_data.append((category, lesson['slug']))

            # Connect to row-activated signal on the ListBox
            list_box.connect("row-activated", self._on_row_activated)

            category_box.append(list_box)
        else:
            empty_label = Gtk.Label(label="No lessons in this category")
            empty_label.add_css_class("dim-label")
            empty_label.set_halign(Gtk.Align.START)
            empty_label.set_margin_start(12)
            category_box.append(empty_label)

        return category_box

    def _on_row_activated(self, list_box, row):
        """Handle row activation."""
        category = row._category
        lesson_slug = row._lesson_slug
        print(f"DEBUG: Row activated - emitting signal for {category}/{lesson_slug}")
        self.emit("lesson-selected", category, lesson_slug)

    def _create_lesson_row(self, category: str, lesson: dict):
        """Create a row for a single lesson."""
        row = Gtk.ListBoxRow()
        row.set_activatable(True)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        # Lesson info
        lesson_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lesson_info_box.set_hexpand(True)

        # Title row with status indicator on the right
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        title_label = Gtk.Label(label=lesson['title'])
        title_label.set_halign(Gtk.Align.START)
        title_label.add_css_class("heading")
        title_label.set_hexpand(True)
        title_row.append(title_label)

        # Status indicator (check mark on the right)
        status = self.progress_tracker.get_lesson_status(category, lesson['slug'])
        if status == 'completed':
            status_icon = "✓"
            icon_label = Gtk.Label(label=status_icon)
            icon_label.add_css_class("success")
            icon_label.set_halign(Gtk.Align.END)
            title_row.append(icon_label)

        lesson_info_box.append(title_row)

        if lesson.get('description'):
            desc_label = Gtk.Label(label=lesson['description'])
            desc_label.set_halign(Gtk.Align.START)
            desc_label.add_css_class("dim-label")
            desc_label.add_css_class("caption")
            desc_label.set_wrap(True)
            desc_label.set_xalign(0)
            lesson_info_box.append(desc_label)

        box.append(lesson_info_box)

        row.set_child(box)

        return row


class TerminalFunApp(Adw.Application):
    """Main application."""

    def __init__(self):
        super().__init__()
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        """Application activation."""
        self.win = TerminalFunWindow(self)
        self.win.present()


def main():
    """Main entry point."""
    app = TerminalFunApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
