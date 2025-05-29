import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from process import ProcessManager
from memory import MemoryManager
from concurrency import ConcurrencyManager
from filesystem import FileSystemManager

# Tooltip helper
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 40
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#444459", foreground="#fff",
                         relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 10), padx=8, pady=4)
        label.pack()
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class MiniOSGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini OS Simulation GUI")
        self.geometry("1050x750")
        self.resizable(False, False)
        self.configure(bg="#23232b")
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager()
        self.concurrency_manager = ConcurrencyManager()
        self.fs_manager = FileSystemManager()
        self.status_var = tk.StringVar(value="Welcome to Mini OS Simulation!")
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
        style.configure("TButton", background="#5c5c7a", foreground="#fff", font=("Segoe UI", 11, "bold"), padding=10, borderwidth=0, relief="flat")
        style.map("TButton", background=[("active", "#7a7ab8")])
        style.configure("TEntry", fieldbackground="#23232b", foreground="#fff")

    def create_widgets(self):
        # Header
        header = ttk.Label(self, text="VirtuOS", font=("Segoe UI", 22, "bold"), anchor="center")
        header.pack(pady=(18, 8))

        tab_control = ttk.Notebook(self)
        self.process_tab = ttk.Frame(tab_control)
        self.memory_tab = ttk.Frame(tab_control)
        self.concurrency_tab = ttk.Frame(tab_control)
        self.fs_tab = ttk.Frame(tab_control)

        tab_control.add(self.process_tab, text='🧑‍💻 Process Management')
        tab_control.add(self.memory_tab, text='💾 Memory Management')
        tab_control.add(self.concurrency_tab, text='🔄 Concurrency')
        tab_control.add(self.fs_tab, text='📁 File System')
        tab_control.pack(expand=1, fill='both', padx=16, pady=8)

        self.init_process_tab()
        self.init_memory_tab()
        self.init_concurrency_tab()
        self.init_fs_tab()

        # Status bar
        status_bar = tk.Label(self, textvariable=self.status_var, anchor="w", bg="#2d2d39", fg="#fff", font=("Segoe UI", 11), relief="flat", padx=10)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, msg):
        self.status_var.set(msg)

    def init_process_tab(self):
        label = ttk.Label(self.process_tab, text="Process Management", font=("Arial", 16))
        label.pack(pady=10)

        # Scheduler label
        self.scheduler_label = ttk.Label(self.process_tab, text=f"Scheduler: {self.process_manager.scheduler_type}", font=("Segoe UI", 12, "italic"))
        self.scheduler_label.pack(pady=(0, 8))

        btn_frame = ttk.Frame(self.process_tab)
        btn_frame.pack(pady=5)

        btns = [
            ("Create Process", self.gui_create_process, "Create a new process with name and power profile."),
            ("Switch Process", self.gui_switch_process, "Switch to the next process in the queue."),
            ("Terminate Process", self.gui_terminate_process, "Terminate the currently running process."),
            ("List Processes", self.gui_list_processes, "Show all processes and their states."),
            ("Set Scheduler", self.gui_set_scheduler, "Choose the scheduling algorithm."),
            ("Visualize Queues", self.gui_visualize_queues, "Show the ready/running queues."),
            ("Set CPU Cores", self.gui_set_cores, "Set the number of CPU cores to simulate."),
            ("Start Cores", self.gui_start_cores, "Start all CPU core threads."),
            ("Stop Cores", self.gui_stop_cores, "Stop all CPU core threads."),
            ("Show Core Status", self.gui_show_cores, "Show the status of each CPU core."),
        ]
        for i, (text, cmd, tip) in enumerate(btns):
            btn = ttk.Button(btn_frame, text=text, command=cmd)
            btn.grid(row=i//4, column=i%4, padx=8, pady=6, sticky="ew")
            ToolTip(btn, tip)

        self.proc_output = tk.Text(self.process_tab, height=18, width=110, font=("Consolas", 11), bg="#181820", fg="#fff", insertbackground="#fff", relief="flat", borderwidth=8)
        self.proc_output.pack(pady=10)
        self.proc_output.config(state=tk.DISABLED)

    def gui_create_process(self):
        name = simpledialog.askstring("Create Process", "Enter app name:")
        if not name:
            return
        power = simpledialog.askstring("Create Process", "Power profile (low/medium/high):")
        if not power:
            return
        pcb_input = [name, power]
        orig_input = __builtins__.input
        __builtins__.input = lambda prompt=None: pcb_input.pop(0)
        try:
            self.process_manager.create_process()
            self.set_status(f"Process '{name}' created.")
            self.gui_list_processes()
        finally:
            __builtins__.input = orig_input

    def gui_switch_process(self):
        self.process_manager.switch_process()
        self.set_status("Switched process.")
        self.gui_list_processes()

    def gui_terminate_process(self):
        self.process_manager.terminate_process()
        self.set_status("Terminated running process.")
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
        self.scheduler_label.config(text=f"Scheduler: {self.process_manager.scheduler_type}")

    def gui_set_scheduler(self):
        scheds = ["FIFO", "RR", "MLFQ", "POWER"]
        sched = simpledialog.askstring("Set Scheduler", "Enter scheduler (FIFO/RR/MLFQ/POWER):")
        if sched and sched.upper() in scheds:
            orig_input = __builtins__.input
            __builtins__.input = lambda prompt=None: str(scheds.index(sched.upper())+1)
            try:
                self.process_manager.set_scheduler()
                self.set_status(f"Scheduler set to {sched.upper()}.")
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
        self.set_status("Visualized process queues.")

    def gui_set_cores(self):
        n = simpledialog.askinteger("Set CPU Cores", "Enter number of CPU cores:", minvalue=1, maxvalue=16)
        if n:
            orig_input = __builtins__.input
            __builtins__.input = lambda prompt=None: str(n)
            try:
                self.process_manager.set_cores()
                self.set_status(f"CPU cores set to {n}.")
            finally:
                __builtins__.input = orig_input
            self.gui_show_cores()

    def gui_start_cores(self):
        self.process_manager.start_cores()
        self.set_status("Started CPU cores.")
        self.gui_show_cores()

    def gui_stop_cores(self):
        self.process_manager.stop_cores_func()
        self.set_status("Stopped CPU cores.")
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
        self.set_status("Showing core status.")

    def init_memory_tab(self):
        label = ttk.Label(self.memory_tab, text="Memory Management", font=("Arial", 16))
        label.pack(pady=10)

        btn_frame = ttk.Frame(self.memory_tab)
        btn_frame.pack(pady=5, fill='x')

        btns = [
            ("Create Page Table", self.gui_create_page_table),
            ("Translate Address", self.gui_translate_address),
            ("Visualize Memory", self.gui_visualize_memory),
            ("Visualize Fragmentation", self.gui_visualize_fragmentation),
            ("Swap Out Process", self.gui_swap_out),
            ("Swap In Process", self.gui_swap_in),
        ]
        cols = 4
        for i, (text, cmd) in enumerate(btns):
            btn = ttk.Button(btn_frame, text=text, command=cmd)
            btn.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
            btn_frame.grid_columnconfigure(i%cols, weight=1)
        for r in range((len(btns)+cols-1)//cols):
            btn_frame.grid_rowconfigure(r, weight=1)

        self.mem_output = tk.Text(self.memory_tab, height=18, width=110, font=("Consolas", 11), bg="#181820", fg="#fff", insertbackground="#fff", relief="flat", borderwidth=8)
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
        btn_frame.pack(pady=5, fill='x')

        btns = [
            ("Produce (Producer)", self.gui_produce),
            ("Consume (Consumer)", self.gui_consume),
            ("Show Buffer", self.gui_show_buffer),
        ]
        cols = 3
        for i, (text, cmd) in enumerate(btns):
            btn = ttk.Button(btn_frame, text=text, command=cmd)
            btn.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
            btn_frame.grid_columnconfigure(i%cols, weight=1)
        for r in range((len(btns)+cols-1)//cols):
            btn_frame.grid_rowconfigure(r, weight=1)

        self.conc_output = tk.Text(self.concurrency_tab, height=10, width=110, font=("Consolas", 11), bg="#181820", fg="#fff", insertbackground="#fff", relief="flat", borderwidth=8)
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
        btn_frame.pack(pady=5, fill='x')

        btns = [
            ("Create File", self.gui_create_file),
            ("Write File", self.gui_write_file),
            ("Read File", self.gui_read_file),
            ("Delete File", self.gui_delete_file),
            ("Create Directory", self.gui_create_directory),
            ("Change Directory", self.gui_change_directory),
            ("List Directory", self.gui_list_directory),
            ("Switch User", self.gui_set_user),
            ("Search File", self.gui_search_file),
            ("Visualize Directory Tree", self.gui_visualize_tree),
        ]
        cols = 5
        for i, (text, cmd) in enumerate(btns):
            btn = ttk.Button(btn_frame, text=text, command=cmd)
            btn.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
            btn_frame.grid_columnconfigure(i%cols, weight=1)
        for r in range((len(btns)+cols-1)//cols):
            btn_frame.grid_rowconfigure(r, weight=1)

        self.fs_output = tk.Text(self.fs_tab, height=18, width=110, font=("Consolas", 11), bg="#181820", fg="#fff", insertbackground="#fff", relief="flat", borderwidth=8)
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