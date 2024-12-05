import tkinter as tk
from grading_system import GradingSystem

def main():
    root = tk.Tk()
    root.title("Grading App")
    root.geometry("500x400")
    app = GradingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
