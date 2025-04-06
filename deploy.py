#!/usr/bin/env python
"""
Helper script for deploying the AI Prompt Generator.
This script automates several deployment tasks.
"""
import os
import subprocess
import sys
import argparse

def run_command(command, description):
    """Run a command and print its output"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)
        return False

def main():
    """Run deployment tasks"""
    parser = argparse.ArgumentParser(description="Deploy AI Prompt Generator")
    parser.add_argument("--platform", choices=["heroku", "digitalocean", "aws"], 
                        help="Platform to deploy to")
    parser.add_argument("--collect-static", action="store_true", 
                        help="Only collect static files")
    parser.add_argument("--migrate", action="store_true", 
                        help="Only run migrations")
    parser.add_argument("--load-data", action="store_true", 
                        help="Only load initial data")
    
    args = parser.parse_args()
    
    # Ensure we're in a Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prompt_generator.settings')
    
    # If only specific tasks are requested
    if args.collect_static:
        return 0 if run_command([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                               "Collecting static files") else 1
    
    if args.migrate:
        return 0 if run_command([sys.executable, 'manage.py', 'migrate'], 
                               "Running database migrations") else 1
    
    if args.load_data:
        return 0 if run_command([sys.executable, 'manage.py', 'load_initial_data'], 
                                "Loading initial data") else 1
    
    # Full deployment process
    print("=== Starting deployment process ===")
    
    # 1. Collect static files
    if not run_command([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                      "Collecting static files"):
        return 1
    
    # 2. Run migrations
    if not run_command([sys.executable, 'manage.py', 'migrate'], 
                      "Running database migrations"):
        return 1
    
    # 3. Load initial data (if database is empty)
    if not run_command([sys.executable, 'manage.py', 'load_initial_data'], 
                      "Loading initial data"):
        return 1
    
    # 4. Platform-specific deployment
    if args.platform:
        if args.platform == "heroku":
            print("\nDeploying to Heroku...")
            print("Please use 'git push heroku main' to deploy to Heroku.")
        elif args.platform == "digitalocean":
            print("\nDeploying to DigitalOcean...")
            print("Please follow the instructions in DEPLOYMENT.md for DigitalOcean deployment.")
        elif args.platform == "aws":
            print("\nDeploying to AWS...")
            print("Please follow the instructions in DEPLOYMENT.md for AWS deployment.")
    else:
        print("\nLocal deployment preparation complete!")
        print("To start the production server locally, run:")
        print("    gunicorn prompt_generator.wsgi")
    
    print("\n=== Deployment process completed ===")
    return 0

if __name__ == '__main__':
    sys.exit(main()) 