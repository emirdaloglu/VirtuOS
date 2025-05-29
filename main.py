import sys
from process import ProcessManager
from memory import MemoryManager
from concurrency import ConcurrencyManager
from filesystem import FileSystemManager

def main():
    print("\n=== Mini Mobile OS Simulation ===")
    process_manager = ProcessManager()
    memory_manager = MemoryManager()
    concurrency_manager = ConcurrencyManager()
    fs_manager = FileSystemManager()
    while True:
        print("\nSelect a component to interact with:")
        print("1. Process Management")
        print("2. Memory Management")
        print("3. Concurrency & Synchronization")
        print("4. File System")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            process_manager.menu(memory_manager)
        elif choice == '2':
            memory_manager.menu()
        elif choice == '3':
            concurrency_manager.menu()
        elif choice == '4':
            fs_manager.menu()
        elif choice == '5':
            print("Exiting Mini Mobile OS. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()