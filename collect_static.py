#!/usr/bin/env python
"""
Helper script to collect static files for production.
This ensures all static files are properly gathered before deployment.
"""
import os
import subprocess
import sys

def main():
    """Collect static files for production deployment"""
    # Ensure we're in a Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prompt_generator.settings')
    
    # Set DEBUG to False temporarily to simulate production
    os.environ['DEBUG'] = 'False'
    
    print("Collecting static files...")
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], check=True)
        print("Static files collected successfully!")
        print("Files are located in the 'staticfiles' directory.")
    except subprocess.CalledProcessError as e:
        print(f"Error collecting static files: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 