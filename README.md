# python-contact-manager
An contact manager written in python with the help of Google Gemini AI. 

!(img/python-contact-manager-main-window.png) 
!(img/python-contact-manager-file-menu.png) 
!(img/python-contact-manager-about-window.png)

### Dependencies 
 - The only library that you need to install is Pillow.
 - Run `pip install pillow` or use your IDE's package manager. 

# Here's a summary of the process and prompts used during this chat to create the contact manager app:

Initial Goal: Create a basic contact management application using Tkinter (for the GUI) and SQLite (for data storage).

# Phase 1: Basic Structure and Database
 - Prompt 1: Initial request to create a contact management application.
 - Process: Created the basic Tkinter window structure, defined functions for database operations (create table, add contact), and set up basic input fields.
 - Key Features: Basic GUI layout, SQLite database creation, adding contacts to the database.

# Phase 2: Listbox and Viewing Contacts
 - Prompt 2: Add a listbox to display contacts.
 - Prompt 3: Add the ability to view contact details by double-clicking on the listbox entries.
 - Process: Implemented the listbox to display contact names, implemented the double-click functionality to populate the input fields with the selected contact's details.
 - Key Features: Listbox display, double-click to view contact details.

# Phase 3: Deleting Contacts and Menu Bar
 - Prompt 4: Add a "Delete Contact" button.
 - Prompt 5: Add a menu bar with "File" (Exit) and "Help" (About) menus.
 - Process: Implemented the delete functionality, added a confirmation dialog, and created the menu bar structure.
 - Key Features: Contact deletion, menu bar with "Exit" and "About" options.

# Phase 4: Enhancements and Refinements
 - Prompt 6: Show the total number of contacts.
 - Process: Added a label to display the total contact count and updated it dynamically.
 - Key Features: Total contact count display.

# Phase 5: Delete by Selection and Layout Improvements
 - Prompt 7: Add the ability to delete a contact by highlighting the contact in the list.
 - Process: Modified the delete function to work directly with the listbox selection, eliminating the need for a global selected ID.
 - Prompt 8-12: Multiple prompts to adjust the layout of buttons (Clear Form, View Contact, Delete Contact).
 - Process: Adjusted the grid layout of the buttons to achieve the desired arrangement.
 - Key Features: Delete by selection from the listbox, improved button layout.

# Phase 6: JSON Import/Export
 - Prompt 13: Add an option to export all contacts to a JSON file.
 - Prompt 14: Add an option to import contacts from a JSON file.
 - Process: Implemented functions for exporting and importing contacts in JSON format, including error handling and file dialogs.
 - Key Features: JSON export and import functionality.

# Phase 7: Database Location and Size, About Page Enhancements
 - Prompt 15: Add an option to open the location of the database file.
 - Process: Implemented a cross-platform function to open the database file's directory.
 - Prompt 16: Show the location and size of the database file on the "About" page.
 - Prompt 17: Add the total number of contacts to the about page.
 - Prompt 18: Make the website on the about page a clickable link.
 - Prompt 19: Add an image to the about page.
 - Process: Enhanced the "About" window to display the database path, size, and contact count, and added a clickable link and image.
 - Key Features: Database location display, database size display, total contact count on the "About" page, clickable link, image on about page.

# Key Challenges and Solutions:
 - Code Truncation: Faced repeated issues with code being truncated in the chat. Solved by providing the code in smaller, numbered parts to be assembled and also by providing a complete version at the end.
 - Tkinter Layout: Required multiple iterations and prompts to achieve the desired layout of buttons and other GUI elements.
 - Error Handling: Added robust error handling throughout the application, especially for database operations and file I/O.
 - Clickable Link in Tkinter: Learned that standard message boxes don't support HTML/Markdown and implemented a custom window with a clickable label.

This summarizes the iterative process of building the contact manager. The key was the step-by-step approach, adding features incrementally and refining the code based on the prompts and feedback.

