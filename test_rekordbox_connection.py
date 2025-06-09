#!/usr/bin/env python3
"""
Test script to check Rekordbox connection and show available data.
"""

import sys
from pathlib import Path

try:
    from pyrekordbox import Rekordbox6Database, show_config
    from pyrekordbox.rbxml import RekordboxXml
except ImportError:
    print("Error: pyrekordbox not installed. Install with: pip install pyrekordbox")
    sys.exit(1)


def test_rekordbox_config():
    """Test Rekordbox configuration."""
    print("=== Rekordbox Configuration ===")
    try:
        show_config()
        return True
    except Exception as e:
        print(f"Configuration error: {e}")
        return False


def test_rekordbox_database():
    """Test connection to Rekordbox 6/7 database."""
    print("\n=== Testing Rekordbox 6/7 Database Connection ===")
    try:
        db = Rekordbox6Database()
        print("✅ Successfully connected to Rekordbox database!")

        # Get some basic info
        contents = db.get_content()

        # Convert query to list if needed
        if hasattr(contents, '__iter__') and not isinstance(contents, list):
            contents = list(contents)

        print(f"📊 Found {len(contents)} tracks in database")

        if contents and len(contents) > 0:
            # Show first few tracks
            print("\n📀 Sample tracks:")
            for i, content in enumerate(contents[:5]):
                try:
                    title = getattr(content, 'Title', 'Unknown Title')
                    artist = getattr(content.Artist, 'Name', 'Unknown Artist') if hasattr(content, 'Artist') and content.Artist else 'Unknown Artist'
                    date_added = getattr(content, 'DateAdded', None) or getattr(content, 'created_at', None)
                    folder_path = getattr(content, 'FolderPath', 'No path')
                    print(f"  {i+1}. {artist} - {title}")
                    if date_added:
                        print(f"     Date added: {date_added}")
                    else:
                        print(f"     Date added: Not found")
                    print(f"     Path: {folder_path}")
                except Exception as track_error:
                    print(f"  {i+1}. Error reading track: {track_error}")

        return True

    except Exception as e:
        print(f"❌ Failed to connect to Rekordbox database: {e}")
        print("💡 This might be normal if:")
        print("   - Rekordbox is not installed")
        print("   - Rekordbox has never been run")
        print("   - You're using an older version of Rekordbox")
        return False


def test_xml_export(xml_path=None):
    """Test XML export functionality."""
    print(f"\n=== Testing XML Export ===")
    
    if not xml_path:
        print("ℹ️  No XML path provided. To test XML functionality:")
        print("   1. Export your Rekordbox collection: File → Export Collection in xml format")
        print("   2. Run: python test_rekordbox_connection.py /path/to/export.xml")
        return False
    
    xml_file = Path(xml_path)
    if not xml_file.exists():
        print(f"❌ XML file not found: {xml_path}")
        return False
    
    try:
        xml = RekordboxXml(xml_path)
        tracks = xml.get_tracks()
        print(f"✅ Successfully loaded XML export!")
        print(f"📊 Found {len(tracks)} tracks in XML")
        
        if tracks:
            print("\n📀 Sample tracks:")
            for i, track in enumerate(tracks[:5]):
                title = track.get('Name', 'Unknown Title')
                artist = track.get('Artist', 'Unknown Artist')
                date_added = track.get('DateAdded', 'Not found')
                location = track.get('Location', 'No location')
                print(f"  {i+1}. {artist} - {title}")
                print(f"     Date added: {date_added}")
                print(f"     Location: {location}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to load XML export: {e}")
        return False


def main():
    """Main test function."""
    print("🎵 Rekordbox Connection Test")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_rekordbox_config()
    
    # Test database connection
    db_ok = test_rekordbox_database()
    
    # Test XML if path provided
    xml_ok = False
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
        xml_ok = test_xml_export(xml_path)
    else:
        test_xml_export()  # Show instructions
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Configuration: {'✅' if config_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"XML Export: {'✅' if xml_ok else 'ℹ️  Not tested'}")
    
    if db_ok or xml_ok:
        print(f"\n🎉 Great! You can use the Rekordbox organizer tool.")
        if db_ok:
            print("   Use without --xml parameter to use the database directly.")
        if xml_ok:
            print(f"   Use --xml {sys.argv[1]} to use the XML export.")
    else:
        print(f"\n⚠️  Rekordbox integration not available.")
        print("   You can still use the music file scanner for analysis.")


if __name__ == "__main__":
    main()
