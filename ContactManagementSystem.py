import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFormLayout, QDialog, QDialogButtonBox
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
import json
import os


class AddressBook:
    def __init__(self, filename='contacts.json'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)
        with open(self.filename, 'r') as file:
            self._contacts = json.load(file)

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self._contacts, file)


    def add(self, name, phone, email):
        name = name.lower()
        if name not in self._contacts:
            self._contacts[name] = {
                'name': name,
                'phone': phone,
                'email': email,
            }
            self.save_contacts()
            return True
        else:
            return False

    def view(self, name):
        name = name.lower()
        return self._contacts.get(name, None)

    def edit(self, name, phone, email):
        name = name.lower()
        if name in self._contacts:
            self._contacts[name] = {
                'name': name,
                'phone': phone,
                'email': email,
            }
            self.save_contacts()
            return True
        else:
            return False

    def delete(self, name):
        name = name.lower()
        if name in self._contacts:
            del self._contacts[name]
            self.save_contacts()
            return True
        else:
            return False


class ContactDialog(QDialog):
    def __init__(self, parent=None, name='', phone='', email=''):
        super().__init__(parent)

        self.setWindowTitle("Contact Details")

        self.layout = QFormLayout(self)

        self.name_entry = QLineEdit()
        self.name_entry.setText(name)
        self.layout.addRow(QLabel("Name"), self.name_entry)

        self.phone_entry = QLineEdit()
        self.phone_entry.setText(phone)
        self.layout.addRow(QLabel("Phone"), self.phone_entry)

        self.email_entry = QLineEdit()
        self.email_entry.setText(email)
        self.layout.addRow(QLabel("Email"), self.email_entry)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)

    def get_values(self):
        return self.name_entry.text(), self.phone_entry.text(), self.email_entry.text()


class MainWindow(QMainWindow):
    def __init__(self, address_book):
        super().__init__()

        self.address_book = address_book

        self.setWindowTitle("Stylish Contact Manager")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(200, 200, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #444444;
                color: #BBBBBB;
                font-family: 'Verdana';
            }
            QLabel {
                font-size: 20px;
            }
            QLineEdit {
                background-color: #333333;
                color: #BBBBBB;
                border: 2px solid #BBBBBB;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton {
                background-color: #DD5555;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #EE6666;
            }
            QPushButton:pressed {
                background-color: #CC4444;
            }
        """)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.name_entry = QLineEdit()
        self.layout.addWidget(QLabel("Name"))
        self.layout.addWidget(self.name_entry)

        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.add_contact)
        self.layout.addWidget(self.add_button)

        self.view_button = QPushButton("View Contact")
        self.view_button.clicked.connect(self.view_contact)
        self.layout.addWidget(self.view_button)

        self.edit_button = QPushButton("Edit Contact")
        self.edit_button.clicked.connect(self.edit_contact)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Contact")
        self.delete_button.clicked.connect(self.delete_contact)
        self.layout.addWidget(self.delete_button)

    def add_contact(self):
        dialog = ContactDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            name, phone, email = dialog.get_values()
            if self.address_book.add(name, phone, email):
                QMessageBox.information(self, "Success", f"Contact {name} added successfully")
            else:
                QMessageBox.warning(self, "Error", f"Contact {name} already exists")

    def view_contact(self):
        name = self.name_entry.text()
        contact = self.address_book.view(name)

        if contact:
            dialog = ContactDialog(self, contact['name'], contact['phone'], contact['email'])
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", f"No contact named {name}")

    def edit_contact(self):
        name = self.name_entry.text()
        contact = self.address_book.view(name)

        if contact:
            dialog = ContactDialog(self, contact['name'], contact['phone'], contact['email'])
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                name, phone, email = dialog.get_values()
                if self.address_book.edit(name, phone, email):
                    QMessageBox.information(self, "Success", f"Contact {name} edited successfully")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to edit contact {name}")
        else:
            QMessageBox.warning(self, "Error", f"No contact named {name}")

    def delete_contact(self):
        name = self.name_entry.text()
        if self.address_book.delete(name):
            QMessageBox.information(self, "Success", f"Contact {name} deleted successfully")
        else:
            QMessageBox.warning(self, "Error", f"No contact named {name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    address_book = AddressBook()
    window = MainWindow(address_book)
    window.show()
    sys.exit(app.exec())
