# Rekordbox Music Organizer

A Python tool to organize music files based on their Rekordbox "date added" metadata. Files are organized into `YYYY-MM` folders with a flat structure (no subdirectories within each month folder).

## Features

- 🎵 **Music File Discovery**: Recursively scans directories for music files (MP3, FLAC, WAV, etc.)
- 📅 **Rekordbox Integration**: Reads "date added" metadata from Rekordbox database or XML exports
- 📁 **Flat Organization**: Organizes files into `YYYY-MM` folders with all files at the root level
- 🔄 **Conflict Resolution**: Handles filename conflicts by appending numbers (`-1`, `-2`, etc.)
- 👀 **Dry Run Mode**: Preview changes before executing
- 📊 **Progress Tracking**: Shows detailed progress and statistics

## Installation

1. **Install dependencies** (pyrekordbox is already installed):
   ```bash
   source venv/bin/activate
   # pyrekordbox is already installed
   ```

2. **Ensure Rekordbox is installed** on your system, or have a Rekordbox XML export file ready.

## Usage

### Basic Usage

```bash
# Dry run (preview only) - DEFAULT MODE
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized

# Execute the organization
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --execute

# Use with Rekordbox XML export
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --xml /path/to/rekordbox.xml --execute
```

### Music File Scanner (Utility)

```bash
# Scan directory and show statistics
python music_file_scanner.py /path/to/music --stats

# Analyze directory depth structure
python music_file_scanner.py /path/to/music --depth-analysis

# Preview filename conflicts if flattened
python music_file_scanner.py /path/to/music --flatten-preview

# Scan for specific file types only
python music_file_scanner.py /path/to/music --extensions .mp3 .flac
```

## How It Works

1. **Scans** the source directory recursively for music files
2. **Connects** to Rekordbox database (or reads XML export)
3. **Matches** each music file with its Rekordbox entry
4. **Extracts** the "date added" metadata
5. **Creates** target folders in `YYYY-MM` format
6. **Moves** files to appropriate folders with flat structure
7. **Resolves** filename conflicts automatically

## Output Structure

```
target_directory/
├── 2024-01/
│   ├── song1.mp3
│   ├── song2.flac
│   └── song3.wav
├── 2024-02/
│   ├── track1.mp3
│   ├── track2-1.mp3  # Conflict resolved
│   └── track2-2.mp3  # Conflict resolved
└── 2024-03/
    └── music.flac
```

## Supported File Formats

- **MP3** (.mp3)
- **FLAC** (.flac)
- **WAV** (.wav)
- **AIFF** (.aiff, .aif)
- **M4A** (.m4a)
- **AAC** (.aac)
- **OGG** (.ogg)
- **Opus** (.opus)
- **WMA** (.wma)

## Rekordbox Integration

### Rekordbox 6/7 Database
The tool automatically connects to your Rekordbox 6 or 7 database. Make sure Rekordbox is installed and has been run at least once.

### Rekordbox XML Export
If you prefer to use an XML export:
1. In Rekordbox: File → Export Collection in xml format
2. Use the `--xml` parameter to specify the XML file path

## Command Line Options

### rekordbox_organizer.py
- `--source, -s`: Source directory containing music files (required)
- `--target, -t`: Target directory for organized files (required)
- `--xml, -x`: Path to Rekordbox XML export file (optional)
- `--dry-run`: Preview changes without executing (default)
- `--execute`: Execute the organization (overrides --dry-run)

### music_file_scanner.py
- `directory`: Directory to scan (required)
- `--extensions, -e`: File extensions to include (e.g., .mp3 .flac)
- `--no-recursive`: Don't scan subdirectories
- `--stats`: Show detailed statistics
- `--depth-analysis`: Analyze files by directory depth
- `--flatten-preview`: Preview filename conflicts if flattened

## Examples

### Example 1: Basic Organization
```bash
# Preview what would happen
python rekordbox_organizer.py --source ~/Music/Unsorted --target ~/Music/Organized

# Execute the organization
python rekordbox_organizer.py --source ~/Music/Unsorted --target ~/Music/Organized --execute
```

### Example 2: Using XML Export
```bash
# Export your Rekordbox collection to XML first, then:
python rekordbox_organizer.py \
  --source ~/Music/Unsorted \
  --target ~/Music/Organized \
  --xml ~/Desktop/rekordbox_export.xml \
  --execute
```

### Example 3: Analyze Before Organizing
```bash
# Check what files you have
python music_file_scanner.py ~/Music/Unsorted --stats

# Check for potential filename conflicts
python music_file_scanner.py ~/Music/Unsorted --flatten-preview

# Then organize
python rekordbox_organizer.py --source ~/Music/Unsorted --target ~/Music/Organized --execute
```

## Safety Features

- **Dry run by default**: Always previews changes first
- **Conflict resolution**: Automatically handles duplicate filenames
- **Error handling**: Continues processing even if individual files fail
- **Detailed logging**: Shows exactly what's happening
- **Statistics**: Provides summary of operations

## Troubleshooting

### "Failed to connect to Rekordbox"
- Ensure Rekordbox is installed and has been run at least once
- Try using an XML export instead: `--xml /path/to/export.xml`
- Check that you have the latest version of Rekordbox

### "No date added found in Rekordbox"
- The file might not be in your Rekordbox library
- Try importing the files into Rekordbox first
- Check that the file paths match between your filesystem and Rekordbox

### Permission Errors
- Ensure you have write permissions to the target directory
- Make sure the source files aren't currently being used by other applications

## Dependencies

- **pyrekordbox**: For reading Rekordbox databases and XML files
- **pathlib**: For cross-platform path handling (built-in)
- **shutil**: For file operations (built-in)
- **argparse**: For command-line interface (built-in)

## Notes

- The tool preserves original files during the move operation
- Files without Rekordbox metadata are skipped
- The flat structure means no subdirectories within month folders
- Filename conflicts are resolved by appending `-1`, `-2`, etc.
- The tool works with both Rekordbox 6/7 databases and XML exports
