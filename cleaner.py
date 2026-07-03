import os
import shutil
import sys
from pathlib import Path
import questionary
from questionary import Choice

# System, OS, and Cloud-sync directories that should NEVER be scanned under any circumstance
BANNED_DIR_NAMES = {
    'iCloudDrive', 'com~apple~CloudDocs', 'Mobile Documents',
    'Library', 'Applications', 'System', 'Network', 'Volumes',  
    'Windows', 'Program Files', 'Program Files (x86)', 'AppData', 
    '.git', '.svn', '.idea', '.vscode', '.cache', '♻️', '$RECYCLE.BIN' 
}

def is_safe_to_scan(current_dir):
    """Checks if the user is accidentally running the script in a critical system root."""
    path = Path(current_dir).resolve()
    if path == path.parent:  
        return False
    for part in path.parts:
        if part in BANNED_DIR_NAMES:
            return False
    return True

def get_dir_size(path):
    """Calculates the total size of a directory in bytes."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip symlinks to avoid infinite loops or inaccurate sizes
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass  # Gracefully skip files that cannot be read due to permissions
    return total_size

def format_size(bytes_size):
    """Formats bytes into human-readable MB or GB string."""
    mb = bytes_size / (1024 * 1024)
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.1f} MB"

def find_target_directories(root_dir):
    """Scans recursively, matching node_modules/vendor only if package.json/composer.json exist."""
    targets = []
    
    print("🔍 Scanning safe directories...")
    
    for dirpath, dirnames, _ in os.walk(root_dir):
        current_path = Path(dirpath)
        
        # Skip banned directories and hidden folders completely
        dirnames[:] = [d for d in dirnames if d not in BANNED_DIR_NAMES and not d.startswith('.')]
        
        # Dynamic terminal update using \r
        found_count = len(targets)
        status_text = f"   Found: {found_count} targets | Scanning: {current_path.name[:30]}"
        sys.stdout.write(f"\r\033[K{status_text}")
        sys.stdout.flush()
        
        # Look for node_modules only if package.json is in this same directory
        if 'node_modules' in dirnames:
            if (current_path / 'package.json').exists():
                targets.append((current_path / 'node_modules').resolve())
            dirnames.remove('node_modules')
            
        # Look for vendor only if composer.json is in this same directory
        if 'vendor' in dirnames:
            if (current_path / 'composer.json').exists():
                targets.append((current_path / 'vendor').resolve())
            dirnames.remove('vendor')
                
    print(f"\r\033[K✨ Scan complete! Found {len(targets)} verified dependency directories.")
    return targets

def format_choice_label(path, size_str):
    """Formats the path to give context of size, parent, and grandparent directory."""
    parts = path.parts
    target_name = parts[-1] 
    
    if len(parts) >= 3:
        context = f".../{parts[-3]}/{parts[-2]}/{target_name}"
    elif len(parts) == 2:
        context = f"{parts[-2]}/{target_name}"
    else:
        context = str(path)
        
    return f"[{size_str}] {context}  ➔  ({path.parent})"

def main():
    current_dir = os.getcwd()
    
    if not is_safe_to_scan(current_dir):
        print(f"❌ Safety Halt: The directory '{current_dir}' contains system critical or cloud folders.")
        print("Please run this script inside localized user folders like Documents, Downloads, Desktop, or your code workspace.")
        return

    found_paths = find_target_directories(current_dir)
    
    if not found_paths:
        print("✨ No project-linked 'node_modules' or 'vendor' directories found!")
        return

    # Calculate sizes with a live update
    print("\n⚖️  Calculating directory sizes...")
    choices = []
    total_scanned_bytes = 0
    
    for i, path in enumerate(found_paths, 1):
        status_text = f"   Calculating sizes ({i}/{len(found_paths)}): {path.name} in {path.parent.name[:20]}..."
        sys.stdout.write(f"\r\033[K{status_text}")
        sys.stdout.flush()
        
        size_bytes = get_dir_size(path)
        total_scanned_bytes += size_bytes
        size_str = format_size(size_bytes)
        
        choices.append(
            Choice(title=format_choice_label(path, size_str), value=(path, size_bytes), checked=False)
        )
        
    # Clear the dynamic calculation line
    sys.stdout.write("\r\033[K")
    print(f"📊 Total discoverable size: {format_size(total_scanned_bytes)}\n")

    print("How to navigate:")
    print("  [Space]  - Select/Deselect an individual item")
    print("  [a]      - Toggle/Select ALL items")
    print("  [i]      - Invert selection")
    print("  [Enter]  - Confirm selection\n")
    
    selected_items = questionary.checkbox(
        "Select the directories you want to DELETE:",
        choices=choices
    ).ask()

    if not selected_items:
        print("❌ No directories selected or operation cancelled. Exiting safely.")
        return

    # Unpack paths and sum up the exact target data saved
    selected_paths = [item[0] for item in selected_items]
    freed_space_bytes = sum([item[1] for item in selected_items])
    freed_space_str = format_size(freed_space_bytes)

    # Final confirmation prompt
    confirm = questionary.confirm(
        f"⚠️ Are you absolutely sure you want to permanently delete these {len(selected_paths)} folders? (Will free up {freed_space_str})",
        default=False
    ).ask()

    if confirm:
        print("\n🗑️ Starting deletion process...")
        for i, path in enumerate(selected_paths, 1):
            print(f"   [{i}/{len(selected_paths)}] Deleting: {path.name} in .../{path.parent.name}")
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f"   ❌ Failed to delete {path}. Error: {e}")
                    
        print(f"\n🎉 Cleanup complete! You saved {freed_space_str} of space!")
    else:
        print("❌ Operation cancelled. No files were deleted.")

if __name__ == "__main__":
    main()