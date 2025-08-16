#!/usr/bin/env python3
"""
Dream Journal Analyzer Setup Script
This script helps set up the Dream Journal Analyzer application.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    
    packages = [
        "customtkinter==5.2.0",
        "pillow==10.0.0", 
        "matplotlib==3.7.2",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "textblob==0.17.1",
        "wordcloud==1.9.2",
        "seaborn==0.12.2",
        "tkcalendar==1.6.1"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install {package}: {e}")
            continue
    
    print("✅ Package installation completed!")

def download_nltk_data():
    """Download required NLTK data for TextBlob"""
    print("📚 Downloading NLTK data for text analysis...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "textblob.download_corpora"])
        print("✅ NLTK data downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Failed to download NLTK data: {e}")
        print("You can manually run: python -m textblob.download_corpora")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if sys.platform == "win32":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Dream Journal Analyzer.lnk")
            target = os.path.join(os.getcwd(), "main_gui.py")
            wDir = os.getcwd()
            icon = target
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            
            print("✅ Desktop shortcut created!")
        except ImportError:
            print("⚠️ Could not create desktop shortcut (winshell not available)")
        except Exception as e:
            print(f"⚠️ Could not create desktop shortcut: {e}")

def main():
    """Main setup function"""
    print("🌙 Dream Journal Analyzer Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install packages
    install_requirements()
    
    # Download NLTK data
    download_nltk_data()
    
    # Create desktop shortcut (Windows only)
    if sys.platform == "win32":
        create_shortcut = input("\n🖥️ Create desktop shortcut? (y/n): ").lower().strip()
        if create_shortcut in ['y', 'yes']:
            create_desktop_shortcut()
    
    print("\n🎉 Setup completed!")
    print("\nTo run the application:")
    print("  python main_gui.py")
    print("\nOr double-click main_gui.py if you have Python associated with .py files")
    
    # Ask if user wants to run the app now
    run_now = input("\n🚀 Run Dream Journal Analyzer now? (y/n): ").lower().strip()
    if run_now in ['y', 'yes']:
        print("\nStarting Dream Journal Analyzer...")
        try:
            subprocess.run([sys.executable, "main_gui.py"])
        except KeyboardInterrupt:
            print("\nApplication closed by user.")
        except Exception as e:
            print(f"Error running application: {e}")

if __name__ == "__main__":
    main()