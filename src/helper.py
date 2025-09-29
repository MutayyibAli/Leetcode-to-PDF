import os
import shutil


def clear_folder(folder_path: str):
    """Delete all files and sub-folders inside a folder, but keep the folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # remove file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove subfolder
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def remove_small_files(folder_path, max_size=100):
    """Recursively remove all files in a folder (and sub-folders) that are <= max_size bytes."""
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if os.path.getsize(file_path) <= max_size:
                    os.remove(file_path)
            except Exception as e:
                print(f"⚠️ Error deleting {file_path}: {e}")
