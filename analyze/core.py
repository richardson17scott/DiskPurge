import os
from pathlib import Path


def file_size(byte_size):
    """
    This function converts the raw byte size of the file into bytes, KB, MB... etc.

    Parameters:
    byte_size (int): Total number of bytes.

    Raises:
    ValueError: In case of the byte_size being negative.

    Returns:
    str : Formated string with respective units.

    """
    if byte_size < 0:
        raise ValueError("File size cannot be negative")

    for unit in ["Bytes", "KB", "MB", "GB", "TB"]:

        if byte_size < 1024:
            return f"{byte_size:.2f} {unit}"

        else:
            byte_size = byte_size / 1024

    return f"{byte_size:.2f} PB"


def directory_scanner(directory):
    """
    This function yields file path and file size.

    Parameters:
    directory (str): The directory in which the required files are present.

    Raises:
    ValueError: In case of the directory not being found or existing.

    Returns (Yields):
    Tuple : full path of the file and size of the file.

    """
    if not os.path.isdir(directory):
        raise ValueError("Directory not found")

    for root, directorys, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)

            try:
                size = os.path.getsize(full_path)
                yield (full_path, size)

            except FileNotFoundError:
                continue


def largest_files(file_list, limit=10):
    """
    This function takes the list of files with their respective sizes and sorts them to give the largest N number of files.

    Parameters:
    file_list (list): List if files with their respective sizes.
    limit (int): The N number of largest files to return.

    Returns:
    list: A sliced tuple with the largest files sorted in descending order.
    """
    return sorted(file_list, key=lambda x: x[1], reverse=True)[:limit]


def extension_breakdown(file_list):
    """
    This function takes the list of files and calculates the total size of each format of files.

    Parameters:
    file_list (list): List of files with their reapective sizes.

    Returns:
    list: A list of tuples containing (str: extension, int:total bytes) sorted from highest to lowest size.
    """

    breakdown = {}
    for file_path, size in file_list:
        ext = Path(file_path).suffix.lower()
        if not ext:
            ext = "No extension"

        breakdown[ext] = breakdown.get(ext, 0) + size
    return sorted(breakdown.items(), key=lambda x: x[1], reverse=True)

