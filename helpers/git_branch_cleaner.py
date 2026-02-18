#!/usr/bin/env python3
"""
Git Branch Cleaner - Remove merged local branches easily

Usage:
    python git_branch_cleaner.py              # List merged branches
    python git_branch_cleaner.py --delete      # Delete merged branches
    python git_branch_cleaner.py --dry-run     # Preview what would be deleted
"""

import subprocess
import sys
import re
from datetime import datetime, timedelta

def get_merged_branches():
    """Get list of branches merged into current branch"""
    result = subprocess.run(
        ["git", "branch", "--merged", "main"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Try master branch
        result = subprocess.run(
            ["git", "branch", "--merged", "master"],
            capture_output=True, text=True
        )
    
    branches = []
    for line in result.stdout.splitlines():
        branch = line.strip()
        if branch and not branch.startswith('*'):
            branches.append(branch)
    return branches

def get_branch_age(branch_name):
    """Get the last commit date for a branch"""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ci", branch_name],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            date_str = result.stdout.strip()
            # Parse the date
            date = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
            return date
        except:
            pass
    return None

def get_stale_branches(days=30):
    """Get branches older than X days that are merged"""
    merged = get_merged_branches()
    cutoff = datetime.now() - timedelta(days=days)
    
    stale = []
    for branch in merged:
        age = get_branch_age(branch)
        if age and age < cutoff:
            stale.append((branch, age))
    
    return stale

def delete_branch(branch_name):
    """Delete a branch"""
    result = subprocess.run(
        ["git", "branch", "-d", branch_name],
        capture_output=True, text=True
    )
    return result.returncode == 0

def main():
    delete_mode = "--delete" in sys.argv
    dry_run = "--dry-run" in sys.argv
    days = 30
    
    for arg in sys.argv:
        if arg.startswith("--days="):
            days = int(arg.split("=")[1])
    
    print("🔍 Finding merged branches...")
    
    if days > 0:
        branches = get_stale_branches(days)
        print(f"\n📋 Branches merged into main/master and older than {days} days:")
    else:
        branches = [(b, None) for b in get_merged_branches()]
        print("\n📋 All branches merged into main/master:")
    
    if not branches:
        print("  No merged branches found! ✨")
        return
    
    for branch, age in branches:
        if age:
            days_old = (datetime.now() - age).days
            print(f"  - {branch} ({days_old} days old)")
        else:
            print(f"  - {branch}")
    
    if dry_run:
        print(f"\n🔍 Dry run - would delete {len(branches)} branches")
        return
    
    if delete_mode:
        print(f"\n🗑️  Deleting {len(branches)} branches...")
        deleted = 0
        for branch, _ in branches:
            if delete_branch(branch):
                print(f"  ✅ Deleted: {branch}")
                deleted += 1
            else:
                print(f"  ⚠️  Failed to delete (may need -D): {branch}")
        print(f"\n✨ Done! Deleted {deleted} branches")
    else:
        print(f"\n💡 Run with --delete to remove these branches")
        print(f"   or --dry-run to preview")

if __name__ == "__main__":
    main()
