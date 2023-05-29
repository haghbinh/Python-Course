from tkinter import Tk, Label, Entry, Listbox, Scrollbar, Button, StringVar
from backend import ContactManager
from tkinter import messagebox

class PhonebookApp:
    def __init__(self, db_file):
        self.contact_manager = ContactManager(db_file)

        self.root = Tk()
        self.root.title("Phonebook")
        self.root.geometry("400x200")

        self.create_labels()
        self.create_entries()
        self.create_listbox()
        self.create_buttons()

    def create_labels(self):
        labels = ['نام', 'نام خانوادگی', 'شماره تلفن', 'شماره موبایل']
        for i, label_text in enumerate(labels):
            Label(self.root, text=label_text).grid(row=i*2, column=0)

    def create_entries(self):
        self.name_text = StringVar()
        Entry(self.root, textvariable=self.name_text).grid(row=0, column=1, columnspan=3)

        self.family_text = StringVar()
        Entry(self.root, textvariable=self.family_text).grid(row=2, column=1, columnspan=3)

        self.phone_text = StringVar()
        Entry(self.root, textvariable=self.phone_text).grid(row=4, column=1, columnspan=3)

        self.mobile_text = StringVar()
        Entry(self.root, textvariable=self.mobile_text).grid(row=6, column=1, columnspan=3)

    def create_listbox(self):
        self.list1 = Listbox(self.root, width=40, height=6)
        self.list1.grid(row=8, column=0, rowspan=6, columnspan=12)

        sb1 = Scrollbar(self.root)
        sb1.grid(row=8, column=12)

        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

    def create_buttons(self):
        Button(self.root, text="Insert", width=10, command=self.insert_command).grid(row=0, column=12)
        Button(self.root, text="View All", width=10, command=self.view_command).grid(row=2, column=12)
        Button(self.root, text="Search", width=10, command=self.search_command).grid(row=4, column=12)
        Button(self.root, text="Delete", width=10, command=self.delete_command).grid(row=6, column=12)
        Button(self.root, text="Close", width=10, command=self.root.quit).grid(row=8, column=12)

    def view_command(self):
        self.list1.delete(0, 'end')
        contacts = self.contact_manager.view()
        for contact in contacts:
            self.list1.insert('end', contact)

    def search_command(self):
        self.list1.delete(0, 'end')
        contacts = self.contact_manager.search(
            self.name_text.get(),
            self.family_text.get(),
            self.phone_text.get(),
            self.mobile_text.get()
        )
        for contact in contacts:
            self.list1.insert('end', contact)

    def insert_command(self):
        name = self.name_text.get()
        family = self.family_text.get()
        phone = self.phone_text.get()
        mobile = self.mobile_text.get()

        if not name or not family:
            messagebox.showerror("Error", "Name and family fields are required.")
            return

        if self.contact_manager.insert(name, family, phone, mobile):
            messagebox.showinfo("Success", "Data inserted successfully.")
            self.view_command()
        else:
            messagebox.showerror("Error", "Failed to insert contact.")

    def delete_command(self):
        selected_indices = self.list1.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No contact selected.")
            return

        selected_index = selected_indices[0]
        selected_contact = self.list1.get(selected_index)
        contact_id = selected_contact[0]

        if self.contact_manager.delete(contact_id):
            messagebox.showinfo("Success", "Contact deleted successfully.")
            self.view_command()
        else:
            messagebox.showerror("Error", "Failed to delete contact.")

    def run(self):
        self.root.mainloop()

