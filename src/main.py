import tkinter as tk
from tkinter import messagebox
from data_splitter import split_dataset
from model import train_and_evaluate

# Arc-Dark Colors and Fonts
BG_COLOR = "#383c4a"
BUTTON_BG = "#4E5665"
BUTTON_HOVER = "#528BFF"
TEXT_COLOR = "#FFFFFF"
TEXT_SECONDARY = "#A9B7C6"
INPUT_BG = "#2B2B2B"

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_SUBTITLE = ("Helvetica", 14)
FONT_BUTTON = ("Helvetica", 16)
FONT_TEXT = ("Helvetica", 12)
FONT_FOOTER = ("Helvetica", 10)

def create_label(parent, text, font, bg=BG_COLOR, fg=TEXT_COLOR, **kwargs):
    return tk.Label(parent, text=text, font=font, bg=bg, fg=fg, **kwargs)

def create_button(parent, text, font, command, bg=BUTTON_BG, fg=TEXT_COLOR, active_bg=BUTTON_HOVER, **kwargs):
    return tk.Button(parent, text=text, font=font, bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg, command=command, **kwargs)

def display_results(report):
    results_window = tk.Toplevel()
    results_window.title("Model Evaluation Results")
    results_window.geometry("600x400")
    results_window.configure(bg=BG_COLOR)

    create_label(results_window, text="Model Evaluation Results", font=FONT_TEXT, fg=TEXT_COLOR).pack(pady=10)

    text_widget = tk.Text(
        results_window, font=("Courier", 12), wrap="none", bg=INPUT_BG, fg=TEXT_SECONDARY, relief="sunken", height=15
    )
    text_widget.insert("1.0", report)
    text_widget.configure(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    create_button(results_window, text="Close", font=FONT_TEXT, command=results_window.destroy).pack(pady=10)

def handle_split():
    base_path = "../data"
    output_dir = "../output"

    try:
        train_real, test_real = split_dataset(base_path, "real", output_dir)
        train_fake_hard, test_fake_hard = split_dataset(base_path, "fake/Altered-Hard", output_dir)
        messagebox.showinfo(
            "Success",
            f"Dataset split completed!\n"
            f"Real - Train: {train_real}, Test: {test_real}\n"
            f"Fake Hard - Train: {train_fake_hard}, Test: {test_fake_hard}",
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def handle_train():
    try:
        report = train_and_evaluate("../output/train", "../output/test")
        display_results(report)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during training: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Fingerprint Spoof Detection")
    root.geometry("600x350")
    root.configure(bg=BG_COLOR)

    main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    create_label(main_frame, text="Fingerprint Spoof Detection", font=FONT_TITLE).pack(pady=10)
    create_label(main_frame, text="Choose an action below:", font=FONT_SUBTITLE, fg=TEXT_SECONDARY).pack(pady=5)

    create_button(main_frame, text="Split Dataset", font=FONT_BUTTON, command=handle_split).pack(pady=10, ipadx=10, ipady=5)
    create_button(
        main_frame, text="Train and Evaluate Model", font=FONT_BUTTON, bg="#28a745", command=handle_train
    ).pack(pady=10, ipadx=10, ipady=5)

    create_label(main_frame, text="© 2024 Fingerprint Spoof Detection System", font=FONT_FOOTER, fg=TEXT_SECONDARY).pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
