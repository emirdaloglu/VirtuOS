import random
import threading
import time

"""
process.py
----------
Process management module for Mini OS Simulation.
Supports process creation, scheduling (FIFO, RR, MLFQ, Power-aware), multi-core simulation, and process visualization.
"""

class PCB:
    """Process Control Block: stores process metadata."""
    def __init__(self, pid, name, power_profile):
        self.pid = pid
        self.name = name
        self.state = 'READY'
        self.power_profile = power_profile  # e.g., 'low', 'medium', 'high'

class ProcessManager:
    """Manages processes, scheduling, and multi-core simulation."""
    def __init__(self):
        self.processes = []
        self.pid_counter = 1
        self.ready_queue = []
        self.running = None
        self.scheduler_type = 'FIFO'  # Default scheduler
        self.time_quantum = 2  # For Round Robin
        self.rr_counter = 0
        self.mlfq_queues = [[], [], []]  # 3-level MLFQ
        self.mlfq_quantums = [1, 2, 4]
        self.mlfq_running_level = 0
        self.num_cores = 1
        self.core_threads = []
        self.core_running = [None]
        self.stop_cores = False

    def set_scheduler(self):
        """Allow user to select the scheduling algorithm."""
        print("\n[Scheduler Selection]")
        print("1. FIFO (Default)")
        print("2. Round Robin")
        print("3. Multi-Level Feedback Queue (MLFQ)")
        print("4. Power-aware")
        choice = input("Select scheduler: ")
        if choice == '1':
            self.scheduler_type = 'FIFO'
        elif choice == '2':
            self.scheduler_type = 'RR'
        elif choice == '3':
            self.scheduler_type = 'MLFQ'
        elif choice == '4':
            self.scheduler_type = 'POWER'
        else:
            print("Invalid choice. Keeping previous scheduler.")
        print(f"Scheduler set to {self.scheduler_type}.")

    def create_process(self):
        """Create a new process and add to the appropriate queue."""
        name = input("Enter app name: ")
        power_profile = input("Power profile (low/medium/high): ")
        pcb = PCB(self.pid_counter, name, power_profile)
        self.processes.append(pcb)
        if self.scheduler_type == 'MLFQ':
            self.mlfq_queues[0].append(pcb)
        else:
            self.ready_queue.append(pcb)
        self.pid_counter += 1
        print(f"Process {pcb.name} (PID {pcb.pid}) created.")

    def terminate_process(self):
        """Terminate the currently running process."""
        if not self.running:
            print("No process is currently running.")
            return
        print(f"Terminating process {self.running.name} (PID {self.running.pid})...")
        self.processes.remove(self.running)
        self.running = None

    def schedule(self):
        """Schedule the next process based on the selected algorithm."""
        if self.scheduler_type == 'FIFO':
            self.fifo_schedule()
        elif self.scheduler_type == 'RR':
            self.rr_schedule()
        elif self.scheduler_type == 'MLFQ':
            self.mlfq_schedule()
        elif self.scheduler_type == 'POWER':
            self.power_aware_schedule()
        else:
            self.fifo_schedule()

    def fifo_schedule(self):
        """First-In-First-Out scheduling."""
        if not self.ready_queue:
            print("No processes in ready queue.")
            self.running = None
            return
        self.running = self.ready_queue.pop(0)
        self.running.state = 'RUNNING'
        print(f"[FIFO] Running process: {self.running.name} (PID {self.running.pid})")

    def rr_schedule(self):
        """Round Robin scheduling."""
        if not self.ready_queue:
            print("No processes in ready queue.")
            self.running = None
            return
        if self.rr_counter >= len(self.ready_queue):
            self.rr_counter = 0
        self.running = self.ready_queue.pop(self.rr_counter)
        self.running.state = 'RUNNING'
        print(f"[Round Robin] Running process: {self.running.name} (PID {self.running.pid})")
        # After time quantum, put it back if not terminated
        self.ready_queue.append(self.running)

    def mlfq_schedule(self):
        """Multi-Level Feedback Queue scheduling."""
        for level, queue in enumerate(self.mlfq_queues):
            if queue:
                self.running = queue.pop(0)
                self.running.state = 'RUNNING'
                self.mlfq_running_level = level
                print(f"[MLFQ] Running process: {self.running.name} (PID {self.running.pid}) at level {level}")
                # Demote process if not finished
                if level < 2:
                    self.mlfq_queues[level+1].append(self.running)
                else:
                    self.mlfq_queues[level].append(self.running)
                return
        print("No processes in MLFQ queues.")
        self.running = None

    def power_aware_schedule(self):
        """Power-aware scheduling: prefers low-power processes if battery is low."""
        if not self.ready_queue:
            print("No processes in ready queue.")
            self.running = None
            return
        battery_level = random.randint(1, 100)
        print(f"[Power-aware] Simulated battery level: {battery_level}%")
        if battery_level < 30:
            low_power = [p for p in self.ready_queue if p.power_profile == 'low']
            if low_power:
                self.running = low_power[0]
                self.ready_queue.remove(self.running)
            else:
                self.running = self.ready_queue.pop(0)
        else:
            self.running = self.ready_queue.pop(0)
        self.running.state = 'RUNNING'
        print(f"[Power-aware] Running process: {self.running.name} (PID {self.running.pid})")

    def switch_process(self):
        """Switch to the next process."""
        if self.running:
            self.running.state = 'READY'
            if self.scheduler_type == 'MLFQ':
                self.mlfq_queues[self.mlfq_running_level].append(self.running)
            else:
                self.ready_queue.append(self.running)
        self.schedule()

    def list_processes(self):
        """List all processes and their states."""
        print("\n[Process Table]")
        for p in self.processes:
            print(f"PID: {p.pid}, Name: {p.name}, State: {p.state}, Power: {p.power_profile}")

    def visualize_queues(self):
        """Visualize the current process queues and running process."""
        print("\n[Process Queues Visualization]")
        if self.scheduler_type == 'MLFQ':
            for i, queue in enumerate(self.mlfq_queues):
                print(f"MLFQ Level {i}: {[p.pid for p in queue]}")
        else:
            print(f"Ready Queue: {[p.pid for p in self.ready_queue]}")
        if self.running:
            print(f"Running: PID {self.running.pid}")
        else:
            print("Running: None")

    def set_cores(self):
        """Set the number of CPU cores to simulate."""
        n = int(input("Enter number of CPU cores to simulate: "))
        if n < 1:
            print("Must have at least 1 core.")
            return
        self.num_cores = n
        self.core_running = [None] * n
        print(f"Number of CPU cores set to {n}.")

    def core_worker(self, core_id):
        """Thread worker for each simulated CPU core."""
        while not self.stop_cores:
            if self.scheduler_type == 'MLFQ':
                for level, queue in enumerate(self.mlfq_queues):
                    if queue:
                        proc = queue.pop(0)
                        proc.state = 'RUNNING'
                        self.core_running[core_id] = proc
                        print(f"[Core {core_id}] Running PID {proc.pid} ({proc.name}) at MLFQ level {level}")
                        time.sleep(1)
                        proc.state = 'READY'
                        if level < 2:
                            self.mlfq_queues[level+1].append(proc)
                        else:
                            self.mlfq_queues[level].append(proc)
                        break
                else:
                    self.core_running[core_id] = None
            else:
                if self.ready_queue:
                    proc = self.ready_queue.pop(0)
                    proc.state = 'RUNNING'
                    self.core_running[core_id] = proc
                    print(f"[Core {core_id}] Running PID {proc.pid} ({proc.name})")
                    time.sleep(1)
                    proc.state = 'READY'
                    self.ready_queue.append(proc)
                else:
                    self.core_running[core_id] = None
            time.sleep(0.1)

    def start_cores(self):
        """Start all CPU core threads."""
        if self.core_threads:
            print("Cores already running.")
            return
        self.stop_cores = False
        self.core_threads = []
        for i in range(self.num_cores):
            t = threading.Thread(target=self.core_worker, args=(i,), daemon=True)
            self.core_threads.append(t)
            t.start()
        print(f"Started {self.num_cores} CPU cores.")

    def stop_cores_func(self):
        """Stop all CPU core threads."""
        self.stop_cores = True
        for t in self.core_threads:
            t.join(timeout=1)
        self.core_threads = []
        print("Stopped all CPU cores.")

    def show_cores(self):
        """Show the status of each CPU core."""
        print("\n[CPU Core Status]")
        for i, proc in enumerate(self.core_running):
            if proc:
                print(f"Core {i}: Running PID {proc.pid} ({proc.name})")
            else:
                print(f"Core {i}: Idle")

    def menu(self, memory_manager):
        """Main menu for process management."""
        while True:
            print("\n[Process Management]")
            print("1. Create Process")
            print("2. Switch Process")
            print("3. Terminate Running Process")
            print("4. List Processes")
            print("5. Set Scheduler")
            print("6. Visualize Queues")
            print("7. Set Number of CPU Cores")
            print("8. Start CPU Cores")
            print("9. Stop CPU Cores")
            print("10. Show Core Status")
            print("11. Back")
            choice = input("Enter choice: ")
            if choice == '1':
                self.create_process()
            elif choice == '2':
                self.switch_process()
            elif choice == '3':
                self.terminate_process()
            elif choice == '4':
                self.list_processes()
            elif choice == '5':
                self.set_scheduler()
            elif choice == '6':
                self.visualize_queues()
            elif choice == '7':
                self.set_cores()
            elif choice == '8':
                self.start_cores()
            elif choice == '9':
                self.stop_cores_func()
            elif choice == '10':
                self.show_cores()
            elif choice == '11':
                self.stop_cores_func()
                break
            else:
                print("Invalid choice.")