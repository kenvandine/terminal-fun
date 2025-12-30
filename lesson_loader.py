"""
Lesson loader for Terminal Fun.
Loads lesson content from markdown files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class LessonLoader:
    """Loads and parses lesson content from markdown files."""

    def __init__(self, lessons_dir: Optional[str] = None):
        # Check environment variable first, then use provided dir, then fallback to "lessons"
        if lessons_dir is None:
            lessons_dir = os.environ.get('TERMINAL_FUN_LESSONS_DIR', 'lessons')

        self.lessons_dir = Path(lessons_dir)
        self._lessons_cache: Dict[str, Dict[str, Dict]] = {}
        self._load_all_lessons()
    
    def _load_all_lessons(self):
        """Load all lessons from the lessons directory."""
        if not self.lessons_dir.exists():
            return
        
        for category_dir in self.lessons_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                category = category_dir.name
                self._lessons_cache[category] = {}
                
                for lesson_file in category_dir.glob("*.md"):
                    lesson_slug = lesson_file.stem
                    self._lessons_cache[category][lesson_slug] = None  # Lazy load
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        return sorted(self._lessons_cache.keys())
    
    def get_category_display_name(self, category: str) -> str:
        """Get a human-readable name for a category."""
        # Convert directory name to display name
        return category.replace('-', ' ').replace('_', ' ').title() 

    def get_lessons(self, category: str) -> List[Dict]:
        """Get all lessons in a category."""
        if category not in self._lessons_cache:
            return []
        
        lessons = []
        category_dir = self.lessons_dir / category
        
        for lesson_file in category_dir.glob("*.md"):
            lesson_slug = lesson_file.stem
            lesson_meta = self._load_lesson_metadata(category, lesson_slug)
            if lesson_meta:
                lessons.append({
                    'slug': lesson_slug,
                    'title': lesson_meta.get('title', lesson_slug),
                    'description': lesson_meta.get('description', ''),
                    'order': lesson_meta.get('order', 999)
                })
        
        # Sort by order
        lessons.sort(key=lambda x: x['order'])
        return lessons
    
    def load_lesson(self, category: str, lesson_slug: str) -> Optional[Dict]:
        """Load a complete lesson."""
        # Check cache first
        if (category in self._lessons_cache and 
            lesson_slug in self._lessons_cache[category] and
            self._lessons_cache[category][lesson_slug] is not None):
            return self._lessons_cache[category][lesson_slug]
        
        lesson_file = self.lessons_dir / category / f"{lesson_slug}.md"
        
        if not lesson_file.exists():
            return None
        
        try:
            content = lesson_file.read_text()
            lesson_data = self._parse_lesson_markdown(content)
            lesson_data['slug'] = lesson_slug
            lesson_data['category'] = category
            
            # Cache it
            if category not in self._lessons_cache:
                self._lessons_cache[category] = {}
            self._lessons_cache[category][lesson_slug] = lesson_data
            
            return lesson_data
        except Exception as e:
            print(f"Error loading lesson {category}/{lesson_slug}: {e}")
            return None
    
    def _load_lesson_metadata(self, category: str, lesson_slug: str) -> Optional[Dict]:
        """Load just the metadata (frontmatter) of a lesson."""
        lesson_file = self.lessons_dir / category / f"{lesson_slug}.md"
        
        if not lesson_file.exists():
            return None
        
        try:
            content = lesson_file.read_text()
            frontmatter, _ = self._split_frontmatter(content)
            if frontmatter:
                return yaml.safe_load(frontmatter)
            return {}
        except Exception:
            return {}
    
    def _parse_lesson_markdown(self, content: str) -> Dict:
        """Parse a lesson markdown file into structured data."""
        frontmatter, body = self._split_frontmatter(content)
        
        metadata = {}
        if frontmatter:
            metadata = yaml.safe_load(frontmatter) or {}
        
        # Parse the body for sections
        sections = self._parse_body_sections(body)
        
        lesson_data = {
            'title': metadata.get('title', 'Untitled Lesson'),
            'description': metadata.get('description', ''),
            'instructions': sections.get('instructions', ''),
            'exercises': sections.get('exercises', [])
        }
        
        return lesson_data
    
    def _split_frontmatter(self, content: str) -> Tuple[Optional[str], str]:
        """Split YAML frontmatter from markdown content."""
        if not content.startswith('---'):
            return None, content
        
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[1].strip(), parts[2].strip()
        
        return None, content
    
    def _parse_body_sections(self, body: str) -> Dict:
        """Parse the body into instructions and exercises."""
        sections = {
            'instructions': '',
            'exercises': []
        }
        
        # Split by exercise markers
        parts = body.split('## Exercise')
        
        # First part is instructions (if exists)
        if len(parts) > 0:
            instructions_part = parts[0].strip()
            # Remove section header if present
            if instructions_part.startswith('## Instructions'):
                instructions_part = '\n'.join(instructions_part.split('\n')[1:]).strip()
            sections['instructions'] = instructions_part
        
        # Parse exercises
        for i, exercise_part in enumerate(parts[1:], 1):
            # Extract title from first line
            lines = exercise_part.strip().split('\n')
            title_line = lines[0] if lines else ""
            title = title_line.replace('#', '').strip() or f"Exercise {i}"
            
            # Find Command and Verify sections
            description_lines = []
            command = None
            verify = None
            in_verify_block = False
            verify_lines = []
            
            j = 1  # Start after title line
            while j < len(lines):
                line = lines[j]
                stripped = line.strip()
                
                if stripped.startswith('**Command:**'):
                    # Extract command
                    cmd_text = stripped.replace('**Command:**', '').strip()
                    # Remove backticks if present
                    command = cmd_text.strip('`').strip()
                    j += 1
                elif stripped.startswith('**Verify:**'):
                    # Start collecting verify YAML
                    in_verify_block = True
                    j += 1
                    # Check if next line is code block
                    if j < len(lines) and lines[j].strip().startswith('```'):
                        j += 1  # Skip opening ```
                        # Collect until closing ```
                        while j < len(lines) and not lines[j].strip().endswith('```'):
                            verify_lines.append(lines[j])
                            j += 1
                        if j < len(lines):
                            j += 1  # Skip closing ```
                    else:
                        # Inline YAML
                        while j < len(lines) and not lines[j].strip().startswith('**'):
                            verify_lines.append(lines[j])
                            j += 1
                        j -= 1  # Backup one since we'll increment
                    
                    # Parse YAML
                    if verify_lines:
                        try:
                            verify = yaml.safe_load('\n'.join(verify_lines))
                        except Exception:
                            pass
                    in_verify_block = False
                    verify_lines = []
                elif not in_verify_block and stripped and not stripped.startswith('```'):
                    # Collect description (everything that's not Command/Verify)
                    description_lines.append(line)
                
                j += 1
            
            exercise = {
                'title': title,
                'description': '\n'.join(description_lines).strip(),
                'command': command,
                'verify': verify
            }
            sections['exercises'].append(exercise)
        
        return sections

