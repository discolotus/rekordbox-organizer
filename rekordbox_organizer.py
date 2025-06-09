#!/usr/bin/env python3
"""
Rekordbox Music Organizer

A tool to organize music files based on their Rekordbox "date added" metadata.
Files are organized into YYYY-MM folders with a flat structure (no subdirectories).

Usage:
    python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --dry-run
    python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --execute
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from pyrekordbox import Rekordbox6Database
    from pyrekordbox.rbxml import RekordboxXml
except ImportError:
    print("Error: pyrekordbox not installed. Install with: pip install pyrekordbox")
    sys.exit(1)

from music_file_scanner import MusicFileScanner


class RekordboxOrganizer:
    """Organizes music files based on Rekordbox date added metadata."""
    
    SUPPORTED_FORMATS = {'.mp3', '.flac', '.wav', '.aiff', '.m4a', '.aac', '.ogg'}
    
    def __init__(self, source_dir: str, target_dir: str, dry_run: bool = True):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.scanner = MusicFileScanner()
        self.rekordbox_db = None
        self.rekordbox_xml = None
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'no_date_files': 0,
            'skipped_files': 0,
            'errors': 0,
            'conflicts_resolved': 0
        }
    
    def connect_to_rekordbox(self, xml_path: Optional[str] = None) -> bool:
        """Connect to Rekordbox database or XML file."""
        try:
            if xml_path and Path(xml_path).exists():
                print(f"Loading Rekordbox XML: {xml_path}")
                self.rekordbox_xml = RekordboxXml(xml_path)
                return True
            else:
                print("Attempting to connect to Rekordbox 6/7 database...")
                self.rekordbox_db = Rekordbox6Database()
                return True
        except Exception as e:
            print(f"Failed to connect to Rekordbox: {e}")
            print("Please ensure Rekordbox is installed or provide an XML export file.")
            return False
    
    def get_date_added(self, file_path: Path) -> Optional[datetime]:
        """Get the date added from Rekordbox for a given file."""
        try:
            file_str = str(file_path)
            file_name = file_path.name

            if self.rekordbox_db:
                # Search in Rekordbox 6/7 database
                contents = self.rekordbox_db.get_content()

                # Convert query to list if needed
                if hasattr(contents, '__iter__') and not isinstance(contents, list):
                    contents = list(contents)

                for content in contents:
                    content_path = getattr(content, 'FolderPath', '')
                    if content_path:
                        # Try exact path match first
                        if file_str == content_path or file_str.endswith(content_path):
                            date_added = getattr(content, 'DateAdded', None) or getattr(content, 'created_at', None)
                            if date_added:
                                return date_added

                        # Try filename match as fallback
                        if content_path.endswith(file_name):
                            date_added = getattr(content, 'DateAdded', None) or getattr(content, 'created_at', None)
                            if date_added:
                                return date_added

            elif self.rekordbox_xml:
                # Search in XML database
                tracks = self.rekordbox_xml.get_tracks()
                for track in tracks:
                    track_location = track.get('Location', '')
                    if track_location:
                        # Clean up the location path
                        clean_location = track_location.replace('file://localhost', '').replace('file://', '')
                        if file_str == clean_location or file_str.endswith(clean_location) or clean_location.endswith(file_name):
                            date_added = track.get('DateAdded')
                            if date_added:
                                return datetime.fromisoformat(date_added.replace('Z', '+00:00'))

            return None

        except Exception as e:
            print(f"Error getting date added for {file_path}: {e}")
            return None
    
    def create_target_path(self, date_added: Optional[datetime], original_file: Path) -> Path:
        """Create target path based on date added (YYYY-MM format) or no-date folder."""
        if date_added:
            year_month = date_added.strftime("%Y-%m")
            target_folder = self.target_dir / year_month
        else:
            target_folder = self.target_dir / "no-date"
        return target_folder / original_file.name
    
    def resolve_filename_conflict(self, target_path: Path) -> Path:
        """Resolve filename conflicts by appending numbers."""
        if not target_path.exists():
            return target_path
        
        base_name = target_path.stem
        extension = target_path.suffix
        parent = target_path.parent
        counter = 1
        
        while True:
            new_name = f"{base_name}-{counter}{extension}"
            new_path = parent / new_name
            if not new_path.exists():
                self.stats['conflicts_resolved'] += 1
                return new_path
            counter += 1
    
    def move_file(self, source: Path, target: Path) -> bool:
        """Move file from source to target, creating directories as needed."""
        try:
            if self.dry_run:
                print(f"[DRY RUN] Would move: {source} -> {target}")
                return True
            
            # Create target directory if it doesn't exist
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Resolve conflicts
            final_target = self.resolve_filename_conflict(target)
            
            # Move the file
            shutil.move(str(source), str(final_target))
            print(f"Moved: {source} -> {final_target}")
            return True
            
        except Exception as e:
            print(f"Error moving {source} to {target}: {e}")
            self.stats['errors'] += 1
            return False
    
    def organize_files(self, xml_path: Optional[str] = None) -> None:
        """Main method to organize files based on Rekordbox metadata."""
        print("=== Rekordbox Music Organizer ===")
        print(f"Source: {self.source_dir}")
        print(f"Target: {self.target_dir}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print()
        
        # Connect to Rekordbox
        if not self.connect_to_rekordbox(xml_path):
            return
        
        # Scan for music files
        print("Scanning for music files...")
        music_files = self.scanner.scan_directory(self.source_dir, self.SUPPORTED_FORMATS)
        self.stats['total_files'] = len(music_files)
        
        if not music_files:
            print("No music files found!")
            return
        
        print(f"Found {len(music_files)} music files")
        print()
        
        # Process each file
        for i, file_path in enumerate(music_files, 1):
            print(f"Processing {i}/{len(music_files)}: {file_path.name}")

            # Get date added from Rekordbox
            date_added = self.get_date_added(file_path)

            # Create target path (handles both dated and no-date files)
            target_path = self.create_target_path(date_added, file_path)

            if date_added:
                print(f"  📅 Date added: {date_added.strftime('%Y-%m-%d')}")
                print(f"  📁 Target: {target_path}")
            else:
                print(f"  ⚠️  No date added found in Rekordbox")
                print(f"  📁 Target: {target_path} (no-date folder)")
                self.stats['no_date_files'] += 1

            # Move file
            if self.move_file(file_path, target_path):
                self.stats['processed_files'] += 1
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print operation summary."""
        print("\n=== Summary ===")
        print(f"Total files found: {self.stats['total_files']}")
        print(f"Files processed: {self.stats['processed_files']}")
        print(f"  - With date metadata: {self.stats['processed_files'] - self.stats['no_date_files']}")
        print(f"  - Without date (moved to no-date): {self.stats['no_date_files']}")
        print(f"Files skipped: {self.stats['skipped_files']}")
        print(f"Conflicts resolved: {self.stats['conflicts_resolved']}")
        print(f"Errors: {self.stats['errors']}")


def main():
    parser = argparse.ArgumentParser(description="Organize music files based on Rekordbox date added metadata")
    parser.add_argument("--source", "-s", required=True, help="Source directory containing music files")
    parser.add_argument("--target", "-t", required=True, help="Target directory for organized files")
    parser.add_argument("--xml", "-x", help="Path to Rekordbox XML export file (optional)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview changes without executing (default)")
    parser.add_argument("--execute", action="store_true", help="Execute the organization (overrides --dry-run)")
    
    args = parser.parse_args()
    
    # Validate directories
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        sys.exit(1)
    
    # Determine if this is a dry run
    dry_run = not args.execute
    
    # Create organizer and run
    organizer = RekordboxOrganizer(args.source, args.target, dry_run=dry_run)
    organizer.organize_files(xml_path=args.xml)


if __name__ == "__main__":
    main()
