#!/usr/bin/env python3
"""
Setup script for Rekordbox Music Organizer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rekordbox-organizer",
    version="1.0.0",
    author="discolotus",
    description="A tool to organize music files based on Rekordbox date added metadata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/discolotus/rekordbox-organizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rekordbox-organizer=rekordbox_organizer:main",
            "music-scanner=music_file_scanner:main",
            "test-rekordbox=test_rekordbox_connection:main",
        ],
    },
    py_modules=["rekordbox_organizer", "music_file_scanner", "test_rekordbox_connection"],
    keywords="rekordbox music organizer dj audio files metadata",
    project_urls={
        "Bug Reports": "https://github.com/discolotus/rekordbox-organizer/issues",
        "Source": "https://github.com/discolotus/rekordbox-organizer",
    },
)
