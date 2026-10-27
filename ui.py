import tkinter as tk
from tkinter import ttk, messagebox
from algorithm import run_floyd_warshall, reconstruct_path, INF

class FloydWarshallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Floyd-Warshall Algorithm Visualizer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")

        self.num_nodes = tk.IntVar(value=4)
        self.entries = []
        self.k_matrices = []
        self.next_matrices = []
        self.current_step = 0

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(self.root, text="Floyd-Warshall All-Pairs Shortest Path", font=("Helvetica", 18, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        title_label.pack(pady=10)

        control_frame = tk.Frame(self.root, bg="#313244", bd=2, relief=tk.RAISED)
        control_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(control_frame, text="Number of Nodes:", font=("Helvetica", 11), fg="#cdd6f4", bg="#313244").pack(side=tk.LEFT, padx=10, pady=10)
        
        node_spinner = ttk.Spinbox(control_frame, from_=2, to=8, textvariable=self.num_nodes, width=5, command=self.generate_matrix_inputs)
        node_spinner.pack(side=tk.LEFT, padx=5)

        btn_generate = tk.Button(control_frame, text="Set Matrix", command=self.generate_matrix_inputs, bg="#89b4fa", fg="#11111b", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=10)
        btn_generate.pack(side=tk.LEFT, padx=10)

        btn_solve = tk.Button(control_frame, text="Run Floyd-Warshall", command=self.run_algorithm, bg="#a6e3a1", fg="#11111b", font=("Helvetica", 10, "bold"), relief=tk.FLAT, padx=10)
        btn_solve.pack(side=tk.LEFT, padx=10)

        content_frame = tk.Frame(self.root, bg="#1e1e2e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.input_frame = tk.LabelFrame(content_frame, text=" Adjacency Matrix Input (Leave blank or 'inf' for ∞) ", font=("Helvetica", 11, "bold"), fg="#89b4fa", bg="#1e1e2e", bd=2)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_frame = tk.LabelFrame(content_frame, text=" Solution & Path Lookup ", font=("Helvetica", 11, "bold"), fg="#a6e3a1", bg="#1e1e2e", bd=2)
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.matrix_display_frame = tk.Frame(self.result_frame, bg="#1e1e2e")
        self.matrix_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.step_frame = tk.Frame(self.result_frame, bg="#1e1e2e")
        self.step_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_prev = tk.Button(self.step_frame, text="◄ Prev Step", command=self.prev_step, state=tk.DISABLED, bg="#45475a", fg="#cdd6f4")
        self.btn_prev.pack(side=tk.LEFT, padx=5)

        self.lbl_step_info = tk.Label(self.step_frame, text="Step: 0 / 0", font=("Helvetica", 10), fg="#cdd6f4", bg="#1e1e2e")
        self.lbl_step_info.pack(side=tk.LEFT, expand=True)

        self.btn_next = tk.Button(self.step_frame, text="Next Step ►", command=self.next_step, state=tk.DISABLED, bg="#45475a", fg="#cdd6f4")
        self.btn_next.pack(side=tk.RIGHT, padx=5)

        path_frame = tk.Frame(self.result_frame, bg="#313244", bd=1, relief=tk.SOLID)
        path_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(path_frame, text="Find Path:", font=("Helvetica", 10, "bold"), fg="#cdd6f4", bg="#313244").grid(row=0, column=0, padx=5, pady=5)
        
        tk.Label(path_frame, text="From:", fg="#cdd6f4", bg="#313244").grid(row=0, column=1, padx=2)
        self.src_var = tk.IntVar(value=0)
        self.src_spin = ttk.Spinbox(path_frame, from_=0, to=3, textvariable=self.src_var, width=3)
        self.src_spin.grid(row=0, column=2, padx=5)

        tk.Label(path_frame, text="To:", fg="#cdd6f4", bg="#313244").grid(row=0, column=3, padx=2)
        self.dst_var = tk.IntVar(value=1)
        self.dst_spin = ttk.Spinbox(path_frame, from_=0, to=3, textvariable=self.dst_var, width=3)
        self.dst_spin.grid(row=0, column=4, padx=5)

        btn_find_path = tk.Button(path_frame, text="Get Path", command=self.display_path, bg="#f9e2af", fg="#11111b", font=("Helvetica", 9, "bold"))
        btn_find_path.grid(row=0, column=5, padx=10, pady=5)

        self.lbl_path_result = tk.Label(self.result_frame, text="Path: N/A", font=("Helvetica", 11, "bold"), fg="#f9e2af", bg="#1e1e2e")
        self.lbl_path_result.pack(pady=5)

        self.generate_matrix_inputs()
        self.load_sample_data()

    def generate_matrix_inputs(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        n = self.num_nodes.get()
        self.src_spin.config(to=n-1)
        self.dst_spin.config(to=n-1)

        self.entries = []
        for i in range(n):
            tk.Label(self.input_frame, text=f"Node {i}", font=("Helvetica", 9, "bold"), fg="#89b4fa", bg="#1e1e2e").grid(row=0, column=i+1, padx=5, pady=5)
            tk.Label(self.input_frame, text=f"Node {i}", font=("Helvetica", 9, "bold"), fg="#89b4fa", bg="#1e1e2e").grid(row=i+1, column=0, padx=5, pady=5)

        for i in range(n):
            row_entries = []
            for j in range(n):
                e = tk.Entry(self.input_frame, width=6, justify="center", font=("Helvetica", 10), bg="#45475a", fg="#cdd6f4", insertbackground="white")
                e.grid(row=i+1, column=j+1, padx=3, pady=3)
                if i == j:
                    e.insert(0, "0")
                    e.config(state="disabled", disabledbackground="#313244", disabledforeground="#a6adc8")
                row_entries.append(e)
            self.entries.append(row_entries)

    def load_sample_data(self):
        sample = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
        n = min(self.num_nodes.get(), len(sample))
        for i in range(n):
            for j in range(n):
                if i != j:
                    val = sample[i][j]
                    self.entries[i][j].delete(0, tk.END)
                    if val != INF:
                        self.entries[i][j].insert(0, str(val))

    def parse_input_graph(self):
        n = self.num_nodes.get()
        graph = [[INF]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    graph[i][j] = 0
                    continue
                val = self.entries[i][j].get().strip().lower()
                if val == "" or val == "inf" or val == "∞":
                    graph[i][j] = INF
                else:
                    try:
                        graph[i][j] = float(val)
                    except ValueError:
                        messagebox.showerror("Input Error", f"Invalid value at Row {i}, Col {j}: '{val}'")
                        return None
        return graph

    def run_algorithm(self):
        graph = self.parse_input_graph()
        if graph is None:
            return

        self.k_matrices, self.next_matrices, has_negative_cycle = run_floyd_warshall(graph)

        if has_negative_cycle:
            messagebox.showwarning("Warning", "Negative Weight Cycle Detected!")

        self.current_step = len(self.k_matrices) - 1
        self.update_step_display()

    def update_step_display(self):
        for widget in self.matrix_display_frame.winfo_children():
            widget.destroy()

        if not self.k_matrices:
            return

        matrix, title = self.k_matrices[self.current_step]
        n = len(matrix)

        tk.Label(self.matrix_display_frame, text=title, font=("Helvetica", 11, "bold"), fg="#f9e2af", bg="#1e1e2e").pack(pady=5)
        table_frame = tk.Frame(self.matrix_display_frame, bg="#1e1e2e")
        table_frame.pack()

        for j in range(n):
            tk.Label(table_frame, text=f"Node {j}", font=("Helvetica", 9, "bold"), fg="#89b4fa", bg="#1e1e2e", width=6).grid(row=0, column=j+1, padx=3, pady=3)

        for i in range(n):
            tk.Label(table_frame, text=f"Node {i}", font=("Helvetica", 9, "bold"), fg="#89b4fa", bg="#1e1e2e", width=6).grid(row=i+1, column=0, padx=3, pady=3)
            for j in range(n):
                val = matrix[i][j]
                text = "∞" if val == INF else (f"{int(val)}" if val == int(val) else f"{val:.1f}")
                bg_color, fg_color = "#313244", "#cdd6f4"
                if i == j:
                    bg_color = "#45475a"
                elif 0 < self.current_step <= n and (i == self.current_step-1 or j == self.current_step-1):
                    bg_color, fg_color = "#fab387", "#11111b"

                tk.Label(table_frame, text=text, font=("Helvetica", 10, "bold"), width=6, height=2, bg=bg_color, fg=fg_color, relief=tk.RIDGE).grid(row=i+1, column=j+1, padx=2, pady=2)

        self.lbl_step_info.config(text=f"Step {self.current_step} of {len(self.k_matrices)-1}")
        self.btn_prev.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_step < len(self.k_matrices)-1 else tk.DISABLED)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_display()

    def next_step(self):
        if self.current_step < len(self.k_matrices) - 1:
            self.current_step += 1
            self.update_step_display()

    def display_path(self):
        if not self.next_matrices:
            messagebox.showinfo("Info", "Please run the algorithm first.")
            return

        u, v = self.src_var.get(), self.dst_var.get()
        dist_matrix = self.k_matrices[-1][0]
        next_matrix = self.next_matrices[-1]

        path, cost = reconstruct_path(u, v, dist_matrix, next_matrix)
        if path is None:
            self.lbl_path_result.config(text=f"Path ({u} ➔ {v}): No path exists")
        else:
            path_str = " ➔ ".join(f"Node {node}" for node in path)
            cost_str = int(cost) if cost == int(cost) else f"{cost:.1f}"
            self.lbl_path_result.config(text=f"Path ({u} ➔ {v}): {path_str} | Cost = {cost_str}")
