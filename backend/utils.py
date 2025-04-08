import os

def ensure_directory_exists(directory):
    """
    Ensures that a directory exists. Creates it if it doesn't.

    Args:
        directory (str): Path to the directory.
    """
    os.makedirs(directory, exist_ok=True)
