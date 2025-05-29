"""
memory.py
---------
Memory management module for Mini OS Simulation.
Supports paging, address translation, memory visualization, fragmentation, and swapping.
"""

class PageTableEntry:
    """Represents a page table entry for a process."""
    def __init__(self, page_number, frame_number, valid=True):
        self.page_number = page_number
        self.frame_number = frame_number
        self.valid = valid

class MemoryManager:
    """Manages memory allocation, paging, fragmentation, and swapping."""
    def __init__(self, num_frames=8, page_size=1024):
        self.num_frames = num_frames
        self.page_size = page_size
        self.frames = [None] * num_frames  # Simulate physical memory frames
        self.page_tables = {}  # pid -> [PageTableEntry]
        self.memory_constraints = 4  # Max processes in memory
        self.swapped_out = {}  # pid -> [PageTableEntry] (simulated disk)

    def create_page_table(self, pid, num_pages):
        """Create a page table for a process and allocate frames."""
        if len(self.page_tables) >= self.memory_constraints:
            print("Memory full! Cannot allocate more processes.")
            return False
        page_table = []
        for i in range(num_pages):
            frame = self.find_free_frame()
            if frame is not None:
                self.frames[frame] = (pid, i)
                page_table.append(PageTableEntry(i, frame))
            else:
                print("No free frames available!")
                return False
        self.page_tables[pid] = page_table
        print(f"Page table created for PID {pid}.")
        return True

    def find_free_frame(self):
        """Find a free frame in physical memory."""
        for i, frame in enumerate(self.frames):
            if frame is None:
                return i
        return None

    def translate(self, pid, virtual_address):
        """Translate a virtual address to a physical address for a process."""
        if pid not in self.page_tables:
            print("No page table for this PID.")
            return None
        page_number = virtual_address // self.page_size
        offset = virtual_address % self.page_size
        for entry in self.page_tables[pid]:
            if entry.page_number == page_number and entry.valid:
                physical_address = entry.frame_number * self.page_size + offset
                print(f"Virtual address {virtual_address} -> Physical address {physical_address}")
                return physical_address
        print("Invalid page access!")
        return None

    def visualize_memory(self):
        """Print the current state of memory frames."""
        print("\n[Memory Frames]")
        for i, frame in enumerate(self.frames):
            if frame:
                print(f"Frame {i}: PID {frame[0]}, Page {frame[1]}")
            else:
                print(f"Frame {i}: Free")

    def visualize_fragmentation(self):
        """Show the number of free fragments and memory state."""
        print("\n[Memory Fragmentation]")
        fragments = 0
        in_fragment = False
        for frame in self.frames:
            if frame is None:
                if not in_fragment:
                    fragments += 1
                    in_fragment = True
            else:
                in_fragment = False
        print(f"Number of free fragments: {fragments}")
        self.visualize_memory()

    def swap_out(self):
        """Swap a process out to simulated disk (free its frames)."""
        pid = int(input("Enter PID to swap out: "))
        if pid not in self.page_tables:
            print("No such process in memory.")
            return
        self.swapped_out[pid] = self.page_tables.pop(pid)
        # Free frames
        for entry in self.swapped_out[pid]:
            self.frames[entry.frame_number] = None
        print(f"Process {pid} swapped out to disk.")

    def swap_in(self):
        """Swap a process in from simulated disk (allocate frames)."""
        pid = int(input("Enter PID to swap in: "))
        if pid not in self.swapped_out:
            print("No such process on disk.")
            return
        if len(self.page_tables) >= self.memory_constraints:
            print("Memory full! Cannot swap in.")
            return
        # Try to allocate frames
        for entry in self.swapped_out[pid]:
            frame = self.find_free_frame()
            if frame is not None:
                self.frames[frame] = (pid, entry.page_number)
                entry.frame_number = frame
            else:
                print("Not enough free frames to swap in.")
                return
        self.page_tables[pid] = self.swapped_out.pop(pid)
        print(f"Process {pid} swapped in from disk.")

    def menu(self):
        """Main menu for memory management."""
        while True:
            print("\n[Memory Management]")
            print("1. Create Page Table for Process")
            print("2. Translate Virtual Address")
            print("3. Visualize Memory")
            print("4. Visualize Fragmentation")
            print("5. Swap Out Process")
            print("6. Swap In Process")
            print("7. Back")
            choice = input("Enter choice: ")
            if choice == '1':
                pid = int(input("Enter PID: "))
                num_pages = int(input("Number of pages: "))
                self.create_page_table(pid, num_pages)
            elif choice == '2':
                pid = int(input("Enter PID: "))
                vaddr = int(input("Enter virtual address: "))
                self.translate(pid, vaddr)
            elif choice == '3':
                self.visualize_memory()
            elif choice == '4':
                self.visualize_fragmentation()
            elif choice == '5':
                self.swap_out()
            elif choice == '6':
                self.swap_in()
            elif choice == '7':
                break
            else:
                print("Invalid choice.")