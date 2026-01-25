#!/usr/bin/env python3
"""
Setup script for OpenDeepResearcher
Helps users initialize the project and check dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("\n🔧 Creating .env file...")
        with open(env_path, "w") as f:
            f.write("TAVILY_API_KEY=your_tavily_api_key_here\n")
        print("✅ .env file created")
        print("⚠️  Please add your Tavily API key to the .env file")
    else:
        print("✅ .env file already exists")

def check_lm_studio():
    """Check if LM Studio is accessible"""
    print("\n🤖 Checking LM Studio connection...")
    try:
        import requests
        response = requests.get("http://127.0.0.1:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ LM Studio is running and accessible")
            return True
        else:
            print("⚠️  LM Studio responded but may not be ready")
            return False
    except Exception as e:
        print("❌ LM Studio not accessible:", str(e))
        print("   Please start LM Studio and load a model")
        return False

def main():
    """Main setup function"""
    print("🧠 OpenDeepResearcher Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup environment file
    setup_env_file()
    
    # Check LM Studio
    lm_studio_ok = check_lm_studio()
    
    print("\n" + "=" * 40)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Add your Tavily API key to .env file")
    if not lm_studio_ok:
        print("2. Start LM Studio and load a model")
        print("3. Run: streamlit run app.py")
    else:
        print("2. Run: streamlit run app.py")
    
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()