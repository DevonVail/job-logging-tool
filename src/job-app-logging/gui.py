import tkinter as tk
from tkinter import ttk
import keyring
import json
from dataclasses import dataclass, asdict
from mysql_db_manager import MySQLDatabaseManager

@dataclass
class GUIData:
    url: str
    title: str
    company: str
    location: str
    salary: float
    salary_type: str
    job_type: str

    def to_dict(self):
        return asdict(self)

@dataclass
class MySQLConf:
    host: str='localhost'
    user: str='root'
    password: str=''
    db_name: str='mydatabase'

    def to_json(self):
        data_dict = asdict(self)
        data_json = json.dumps(data_dict, indent=4)
        return data_json


class ApplicationLoggingGUI(ttk.Entry):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize tk root
        self.root = root

        # Get window geometry. Not sure how this works in multiple monitor scenarios so I converted it to a list if it's not already a list
        self.screen_width = [self.root.winfo_screenwidth()] if not isinstance(self.root.winfo_screenwidth(), list) else self.root.winfo_screenwidth()
        self.screen_height = [self.root.winfo_screenheight()] if not isinstance(self.root.winfo_screenheight(), list) else self.root.winfo_screenheight()
        
        # Create instance of MySQLCong dataclass
        self.save_decision = 1

        # Check to see if MySQL conf has been previously saved
        self.SERVICE_NAME = "job_application_logging_my_sql_loging"
        self.KEYRING_USERNAME = "root"

        # Store the retrieved login data, if found
        retrieved_login_info = keyring.get_password(service_name=self.SERVICE_NAME, username=self.KEYRING_USERNAME)
        if retrieved_login_info:
            config_dict = json.loads(retrieved_login_info)
            self.mysql_conf = self.mysql_conf = MySQLConf(**config_dict)
        # If no login data is found, use the default data from the dataclass
        else:
            self.mysql_conf = MySQLConf()

        # Create instance of GUIData dataclass
        self.gui_data = GUIData

        #### Create cut, copy, and paste menu for GUI ###
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Cut", command=self.popup_cut)
        self.menu.add_command(label="Copy", command=self.popup_copy)
        self.menu.add_separator()
        self.menu.add_command(label="Paste", command=self.popup_paste)
        # Bind the right-click event (Button-3) to the display_popup method
        self.bind("<Button-3>", self.display_popup)

    # The following 4 functions define the Cut, Copy, Paste menu for the windows

    def display_popup(self, event):
        """ Displays the popup menu at the mouse cursor's position. """
        try:
            # Post the menu at the absolute screen coordinates of the mouse click
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            # Release the grab on the menu
            self.menu.grab_release()

    def popup_copy(self):
        """ Generates the standard Tkinter copy event. """
        self.focus_get().event_generate("<<Copy>>")

    def popup_cut(self):
        """ Generates the standard Tkinter cut event. """
        self.focus_get().event_generate("<<Cut>>")

    def popup_paste(self):
        """ Generates the standard Tkinter paste event. """
        self.focus_get().event_generate("<<Paste>>")

    # 
    def get_login_input(self):
        """
        Once the login data is submitted, retrieve it here, hide the login window, and open the logging window 
        """
        self.mysql_conf.host = self.mysql_host_entry.get()
        self.mysql_conf.user = self.mysql_user_entry.get()
        self.mysql_conf.password = self.mysql_password_entry.get()
        self.mysql_conf.db_name = self.mysql_db_name_entry.get()

        if self.save_decision:
            config_json_str = self.mysql_conf.to_json()
            keyring.set_password(self.SERVICE_NAME, self.KEYRING_USERNAME, config_json_str)
        else:
            try:
                keyring.delete_password(self.SERVICE_NAME, self.KEYRING_USERNAME)
            except keyring.errors.PasswordDeleteError:
                pass

        self.root.withdraw()
        self.logging_gui()

    def save_login_yes_no(self):
        self.save_decision = self.yes_no_int_var.get()

    def log_input(self):
        """Retrieves the text from the entry field and displays it in the label."""
        self.gui_data.url = self.job_url_entry.get()
        self.gui_data.title = self.job_title_entry.get()
        self.gui_data.company = self.job_company_entry.get()
        self.gui_data.location = self.job_location_entry.get()
        self.gui_data.salary = self.job_salary_entry.get()

    def update_mysql_table(self):
        table_input = {'URL': self.gui_data.url, 'Title': self.gui_data.title, 'Company': self.gui_data.company,
                        'Location': self.gui_data.location, 'Salary': self.gui_data.salary, 'Salary_Type': self.gui_data.salary_type,
                        'Job_Type': self.gui_data.job_type}
        self.mysql_db_manager.update_table(table_input=table_input)

    def get_salary_type(self):
        """Prints the currently selected value to the console."""
        if self.salary_type_var.get() == 0:
            self.gui_data.salary_type = "Hourly"
        else:
            self.gui_data.salary_type = "Yearly"

    def get_job_type(self):
        """Prints the currently selected value to the console."""
        if self.job_type_var.get() == 0:
            self.gui_data.job_type = "Engineering"
        else:
            self.gui_data.job_type = "Education"

    def setup_gui(self):
        # Create main window
        self.root.title("MySQL Setup")
        self.root.geometry(f"{450}x{200}+{int((self.screen_width[0]/2)-225)}+{int((self.screen_height[0]/2)-100)}") # Set the initial size of the window

        # Create an Entry field for MySQL host
        self.mysql_host_default_val = tk.StringVar(value=self.mysql_conf.host)
        host_label = ttk.Label(self.root, text="MySQL Host:", font=("Helvetica", 10, "bold"))
        host_label.grid(row=0, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.mysql_host_entry = ApplicationLoggingGUI(self.root, textvariable=self.mysql_host_default_val, width=35)
        self.mysql_host_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # Create an Entry field for MySQL user
        self.mysql_user_default_val = tk.StringVar(value=self.mysql_conf.user)
        user_label = ttk.Label(self.root, text="MySQL User:", font=("Helvetica", 10, "bold"))
        user_label.grid(row=1, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.mysql_user_entry = ApplicationLoggingGUI(self.root, textvariable=self.mysql_user_default_val, width=35)
        self.mysql_user_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))

        # Create an Entry field for MySQL password
        self.mysql_password_default_val = tk.StringVar(value=self.mysql_conf.password)
        password_label = ttk.Label(self.root, text="MySQL Password:", font=("Helvetica", 10, "bold"))
        password_label.grid(row=2, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.mysql_password_entry = ApplicationLoggingGUI(self.root, show='*', textvariable=self.mysql_password_default_val, width=35)
        self.mysql_password_entry.grid(row=2, column=1, sticky="ew", pady=(0, 5))

        # Create an Entry field for MySQL database name
        self.mysql_db_name_default_val = tk.StringVar(value=self.mysql_conf.db_name)
        db_name_label = ttk.Label(self.root, text="MySQL Database Name:", font=("Helvetica", 10, "bold"))
        db_name_label.grid(row=3, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.mysql_db_name_entry = ApplicationLoggingGUI(self.root, textvariable=self.mysql_db_name_default_val, width=35)
        self.mysql_db_name_entry.grid(row=3, column=1, sticky="ew", pady=(0, 5))

        # Create a label to provide instructions
        self.yes_no_int_var = tk.IntVar()
        self.yes_no_int_var.set(1)
        save_login_label = ttk.Label(self.root, text="Save MySQL Login Information:", font=("Helvetica", 10, "bold"))
        save_login_label.grid(row=4, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        yes_bttn = ttk.Radiobutton(
                self.root,
                text='Yes',
                variable=self.yes_no_int_var,  # Link to the shared variable
                command=self.save_login_yes_no, # Function to call when clicked
                value=1    # Unique value for this button
            )
        yes_bttn.grid(row=4, column=1, sticky="ew", pady=(0, 5))

        no_bttn = ttk.Radiobutton(
                self.root,
                text='No',
                variable=self.yes_no_int_var,  # Link to the shared variable
                command=self.save_login_yes_no, # Function to call when clicked
                value=0    # Unique value for this button
            )
        no_bttn.grid(row=5, column=1, sticky="ew", pady=(0, 5))

        submit_btn = ttk.Button(self.root, text="Submit", command=self.get_login_input)
        submit_btn.grid(row=6, column=0, columnspan=2, sticky="ew", padx=(10, 0), pady=(10, 5))
        
    def logging_gui(self):
        
        self.mysql_db_manager = MySQLDatabaseManager(self.mysql_conf)

        # Create the main window
        self.logging_window = tk.Toplevel(self.root)
        self.logging_window.title("Job Application Logging")
        self.logging_window.geometry(f"{int(self.screen_width[0]/2)}x{int(self.screen_height[0] - 80)}+{int(self.screen_width[0]/2)}+0") # Set the initial size of the window

        # Add a row counter to allow for a dynamic number of rows
        row_num = 0

        # Create an Entry field for user input
        job_url_label = ttk.Label(self.logging_window, text="Enter job posting URL:", font=("Helvetica", 10, "bold"))
        job_url_label.grid(row=row_num, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.job_url_entry = ttk.Entry(self.logging_window, width=180)
        self.job_url_entry.grid(row=row_num, column=1, sticky="ew", pady=(0, 5))
        row_num += 1

        # Create an Entry field for job title
        job_title_label = ttk.Label(self.logging_window, text="Enter job title:", font=("Helvetica", 10, "bold"))
        job_title_label.grid(row=row_num, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.job_title_entry = ttk.Entry(self.logging_window, width=180)
        self.job_title_entry.grid(row=row_num, column=1, sticky="ew", pady=(0, 5))
        row_num += 1

        # Create an Entry field for company
        job_title_label = ttk.Label(self.logging_window, text="Enter company job is at:", font=("Helvetica", 10, "bold"))
        job_title_label.grid(row=row_num, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.job_company_entry = ttk.Entry(self.logging_window, width=180)
        self.job_company_entry.grid(row=row_num, column=1, sticky="ew", pady=(0, 5))
        row_num += 1

        # Create an Entry field for company
        job_location_label = ttk.Label(self.logging_window, text="Enter job location:", font=("Helvetica", 10, "bold"))
        job_location_label.grid(row=row_num, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.job_location_entry = ttk.Entry(self.logging_window, width=180)
        self.job_location_entry.grid(row=row_num, column=1, sticky="ew", pady=(0, 5))
        row_num += 1

        # Create an Entry field for job salary
        job_salary_label = ttk.Label(self.logging_window, text="Enter job salary:", font=("Helvetica", 10, "bold"))
        job_salary_label.grid(row=row_num, column=0, sticky="ew", padx=(10, 2), pady=(0, 5))
        self.job_salary_entry = ttk.Entry(self.logging_window, width=180)
        self.job_salary_entry.grid(row=row_num, column=1, sticky="ew", pady=(0, 5))
        row_num += 1

        # Create a Tkinter variable to track the selection
        self.salary_type_var = tk.IntVar()
        self.salary_type_var.set(0)

        # Create a label to provide instructions
        label = tk.Label(self.logging_window, text="Salary type:", justify=tk.LEFT, padx=35, font=("Helvetica", 10, "bold"))
        label.grid(row=row_num, column=0, sticky="ew", pady=(0, 5))
        
        # Define the options as a list of tuples (label text, value)
        salary_types = [
            ("Hourly", 0),
            ("Yearly", 1)
        ]

        # Create Radiobutton widgets using a loop
        for text, val in salary_types:
            tk.Radiobutton(
                self.logging_window,
                text=text,
                variable=self.salary_type_var,  # Link to the shared variable
                command=self.get_salary_type, # Function to call when clicked
                value=val    # Unique value for this button
            ).grid(row=row_num, column=1, sticky='w', pady=(0, 1))
            row_num += 1

        #  Create a label to provide instructions
        label = tk.Label(self.logging_window, text="Type of job:", justify=tk.LEFT, padx=35, font=("Helvetica", 10, "bold"))
        label.grid(sticky='w') # Anchor westward for left alignment

        # Define the options as a list of tuples (label text, value)
        job_types = [
            ("Engineering", 0),
            ("Education", 1)
        ]

        self.job_type_var = tk.IntVar()
        self.job_type_var.set(0)
        
        # Create Radiobutton widgets using a loop
        for text, val in job_types:
            tk.Radiobutton(
                self.logging_window,
                text=text,
                variable=self.job_type_var,  # Link to the shared variable
                command=self.get_job_type, # Function to call when clicked
                value=val    # Unique value for this button
            ).grid(row=row_num, column=1, sticky="w", pady=(0, 1))
            row_num += 1

        # Create a Button to trigger the action
        submit_btn = ttk.Button(self.logging_window, text="Submit", command=self.log_input)
        submit_btn.grid(row=row_num, column=0, columnspan=2, sticky="ew", padx=(10, 0), pady=(10, 5))

        # Bind the window close event (WM_DELETE_WINDOW protocol) to the on_closing function
        self.logging_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    ApplicationLoggingGUI(root=root).setup_gui()
    root.mainloop()
    
    
