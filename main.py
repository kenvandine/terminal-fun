#!/usr/bin/env python3
"""
Terminal Fun - An interactive learning app for mastering the Linux command line.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from lesson_loader import LessonLoader
from progress_tracker import ProgressTracker
from ui import TerminalUI


def main():
    """Main entry point for Terminal Fun."""
    ui = TerminalUI()
    progress_tracker = ProgressTracker()
    lesson_loader = LessonLoader()
    
    # Show welcome screen
    ui.show_welcome()
    
    # Main menu loop
    while True:
        choice = ui.show_main_menu(progress_tracker)
        
        if choice == '1':
            # Continue learning
            continue_learning(ui, progress_tracker, lesson_loader)
        elif choice == '2':
            # View progress
            ui.show_progress(progress_tracker)
        elif choice == '3':
            # Select specific lesson
            select_lesson(ui, progress_tracker, lesson_loader)
        elif choice == '4':
            # Exit
            ui.show_goodbye()
            break
        else:
            ui.print_error("Invalid choice. Please try again.")


def continue_learning(ui: TerminalUI, progress_tracker: ProgressTracker, lesson_loader: LessonLoader):
    """Continue from where the user left off."""
    # Get all lessons to find the next one
    categories = lesson_loader.get_categories()
    next_lesson = None
    
    for category in categories:
        lessons = lesson_loader.get_lessons(category)
        for lesson in lessons:
            status = progress_tracker.get_lesson_status(category, lesson['slug'])
            if status != 'completed':
                next_lesson = {'category': category, 'slug': lesson['slug'], 'title': lesson['title']}
                break
        if next_lesson:
            break
    
    if next_lesson is None:
        ui.print_success("🎉 Congratulations! You've completed all lessons!")
        ui.print_info("You are now a Linux command line master!")
        return
    
    ui.print_info(f"Resuming from: {next_lesson['category']} - {next_lesson['title']}")
    run_lesson(ui, progress_tracker, lesson_loader, next_lesson['category'], next_lesson['slug'])


def select_lesson(ui: TerminalUI, progress_tracker: ProgressTracker, lesson_loader: LessonLoader):
    """Allow user to select a specific lesson."""
    categories = lesson_loader.get_categories()
    
    if not categories:
        ui.print_error("No lessons found!")
        return
    
    ui.print_header("Select a Category")
    for idx, category in enumerate(categories, 1):
        ui.print(f"  {idx}. {category}")
    
    try:
        cat_choice = int(ui.get_input("\nEnter category number: ")) - 1
        if cat_choice < 0 or cat_choice >= len(categories):
            ui.print_error("Invalid category selection.")
            return
        
        selected_category = categories[cat_choice]
        lessons = lesson_loader.get_lessons(selected_category)
        
        ui.print_header(f"Lessons in {selected_category}")
        for idx, lesson in enumerate(lessons, 1):
            status = progress_tracker.get_lesson_status(selected_category, lesson['slug'])
            status_icon = "✓" if status == "completed" else "✗" if status == "failed" else "○"
            ui.print(f"  {idx}. {status_icon} {lesson['title']}")
        
        lesson_choice = int(ui.get_input("\nEnter lesson number: ")) - 1
        if lesson_choice < 0 or lesson_choice >= len(lessons):
            ui.print_error("Invalid lesson selection.")
            return
        
        selected_lesson = lessons[lesson_choice]
        run_lesson(ui, progress_tracker, lesson_loader, selected_category, selected_lesson['slug'])
        
    except ValueError:
        ui.print_error("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        ui.print("\n")
        return


def run_lesson(ui: TerminalUI, progress_tracker: ProgressTracker, lesson_loader: LessonLoader, 
               category: str, lesson_slug: str):
    """Run a specific lesson."""
    lesson = lesson_loader.load_lesson(category, lesson_slug)
    
    if not lesson:
        ui.print_error(f"Lesson not found: {category}/{lesson_slug}")
        return
    
    ui.print_header(f"{lesson['title']}")
    ui.print(f"\n{lesson['description']}\n")
    
    # Show instructions
    if lesson.get('instructions'):
        ui.print_section("📚 Instructions")
        ui.print(lesson['instructions'])
        ui.print()
    
    # Run exercises
    if lesson.get('exercises'):
        ui.print_section("🎯 Hands-On Practice")
        
        for idx, exercise in enumerate(lesson['exercises'], 1):
            ui.print_subheader(f"Exercise {idx}: {exercise['title']}")
            ui.print(f"{exercise['description']}\n")
            
            if exercise.get('command'):
                ui.print_info(f"Try running: {exercise['command']}")
            
            # Check if user completed the exercise
            ui.print_info("Press Enter when you've completed this exercise, or 's' to skip...")
            user_input = ui.get_input("> ").strip().lower()
            
            if user_input == 's':
                ui.print_warning("Skipped this exercise.")
                continue
            
            # Verify exercise completion (basic check)
            if exercise.get('verify'):
                if verify_exercise(exercise['verify']):
                    ui.print_success("✓ Exercise completed successfully!")
                    progress_tracker.complete_exercise(category, lesson_slug, idx - 1)
                else:
                    ui.print_warning("⚠ Exercise may not be completed correctly.")
                    ui.print_info("You can continue anyway, or try again.")
                    retry = ui.get_input("Try again? (y/n): ").strip().lower()
                    if retry == 'y':
                        continue
                    progress_tracker.fail_exercise(category, lesson_slug, idx - 1)
            else:
                # No verification, just mark as attempted
                ui.print_info("Exercise marked as attempted.")
                progress_tracker.complete_exercise(category, lesson_slug, idx - 1)
            
            ui.print()
    
    # Mark lesson as completed
    progress_tracker.complete_lesson(category, lesson_slug)
    ui.print_success(f"\n🎉 Lesson '{lesson['title']}' completed!")
    ui.print_info("Press Enter to continue...")
    ui.get_input()


def verify_exercise(verify_config: Dict) -> bool:
    """Verify if an exercise has been completed correctly."""
    import subprocess
    from os.path import expanduser
    
    verify_type = verify_config.get('type')
    
    if verify_type == 'file_exists':
        path_str = verify_config['path']
        if path_str.startswith('~'):
            path_str = expanduser(path_str)
        file_path = Path(path_str)
        return file_path.exists()
    
    elif verify_type == 'directory_exists':
        path_str = verify_config['path']
        if path_str.startswith('~'):
            path_str = expanduser(path_str)
        dir_path = Path(path_str)
        return dir_path.exists() and dir_path.is_dir()
    
    elif verify_type == 'command_output':
        try:
            result = subprocess.run(
                verify_config['command'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            expected = verify_config.get('contains', '')
            if expected:
                return expected in result.stdout or expected in result.stderr
            # If no expected content, just check that command ran successfully
            return result.returncode == 0
        except Exception:
            return False
    
    elif verify_type == 'current_directory':
        path_str = verify_config['path']
        if path_str == '~' or path_str.startswith('~/'):
            expected_path = Path(expanduser(path_str)).resolve()
        else:
            expected_path = Path(path_str).resolve()
        current_path = Path.cwd().resolve()
        return expected_path == current_path
    
    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Your progress has been saved.")
        sys.exit(0)

