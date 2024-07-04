import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def analyze_code_with_flake8(file_path):
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    return result.stdout

def analyze_code_with_pylint(file_path):
    result = subprocess.run(['pylint', file_path, '--output-format=text'], capture_output=True, text=True)
    return result.stdout

def generate_report(flake8_report, pylint_report):
    report = "Code Review Report:\n\n"
    report += "Flake8 Analysis:\n"
    report += flake8_report
    report += "\n\nPylint Analysis:\n"
    report += pylint_report
    return report

def save_report(report, output_path):
    with open(output_path, 'w') as file:
        file.write(report)

def main():
    def select_code_file():
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            code_path_entry.delete(0, tk.END)
            code_path_entry.insert(0, file_path)

    def perform_analysis():
        code_path = code_path_entry.get()
        
        if not code_path:
            messagebox.showerror("Error", "Please select a code file path.")
            return

        flake8_report = analyze_code_with_flake8(code_path)
        pylint_report = analyze_code_with_pylint(code_path)
        
        report = generate_report(flake8_report, pylint_report)

        output_path = os.path.splitext(code_path)[0] + "_review.txt"
        save_report(report, output_path)
        messagebox.showinfo("Success", f"Code review report saved to {output_path}")

    root = tk.Tk()
    root.title("Code Review Tool")

    tk.Label(root, text="Select Code File:").grid(row=0, column=0, padx=10, pady=5)
    code_path_entry = tk.Entry(root, width=50)
    code_path_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_code_file).grid(row=0, column=2, padx=10, pady=5)

    tk.Button(root, text="Analyze", command=perform_analysis).grid(row=1, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
