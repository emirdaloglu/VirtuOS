"""
filesystem.py
-------------
File system module for Mini OS Simulation.
Supports directory structure, file operations, permissions, search, and visualization.
"""

class File:
    """Represents a file with content, owner, encryption, and permissions."""
    def __init__(self, name, content="", owner="user", encrypted=False, permissions=None):
        self.name = name
        self.content = content
        self.owner = owner
        self.encrypted = encrypted
        if permissions is None:
            self.permissions = {"user": "rwx", "admin": "rwx"}
        else:
            self.permissions = permissions

    def read(self, user="user"):
        """Read file content if permitted."""
        if 'r' not in self.permissions.get(user, ''):
            return "[Permission Denied]"
        if self.encrypted:
            return "[Encrypted Content]"
        return self.content

    def write(self, data, user="user"):
        """Write to file if permitted."""
        if 'w' not in self.permissions.get(user, ''):
            print("[Permission Denied]")
            return
        if self.encrypted:
            print("Cannot write to encrypted file.")
        else:
            self.content = data

class Directory:
    """Represents a directory containing files and subdirectories."""
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.subdirs = {}

class FileSystemManager:
    """Manages the file system, directories, files, permissions, and visualization."""
    def __init__(self):
        self.root = Directory("root")
        self.current_dir = self.root
        self.current_user = "user"

    def create_file(self):
        """Create a new file with permissions and encryption."""
        name = input("File name: ")
        owner = input("Owner (user/admin): ")
        encrypted = input("Encrypted? (y/n): ").lower() == 'y'
        perms = input("Permissions for user (e.g. rwx): ") or "rwx"
        perms_admin = input("Permissions for admin (e.g. rwx): ") or "rwx"
        if name in self.current_dir.files:
            print("File already exists.")
            return
        permissions = {"user": perms, "admin": perms_admin}
        self.current_dir.files[name] = File(name, owner=owner, encrypted=encrypted, permissions=permissions)
        print(f"File '{name}' created.")

    def write_file(self):
        """Write content to a file as the current user."""
        name = input("File name: ")
        if name not in self.current_dir.files:
            print("File does not exist.")
            return
        data = input("Enter file content: ")
        self.current_dir.files[name].write(data, user=self.current_user)
        print(f"Written to '{name}'.")

    def read_file(self):
        """Read content from a file as the current user."""
        name = input("File name: ")
        if name not in self.current_dir.files:
            print("File does not exist.")
            return
        print(f"Content: {self.current_dir.files[name].read(user=self.current_user)}")

    def delete_file(self):
        """Delete a file from the current directory."""
        name = input("File name: ")
        if name in self.current_dir.files:
            del self.current_dir.files[name]
            print(f"File '{name}' deleted.")
        else:
            print("File does not exist.")

    def create_directory(self):
        """Create a new subdirectory in the current directory."""
        name = input("Directory name: ")
        if name in self.current_dir.subdirs:
            print("Directory already exists.")
            return
        self.current_dir.subdirs[name] = Directory(name)
        print(f"Directory '{name}' created.")

    def change_directory(self):
        """Change the current working directory."""
        name = input("Directory name (.. for parent): ")
        if name == "..":
            # No parent reference for root
            print("Already at root directory.")
            return
        if name in self.current_dir.subdirs:
            self.current_dir = self.current_dir.subdirs[name]
            print(f"Changed to directory '{name}'.")
        else:
            print("Directory does not exist.")

    def list_directory(self):
        """List files and directories in the current directory."""
        print("\n[Directory Listing]")
        print("Directories:", list(self.current_dir.subdirs.keys()))
        print("Files:", list(self.current_dir.files.keys()))

    def set_user(self):
        """Switch the current user (user/admin)."""
        user = input("Switch user (user/admin): ")
        if user in ["user", "admin"]:
            self.current_user = user
            print(f"Current user set to {user}.")
        else:
            print("Invalid user.")

    def search_file(self):
        """Search for a file by name recursively from the root."""
        name = input("Enter file name to search: ")
        print("[Search Results]")
        self._search_file_recursive(self.root, name, path="/root")

    def _search_file_recursive(self, directory, name, path):
        if name in directory.files:
            print(f"Found: {path}/{name}")
        for subdir_name, subdir in directory.subdirs.items():
            self._search_file_recursive(subdir, name, path + f"/{subdir_name}")

    def visualize_tree(self):
        """Visualize the directory tree from the root."""
        print("\n[Directory Tree]")
        self._visualize_tree_recursive(self.root, prefix="")

    def _visualize_tree_recursive(self, directory, prefix):
        print(prefix + directory.name + "/")
        for fname in directory.files:
            print(prefix + "  " + fname)
        for subdir in directory.subdirs.values():
            self._visualize_tree_recursive(subdir, prefix + "  ")

    def menu(self):
        """Main menu for file system operations."""
        while True:
            print("\n[File System]")
            print("1. Create File")
            print("2. Write File")
            print("3. Read File")
            print("4. Delete File")
            print("5. Create Directory")
            print("6. Change Directory")
            print("7. List Directory")
            print("8. Switch User")
            print("9. Search File")
            print("10. Visualize Directory Tree")
            print("11. Back")
            choice = input("Enter choice: ")
            if choice == '1':
                self.create_file()
            elif choice == '2':
                self.write_file()
            elif choice == '3':
                self.read_file()
            elif choice == '4':
                self.delete_file()
            elif choice == '5':
                self.create_directory()
            elif choice == '6':
                self.change_directory()
            elif choice == '7':
                self.list_directory()
            elif choice == '8':
                self.set_user()
            elif choice == '9':
                self.search_file()
            elif choice == '10':
                self.visualize_tree()
            elif choice == '11':
                break
            else:
                print("Invalid choice.")