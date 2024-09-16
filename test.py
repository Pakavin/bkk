import customtkinter as ctk

def main():
    # Create the main application window
    app = ctk.CTk()
    app.title("CustomTkinter Example")
    app.geometry("400x300")  # Width x Height

    # Create a label
    label = ctk.CTkLabel(app, text="Hello, CustomTkinter!", font=("Arial", 24))
    label.pack(pady=20)

    # Create a button
    button = ctk.CTkButton(app, text="Click Me", command=lambda: label.configure(text="Button Clicked!"))
    button.pack(pady=20)

    # Run the application
    app.mainloop()

if __name__ == "__main__":
    main()