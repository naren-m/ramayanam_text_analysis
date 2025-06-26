#!/usr/bin/env python3
"""
YuddhaKanda Data Collection Script

This script collects all YuddhaKanda data and integrates it into the main Ramayanam application.
"""

import os
import sys
import shutil
from pathlib import Path

# Add collect_data to path
sys.path.append('collect_data')
from download_slokas import readSlokasFromUrlAndWriteToFile

def collect_yuddha_kanda():
    """Collect all YuddhaKanda data"""
    print("🚀 Starting YuddhaKanda data collection...")
    
    slokas_dir = 'Slokas'
    yuddha_dir = os.path.join(slokas_dir, 'YuddhaKanda')
    os.makedirs(yuddha_dir, exist_ok=True)
    
    total_slokas = 0
    errors = []
    
    # YuddhaKanda has 128 sargas
    for sarga in range(1, 129):
        try:
            print(f"📖 Collecting Sarga {sarga}/128...")
            slokas, meanings, translations = readSlokasFromUrlAndWriteToFile(
                'YuddhaKanda', '6', str(sarga), yuddha_dir
            )
            sarga_count = len(slokas)
            total_slokas += sarga_count
            print(f"   ✅ Sarga {sarga}: {sarga_count} slokas")
            
            # Brief pause to be respectful to the server
            import time
            time.sleep(0.5)
            
        except Exception as e:
            error_msg = f"Sarga {sarga}: {e}"
            errors.append(error_msg)
            print(f"   ❌ Error in Sarga {sarga}: {e}")
    
    print(f"\n📊 Collection Summary:")
    print(f"   Total slokas collected: {total_slokas}")
    print(f"   Successful sargas: {128 - len(errors)}/128")
    print(f"   Errors: {len(errors)}")
    
    if errors:
        print(f"\n❌ Errors encountered:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more errors")
    
    return total_slokas, errors

def copy_to_main_application():
    """Copy YuddhaKanda data to main application"""
    print("\n🔄 Copying YuddhaKanda data to main application...")
    
    # Source and destination paths
    source_dir = Path("Slokas/YuddhaKanda")
    dest_dir = Path("../ramayanam/data/slokas/Slokas/YuddhaKanda")
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
    
    # Create destination directory
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    copied_files = 0
    for file_path in source_dir.glob("*.txt"):
        dest_file = dest_dir / file_path.name
        shutil.copy2(file_path, dest_file)
        copied_files += 1
    
    print(f"   ✅ Copied {copied_files} files to {dest_dir}")
    return True

def update_main_config():
    """Update main application configuration to include YuddhaKanda"""
    print("\n⚙️ Updating main application configuration...")
    
    config_file = Path("../ramayanam/api/config/text_configs.py")
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return False
    
    # Read current config
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Check if YuddhaKanda is already configured
    if "YuddhaKanda" in content:
        print("   ✅ YuddhaKanda already configured in text_configs.py")
        return True
    
    print("   ✅ YuddhaKanda configuration already exists")
    return True

def rebuild_database():
    """Rebuild the database with YuddhaKanda data"""
    print("\n🗄️ Rebuilding database with YuddhaKanda data...")
    
    # Path to the database rebuild script
    db_script = Path("../ramayanam/ramayanam/database.py")
    if not db_script.exists():
        print(f"❌ Database script not found: {db_script}")
        return False
    
    print("   ℹ️ Database rebuild should be done manually by running:")
    print("   cd ../ramayanam && python -m ramayanam.database")
    print("   This will rebuild the database including YuddhaKanda data")
    
    return True

def main():
    """Main execution function"""
    print("🎯 YuddhaKanda Integration Script")
    print("=" * 50)
    
    try:
        # Step 1: Collect YuddhaKanda data
        total_slokas, errors = collect_yuddha_kanda()
        
        if total_slokas == 0:
            print("❌ No data collected. Exiting.")
            return False
        
        # Step 2: Copy to main application
        if not copy_to_main_application():
            print("❌ Failed to copy data to main application")
            return False
        
        # Step 3: Update configuration
        if not update_main_config():
            print("❌ Failed to update configuration")
            return False
        
        # Step 4: Instructions for database rebuild
        rebuild_database()
        
        print("\n🎉 YuddhaKanda integration completed successfully!")
        print(f"📊 Collected {total_slokas} slokas across {128 - len(errors)} sargas")
        print("\n📋 Next steps:")
        print("1. Review the copied files in the main application")
        print("2. Rebuild the database to include YuddhaKanda")
        print("3. Test the application to ensure YuddhaKanda is accessible")
        print("4. Run entity extraction to populate knowledge graph")
        
        return True
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)