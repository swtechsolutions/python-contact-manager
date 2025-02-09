# This app was created with the help of Google Gemini.
# It is packaged used pyinstaller (pip install pyinstaller)
# pyinstaller --onefile --noconsole --add-data "sw_tech_logo.png;." contact_manager.py

import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar, filedialog
import sqlite3
import webbrowser
from PIL import Image, ImageTk
import json
import os
import sys
import platform


def create_table():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            business_name TEXT,
            mailing_address TEXT,
            street_address TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_contact():
    global selected_contact_id
    if not all([first_name_entry.get(), last_name_entry.get(), email_entry.get(), phone_entry.get()]):
        messagebox.showerror("Error", "First Name, Last Name, Email, and Phone are required.")
        return

    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    try:
        if selected_contact_id is not None:
            cursor.execute("UPDATE contacts SET first_name=?, last_name=?, email=?, phone=?, business_name=?, mailing_address=?, street_address=? WHERE id=?",
                           (first_name_entry.get(), last_name_entry.get(), email_entry.get(), phone_entry.get(), business_name_entry.get(), mailing_address_entry.get(), street_address_entry.get(), selected_contact_id))
            message = "Contact updated successfully."
            selected_contact_id = None
        else:
            cursor.execute("INSERT INTO contacts (first_name, last_name, email, phone, business_name, mailing_address, street_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (first_name_entry.get(), last_name_entry.get(), email_entry.get(), phone_entry.get(), business_name_entry.get(), mailing_address_entry.get(), street_address_entry.get()))
            message = "Contact added successfully."
        conn.commit()
        clear_entries()
        populate_listbox()
        messagebox.showinfo("Success", message)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()


def clear_entries():
    for entry in entries:
        entry.delete(0, tk.END)


def populate_listbox():
    contacts_listbox.delete(0, tk.END)
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, first_name, last_name FROM contacts")
        rows = cursor.fetchall()
        for row in rows:
            contacts_listbox.insert(tk.END, f"{row[0]}: {row[1]} {row[2]}")

        cursor.execute("SELECT COUNT(*) FROM contacts")
        count = cursor.fetchone()[0]
        total_contacts_label.config(text=f"Total Contacts: {count}")
    except sqlite3.Error as e:
        print(f"Database error in populate_listbox: {e}")
    finally:
        conn.close()


def view_contact(event=None):
    global selected_contact_id
    if event:
        selection = contacts_listbox.curselection()
    else:
        selection = contacts_listbox.curselection()
    if selection:
        selected_contact = contacts_listbox.get(selection[0])
        selected_contact_id = int(selected_contact.split(":")[0])
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id=?", (selected_contact_id,))
        contact_data = cursor.fetchone()
        conn.close()

        if contact_data:
            clear_entries()
            for i, value in enumerate(contact_data[1:]):
                entries[i].insert(0, value)
    else:
        if not event:
            messagebox.showinfo("Info", "Please select a contact to view.")


def delete_contact():
    selection = contacts_listbox.curselection()
    if selection:
        selected_contact = contacts_listbox.get(selection[0])
        selected_contact_id = int(selected_contact.split(":")[0])

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM contacts WHERE id=?", (selected_contact_id,))
                conn.commit()
                clear_entries()
                populate_listbox()
                messagebox.showinfo("Success", "Contact deleted successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
            finally:
                conn.close()
    else:
        messagebox.showinfo("Info", "Please select a contact to delete.")


def export_to_json():
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Export Contacts to JSON")
        if filename:
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()
            conn.close()

            contacts = []
            for row in rows:
                contact = {
                    "id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "business_name": row[5],
                    "mailing_address": row[6],
                    "street_address": row[7]
                }
                contacts.append(contact)

            with open(filename, 'w') as f:
                json.dump(contacts, f, indent=4)  # Use indent for pretty formatting

            messagebox.showinfo("Export Successful", f"Contacts exported to {os.path.basename(filename)} successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Export Error", f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred during export: {e}")


def import_from_json():
    try:
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Import Contacts from JSON")
        if filename:
            with open(filename, 'r') as f:
                contacts = json.load(f)

            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            try:
                for contact in contacts:
                    try:
                        cursor.execute("INSERT INTO contacts (first_name, last_name, email, phone, business_name, mailing_address, street_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                       (contact['first_name'], contact['last_name'], contact['email'], contact['phone'], contact.get('business_name', ''), contact.get('mailing_address', ''), contact.get('street_address', '')))
                    except KeyError as e:
                        print(f"KeyError in contact: {contact}. Missing key: {e}")
                        continue  # if there is a key error, skip the contact and continue with the next one.
                conn.commit()
                populate_listbox()
                messagebox.showinfo("Import Successful", "Contacts imported successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Import Error", f"Database error: {e}")
                conn.rollback()  # if there is an error during insertion, rollback the changes
            finally:
                conn.close()
    except FileNotFoundError:
        messagebox.showerror("Import Error", "File not found.")
    except json.JSONDecodeError:
        messagebox.showerror("Import Error", "Invalid JSON file.")
    except Exception as e:
        messagebox.showerror("Import Error", f"An error occurred during import: {e}")


def open_database_location():
    try:
        db_path = os.path.abspath('contacts.db')  # gets absolute path to db
        if platform.system() == "Windows":
            os.startfile(os.path.dirname(db_path))  # opens folder in windows
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{os.path.dirname(db_path)}'")
        elif platform.system() == "Linux":
            os.system(f"xdg-open '{os.path.dirname(db_path)}'")
        else:
            messagebox.showinfo("Info", "Opening database location is not supported on this operating system.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open database location: {e}")


def create_menu_bar():
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open DB Folder", command=open_database_location)  # Add Open Database Location
    file_menu.add_command(label="Export (JSON)", command=export_to_json)  # added export to json
    file_menu.add_command(label="Import (JSON)", command=import_from_json)  # Add Import from JSON
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)


def show_about():
    about_window = tk.Toplevel(window)
    about_window.title("About")

    try:

        if getattr(sys, 'frozen', False):
            # we are running in a |PyInstaller| bundle
            basedir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            basedir = os.path.dirname(os.path.abspath(__file__))

        # Load the image
        image_path = os.path.join(basedir, "sw_tech_logo.png")
        about_image = Image.open(image_path)  # Replace with your image file
        about_photo = ImageTk.PhotoImage(about_image)

        image_label = ttk.Label(about_window, image=about_photo)
        image_label.image = about_photo  # Keep a reference
        image_label.pack(pady=(10, 0))

    except FileNotFoundError:
        print("Error: sw_tech_logo.png not found. Using text instead.")
        pass # Handle the case where the image file is not found

    about_label = ttk.Label(
        about_window,
        text="Created using",
        wraplength=300
    )

    link_label = ttk.Label(
        about_window,
        text="Southwest Tech Solutions",
        cursor="hand2",
        foreground="blue"
    )

    link_label.pack(padx=10, pady=(0, 0))
    link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://swtechsolutions.ca"))

    about_label.pack(padx=0, pady=(0, 0))

    gemini_label = ttk.Label(
        about_window,
        text="Google Gemini",
        cursor="hand2",
        foreground="blue"
    )
    gemini_label.pack(padx=10, pady=(0, 10))
    gemini_label.bind("<Button-2>", lambda e: webbrowser.open_new("https://gemini.google.com/"))

    try:
        db_path = os.path.abspath('contacts.db')
        file_size = os.path.getsize(db_path)
        file_size_kb = file_size / 1024
        file_size_str = f"{file_size_kb:.2f} KB"

        db_location_label = ttk.Label(about_window, text=f"DB Location: {db_path}")
        db_location_label.pack(padx=10, pady=(10, 0))

        db_size_label = ttk.Label(about_window, text=f"DB Size: {file_size_str}")
        db_size_label.pack(padx=10, pady=(0, 10))
        # Get the contact count
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM contacts")
        contact_count = cursor.fetchone()[0]
        conn.close()

        contact_count_label = ttk.Label(about_window, text=f"Total Contacts: {contact_count}")
        contact_count_label.pack(padx=10, pady=(0, 10))

    except FileNotFoundError:
        db_location_label = ttk.Label(about_window, text="Database file not found.")
        db_location_label.pack(padx=10, pady=(10, 0))
    except OSError as e:
        db_location_label = ttk.Label(about_window, text=f"Error getting database info: {e}")
        db_location_label.pack(padx=10, pady=(10, 0))
    except sqlite3.Error as e:
        contact_count_label = ttk.Label(about_window, text=f"Error getting contact count: {e}")
        contact_count_label.pack(padx=10, pady=(0, 10))


selected_contact_id = None
create_table()

window = tk.Tk()
create_menu_bar()
window.title("Contact Manager")

labels = ["First Name:", "Last Name:", "Email:", "Phone:", "Business Name:", "Mailing Address:", "Street Address:"]
entries = []

for i, label_text in enumerate(labels):
    label = ttk.Label(window, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
    entry = ttk.Entry(window)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
    entries.append(entry)

first_name_entry, last_name_entry, email_entry, phone_entry, business_name_entry, mailing_address_entry, street_address_entry = entries

add_button = ttk.Button(window, text="Add/Update Contact", command=add_contact)
add_button.grid(row=len(labels), column=0, padx=5, pady=10)

clear_button = ttk.Button(window, text="Clear Form", command=clear_entries)
clear_button.grid(row=len(labels), column=1, padx=5, pady=10)

total_contacts_label = ttk.Label(window, text="Total Contacts: 0")
total_contacts_label.grid(row=len(labels) + 2, column=0, sticky=tk.SW, padx=5, pady=5)

contacts_frame = ttk.LabelFrame(window, text="Contacts")
contacts_frame.grid(row=0, column=2, rowspan=len(labels) + 1, padx=10, pady=5, sticky=tk.NSEW)

contacts_listbox = Listbox(contacts_frame, width=30)
contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(contacts_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

contacts_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=contacts_listbox.yview)

contacts_listbox.bind("<Double-Button-1>", view_contact)

view_button = ttk.Button(window, text="View Contact", command=view_contact)
view_button.grid(row=len(labels) + 1, column=2, padx=10, pady=5)

delete_button = ttk.Button(window, text="Delete Contact", command=delete_contact)
delete_button.grid(row=len(labels) + 2, column=2, padx=10, pady=5)  # Below view button

window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(len(labels)+2, weight=0)  # Prevent total contacts label row from expanding

populate_listbox()

window.mainloop()
