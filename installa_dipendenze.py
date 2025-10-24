#!/usr/bin/env python3
"""
Script di installazione dipendenze per 3DS Modding Tool
"""

import subprocess
import sys

def install_dependencies():
    """Installa tutte le dipendenze necessarie"""
    dependencies = [
        "requests>=2.28.0",
        "colorama>=0.4.6", 
        "tqdm>=4.64.0"
    ]
    
    print("Installing dependencies for 3DS Modding Tool...")
    
    for package in dependencies:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("\n🎉 All dependencies installed successfully!")
    print("You can now run: python 3ds_mod_tool.py")
    return True

if __name__ == "__main__":
    install_dependencies()