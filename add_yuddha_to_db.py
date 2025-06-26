#!/usr/bin/env python3
"""
Add YuddhaKanda data to existing database
"""

import sqlite3
import os
import glob

def add_yuddha_kanda_to_db():
    """Add YuddhaKanda data to the existing database"""
    db_path = "ramayanam_with_yuddha.db"
    yuddha_dir = "Slokas/YuddhaKanda"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    if not os.path.exists(yuddha_dir):
        print(f"❌ YuddhaKanda directory not found: {yuddha_dir}")
        return False
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all YuddhaKanda files
    sloka_files = glob.glob(f"{yuddha_dir}/*_sloka.txt")
    meaning_files = glob.glob(f"{yuddha_dir}/*_meaning.txt") 
    translation_files = glob.glob(f"{yuddha_dir}/*_translation.txt")
    
    print(f"📁 Found {len(sloka_files)} sloka files")
    print(f"📁 Found {len(meaning_files)} meaning files")
    print(f"📁 Found {len(translation_files)} translation files")
    
    # Parse file data
    yuddha_data = {}
    
    # Process sloka files
    for file_path in sloka_files:
        # Extract sarga number from filename
        # Format: YuddhaKanda_sarga_1_sloka.txt
        filename = os.path.basename(file_path)
        parts = filename.replace('.txt', '').split('_')
        if len(parts) >= 3 and parts[1] == 'sarga':
            kanda_id = 6  # YuddhaKanda is always 6
            sarga_id = int(parts[2])
            
            # Read the file content which contains multiple slokas
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Each line represents a sloka with format: kanda_id::sarga_id::sloka_id::sloka_text
            lines = content.split('\n')
            for line in lines:
                if line.strip() and '::' in line:
                    parts = line.split('::')
                    if len(parts) >= 4:
                        try:
                            file_kanda_id = int(parts[0])
                            file_sarga_id = int(parts[1])
                            sloka_id = int(parts[2])
                            sloka_text = '::'.join(parts[3:])  # Join back in case sloka contains ::
                            
                            key = (file_kanda_id, file_sarga_id, sloka_id)
                            if key not in yuddha_data:
                                yuddha_data[key] = {}
                            yuddha_data[key]['sloka'] = sloka_text
                        except ValueError:
                            continue
    
    # Process meaning files
    for file_path in meaning_files:
        filename = os.path.basename(file_path)
        parts = filename.replace('.txt', '').split('_')
        if len(parts) >= 3 and parts[1] == 'sarga':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            lines = content.split('\n')
            for line in lines:
                if line.strip() and '::' in line:
                    parts = line.split('::')
                    if len(parts) >= 4:
                        try:
                            file_kanda_id = int(parts[0])
                            file_sarga_id = int(parts[1])
                            sloka_id = int(parts[2])
                            meaning_text = '::'.join(parts[3:])
                            
                            key = (file_kanda_id, file_sarga_id, sloka_id)
                            if key not in yuddha_data:
                                yuddha_data[key] = {}
                            yuddha_data[key]['meaning'] = meaning_text
                        except ValueError:
                            continue
    
    # Process translation files
    for file_path in translation_files:
        filename = os.path.basename(file_path)
        parts = filename.replace('.txt', '').split('_')
        if len(parts) >= 3 and parts[1] == 'sarga':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            lines = content.split('\n')
            for line in lines:
                if line.strip() and '::' in line:
                    parts = line.split('::')
                    if len(parts) >= 4:
                        try:
                            file_kanda_id = int(parts[0])
                            file_sarga_id = int(parts[1])
                            sloka_id = int(parts[2])
                            translation_text = '::'.join(parts[3:])
                            
                            key = (file_kanda_id, file_sarga_id, sloka_id)
                            if key not in yuddha_data:
                                yuddha_data[key] = {}
                            yuddha_data[key]['translation'] = translation_text
                        except ValueError:
                            continue
    
    print(f"📊 Parsed {len(yuddha_data)} unique slokas")
    
    # Insert data into database
    inserted_count = 0
    for (kanda_id, sarga_id, sloka_id), data in yuddha_data.items():
        if 'sloka' in data and 'meaning' in data and 'translation' in data:
            try:
                cursor.execute("""
                    INSERT INTO slokas (kanda_id, sarga_id, sloka_id, sloka, meaning, translation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (kanda_id, sarga_id, sloka_id, data['sloka'], data['meaning'], data['translation']))
                inserted_count += 1
            except sqlite3.IntegrityError:
                # Handle duplicate key error
                print(f"   ⚠️ Duplicate sloka: {kanda_id}.{sarga_id}.{sloka_id}")
            except Exception as e:
                print(f"   ❌ Error inserting {kanda_id}.{sarga_id}.{sloka_id}: {e}")
    
    # Commit changes
    conn.commit()
    
    # Verify the data
    cursor.execute("SELECT COUNT(*) FROM slokas WHERE kanda_id = 6")
    yuddha_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM slokas")
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ Inserted {inserted_count} YuddhaKanda slokas")
    print(f"📊 YuddhaKanda slokas in DB: {yuddha_count}")
    print(f"📊 Total slokas in DB: {total_count}")
    
    return True

if __name__ == "__main__":
    success = add_yuddha_kanda_to_db()
    if success:
        print("🎉 YuddhaKanda successfully added to database!")
    else:
        print("❌ Failed to add YuddhaKanda to database")