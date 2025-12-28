#!/usr/bin/env python3
"""
Terminal Fun - GTK4 Application
A graphical learning app for mastering the Linux command line.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Vte', '3.91')

from gi.repository import Gtk, Adw, Vte, GLib, Pango, Gio
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
        
        # Step 0: Handle fenced code blocks ```code```
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
        
        # Step 1: Handle headings ### Heading
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
        
        # Step 2: Handle **`code`** patterns (bold code) first
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
        
        # Step 3: Handle standalone code `code`
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
        
        # Step 4: Handle standalone bold **text** (but not if it contains placeholders)
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
        
        # Step 5: Escape remaining text (but not placeholders - they're safe)
        text = GLib.markup_escape_text(text)
        
        # Step 6: Restore all placeholders with their HTML
        for placeholder, html in (heading_placeholders + code_block_placeholders + 
                                  bold_code_placeholders + code_placeholders + bold_placeholders):
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
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        
        # Progress button
        self.progress_button = Gtk.Button.new_from_icon_name("view-list-symbolic")
        self.progress_button.set_tooltip_text("View Progress")
        self.progress_button.connect("clicked", self.on_progress_clicked)
        header.pack_start(self.progress_button)
        
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
        
        # Spawn shell
        shell = os.environ.get("SHELL", "/bin/bash")
        working_dir = os.environ.get("HOME", None)
        
        # Spawn the shell process using spawn_async
        # For VTE 3.91, spawn_async signature is:
        # spawn_async(pty_flags, working_directory, argv, envv, spawn_flags,
        #             child_setup, child_setup_data, timeout, cancellable, callback, user_data)
        # Callback signature: callback(source_object, result, user_data)
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,  # pty_flags
            working_dir,           # working_directory  
            [shell],               # argv
            None,                  # envv (None = inherit environment)
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
    
    def on_progress_clicked(self, button):
        """Show progress dialog."""
        dialog = ProgressDialog(self)
        dialog.present()
    
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


class ProgressDialog(Adw.Window):
    """Progress viewing dialog."""
    
    def __init__(self, parent):
        super().__init__(transient_for=parent, title="Progress", modal=True)
        self.set_default_size(500, 600)
        self.progress_tracker = ProgressTracker()
        
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        
        # Main content box that expands
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_vexpand(True)
        main_box.set_hexpand(True)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_start(20)
        content.set_margin_end(20)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_vexpand(True)
        content.set_hexpand(True)
        
        stats = self.progress_tracker.get_stats()
        
        stats_label = Gtk.Label(label=f"Completed: {stats['completed']}\nFailed: {stats['failed']}\nNot Started: {stats['not_started']}")
        stats_label.add_css_class("heading")
        content.append(stats_label)
        
        # Scrolled window that expands
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_propagate_natural_height(False)
        
        list_box = Gtk.ListBox()
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        progress = self.progress_tracker.get_all_progress()
        if progress.get('lessons'):
            for lesson_key, lesson_data in sorted(progress['lessons'].items()):
                row = Gtk.ListBoxRow()
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
                box.set_margin_start(12)
                box.set_margin_end(12)
                box.set_margin_top(8)
                box.set_margin_bottom(8)
                
                status = lesson_data.get('status', 'not_started')
                status_icon = "✓" if status == "completed" else "✗" if status == "failed" else "○"
                icon_label = Gtk.Label(label=status_icon)
                icon_label.set_size_request(30, -1)
                box.append(icon_label)
                
                name_label = Gtk.Label(label=lesson_key)
                name_label.set_halign(Gtk.Align.START)
                name_label.set_hexpand(True)
                box.append(name_label)
                
                row.set_child(box)
                list_box.append(row)
        else:
            empty_label = Gtk.Label(label="No progress yet. Start learning!")
            empty_label.set_margin_top(20)
            list_box.append(empty_label)
        
        scrolled.set_child(list_box)
        content.append(scrolled)
        
        # Close button
        close_button = Gtk.Button(label="Close")
        close_button.add_css_class("suggested-action")
        close_button.connect("clicked", lambda b: self.destroy())
        content.append(close_button)
        
        main_box.append(header)
        main_box.append(content)
        
        self.set_content(main_box)


class TerminalFunApp(Adw.Application):
    """Main application."""
    
    def __init__(self):
        super().__init__(application_id="com.terminalfun.app")
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

