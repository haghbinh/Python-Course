import tkinter as tk
from tkinter import messagebox

# Dictionary to store usernames and passwords
user_credentials = {}

# Function to read user credentials from a file
def read_credentials():
    try:
        with open('user_credentials.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                user_credentials[username] = password
    except FileNotFoundError:
        # Handle the case where the file does not exist
        pass

    
# Function to save user credentials to a file
def save_credentials():
    with open('user_credentials.txt', 'w') as file:
        for username, password in user_credentials.items():
            file.write(f"{username}:{password}\n")

# Function to register a new user
def register_user():
    # Get username and password from the registration window input fields
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    # Check if the username is already registered
    if new_username in user_credentials:
        messagebox.showerror("Registration Error", "Username already exists. Please choose another.")
    else:
        # Register the new username and password
        user_credentials[new_username] = new_password
        save_credentials()  # Save the updated credentials to the file
        messagebox.showinfo("Registration Success", "Registration successful! You can now log in.")
        # Close the registration window
        registration_window.destroy()

def open_registration_window():
    global registration_window
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    # Create and place widgets for the registration window
    new_username_label = tk.Label(registration_window, text="New Username:")
    new_username_label.pack()

    global new_username_entry
    new_username_entry = tk.Entry(registration_window)
    registration_window.geometry('300x150')
    new_username_entry.pack()

    new_password_label = tk.Label(registration_window, text="New Password:")
    new_password_label.pack()

    global new_password_entry
    new_password_entry = tk.Entry(registration_window, show="*")
    new_password_entry.pack()

    register_button = tk.Button(registration_window, text="Register", command=register_user)
    register_button.pack()

# Function to handle login
def login():
    # Get username and password from the input fields
    username = username_entry.get()
    password = password_entry.get()

    # Check if the entered username exists in the dictionary
    if username in user_credentials:
        # Check if the entered password matches the stored password
        if user_credentials[username] == password:
            result_label.config(text="Login successful!", fg="green")
        else:
            result_label.config(text="Incorrect password. Please try again.", fg="red")
    else:
        result_label.config(text="Username not found. Please try again.", fg="red")

def exit_program():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Read user credentials from the file when the program starts
read_credentials()

# Create the main window
root = tk.Tk()
root.geometry("300x200")
root.title("Simple Login and Registration System")

# Create and place widgets for the main window
username_label = tk.Label(root, text="Username:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")  # Use '*' to hide the password
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

register_button = tk.Button(root, text="Register", command=open_registration_window)
register_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

result_label = tk.Label(root, text="", fg="green")
result_label.pack()

# Run the Tkinter main loop
root.mainloop()
