#!/usr/bin/env python3
"""
Text Diff Checker - Compare two texts and show differences

A simple tool to compare two pieces of text and highlight differences.
Useful for comparing documents, code snippets, or any text content.

Usage:
    python3 text_diff.py "Hello World" "Hello Python"
    python3 text_diff.py -f file1.txt -f2 file2.txt
    python3 text_diff.py --interactive

Requirements:
    - Python 3.6+
    - difflib (built-in)
"""

import sys
import argparse
from difflib import unified_diff, context_diff, HtmlDiff, SequenceMatcher

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False
    class Fore:
        RED = GREEN = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = BRIGHT = ""


def read_file(filepath):
    """Read content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def compare_text(text1, text2, unified=True):
    """Compare two texts and return differences."""
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    
    if unified:
        diff = unified_diff(lines1, lines2, lineterm='')
        return list(diff)
    else:
        diff = context_diff(lines1, lines2, lineterm='')
        return list(diff)


def print_colored_diff(diff_lines):
    """Print diff with colors."""
    for line in diff_lines:
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            if COLOR:
                print(Fore.CYAN + line + Style.RESET_ALL)
            else:
                print(line)
        elif line.startswith('+'):
            if COLOR:
                print(Fore.GREEN + line + Style.RESET_ALL)
            else:
                print(line)
        elif line.startswith('-'):
            if COLOR:
                print(Fore.RED + line + Style.RESET_ALL)
            else:
                print(line)
        else:
            print(line)


def print_simple_diff(text1, text2):
    """Print a simple side-by-side style diff."""
    matcher = SequenceMatcher(None, text1, text2)
    
    print("\n" + "="*60)
    print("TEXT DIFFERENCES")
    print("="*60)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Show unchanged (truncated)
            if i2 - i1 < 5:
                print(f"  {text1[i1:i2]}")
        elif tag == 'replace':
            if COLOR:
                print(f"{Fore.RED}- {text1[i1:i2]}")
                print(f"{Fore.GREEN}+ {text2[j1:j2]}")
            else:
                print(f"- {text1[i1:i2]}")
                print(f"+ {text2[j1:j2]}")
        elif tag == 'delete':
            if COLOR:
                print(f"{Fore.RED}- {text1[i1:i2]}")
            else:
                print(f"- {text1[i1:i2]}")
        elif tag == 'insert':
            if COLOR:
                print(f"{Fore.GREEN}+ {text2[j1:j2]}")
            else:
                print(f"+ {text2[j1:j2]}")
    
    # Similarity ratio
    ratio = matcher.ratio()
    print("\n" + "="*60)
    print(f"Similarity: {ratio*100:.1f}%")
    print("="*60)


def interactive_mode():
    """Run in interactive mode."""
    print("Text Diff Checker - Interactive Mode")
    print("="*40)
    print("Enter first text (press Ctrl+D when done):")
    text1 = sys.stdin.read()
    
    print("\nEnter second text (press Ctrl+D when done):")
    text2 = sys.stdin.read()
    
    print_simple_diff(text1, text2)


def main():
    parser = argparse.ArgumentParser(
        description='Compare two texts and show differences',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('text1', nargs='?', help='First text or file path')
    parser.add_argument('text2', nargs='?', help='Second text or file path')
    parser.add_argument('-f', '--file1', help='First file path')
    parser.add_argument('-f2', '--file2', help='Second file path')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode')
    parser.add_argument('-u', '--unified', action='store_true', default=True,
                       help='Unified diff format (default)')
    parser.add_argument('-c', '--context', action='store_true',
                       help='Context diff format')
    parser.add_argument('-s', '--simple', action='store_true',
                       help='Simple diff with similarity percentage')
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return 0
    
    # Get text inputs
    text1 = None
    text2 = None
    
    # From positional args
    if args.text1:
        if args.text1.startswith('-'):
            pass  # Could be an option
        else:
            text1 = args.text1
    
    if args.text2:
        text2 = args.text2
    
    # From file args
    if args.file1:
        text1 = read_file(args.file1)
        if text1 is None:
            return 1
    
    if args.file2:
        text2 = read_file(args.file2)
        if text2 is None:
            return 1
    
    # Check if we have both texts
    if not text1 or not text2:
        parser.print_help()
        print("\n\nExample usage:")
        print("  python3 text_diff.py 'Hello World' 'Hello Python'")
        print("  python3 text_diff.py -f file1.txt -f2 file2.txt")
        print("  python3 text_diff.py --interactive")
        return 1
    
    # Show diff
    if args.simple:
        print_simple_diff(text1, text2)
    elif args.context:
        diff = compare_text(text1, text2, unified=False)
        print(''.join(diff))
    else:
        diff = compare_text(text1, text2, unified=True)
        if COLOR:
            print_colored_diff(diff)
        else:
            print(''.join(diff))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
