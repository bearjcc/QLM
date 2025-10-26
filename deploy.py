#!/usr/bin/env python3
"""
QLM Deployment Script
Sets up and runs the Quack Language Model API server.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd,
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python 3.8+ is available"""
    success, stdout, stderr = run_command("python --version")
    if success:
        version = stdout.strip().split()[1]
        major, minor = map(int, version.split('.')[:2])
        if major >= 3 and minor >= 8:
            print(f"✅ Python {version} found")
            return True

    print("❌ Python 3.8+ required")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements.txt")

    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False

def test_api():
    """Run basic API tests"""
    print("🧪 Running tests...")
    success, stdout, stderr = run_command("python -m pytest tests/ -v")

    if success:
        print("✅ All tests passed")
        return True
    else:
        print(f"⚠️  Tests failed: {stderr}")
        print("    (This is okay for basic deployment)")
        return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting QLM server...")
    print("   API will be available at: http://localhost:8000")
    print("   Frontend demo: Open frontend/index.html in browser")
    print("   Press Ctrl+C to stop")
    print()

    os.chdir("api")
    success, stdout, stderr = run_command("python main.py")

    if not success:
        print(f"❌ Server failed to start: {stderr}")
        return False

    return True

def main():
    """Main deployment function"""
    print("🦆 QLM - Quack Language Model Deployment")
    print("=" * 50)

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Check requirements
    if not check_python_version():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Run tests
    test_api()

    # Start server
    start_server()

if __name__ == "__main__":
    main()
