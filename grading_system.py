import tkinter as tk
from tkinter import messagebox
import csv  # Importing csv library
from calculator import GradeCalculator  # Importing GradeCalculator class


class CSVManager:
    def __init__(self, filename='grades.csv'):
        self.filename = filename

    def append_grade(self, data):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final", "Grade"])
            writer.writerow(data)

    def save_all(self, students):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final", "Grade"])
            for name, details in students.items():
                writer.writerow([name] + details['scores'] + [details['final_score'], details['grade']])


class StudentManager:
    def __init__(self, calculator, csv_manager):
        self.calculator = calculator
        self.csv_manager = csv_manager
        self.students = {}

    def submit_scores(self, name, scores):
        final_score = max(scores) if scores else 0
        grade = self.calculator.calculate_grade(final_score)
        self.students[name] = {
            'scores': scores + [0] * (4 - len(scores)),
            'final_score': final_score,
            'grade': grade,
        }
        self.csv_manager.append_grade([name] + self.students[name]['scores'] + [final_score, grade])

    def save_students(self):
        self.csv_manager.save_all(self.students)


class GUIManager:
    def __init__(self, root, student_manager):
        self.root = root
        self.student_manager = student_manager
        self.setup_gui()

    def setup_gui(self):
        # Create and arrange widgets
        tk.Label(self.root, text="Enter student's name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Enter number of attempts (1-4):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.attempts_entry = tk.Entry(self.root, font=("Arial", 12))
        self.attempts_entry.grid(row=1, column=1, padx=10, pady=10)

        vcmd = (self.root.register(self.on_attempts_change), '%P')
        self.attempts_entry.configure(validate='key', validatecommand=vcmd)

        # Buttons
        add_button = tk.Button(
            self.root, text="Add", command=self.add_student, bg="purple", fg="white", font=("Arial", 12), padx=20, pady=10
        )
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        clear_button = tk.Button(
            self.root, text="Clear", command=self.clear_entries, bg="purple", fg="white", font=("Arial", 12), padx=20, pady=10
        )
        clear_button.grid(row=4, column=0, pady=10)

        exit_button = tk.Button(
            self.root, text="Exit", command=self.root.destroy, bg="purple", fg="white", font=("Arial", 12), padx=20, pady=10
        )
        exit_button.grid(row=4, column=1, pady=10)

        self.score_frame = tk.Frame(self.root)
        self.score_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.score_entries = []

    def on_attempts_change(self, value):
        if value.isdigit() and 1 <= int(value) <= 4:
            self.create_score_entries(int(value))
            return True
        elif value == "":
            self.clear_score_entries()
            return True
        return False

    def create_score_entries(self, num_attempts):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        self.score_entries = []
        for i in range(num_attempts):
            tk.Label(self.score_frame, text=f"Score {i + 1}:", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.score_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.score_entries.append(entry)

    def clear_score_entries(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        self.score_entries = []

    def add_student(self):
        name = self.name_entry.get().strip()
        attempts = self.attempts_entry.get()
        if not name or not attempts.isdigit() or not 1 <= int(attempts) <= 4:
            messagebox.showerror("Error", "Invalid input. Check the name and number of attempts.")
            return

        scores = [int(entry.get()) for entry in self.score_entries if entry.get().isdigit() and 0 <= int(entry.get()) <= 100]
        if len(scores) != int(attempts):
            messagebox.showerror("Error", "Please enter valid scores for all attempts.")
            return

        self.student_manager.submit_scores(name, scores)
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.attempts_entry.delete(0, tk.END)
        self.clear_score_entries()


class GradingSystem:
    def __init__(self, root):
        self.root = root
        self.calculator = GradeCalculator()
        self.csv_manager = CSVManager()
        self.student_manager = StudentManager(self.calculator, self.csv_manager)
        self.gui_manager = GUIManager(root, self.student_manager)
