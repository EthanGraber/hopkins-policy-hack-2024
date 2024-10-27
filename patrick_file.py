from pathlib import Path


def process_folder(folder: Path) -> bool:
    """
    Process the contents of a given folder.

    Args:
    folder (Path): The path to the folder to be processed.

    Returns:
    bool: True for now, will be used to indicate successful processing in the future.
    """
    try:
        # Check if the folder exists
        if not folder.exists():
            print(f"The folder '{folder}' does not exist.")
            return False

        # Check if the path is a folder
        if not folder.is_dir():
            print(f"'{folder}' is not a folder.")
            return False

        # Print the folder contents
        print(f"Folder contents: {folder.name}")
        for item in folder.iterdir():
            print(item.name)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
