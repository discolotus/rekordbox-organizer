# Rekordbox Music Organizer

A Python tool to organize music files based on their Rekordbox "date added" metadata. Files are organized into `YYYY-MM` folders with a flat structure (no subdirectories within each month folder).

## Features

- 🎵 **Music File Discovery**: Recursively scans directories for music files (MP3, FLAC, WAV, etc.)
- 📅 **Rekordbox Integration**: Reads "date added" metadata from Rekordbox database or XML exports
- 📁 **Flat Organization**: Organizes files into `YYYY-MM` folders with all files at the root level
- 📂 **No-Date Handling**: Files without date metadata go to a `no-date` folder
- 🔄 **Conflict Resolution**: Handles filename conflicts by appending numbers (`-1`, `-2`, etc.)
- 👀 **Dry Run Mode**: Preview changes before executing
- � **Safe Mode**: Copy files to import directory first, then organize copies (preserves originals)
- �📊 **Progress Tracking**: Shows detailed progress and statistics

## Installation

### Option 1: Global CLI Installation (Recommended)

Install globally using pipx for easy command-line access:

```bash
# Clone the repository
git clone https://github.com/discolotus/rekordbox-organizer.git
cd rekordbox-organizer

# Install globally with pipx (recommended)
make install-cli
```

This installs three global commands:
- `rekordbox-organizer` - Main organizer tool
- `music-scanner` - Music file analysis tool
- `test-rekordbox` - Test Rekordbox connection

### Option 2: Development Installation

For development or if you prefer pip:

```bash
# Clone the repository
git clone https://github.com/discolotus/rekordbox-organizer.git
cd rekordbox-organizer

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
make install-dev
```

### Requirements

- **Python 3.8+**
- **pipx** (for global installation): `python -m pip install --user pipx`
- **Rekordbox** installed on your system, or have a Rekordbox XML export file ready

### Makefile Commands

The project includes a Makefile for easy management:

```bash
make help           # Show all available commands
make install-cli    # Install globally with pipx (recommended)
make install-dev    # Install in development mode
make uninstall      # Uninstall the package
make test           # Run basic functionality tests
make status         # Show installation status
make clean          # Clean build artifacts
```

## Quick Start

After installation with `make install-cli`:

```bash
# Test your Rekordbox connection first
test-rekordbox

# Preview organization (dry run - safe)
rekordbox-organizer --source /path/to/music --target /path/to/organized --dry-run

# Execute the organization
rekordbox-organizer --source /path/to/music --target /path/to/organized --execute
```

Or using Python directly (development mode):

```bash
# Test your Rekordbox connection first
python test_rekordbox_connection.py

# Preview organization (dry run - safe)
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --dry-run

# Execute the organization
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --execute
```

## Usage

### Basic Commands

**Using CLI commands (after `make install-cli`):**

```bash
# Dry run (preview only) - DEFAULT MODE
rekordbox-organizer --source /path/to/music --target /path/to/organized

# Execute the organization
rekordbox-organizer --source /path/to/music --target /path/to/organized --execute

# Safe mode: copy files first, then organize copies (preserves originals)
rekordbox-organizer --source /path/to/music --target /path/to/organized --safe --execute

# Use with Rekordbox XML export
rekordbox-organizer --source /path/to/music --target /path/to/organized --xml /path/to/rekordbox.xml --execute
```

**Using Python directly:**

```bash
# Dry run (preview only) - DEFAULT MODE
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized

# Execute the organization
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --execute

# Safe mode: copy files first, then organize copies (preserves originals)
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --safe --execute

# Use with Rekordbox XML export
python rekordbox_organizer.py --source /path/to/music --target /path/to/organized --xml /path/to/rekordbox.xml --execute
```

### Music File Scanner (Analysis Tool)

**Using CLI commands:**

```bash
# Scan directory and show statistics
music-scanner /path/to/music --stats

# Analyze directory depth structure
music-scanner /path/to/music --depth-analysis

# Preview filename conflicts if flattened
music-scanner /path/to/music --flatten-preview
```

**Using Python directly:**

```bash
# Scan directory and show statistics
python music_file_scanner.py /path/to/music --stats

# Analyze directory depth structure
python music_file_scanner.py /path/to/music --depth-analysis

# Preview filename conflicts if flattened
python music_file_scanner.py /path/to/music --flatten-preview
```

## Output Structure

```
target_directory/
├── import/              # Safe mode: temporary copies (only with --safe)
│   ├── file1.mp3
│   └── file2.flac
├── 2024-01/
│   ├── song1.mp3
│   ├── song2.flac
│   └── song3.wav
├── 2024-02/
│   ├── track1.mp3
│   ├── track2-1.mp3  # Conflict resolved
│   └── track2-2.mp3  # Conflict resolved
├── 2025-06/
│   └── newtrack.flac
└── no-date/
    ├── unknown1.mp3  # Files without date metadata
    └── unknown2.flac
```

## How It Works

1. **Scans** the source directory recursively for music files
2. **Connects** to Rekordbox database (or reads XML export)
3. **Matches** each music file with its Rekordbox entry
4. **Extracts** the "date added" metadata
5. **Creates** target folders in `YYYY-MM` format
6. **Moves** files to appropriate folders with flat structure
7. **Handles** files without metadata by placing them in `no-date/`
8. **Resolves** filename conflicts automatically

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

## Command Line Options

### rekordbox_organizer.py
- `--source, -s`: Source directory containing music files (required)
- `--target, -t`: Target directory for organized files (required)
- `--xml, -x`: Path to Rekordbox XML export file (optional)
- `--dry-run`: Preview changes without executing (default)
- `--execute`: Execute the organization (overrides --dry-run)
- `--safe`: Safe mode - copy files to import directory first, then organize copies

### music_file_scanner.py
- `directory`: Directory to scan (required)
- `--extensions, -e`: File extensions to include (e.g., .mp3 .flac)
- `--no-recursive`: Don't scan subdirectories
- `--stats`: Show detailed statistics
- `--depth-analysis`: Analyze files by directory depth
- `--flatten-preview`: Preview filename conflicts if flattened

### test_rekordbox_connection.py
- No arguments: Test database connection
- `xml_path`: Test XML export file

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

### Example 3: Safe Mode Organization
```bash
# Safe mode: copies files first, then organizes copies (preserves originals)
python rekordbox_organizer.py --source ~/Music/Unsorted --target ~/Music/Organized --safe --execute

# This creates:
# ~/Music/Organized/import/     <- temporary copies
# ~/Music/Organized/2024-01/    <- organized files
# ~/Music/Organized/no-date/    <- files without metadata
# Original files remain untouched in ~/Music/Unsorted
```

### Example 4: Analyze Before Organizing
```bash
# Check what files you have
python music_file_scanner.py ~/Music/Unsorted --stats

# Check for potential filename conflicts
python music_file_scanner.py ~/Music/Unsorted --flatten-preview

# Test Rekordbox connection
python test_rekordbox_connection.py

# Then organize
python rekordbox_organizer.py --source ~/Music/Unsorted --target ~/Music/Organized --execute
```

## Rekordbox Integration

### Rekordbox 6/7 Database
The tool automatically connects to your Rekordbox 6 or 7 database. Make sure Rekordbox is installed and has been run at least once.

### Rekordbox XML Export
If you prefer to use an XML export:
1. In Rekordbox: File → Export Collection in xml format
2. Use the `--xml` parameter to specify the XML file path

## Safety Features

- **Dry run by default**: Always previews changes first
- **Safe mode**: `--safe` option copies files to import directory first, preserving originals
- **Conflict resolution**: Automatically handles duplicate filenames
- **Error handling**: Continues processing even if individual files fail
- **Detailed logging**: Shows exactly what's happening
- **Statistics**: Provides summary of operations
- **No-date handling**: Files without metadata aren't lost

## Troubleshooting

### "Failed to connect to Rekordbox"
- Ensure Rekordbox is installed and has been run at least once
- Try using an XML export instead: `--xml /path/to/export.xml`
- Check that you have the latest version of Rekordbox
- Run `python test_rekordbox_connection.py` to diagnose

### "No date added found in Rekordbox"
- The file might not be in your Rekordbox library
- Try importing the files into Rekordbox first
- Check that the file paths match between your filesystem and Rekordbox
- Files will be moved to the `no-date/` folder instead of being skipped

### Permission Errors
- Ensure you have write permissions to the target directory
- Make sure the source files aren't currently being used by other applications

## Dependencies

- **pyrekordbox**: For reading Rekordbox databases and XML files
- **pathlib**: For cross-platform path handling (built-in)
- **shutil**: For file operations (built-in)
- **argparse**: For command-line interface (built-in)

## Contributing

Feel free to open issues or submit pull requests to improve the tool!

## License

This project is open source. Please check the license file for details.
