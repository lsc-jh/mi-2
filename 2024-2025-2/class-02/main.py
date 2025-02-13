import os
import shutil

def write_to_file(filename, content):
    """Write content to a file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Successfully wrote to {filename}")
    except Exception as e:
        print(f"❌ Error writing to {filename}: {e}")

def append_to_file(filename, content):
    """Append content to a file."""
    try:
        with open(filename, 'a') as f:
            f.write(content)
        print(f"✅ Successfully appended to {filename}")
    except Exception as e:
        print(f"❌ Error appending to {filename}: {e}")

def read_from_file(filename):
    """Read and display the contents of a file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        print(f"📄 Contents of {filename}:\n{content}")
        return content
    except Exception as e:
        print(f"❌ Error reading from {filename}: {e}")
        return None


def check_file_exists(filename):
    """Check if a file exists."""
    if os.path.exists(filename):
        print(f"🔍 {filename} exists!")
    else:
        print(f"🔍 {filename} does not exist.")

def create_directory(dirname):
    """Create a directory."""
    try:
        os.mkdir(dirname)
        print(f"✅ Successfully created directory {dirname}")
    except Exception as e:
        print(f"❌ Error creating directory {dirname}: {e}")

def list_directory_contents(dirname):
    """List the contents of a directory."""
    try:
        contents = os.listdir(dirname)
        print(f"📂 Contents of {dirname}:")
        for item in contents:
            print(f" - {item}")
    except Exception as e:
        print(f"❌ Error listing contents of {dirname}: {e}")

def move_file_to_directory(filename, dirname):
    """Move a file to a directory."""
    try:
        shutil.move(filename, dirname)
        print(f"✅ Successfully moved {filename} to {dirname}")
    except Exception as e:
        print(f"❌ Error moving {filename} to {dirname}: {e}")


if __name__ == "__main__":
    # Task 1: Create a directory
    create_directory('my_folder')

    # Task 2: Write to a file
    write_to_file('hello.txt', 'Hello World!\n')

    # Task 3: Append to the file
    append_to_file('hello.txt', 'Hello again!\n')

    # Task 4: Read and display the file contents
    read_from_file('hello.txt')

    # Task 5: Check if the file exists
    check_file_exists('hello.txt')

    # Task 6: Move the file to the directory
    move_file_to_directory('hello.txt', 'my_folder')

    # Task 7: List contents of the directory
    list_directory_contents('my_folder')