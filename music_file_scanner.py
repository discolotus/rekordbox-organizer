#!/usr/bin/env python3
"""
Music File Scanner

A utility for scanning directories and finding music files.
Supports recursive scanning and filtering by file extensions.
"""

import os
from pathlib import Path
from typing import List, Set, Optional
import mimetypes


class MusicFileScanner:
    """Scanner for finding music files in directories."""
    
    # Common music file extensions
    DEFAULT_MUSIC_EXTENSIONS = {
        '.mp3', '.flac', '.wav', '.aiff', '.aif', '.m4a', '.aac', 
        '.ogg', '.oga', '.wma', '.opus', '.mp4', '.m4p', '.3gp'
    }
    
    # MIME types for music files
    MUSIC_MIME_TYPES = {
        'audio/mpeg', 'audio/flac', 'audio/wav', 'audio/x-wav',
        'audio/aiff', 'audio/x-aiff', 'audio/mp4', 'audio/aac',
        'audio/ogg', 'audio/vorbis', 'audio/opus', 'audio/x-ms-wma'
    }
    
    def __init__(self):
        # Initialize mimetypes
        mimetypes.init()
    
    def is_music_file(self, file_path: Path, extensions: Optional[Set[str]] = None) -> bool:
        """
        Check if a file is a music file based on extension and/or MIME type.
        
        Args:
            file_path: Path to the file to check
            extensions: Set of allowed extensions (defaults to DEFAULT_MUSIC_EXTENSIONS)
        
        Returns:
            True if the file is considered a music file
        """
        if extensions is None:
            extensions = self.DEFAULT_MUSIC_EXTENSIONS
        
        # Check by extension
        if file_path.suffix.lower() in extensions:
            return True
        
        # Check by MIME type as fallback
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type in self.MUSIC_MIME_TYPES:
            return True
        
        return False
    
    def scan_directory(self, directory: Path, extensions: Optional[Set[str]] = None, 
                      recursive: bool = True) -> List[Path]:
        """
        Scan a directory for music files.
        
        Args:
            directory: Directory to scan
            extensions: Set of allowed file extensions
            recursive: Whether to scan subdirectories recursively
        
        Returns:
            List of paths to music files found
        """
        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        
        if not directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")
        
        music_files = []
        
        if recursive:
            # Use rglob for recursive scanning
            for file_path in directory.rglob('*'):
                if file_path.is_file() and self.is_music_file(file_path, extensions):
                    music_files.append(file_path)
        else:
            # Scan only the immediate directory
            for file_path in directory.iterdir():
                if file_path.is_file() and self.is_music_file(file_path, extensions):
                    music_files.append(file_path)
        
        # Sort files for consistent ordering
        music_files.sort()
        return music_files
    
    def get_directory_stats(self, directory: Path, extensions: Optional[Set[str]] = None) -> dict:
        """
        Get statistics about music files in a directory.
        
        Args:
            directory: Directory to analyze
            extensions: Set of allowed file extensions
        
        Returns:
            Dictionary with statistics
        """
        music_files = self.scan_directory(directory, extensions)
        
        # Count files by extension
        extension_counts = {}
        total_size = 0
        
        for file_path in music_files:
            ext = file_path.suffix.lower()
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
            
            try:
                total_size += file_path.stat().st_size
            except OSError:
                pass  # Skip files that can't be accessed
        
        return {
            'total_files': len(music_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'extension_counts': extension_counts,
            'files': music_files
        }
    
    def find_nested_files(self, directory: Path, extensions: Optional[Set[str]] = None) -> dict:
        """
        Find music files and organize them by their directory depth.
        Useful for understanding the nesting structure.
        
        Args:
            directory: Root directory to scan
            extensions: Set of allowed file extensions
        
        Returns:
            Dictionary mapping depth levels to lists of files
        """
        music_files = self.scan_directory(directory, extensions)
        depth_map = {}
        
        for file_path in music_files:
            # Calculate depth relative to the root directory
            try:
                relative_path = file_path.relative_to(directory)
                depth = len(relative_path.parts) - 1  # Subtract 1 for the file itself
                
                if depth not in depth_map:
                    depth_map[depth] = []
                depth_map[depth].append(file_path)
            except ValueError:
                # File is not relative to the directory (shouldn't happen)
                continue
        
        return depth_map
    
    def preview_flattening(self, directory: Path, extensions: Optional[Set[str]] = None) -> dict:
        """
        Preview what would happen if all files were flattened to a single directory.
        Shows potential filename conflicts.
        
        Args:
            directory: Directory to analyze
            extensions: Set of allowed file extensions
        
        Returns:
            Dictionary with flattening preview information
        """
        music_files = self.scan_directory(directory, extensions)
        
        filename_map = {}
        conflicts = {}
        
        for file_path in music_files:
            filename = file_path.name
            
            if filename in filename_map:
                # Conflict detected
                if filename not in conflicts:
                    conflicts[filename] = [filename_map[filename]]
                conflicts[filename].append(file_path)
            else:
                filename_map[filename] = file_path
        
        return {
            'total_files': len(music_files),
            'unique_filenames': len(filename_map),
            'conflicts': conflicts,
            'conflict_count': len(conflicts),
            'files_with_conflicts': sum(len(paths) for paths in conflicts.values())
        }


def main():
    """Command-line interface for the music file scanner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan directories for music files")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--extensions", "-e", nargs="+", 
                       help="File extensions to include (e.g., .mp3 .flac)")
    parser.add_argument("--no-recursive", action="store_true", 
                       help="Don't scan subdirectories")
    parser.add_argument("--stats", action="store_true", 
                       help="Show detailed statistics")
    parser.add_argument("--depth-analysis", action="store_true",
                       help="Analyze files by directory depth")
    parser.add_argument("--flatten-preview", action="store_true",
                       help="Preview filename conflicts if flattened")
    
    args = parser.parse_args()
    
    # Validate directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory does not exist: {directory}")
        return
    
    # Prepare extensions
    extensions = None
    if args.extensions:
        extensions = {ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                     for ext in args.extensions}
    
    # Create scanner
    scanner = MusicFileScanner()
    
    try:
        if args.stats:
            stats = scanner.get_directory_stats(directory, extensions)
            print(f"=== Music File Statistics ===")
            print(f"Directory: {directory}")
            print(f"Total files: {stats['total_files']}")
            print(f"Total size: {stats['total_size_mb']} MB")
            print(f"\nFiles by extension:")
            for ext, count in sorted(stats['extension_counts'].items()):
                print(f"  {ext}: {count}")
        
        elif args.depth_analysis:
            depth_map = scanner.find_nested_files(directory, extensions)
            print(f"=== Directory Depth Analysis ===")
            print(f"Directory: {directory}")
            for depth in sorted(depth_map.keys()):
                print(f"Depth {depth}: {len(depth_map[depth])} files")
                if depth <= 2:  # Show examples for shallow depths
                    for file_path in depth_map[depth][:3]:
                        print(f"  {file_path}")
                    if len(depth_map[depth]) > 3:
                        print(f"  ... and {len(depth_map[depth]) - 3} more")
        
        elif args.flatten_preview:
            preview = scanner.preview_flattening(directory, extensions)
            print(f"=== Flattening Preview ===")
            print(f"Directory: {directory}")
            print(f"Total files: {preview['total_files']}")
            print(f"Unique filenames: {preview['unique_filenames']}")
            print(f"Filename conflicts: {preview['conflict_count']}")
            print(f"Files involved in conflicts: {preview['files_with_conflicts']}")
            
            if preview['conflicts']:
                print(f"\nConflicting filenames:")
                for filename, paths in list(preview['conflicts'].items())[:5]:
                    print(f"  {filename} ({len(paths)} files):")
                    for path in paths[:2]:
                        print(f"    {path}")
                    if len(paths) > 2:
                        print(f"    ... and {len(paths) - 2} more")
                
                if len(preview['conflicts']) > 5:
                    print(f"  ... and {len(preview['conflicts']) - 5} more conflicts")
        
        else:
            # Simple file listing
            music_files = scanner.scan_directory(directory, extensions, 
                                                not args.no_recursive)
            print(f"Found {len(music_files)} music files in {directory}")
            for file_path in music_files:
                print(file_path)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
