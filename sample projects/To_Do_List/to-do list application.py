import tkinter as tk

# Create the main application window
app = tk.Tk()
app.title("To-Do List")

tasks = []
def read_tasks():
    with open('tasks.txt',"r") as file:
        x = file.readlines()
        for i in x:
            tasks.append(i.strip())
# Create a list to store tasks
read_tasks()

# Function to add a task
def add_task():
    task = entry.get()
    if task:
        tasks.append(task)
        update_task_list()
        entry.delete(0, tk.END) #entry.set("")

# Function to update the task list
def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task)

# Function to remove a task
def remove_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        update_task_list()

# Create and configure widgets
frame = tk.Frame(app)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter Task:")
label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, width=30)
entry.grid(row=0, column=1, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=2, padx=5)

remove_button = tk.Button(frame, text="Remove Task", command=remove_task)
remove_button.grid(row=0, column=3, padx=5)

task_list = tk.Listbox(app, selectmode=tk.SINGLE, width=40)
task_list.pack(padx=10, pady=5)

# Start the main event loop
app.mainloop()
