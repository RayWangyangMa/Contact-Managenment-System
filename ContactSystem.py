import tkinter as tk
from tkinter import messagebox
import json
import os


class Contact:
    def __init__(self, name, phone, email, group):
        self.name = name.lower()
        self.phone = phone
        self.email = email
        self.group = group


class AddressBook:
    def __init__(self, filename='contacts.json'):
        # The filename is joined with the directory path of this script
        self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)

        with open(self.filename, 'r') as file:
            self._contacts = json.load(file)

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self._contacts, file)

    def add(self, name, phone, email, group):
        name = name.lower()
        if name not in self._contacts:
            self._contacts[name] = {
                'name': name,
                'phone': phone,
                'email': email,
                'group': group
            }
            self.save_contacts()
            return True
        else:
            return False

    def view(self, name):
        name = name.lower()
        return self._contacts.get(name, None)

    def delete(self, name):
        name = name.lower()
        if name in self._contacts:
            del self._contacts[name]
            self.save_contacts()
            return True
        else:
            return False

    def view_all(self, group=None):
        if group:
            group = group.lower()
            return {k: v for k, v in self._contacts.items() if v['group'] == group}
        else:
            return self._contacts


    def edit(self, name, phone, email, group):
        name = name.lower()
        if name in self._contacts:
            self._contacts[name] = {
                'name': name,
                'phone': phone,
                'email': email,
                'group': group
            }
            self.save_contacts()
            return True
        else:
            return False

    def search(self, term):
        term = term.lower()
        return {k: v for k, v in self._contacts.items() if term in k or term in v['phone'] or term in v['email'] or term in v['group']}

class ViewWindow(tk.Toplevel):
    def __init__(self, master, contacts):
        tk.Toplevel.__init__(self, master)
        self.title("Contact Details")
        self.geometry('500x500')
        self.configure(bg='#fff')
        if contacts:
            for name, contact in contacts.items():
                self.name_label = tk.Label(
                    self, text=f"Name: {contact['name'].title()}", bg='#fff')
                self.name_label.pack(pady=5)

                self.phone_label = tk.Label(
                    self, text=f"Phone: {contact['phone']}", bg='#fff')
                self.phone_label.pack(pady=5)

                self.email_label = tk.Label(
                    self, text=f"Email: {contact['email']}", bg='#fff')
                self.email_label.pack(pady=5)

                self.group_label = tk.Label(
                    self, text=f"Group: {contact['group'].title()}", bg='#fff')
                self.group_label.pack(pady=5)

                self.separator = tk.Label(self, text="", bg='#fff')
                self.separator.pack(pady=5)
        else:
            self.error_label = tk.Label(
                self, text="No contacts found", bg='#fff', fg='red')
            self.error_label.pack(pady=5)


class Application(tk.Tk):
    def __init__(self, address_book):
        tk.Tk.__init__(self)
        self.address_book = address_book
        self.title("Address Book")
        self.geometry('500x500')
        self.configure(bg='#fff')
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(
            self, text="Name (Case Insensitive)", bg='#fff')
        self.name_label.pack(pady=(20, 0))
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(self, text="Phone", bg='#fff')
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack(pady=5)

        self.email_label = tk.Label(self, text="Email", bg='#fff')
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        self.group_label = tk.Label(self, text="Group", bg='#fff')
        self.group_label.pack(pady=5)
        self.group_entry = tk.Entry(self)
        self.group_entry.pack(pady=5)

        self.add_button = tk.Button(
            self, text="Add Contact", command=self.add_contact, bg='#4CAF50', fg='white')
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(
            self, text="View Contact", command=self.view_contact, bg='#2196F3', fg='white')
        self.view_button.pack(pady=5)

        self.edit_button = tk.Button(
            self, text="Edit Contact", command=self.edit_contact, bg='#FFC107', fg='white')
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(
            self, text="Delete Contact", command=self.delete_contact, bg='#f44336', fg='white')
        self.delete_button.pack(pady=5)

        self.search_button = tk.Button(
            self, text="Search Contacts", command=self.search_contacts, bg='#9C27B0', fg='white')
        self.search_button.pack(pady=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        group = self.group_entry.get()
        if self.address_book.add(name, phone, email, group):
            messagebox.showinfo("Success", "Contact added successfully")
        else:
            messagebox.showinfo("Failure", "Contact already exists")

    def view_contact(self):
        name = self.name_entry.get()
        contact = self.address_book.view(name)
        ViewWindow(self, {name: contact})

    def edit_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        group = self.group_entry.get()
        if self.address_book.edit(name, phone, email, group):
            messagebox.showinfo("Success", "Contact edited successfully")
        else:
            messagebox.showinfo("Failure", "Contact does not exist")

    def delete_contact(self):
        name = self.name_entry.get()
        if self.address_book.delete(name):
            messagebox.showinfo("Success", "Contact deleted successfully")
        else:
            messagebox.showinfo("Failure", "Contact does not exist")

    def search_contacts(self):
        term = self.name_entry.get()
        results = self.address_book.search(term)
        ViewWindow(self, results)


if __name__ == "__main__":
    address_book = AddressBook()
    app = Application(address_book)
    app.mainloop()
