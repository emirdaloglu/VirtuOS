import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from process import ProcessManager
from memory import MemoryManager
from concurrency import ConcurrencyManager
from filesystem import FileSystemManager

class MiniOSGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini OS Simulation GUI")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.configure(bg="#23232b")
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager()
        self.concurrency_manager = ConcurrencyManager()
        self.fs_manager = FileSystemManager()
        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#23232b", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d39", foreground="#fff", font=("Segoe UI", 12, "bold"), padding=10)
        style.map("TNotebook.Tab", background=[("selected", "#3a3a4d")])
        style.configure("TFrame", background="#23232b")
        style.configure("TLabel", background="#23232b", foreground="#fff", font=("Segoe UI", 14))
        style.configure("TButton", background="#444459", foreground="#fff", font=("Segoe UI", 11, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[("active", "#5c5c7a")])
        style.configure("TEntry", fieldbackground="#23232b", foreground="#fff")

    def create_widgets(self):
        # Header
        header = ttk.Label(self, text="Mini OS Simulation Project", font=("Segoe UI", 22, "bold"), anchor="center")
        header.pack(pady=(18, 8))

        tab_control = ttk.Notebook(self)
        self.process_tab = ttk.Frame(tab_control)
        self.memory_tab = ttk.Frame(tab_control)
        self.concurrency_tab = ttk.Frame(tab_control)
        self.fs_tab = ttk.Frame(tab_control)

        tab_control.add(self.process_tab, text='Process Management')
        tab_control.add(self.memory_tab, text='Memory Management')
        tab_control.add(self.concurrency_tab, text='Concurrency')
        tab_control.add(self.fs_tab, text='File System')
        tab_control.pack(expand=1, fill='both', padx=16, pady=8)

        self.init_process_tab()
        self.init_memory_tab()
        self.init_concurrency_tab()
        self.init_fs_tab()

    def init_process_tab(self):
        label = ttk.Label(self.process_tab, text="Process Management", font=("Arial", 16))
        label.pack(pady=10)

        btn_frame = ttk.Frame(self.process_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Create Process", command=self.gui_create_process).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Switch Process", command=self.gui_switch_process).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Terminate Process", command=self.gui_terminate_process).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(btn_frame, text="List Processes", command=self.gui_list_processes).grid(row=0, column=3, padx=5, pady=2)
        ttk.Button(btn_frame, text="Set Scheduler", command=self.gui_set_scheduler).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Visualize Queues", command=self.gui_visualize_queues).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Set CPU Cores", command=self.gui_set_cores).grid(row=1, column=2, padx=5, pady=2)
        ttk.Button(btn_frame, text="Start Cores", command=self.gui_start_cores).grid(row=1, column=3, padx=5, pady=2)
        ttk.Button(btn_frame, text="Stop Cores", command=self.gui_stop_cores).grid(row=2, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Show Core Status", command=self.gui_show_cores).grid(row=2, column=1, padx=5, pady=2)

        self.proc_output = tk.Text(self.process_tab, height=20, width=100, font=("Consolas", 11))
        self.proc_output.pack(pady=10)
        self.proc_output.config(state=tk.DISABLED)

    def gui_create_process(self):
        name = simpledialog.askstring("Create Process", "Enter app name:")
        if not name:
            return
        power = simpledialog.askstring("Create Process", "Power profile (low/medium/high):")
        if not power:
            return
        # Simulate input
        self.process_manager.pid_counter += 0 # ensure attribute exists
        pcb = self.process_manager
        pcb_input = [name, power]
        # Patch input for create_process
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: pcb_input.pop(0)
        try:
            self.process_manager.create_process()
            self.gui_list_processes()
        finally:
            __builtins__.input = orig_input

    def gui_switch_process(self):
        self.process_manager.switch_process()
        self.gui_list_processes()

    def gui_terminate_process(self):
        self.process_manager.terminate_process()
        self.gui_list_processes()

    def gui_list_processes(self):
        self.proc_output.config(state=tk.NORMAL)
        self.proc_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        self.process_manager.list_processes()
        sys.stdout = sys_stdout
        self.proc_output.insert(tk.END, buf.getvalue())
        self.proc_output.config(state=tk.DISABLED)

    def gui_set_scheduler(self):
        scheds = ["FIFO", "RR", "MLFQ", "POWER"]
        sched = simpledialog.askstring("Set Scheduler", "Enter scheduler (FIFO/RR/MLFQ/POWER):")
        if sched and sched.upper() in scheds:
            orig_input = __builtins__.input
            __builtins__.input = lambda prompt=None: str(scheds.index(sched.upper())+1)
            try:
                self.process_manager.set_scheduler()
            finally:
                __builtins__.input = orig_input
            self.gui_list_processes()
        else:
            messagebox.showerror("Error", "Invalid scheduler.")

    def gui_visualize_queues(self):
        self.proc_output.config(state=tk.NORMAL)
        self.proc_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        self.process_manager.visualize_queues()
        sys.stdout = sys_stdout
        self.proc_output.insert(tk.END, buf.getvalue())
        self.proc_output.config(state=tk.DISABLED)

    def gui_set_cores(self):
        n = simpledialog.askinteger("Set CPU Cores", "Enter number of CPU cores:", minvalue=1, maxvalue=16)
        if n:
            orig_input = __builtins__.input
            __builtins__.input = lambda prompt=None: str(n)
            try:
                self.process_manager.set_cores()
            finally:
                __builtins__.input = orig_input
            self.gui_show_cores()

    def gui_start_cores(self):
        self.process_manager.start_cores()
        self.gui_show_cores()

    def gui_stop_cores(self):
        self.process_manager.stop_cores_func()
        self.gui_show_cores()

    def gui_show_cores(self):
        self.proc_output.config(state=tk.NORMAL)
        self.proc_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        self.process_manager.show_cores()
        sys.stdout = sys_stdout
        self.proc_output.insert(tk.END, buf.getvalue())
        self.proc_output.config(state=tk.DISABLED)

    def init_memory_tab(self):
        label = ttk.Label(self.memory_tab, text="Memory Management", font=("Arial", 16))
        label.pack(pady=10)

        btn_frame = ttk.Frame(self.memory_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Create Page Table", command=self.gui_create_page_table).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Translate Address", command=self.gui_translate_address).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Visualize Memory", command=self.gui_visualize_memory).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(btn_frame, text="Visualize Fragmentation", command=self.gui_visualize_fragmentation).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Swap Out Process", command=self.gui_swap_out).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Swap In Process", command=self.gui_swap_in).grid(row=1, column=2, padx=5, pady=2)

        self.mem_output = tk.Text(self.memory_tab, height=20, width=100, font=("Consolas", 11))
        self.mem_output.pack(pady=10)
        self.mem_output.config(state=tk.DISABLED)

    def gui_create_page_table(self):
        pid = simpledialog.askinteger("Create Page Table", "Enter PID:")
        if pid is None:
            return
        num_pages = simpledialog.askinteger("Create Page Table", "Number of pages:")
        if num_pages is None:
            return
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: str(pid) if 'PID' in prompt else str(num_pages)
        try:
            self.memory_manager.create_page_table(pid, num_pages)
            self.gui_visualize_memory()
        finally:
            __builtins__.input = orig_input

    def gui_translate_address(self):
        pid = simpledialog.askinteger("Translate Address", "Enter PID:")
        if pid is None:
            return
        vaddr = simpledialog.askinteger("Translate Address", "Enter virtual address:")
        if vaddr is None:
            return
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: str(pid) if 'PID' in prompt else str(vaddr)
        try:
            self._show_mem_output(self.memory_manager.translate, pid, vaddr)
        finally:
            __builtins__.input = orig_input

    def gui_visualize_memory(self):
        self._show_mem_output(self.memory_manager.visualize_memory)

    def gui_visualize_fragmentation(self):
        self._show_mem_output(self.memory_manager.visualize_fragmentation)

    def gui_swap_out(self):
        pid = simpledialog.askinteger("Swap Out Process", "Enter PID to swap out:")
        if pid is None:
            return
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: str(pid)
        try:
            self._show_mem_output(self.memory_manager.swap_out)
        finally:
            __builtins__.input = orig_input

    def gui_swap_in(self):
        pid = simpledialog.askinteger("Swap In Process", "Enter PID to swap in:")
        if pid is None:
            return
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: str(pid)
        try:
            self._show_mem_output(self.memory_manager.swap_in)
        finally:
            __builtins__.input = orig_input

    def _show_mem_output(self, func, *args):
        self.mem_output.config(state=tk.NORMAL)
        self.mem_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        func(*args)
        sys.stdout = sys_stdout
        self.mem_output.insert(tk.END, buf.getvalue())
        self.mem_output.config(state=tk.DISABLED)

    def init_concurrency_tab(self):
        label = ttk.Label(self.concurrency_tab, text="Concurrency & Synchronization", font=("Arial", 16))
        label.pack(pady=10)

        btn_frame = ttk.Frame(self.concurrency_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Produce (Producer)", command=self.gui_produce).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Consume (Consumer)", command=self.gui_consume).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Show Buffer", command=self.gui_show_buffer).grid(row=0, column=2, padx=5, pady=2)

        self.conc_output = tk.Text(self.concurrency_tab, height=10, width=80, font=("Consolas", 11))
        self.conc_output.pack(pady=10)
        self.conc_output.config(state=tk.DISABLED)

    def gui_produce(self):
        self._show_conc_output(self.concurrency_manager.producer)

    def gui_consume(self):
        self._show_conc_output(self.concurrency_manager.consumer)

    def gui_show_buffer(self):
        self._show_conc_output(lambda: print(f"Buffer: {list(self.concurrency_manager.buffer)}"))

    def _show_conc_output(self, func):
        self.conc_output.config(state=tk.NORMAL)
        self.conc_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        func()
        sys.stdout = sys_stdout
        self.conc_output.insert(tk.END, buf.getvalue())
        self.conc_output.config(state=tk.DISABLED)

    def init_fs_tab(self):
        label = ttk.Label(self.fs_tab, text="File System", font=("Arial", 16))
        label.pack(pady=10)

        btn_frame = ttk.Frame(self.fs_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Create File", command=self.gui_create_file).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Write File", command=self.gui_write_file).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Read File", command=self.gui_read_file).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(btn_frame, text="Delete File", command=self.gui_delete_file).grid(row=0, column=3, padx=5, pady=2)
        ttk.Button(btn_frame, text="Create Directory", command=self.gui_create_directory).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Change Directory", command=self.gui_change_directory).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="List Directory", command=self.gui_list_directory).grid(row=1, column=2, padx=5, pady=2)
        ttk.Button(btn_frame, text="Switch User", command=self.gui_set_user).grid(row=1, column=3, padx=5, pady=2)
        ttk.Button(btn_frame, text="Search File", command=self.gui_search_file).grid(row=2, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Visualize Directory Tree", command=self.gui_visualize_tree).grid(row=2, column=1, padx=5, pady=2)

        self.fs_output = tk.Text(self.fs_tab, height=20, width=100, font=("Consolas", 11))
        self.fs_output.pack(pady=10)
        self.fs_output.config(state=tk.DISABLED)

    def gui_create_file(self):
        name = simpledialog.askstring("Create File", "File name:")
        if not name:
            return
        owner = simpledialog.askstring("Create File", "Owner (user/admin):")
        if not owner:
            return
        encrypted = messagebox.askyesno("Create File", "Encrypted?")
        perms = simpledialog.askstring("Create File", "Permissions for user (e.g. rwx):") or "rwx"
        perms_admin = simpledialog.askstring("Create File", "Permissions for admin (e.g. rwx):") or "rwx"
        orig_input = __builtins__.input
        fs_inputs = [name, owner, 'y' if encrypted else 'n', perms, perms_admin]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.create_file)
        finally:
            __builtins__.input = orig_input

    def gui_write_file(self):
        name = simpledialog.askstring("Write File", "File name:")
        if not name:
            return
        data = simpledialog.askstring("Write File", "Enter file content:")
        if data is None:
            return
        orig_input = __builtins__.input
        fs_inputs = [name, data]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.write_file)
        finally:
            __builtins__.input = orig_input

    def gui_read_file(self):
        name = simpledialog.askstring("Read File", "File name:")
        if not name:
            return
        orig_input = __builtins__.input
        fs_inputs = [name]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.read_file)
        finally:
            __builtins__.input = orig_input

    def gui_delete_file(self):
        name = simpledialog.askstring("Delete File", "File name:")
        if not name:
            return
        orig_input = __builtins__.input
        fs_inputs = [name]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.delete_file)
        finally:
            __builtins__.input = orig_input

    def gui_create_directory(self):
        name = simpledialog.askstring("Create Directory", "Directory name:")
        if not name:
            return
        orig_input = __builtins__.input
        fs_inputs = [name]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.create_directory)
        finally:
            __builtins__.input = orig_input

    def gui_change_directory(self):
        name = simpledialog.askstring("Change Directory", "Directory name (.. for parent):")
        if not name:
            return
        orig_input = __builtins__.input
        fs_inputs = [name]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.change_directory)
        finally:
            __builtins__.input = orig_input

    def gui_list_directory(self):
        self._show_fs_output(self.fs_manager.list_directory)

    def gui_set_user(self):
        user = simpledialog.askstring("Switch User", "Switch user (user/admin):")
        if not user:
            return
        orig_input = __builtins__.input
        fs_inputs = [user]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.set_user)
        finally:
            __builtins__.input = orig_input

    def gui_search_file(self):
        name = simpledialog.askstring("Search File", "Enter file name to search:")
        if not name:
            return
        orig_input = __builtins__.input
        fs_inputs = [name]
        __builtins__.input = lambda prompt=None: fs_inputs.pop(0)
        try:
            self._show_fs_output(self.fs_manager.search_file)
        finally:
            __builtins__.input = orig_input

    def gui_visualize_tree(self):
        self._show_fs_output(self.fs_manager.visualize_tree)

    def _show_fs_output(self, func):
        self.fs_output.config(state=tk.NORMAL)
        self.fs_output.delete(1.0, tk.END)
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        func()
        sys.stdout = sys_stdout
        self.fs_output.insert(tk.END, buf.getvalue())
        self.fs_output.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = MiniOSGUI()
    app.mainloop() 