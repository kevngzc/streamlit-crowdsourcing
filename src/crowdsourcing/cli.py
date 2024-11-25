"""CLI entry point for the crowdsourcing application."""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main CLI entry point."""
    # Get the path to the main.py file
    main_path = Path(__file__).parent / "main.py"
    
    if not main_path.exists():
        print(f"Error: Could not find main application at {main_path}")
        return 1
    
    # Run streamlit with the main.py file
    cmd = ["streamlit", "run", str(main_path)]
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error running application: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())