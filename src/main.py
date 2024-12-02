import tkinter as tk
from tkinter import messagebox, ttk
from data_splitter import split_dataset
from model import train_and_evaluate

def display_results(report):
    results_window = tk.Toplevel()
    results_window.title("Model Evaluation Results")
    results_window.geometry("600x400")
    results_window.configure(bg="#f5f5f5")

    title_label = tk.Label(
        results_window, text="Model Evaluation Results", font=("Helvetica", 16, "bold"), bg="#f5f5f5"
    )
    title_label.pack(pady=10)

    text_widget = tk.Text(results_window, font=("Courier", 12), wrap="none", bg="white", relief="sunken", height=15)
    text_widget.insert("1.0", report)
    text_widget.configure(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    close_button = tk.Button(
        results_window, text="Close", font=("Helvetica", 12), command=results_window.destroy
    )
    close_button.pack(pady=10)

def on_split_button_click():
    base_path = "../data"
    output_dir = "../output"

    try:
        train_real, test_real = split_dataset(base_path, 'real', output_dir)
        train_fake_hard, test_fake_hard = split_dataset(base_path, 'fake/Altered-Hard', output_dir)
        messagebox.showinfo(
            "Success",
            f"Dataset split completed!\n"
            f"Real - Train: {train_real}, Test: {test_real}\n"
            f"Fake Hard - Train: {train_fake_hard}, Test: {test_fake_hard}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def on_train_button_click():
    try:
        report = train_and_evaluate("../output/train", "../output/test")
        display_results(report)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during training: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Fingerprint Spoof Detection")
    root.geometry("600x300")
    root.configure(bg="#f5f5f5")

    main_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    title_label = tk.Label(
        main_frame, text="Fingerprint Spoof Detection", font=("Helvetica", 24, "bold"), bg="#f5f5f5"
    )
    title_label.pack(pady=10)

    instructions_label = tk.Label(
        main_frame,
        text="Choose an action below:",
        font=("Helvetica", 14),
        bg="#f5f5f5",
    )
    instructions_label.pack(pady=5)

    split_button = tk.Button(
        main_frame, text="Split Dataset", font=("Helvetica", 16), bg="#0078d7", fg="white", command=on_split_button_click
    )
    split_button.pack(pady=10, ipadx=10, ipady=5)

    train_button = tk.Button(
        main_frame,
        text="Train and Evaluate Model",
        font=("Helvetica", 16),
        bg="#28a745",
        fg="white",
        command=on_train_button_click,
    )
    train_button.pack(pady=10, ipadx=10, ipady=5)

    footer_label = tk.Label(
        main_frame,
        text="© 2024 Fingerprint Spoof Detection System",
        font=("Helvetica", 10),
        bg="#f5f5f5",
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
