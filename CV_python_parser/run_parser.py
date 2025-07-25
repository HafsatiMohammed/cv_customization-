#!/usr/bin/env python3
"""
Simple runner script for the CV parser
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from cv_parser import CVParser

def main():
    """Run the CV parser"""
    try:
        parser = CVParser()
        parser.run()
        print("\n✅ CV parsing completed successfully!")
        print(f"📄 Generated file: {parser.output_file}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 