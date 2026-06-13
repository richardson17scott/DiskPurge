import os
import sys
from tabulate import tabulate
import pyfiglet
from analyzer.core import (
    file_size,
    directory_scanner,
    largest_files,
    extension_breakdown,
)

def scanner(directory):
    """Runs the directory scanner with error handeling and returns the list of full file path and respective sizes"""
    try:
        print(f"\nScanning '{directory}'... This might take a few minutes")
        return list(directory_scanner(directory))
    except ValueError as error:
        sys.exit(f"Error:{error}")


def display_largest_files(all_files, limit=10):
    """Collects, formats and displays the largest files in a table"""
    top_files = largest_files(all_files, limit=limit)
    print(f"\n📊 TOP {limit} LARGEST FILES")

    table_data = []
    for index, (path, size) in enumerate(top_files, start=1):
        table_data.append([index, os.path.basename(path), file_size(size)])

    print(tabulate(table_data, headers=["S.No", "File Name", "Size"], tablefmt="grid"))
    return top_files


def display_extension_breakdown(all_files, limit=10):
    """Collects, formats and displays the largest files by extension in a table"""
    ext_breakdown = extension_breakdown(all_files)
    print("\n🗂️ STORAGE BY FILE TYPE")

    table_data = []
    for ext, size in ext_breakdown[:limit]:
        table_data.append([ext, file_size(size)])

    print(tabulate(table_data, headers=["Extension", "Total size"], tablefmt="grid"))


def auto_clean(top_files):
    """Handles the interactive file deletion"""
    print("\n🧼 AUTO-CLEAN COMPONENT")
    choice = input(
        "Enter file numbers to delete (seperated by commas) or press Enter to skip: "
    ).strip()
    if not choice:
        return
    try:
        for num in choice.split(","):
            indices = [int(num.strip()) - 1]
            for index in indices:
                if 0 <= index < len(top_files):
                    target = top_files[index][0]
                    if os.path.exists(target):
                        os.remove(target)
                        print(f"🗑️ Deleted: {os.path.basename(target)}")
    except ValueError:
        print("❌ Invalid input. Please use numbers and commas only.")


def main():
    banner = pyfiglet.figlet_format("DiskPurge")
    print(banner)
    print("✨ DiskPurge v1.0 | Sift through the clutter, reclaim your space. ✨")
    print("-" * 68)

    directory = input("Enter folder path to analyse: ").strip()

    all_files = scanner(directory)
    if not all_files:
        print("No files found in this directory")
        return
    top_files = display_largest_files(all_files)
    display_extension_breakdown(all_files)

    auto_clean(top_files)


if __name__ == "__main__":
    main()
