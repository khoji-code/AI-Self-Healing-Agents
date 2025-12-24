import subprocess
import sys
import os

def run_command(cmd):
    print(f"▶️▶️▶️▶️  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(f"✅✅ Success")
    return True

def main():
    print("🚀 Quick Start: Self-Healing Agents System")
    print("="*60)
    
    # Check Python version
    print("\n1️⃣  Checking Python version...")
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return
    
    # Create virtual environment
    print("\n2️⃣  Setting up virtual environment...")
    if not os.path.exists("venv"):
        run_command("python -m venv venv")
    
    # Activate and install dependencies
    print("\n3️⃣  Installing dependencies...")
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && "
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate && "
    
    install_cmd = f"{activate_cmd}pip install -r requirements.txt"
    run_command(install_cmd)
    
    # Check .env file
    print("\n4️⃣  Checking configuration...")
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("💡 Create .env with:")
        print("   HF_TOKEN=your_huggingface_token")
        print("   Then run this script again")
        return
    
    # Test the system
    print("\n5️⃣  Testing the system.....")
    test_cmd = f"{activate_cmd}python examples/main_demo.py"
    run_command(test_cmd)
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("\nTo run the system:")
    print("  source venv/bin/activate  # On Mac/Linux")
    print("  venv\\Scripts\\activate    # On Windows")
    print("  python examples/main_demo.py")
    print("\nFor help: python quick_start.py --help")

if __name__ == "__main__":
    main()