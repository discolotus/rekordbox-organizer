#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

def main():
    print("=== Update Paths Debug Test ===")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--update-paths", action="store_true")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    
    args = parser.parse_args()
    
    print(f"args.update_paths: {args.update_paths}")
    print(f"args.dry_run: {args.dry_run}")
    print(f"args.execute: {args.execute}")
    
    dry_run = not args.execute
    print(f"computed dry_run: {dry_run}")
    
    if args.update_paths:
        print("✅ Path Updates: Enabled")
        if dry_run:
            print("🔍 DRY RUN: Would update Rekordbox paths")
        else:
            print("🔄 EXECUTE: Will update Rekordbox paths")
    else:
        print("❌ Path Updates: Disabled")

if __name__ == "__main__":
    main()
