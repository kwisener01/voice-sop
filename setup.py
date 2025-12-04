#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for Voice SOP Generator
Initializes database and performs first-time setup
"""

import os
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if all required packages are installed"""
    print("Checking requirements...")
    try:
        import flask
        import openai
        import google.oauth2
        import sqlalchemy
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def check_environment():
    """Check if all required environment variables are set"""
    print("\nChecking environment variables...")

    required_vars = [
        'VAPI_API_KEY',
        'OPENAI_API_KEY',
        'GHL_API_KEY',
        'MAKE_WEBHOOK_SECRET'
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"✗ Missing: {var}")
        else:
            print(f"✓ Found: {var}")

    if missing:
        print(f"\n⚠ Warning: Missing environment variables: {', '.join(missing)}")
        print("Please set these in your .env file")
        return False

    return True


def setup_directories():
    """Create necessary directories"""
    print("\nSetting up directories...")

    directories = [
        'credentials',
        'logs'
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created: {directory}/")
        else:
            print(f"✓ Exists: {directory}/")


def setup_database():
    """Initialize database tables"""
    print("\nSetting up database...")

    try:
        from models import Database
        from config import Config

        database_url = Config.DATABASE_URL

        if not database_url:
            print("✗ DATABASE_URL not set, using SQLite")
            database_url = 'sqlite:///voice_sop.db'

        db = Database(database_url)
        db.create_tables()

        print("✓ Database tables created successfully")
        return True

    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        return False


def test_google_credentials():
    """Test if Google credentials are valid"""
    print("\nChecking Google credentials...")

    credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', './credentials/google_credentials.json')

    if not os.path.exists(credentials_path):
        print(f"⚠ Google credentials not found at: {credentials_path}")
        print("You'll need to:")
        print("1. Create a Google Cloud service account")
        print("2. Download the JSON credentials")
        print("3. Place it at: credentials/google_credentials.json")
        return False

    try:
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/documents']
        )

        print("✓ Google credentials are valid")
        return True

    except Exception as e:
        print(f"✗ Error loading Google credentials: {e}")
        return False


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from .env.example")
            print("⚠ Please edit .env and add your API keys")
        else:
            print("✗ .env.example not found")


def main():
    """Main setup function"""
    print("=" * 60)
    print("Voice SOP Generator - Setup")
    print("=" * 60)

    # Create .env if needed
    create_env_file()

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Check environment
    env_ok = check_environment()

    # Setup directories
    setup_directories()

    # Setup database
    db_ok = setup_database()

    # Test Google credentials
    google_ok = test_google_credentials()

    # Summary
    print("\n" + "=" * 60)
    print("Setup Summary")
    print("=" * 60)

    if env_ok and db_ok:
        print("✓ Setup completed successfully!")

        if not google_ok:
            print("\n⚠ Note: Google credentials need to be configured")

        print("\nNext steps:")
        print("1. Edit .env and add all API keys")
        print("2. Add Google credentials to credentials/")
        print("3. Run: python app.py")
        print("4. Or use Docker: docker-compose up")

    else:
        print("✗ Setup incomplete - please fix errors above")
        sys.exit(1)


if __name__ == '__main__':
    main()
