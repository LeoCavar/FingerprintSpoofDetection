import tkinter as tk

def on_run_button_click():
    print("Run button clicked!")  
    label.config(text="Run button clicked!")  

def main():
    #
    root = tk.Tk()
    root.title("FingerprintSpoofDetection")  
    
    root.geometry("600x400")

    
    title_label = tk.Label(root, text="Welcome to FingerprintSpoofDetection", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=20)

    
    global label  
    label = tk.Label(root, text="Hello!", font=("Helvetica", 16))
    label.pack(pady=20)

    
    run_button = tk.Button(root, text="Run", font=("Helvetica", 14), command=on_run_button_click)
    run_button.pack(pady=10)

    
    root.mainloop()

if __name__ == "__main__":
    main()
