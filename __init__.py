"""
Rekordbox Music Organizer

A Python package to organize music files based on their Rekordbox "date added" metadata.
Files are organized into YYYY-MM folders with a flat structure.
"""

__version__ = "1.0.0"
__author__ = "discolotus"
__email__ = "tanner.m.leo@gmail.com"
__description__ = "A tool to organize music files based on Rekordbox date added metadata"

from .rekordbox_organizer import RekordboxOrganizer
from .music_file_scanner import MusicFileScanner

__all__ = ["RekordboxOrganizer", "MusicFileScanner"]
