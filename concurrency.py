"""
concurrency.py
--------------
Concurrency and synchronization module for Mini OS Simulation.
Implements basic thread API, locks, condition variables, and producer-consumer problem.
"""
import threading
import time
from collections import deque

class Lock:
    """Simple lock for synchronization."""
    def __init__(self):
        self.locked = False

    def acquire(self):
        """Acquire the lock if available."""
        if not self.locked:
            self.locked = True
            return True
        return False

    def release(self):
        """Release the lock."""
        self.locked = False

class Condition:
    """Condition variable for thread synchronization."""
    def __init__(self):
        self.waiting = deque()

    def wait(self, thread_name):
        """Add a thread to the waiting queue."""
        self.waiting.append(thread_name)

    def notify(self):
        """Wake up a waiting thread if any."""
        if self.waiting:
            return self.waiting.popleft()
        return None

class ConcurrencyManager:
    """Manages concurrency, locks, and producer-consumer simulation."""
    def __init__(self):
        self.lock = Lock()
        self.condition = Condition()
        self.buffer = deque()
        self.buffer_size = 3

    def producer(self):
        """Produce an item and add to the buffer if space is available."""
        if len(self.buffer) < self.buffer_size:
            item = f"item{len(self.buffer)+1}"
            self.buffer.append(item)
            print(f"[Producer] Produced {item}. Buffer: {list(self.buffer)}")
        else:
            print("[Producer] Buffer full! Waiting...")

    def consumer(self):
        """Consume an item from the buffer if available."""
        if self.buffer:
            item = self.buffer.popleft()
            print(f"[Consumer] Consumed {item}. Buffer: {list(self.buffer)}")
        else:
            print("[Consumer] Buffer empty! Waiting...")

    def menu(self):
        """Main menu for concurrency and synchronization."""
        while True:
            print("\n[Concurrency & Synchronization]")
            print("1. Produce (Producer)")
            print("2. Consume (Consumer)")
            print("3. Show Buffer")
            print("4. Back")
            choice = input("Enter choice: ")
            if choice == '1':
                self.producer()
            elif choice == '2':
                self.consumer()
            elif choice == '3':
                print(f"Buffer: {list(self.buffer)}")
            elif choice == '4':
                break
            else:
                print("Invalid choice.")