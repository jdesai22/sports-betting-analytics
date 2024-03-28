import os
import shutil

def move_file(file, dest):
    # Move the file to the destination directory
    shutil.move(file, dest)

def move_files(src, dest):
    # Source directory
    source_dir = src

    # Destination directory
    destination_dir = dest

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Move each file to the destination directory
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)
        shutil.move(source_file, destination_file)

    print(f"Files moved from {src} to {dest}")


if __name__ == "__main__":
    # Source directory
    event_dir = "events"

    # Destination directory
    event_dest = "prediction-03-27/event"

    prop_dir = "props"
    prop_dest = "prediction-03-27/props"

    move_files(event_dir, event_dest)
    move_files(prop_dir, prop_dest)


