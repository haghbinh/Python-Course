import tkinter as tk
import tkinter.messagebox as messagebox
import random

# Define dictionaries to store different flashcard sets.
flashcard_sets = {
    "Chemistry": {
        "What is the chemical symbol for water?": "H2O",
        "What is the atomic number of hydrogen?": "1",
    },
    "English Vocabulary": {
        "What is the opposite of 'happy'?": "Sad",
        "Give the synonym for 'exciting'": "Thrilling",
    }
}

# Function to open the flashcard quiz window.
def open_flashcard_quiz(selected_set):
    flashcard_set = flashcard_sets[selected_set]
    
    quiz_window = tk.Toplevel(root)
    quiz_window.title(f"{selected_set} Flashcard Quiz")
    quiz_window.geometry("400x200")  # Set the window size

    def start_quiz():
        def check_answer():
            user_input = entry.get().strip()
            question, answer = random.choice(list(flashcard_set.items()))

            if user_input.lower() == "exit":
                quiz_window.withdraw()  # Hide the quiz window
                return
            elif user_input.lower() == answer.lower():
                result = "Correct! Well done."
            else:
                result = f"Sorry, the correct answer is: {answer}"
            
            entry.delete(0, tk.END)
            messagebox.showinfo("Result", result)
            question, answer = random.choice(list(flashcard_set.items()))
            flashcard_text.config(text=question)

        question, answer = random.choice(list(flashcard_set.items()))
        flashcard_text.config(text=question)
        entry = tk.Entry(quiz_window)
        entry.pack()
        check_button = tk.Button(quiz_window, text="Check Answer", command=check_answer)
        check_button.pack()

        cancel_button = tk.Button(quiz_window, text="Cancel", command=quiz_window.withdraw)
        cancel_button.pack()

    flashcard_text = tk.Label(quiz_window, text="")
    flashcard_text.pack()

    start_quiz()

# Function to open the settings window for creating/editing flashcard sets.
def open_settings_window():
    def save_flashcard_set():
        set_name = entry_set_name.get()
        flashcard_sets[set_name] = {}
        settings_window.destroy()

    settings_window = tk.Toplevel(root)
    settings_window.title("Flashcard Settings")
    settings_window.geometry("300x100")  # Set the window size

    label = tk.Label(settings_window, text="Enter the name of the flashcard set:")
    label.pack()

    entry_set_name = tk.Entry(settings_window)
    entry_set_name.pack()

    save_button = tk.Button(settings_window, text="Save", command=save_flashcard_set)
    save_button.pack()

    cancel_button = tk.Button(settings_window, text="Cancel", command=settings_window.withdraw)
    cancel_button.pack()

root = tk.Tk()
root.title("Flashcard Quiz App")

# Create a frame for flashcard set selection using radio buttons.
set_frame = tk.Frame(root)
set_frame.pack()

selected_set = tk.StringVar()
selected_set.set("Chemistry")  # Set the default selection

for set_name in flashcard_sets.keys():
    tk.Radiobutton(set_frame, text=set_name, variable=selected_set, value=set_name).pack()

start_button = tk.Button(root, text="Start Quiz", command=lambda: open_flashcard_quiz(selected_set.get()))
start_button.pack()

settings_button = tk.Button(root, text="Settings", command=open_settings_window)
settings_button.pack()

root.geometry("400x200")  # Set the main window size
root.mainloop()
