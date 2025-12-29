"""
Progress tracking system for Terminal Fun.
Tracks user progress through lessons and exercises.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


class ProgressTracker:
    """Manages user progress through lessons."""
    
    def __init__(self, progress_file: str = ".terminal_fun_progress.json"):
        self.progress_file = Path(progress_file)
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """Load progress from file or create new progress dict."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_empty_progress()
        return self._create_empty_progress()
    
    def _create_empty_progress(self) -> Dict:
        """Create an empty progress structure."""
        return {
            'lessons': {},
            'last_updated': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat()
        }
    
    def _save_progress(self):
        """Save progress to file."""
        self.progress['last_updated'] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save progress: {e}")
    
    def get_lesson_status(self, category: str, lesson_slug: str) -> str:
        """Get the status of a lesson: 'completed' or 'not_started'."""
        key = f"{category}/{lesson_slug}"
        lesson_data = self.progress['lessons'].get(key, {})
        return lesson_data.get('status', 'not_started')
    
    def complete_lesson(self, category: str, lesson_slug: str):
        """Mark a lesson as completed."""
        key = f"{category}/{lesson_slug}"
        if key not in self.progress['lessons']:
            self.progress['lessons'][key] = {}
        
        self.progress['lessons'][key]['status'] = 'completed'
        self.progress['lessons'][key]['completed_at'] = datetime.now().isoformat()
        self._save_progress()
    
    def uncomplete_lesson(self, category: str, lesson_slug: str):
        """Mark a lesson as not completed (reset)."""
        key = f"{category}/{lesson_slug}"
        if key in self.progress['lessons']:
            self.progress['lessons'][key]['status'] = 'not_started'
            if 'completed_at' in self.progress['lessons'][key]:
                del self.progress['lessons'][key]['completed_at']
            self._save_progress()
    
    def complete_exercise(self, category: str, lesson_slug: str, exercise_index: int):
        """Mark an exercise as completed."""
        key = f"{category}/{lesson_slug}"
        if key not in self.progress['lessons']:
            self.progress['lessons'][key] = {'exercises': {}}
        
        if 'exercises' not in self.progress['lessons'][key]:
            self.progress['lessons'][key]['exercises'] = {}
        
        self.progress['lessons'][key]['exercises'][str(exercise_index)] = {
            'status': 'completed',
            'completed_at': datetime.now().isoformat()
        }
        self._save_progress()
    
    def get_exercise_status(self, category: str, lesson_slug: str, exercise_index: int) -> str:
        """Get the status of an exercise: 'completed' or 'not_started'."""
        key = f"{category}/{lesson_slug}"
        lesson_data = self.progress['lessons'].get(key, {})
        exercises = lesson_data.get('exercises', {})
        exercise_data = exercises.get(str(exercise_index), {})
        return exercise_data.get('status', 'not_started')
    
    def get_all_progress(self) -> Dict:
        """Get all progress data."""
        return self.progress.copy()
    
    def get_stats(self) -> Dict:
        """Get overall progress statistics."""
        lessons = self.progress.get('lessons', {})
        total = len(lessons)
        completed = sum(1 for l in lessons.values() if l.get('status') == 'completed')
        
        return {
            'total': total,
            'completed': completed,
            'not_started': total - completed
        }
