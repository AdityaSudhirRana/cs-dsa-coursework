import tkinter as tk
from tkinter import ttk, messagebox

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def get_elements(self):
        return list(reversed(self.stack))


# --- Business Logic Functions ---
def check_delimiter_matching(expression: str) -> bool:
    s = Stack()
    mapping = {")": "(", "}": "{", "]": "["}
    for char in expression:
        if char in mapping.values():
            s.push(char)
        elif char in mapping.keys():
            if s.is_empty() or s.pop() != mapping[char]:
                return False
    return s.is_empty()

def is_operator(char: str) -> bool:
    return char in {'+', '-', '*', '/', '^'}

def prefix_to_postfix(prefix_expr: str) -> str:
    s = Stack()
    tokens = prefix_expr.split() if " " in prefix_expr else list(prefix_expr)
    
    for token in reversed(tokens):
        if is_operator(token):
            operand1 = s.pop()
            operand2 = s.pop()
            if operand1 is None or operand2 is None:
                return "Error: Invalid Prefix Expression"
            new_expr = f"{operand1} {operand2} {token}"
            s.push(new_expr)
        else:
            s.push(token)
    return s.pop()

def evaluate_postfix(postfix_expr: str):
    s = Stack()
    tokens = postfix_expr.split()
    try:
        for token in tokens:
            if token.replace('.','',1).isdigit() or (token.startswith('-') and token[1:].replace('.','',1).isdigit()):
                s.push(float(token))
            elif is_operator(token):
                operand2 = s.pop()
                operand1 = s.pop()
                if operand1 is None or operand2 is None:
                    raise ValueError("Malformed syntax")
                
                if token == '+': s.push(operand1 + operand2)
                elif token == '-': s.push(operand1 - operand2)
                elif token == '*': s.push(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0: raise ZeroDivisionError("Division by zero")
                    s.push(operand1 / operand2)
                elif token == '^': s.push(operand1 ** operand2)
        return s.pop()
    except Exception as e:
        return f"Error: {str(e)}"


class StackGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Operations Suite")
        self.root.geometry("520x460")
        
        self.demo_stack = Stack()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_operations_tab()
        self.create_delimiter_tab()
        self.create_expression_tab()

    def create_operations_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Core Operations")
        
        entry_frame = ttk.LabelFrame(tab, text=" Stack Control Panel ", padding=10)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(entry_frame, text="Enter Value:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.item_entry = ttk.Entry(entry_frame, width=15)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(entry_frame, text="Push", command=self.gui_push).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(entry_frame, text="Pop", command=self.gui_pop).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(entry_frame, text="Peek", command=self.gui_peek).grid(row=1, column=1, padx=5, pady=5)
        
        display_frame = ttk.LabelFrame(tab, text=" Live Stack Visualization (Top to Bottom) ", padding=10)
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.stack_box = tk.Listbox(display_frame, font=("Courier", 12), justify="center")
        self.stack_box.pack(fill="both", expand=True)
        self.update_stack_display()

    def create_delimiter_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Delimiter Checker")
        
        frame = ttk.LabelFrame(tab, text=" Balanced Bracket Checker ", padding=15)
        frame.pack(fill="x", padx=15, pady=20)
        
        ttk.Label(frame, text="Input Expression:").pack(anchor="w", pady=2)
        self.delim_entry = ttk.Entry(frame, width=40)
        self.delim_entry.insert(0, "{[()()]}")
        self.delim_entry.pack(fill="x", pady=5)
        
        ttk.Button(frame, text="Verify Balance Match", command=self.gui_check_delimiters).pack(pady=10)
        
        self.delim_result_lbl = ttk.Label(frame, text="Result: Waiting for validation...", font=("Arial", 11, "bold"))
        self.delim_result_lbl.pack(pady=5)

    def create_expression_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Expression Converter")
        
        frame = ttk.LabelFrame(tab, text=" Prefix Conversion & Evaluation System ", padding=15)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ttk.Label(frame, text="Prefix Expression (Use spaces for multi-digit terms):").pack(anchor="w", pady=2)
        self.expr_entry = ttk.Entry(frame, width=40)
        self.expr_entry.insert(0, "- + 2 3 4")
        self.expr_entry.pack(fill="x", pady=5)
        
        ttk.Button(frame, text="Process Expression", command=self.gui_process_expression).pack(pady=10)
        
        self.postfix_lbl = ttk.Label(frame, text="Postfix Conversion: ", font=("Arial", 10))
        self.postfix_lbl.pack(anchor="w", pady=5)
        
        self.eval_lbl = ttk.Label(frame, text="Evaluation Result: ", font=("Arial", 11, "bold"))
        self.eval_lbl.pack(anchor="w", pady=5)

    def update_stack_display(self):
        self.stack_box.delete(0, tk.END)
        items = self.demo_stack.get_elements()
        if not items:
            self.stack_box.insert(tk.END, "[ Stack is Empty ]")
            return
        for item in items:
            self.stack_box.insert(tk.END, f"|  {item}  |")
        self.stack_box.insert(tk.END, "========")

    def gui_push(self):
        val = self.item_entry.get().strip()
        if not val:
            messagebox.showwarning("Warning", "Input data missing.")
            return
        self.demo_stack.push(val)
        self.item_entry.delete(0, tk.END)
        self.update_stack_display()

    def gui_pop(self):
        popped = self.demo_stack.pop()
        if popped is None:
            messagebox.showerror("Error", "Stack Underflow! Target structural container is empty.")
        else:
            messagebox.showinfo("Success", f"Removed Element: {popped}")
            self.update_stack_display()

    def gui_peek(self):
        top_item = self.demo_stack.peek()
        if top_item is None:
            messagebox.showinfo("Info", "Stack state contains zero elements.")
        else:
            messagebox.showinfo("Peek Result", f"Element sitting at top boundary: {top_item}")

    def gui_check_delimiters(self):
        expr = self.delim_entry.get().strip()
        if not expr:
            messagebox.showwarning("Input Error", "Please enter structural characters to track.")
            return
        
        if check_delimiter_matching(expr):
            self.delim_result_lbl.config(text="Result: Balanced Layout Structure", foreground="green")
        else:
            self.delim_result_lbl.config(text="Result: Unbalanced Expression Syntax", foreground="red")

    def gui_process_expression(self):
        prefix_in = self.expr_entry.get().strip()
        if not prefix_in:
            messagebox.showwarning("Input Error", "Prefix expression field cannot be empty.")
            return
        
        postfix_out = prefix_to_postfix(prefix_in)
        self.postfix_lbl.config(text=f"Postfix Conversion: {postfix_out}")
        
        if "Error" in postfix_out:
            self.eval_lbl.config(text="Evaluation Result: Execution Cancelled", foreground="red")
        else:
            res = evaluate_postfix(postfix_out)
            if "Error" in str(res):
                self.eval_lbl.config(text=f"Evaluation {res}", foreground="red")
            else:
                self.eval_lbl.config(text=f"Evaluation Result: {res}", foreground="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = StackGUIApp(root)
    root.mainloop()
