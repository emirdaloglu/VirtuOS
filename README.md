# Mini Operating System Simulation Project

## Overview
This project simulates the core components of a simple operating system, including:
- Process management and scheduling
- Memory management (paging, fragmentation, swapping)
- Concurrency and synchronization (producer-consumer, locks)
- File system (directory structure, permissions, search)

It is designed for educational purposes to demonstrate OS principles in a modular, interactive, and extensible way.

## Features
### Core
- Process creation, switching, and termination
- Multiple schedulers: FIFO, Round Robin, MLFQ, Power-aware
- Process queue and multi-core CPU simulation
- Memory paging, address translation, visualization
- Memory fragmentation and swapping (in/out)
- Producer-consumer concurrency with locks and condition variables
- File system with directories, file creation/read/write/delete

### Bonus
- Scheduler selection and visualization
- Multi-core CPU simulation (set number of cores, parallel execution)
- Power-aware scheduling
- File permissions (r/w/x for user/admin)
- File search (recursive)
- Directory tree visualization

## How to Run
1. Ensure you have Python 3 installed (no external dependencies required).
2. Open a terminal and navigate to the project directory.
3. Run the main program:
   ```
   python3 main.py
   ```
4. Follow the interactive menu to explore all OS components.

## Example Usage
- Create and manage processes with different schedulers
- Simulate multiple CPU cores and visualize running processes
- Allocate memory, translate addresses, and visualize fragmentation
- Swap processes in and out of memory
- Use producer-consumer simulation in concurrency
- Create files and directories, set permissions, search, and visualize the file system

## Project Structure
- `main.py` — Entry point, main menu
- `process.py` — Process management and scheduling
- `memory.py` — Memory management
- `concurrency.py` — Concurrency and synchronization
- `filesystem.py` — File system management

## License
MIT License (for educational use) 