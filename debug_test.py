#!/usr/bin/env python3

import sys
import argparse

def main():
    print("DEBUG: main() function called")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-paths", action="store_true")
    parser.add_argument("--dry-run", action="store_true", default=True)
    
    args = parser.parse_args()
    
    print(f"DEBUG: args.update_paths = {args.update_paths}")
    print(f"DEBUG: args.dry_run = {args.dry_run}")

if __name__ == "__main__":
    main()
