#!/usr/bin/env python3
"""
Verification script for Render deployment
Run this script to verify all deployment files are correctly configured
"""

import os
import sys

def check_file_exists(filename, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filename}")
    return exists

def check_env_vars():
    """Check if environment variables are properly configured"""
    print("\n🔧 Environment Variables (for local testing):")
    env_vars = ['FLASK_ENV', 'FLASK_DEBUG', 'MODEL_PATH', 'PORT']
    
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"   {var}: {value}")

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 13):
        print("   ⚠️  Python 3.13+ may have package compatibility issues with some packages")
        print("   📝 Consider using Python 3.12 for better compatibility on Render")
    elif version >= (3, 11):
        print("   ✅ Good Python version for deployment")
    else:
        print("   ⚠️  Python version may be too old for some packages")

def main():
    print("🚀 Render Deployment Verification\n")
    
    check_python_version()
    
    print("\n📁 Required Files:")
    all_good = True
    
    # Required files
    required_files = [
        'main.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'best_model.pkl'
    ]
    
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    print("\n📄 Optional Files:")
    optional_files = [
        'config.py',
        '.env.example',
        '.gitignore',
        'RENDER_DEPLOYMENT.md',
        'requirements-flexible.txt',
        'requirements-locked.txt'
    ]
    
    for file in optional_files:
        check_file_exists(file, required=False)
    
    # Check Procfile content
    print("\n📋 Procfile Content:")
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            print(f"   {content}")
            if 'gunicorn' in content and 'main:app' in content:
                print("   ✅ Procfile looks correct")
            else:
                print("   ❌ Procfile may have issues")
                all_good = False
    except FileNotFoundError:
        print("   ❌ Procfile not found")
        all_good = False
    
    # Check runtime.txt
    print("\n🐍 Runtime Configuration:")
    try:
        with open('runtime.txt', 'r') as f:
            python_version = f.read().strip()
            print(f"   Python version: {python_version}")
            if python_version.startswith('python-3.'):
                version_num = python_version.replace('python-', '')
                if version_num >= '3.11' and version_num < '3.13':
                    print("   ✅ Good Python version for Render")
                elif version_num >= '3.13':
                    print("   ⚠️  Python 3.13+ may have package compatibility issues")
                else:
                    print("   ⚠️  Consider updating to Python 3.11 or 3.12")
            else:
                print("   ❌ Invalid Python version format")
                all_good = False
    except FileNotFoundError:
        print("   ❌ runtime.txt not found")
        all_good = False
    
    # Check requirements.txt
    print("\n📦 Requirements:")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            essential_packages = ['Flask', 'gunicorn', 'scikit-learn', 'numpy']
            for package in essential_packages:
                if package.lower() in requirements.lower():
                    print(f"   ✅ {package}")
                else:
                    print(f"   ❌ {package} missing")
                    all_good = False
    except FileNotFoundError:
        print("   ❌ requirements.txt not found")
        all_good = False
    
    # Check environment variables
    check_env_vars()
    
    print(f"\n{'🎉 Ready for deployment!' if all_good else '⚠️  Some issues found. Please fix before deploying.'}")
    
    if all_good:
        print("\n📋 Next steps for Render deployment:")
        print("1. Push your code to GitHub/GitLab:")
        print("   git add .")
        print("   git commit -m 'Fix deployment configuration'")
        print("   git push origin main")
        print("2. In Render dashboard, set environment variables:")
        print("   - FLASK_ENV=production")
        print("   - FLASK_DEBUG=false")
        print("   - MODEL_PATH=best_model.pkl")
        print("3. Build Command: pip install -r requirements.txt")
        print("4. Start Command: gunicorn main:app --host=0.0.0.0 --port=$PORT")
        print("\n📖 For detailed instructions, see RENDER_DEPLOYMENT.md")
    else:
        print("\n🔧 Fix the issues above, then run this script again.")
        print("💡 You can also run: python setup_deployment.py")

if __name__ == "__main__":
    main()
