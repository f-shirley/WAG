import tkinter as tk
from tkinter import font
from tkinter import messagebox
from threading import Thread


from windows_automation_functions import WindowsAutomationFunctions

class Gui:

    def __init__(self, root, design_parameters):
        self.root = root
        self.design_parameters = design_parameters

        # status variables to control setting button text with current status dynamically
        self.button_tasks_status_dict = {"app_status" : False, "package_status" : False, "processes_status" : False, "activation_status" : False}

        # create main and header fonts using design_parameters
        # creates default if no design_parameters
        if self.design_parameters.font_family_name != None and self.design_parameters.font_size != None:
            self.main_font = font.Font(family=self.design_parameters.font_family_name, size=self.design_parameters.font_size)
            self.header_font = font.Font(
                    family=self.design_parameters.font_family_name, 
                    size=(self.design_parameters.font_size + self.design_parameters.header_font_size_adjuster),
                    weight="bold")
        else:
            self.main_font = font.Font(family="Calibri", size=11)
            self.header_font = font.Font(family="Calibri", size=14, weight="bold")

        # create object holding application logic
        self.app_logic = WindowsAutomationFunctions()

        # configure root to let the functionality containing frames occupy as much space as possible
        # and the info widgets in the header to occupy the appropiate space
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # place menubar
        self.root.config(menu = self.construct_menubar(self.root, self.design_parameters.version))

        # create frame that holds all the functionality frames
        self.frame_for_functionality_frames = tk.Frame(self.root)
        self.frame_for_functionality_frames.grid(row=1, column=0, sticky="nsew")

        # give each column and row in root equal weight
        self.frame_for_functionality_frames.columnconfigure(0, weight=1)
        self.frame_for_functionality_frames.columnconfigure(1, weight=1)
        self.frame_for_functionality_frames.rowconfigure(0, weight=1)
        self.frame_for_functionality_frames.rowconfigure(1, weight=1)

        # call function which constructs the gui
        self.place_all_frames()

        # assign dark color theme as default
        self.change_color_theme(self.root, 'dark')

        if(self.design_parameters.autorun):
            self.autorun_timer()

        # check for installed apps, packages, and running processes on launch:
        self.root.after(1000, self.threading_check_installed_apps)
        self.root.after(1000, self.threading_check_installed_packages)
        self.root.after(1000, self.threading_check_running_processes)
        
    # BEGIN threading logic for button tasks
    def check_thread_process_variable_status(self, status_name, button, default_btn_text="Update"):
        if self.button_tasks_status_dict[status_name] == True:
            self.button_tasks_status_dict[status_name] = False
            button.config(text=default_btn_text, state="normal")
        else:
            self.root.after(1000, self.check_thread_process_variable_status, status_name, button, default_btn_text)

    def threading_check_installed_apps(self):
        thread_action = Thread(target=self.update_app_installstatus_checkmarks)
        self.btn_find_installed_apps.config(text="Processing...", state="disabled")
        thread_action.start()

        # updates button text back to 'Update' after the threaded process finishes
        # the argument is the key for a dictionary (self.button_tasks_status_dict) that holds the status of the threaded process: True or False
        self.check_thread_process_variable_status(status_name="app_status", button=self.btn_find_installed_apps)

    def threading_check_installed_packages(self):
        thread_action = Thread(target=self.update_package_installstatus_checkmarks)
        self.btn_find_installed_programs.config(text="Processing...", state="disabled")
        thread_action.start()

        # updates button text back to 'Update' after the threaded process finishes
        # the argument is the key for a dictionary (self.button_tasks_status_dict) that holds the status of the threaded process: True or False
        self.check_thread_process_variable_status(status_name="package_status", button=self.btn_find_installed_programs)

    def threading_check_running_processes(self):
        thread_action = Thread(target=self.check_running_programs)
        self.btn_check_running_processes.config(text="Processing...", state="disabled")
        thread_action.start()

        # updates button text back to 'Update' after the threaded process finishes
        # the argument is the key for a dictionary (self.button_tasks_status_dict) that holds the status of the threaded process: True or False
        self.check_thread_process_variable_status(status_name="processes_status", button=self.btn_check_running_processes)

    def threading_activate_windows(self, lbl_status, btn_check_and_activate_windows):
        # activate_windows_update_widgets function is nested. Convert to a class method to use threading.
        thread_action = Thread(target=lambda:self.activate_windows_update_widgets(lbl_status, btn_check_and_activate_windows))
        btn_check_and_activate_windows.config(text="Processing...", state="disabled")
        thread_action.start()

        # updates button text back to 'Check and Activate Windows' after the threaded process finishes
        # the argument is the key for a dictionary (self.button_tasks_status_dict) that holds the status of the threaded process: True or False
        self.check_thread_process_variable_status(status_name="activation_status", button=btn_check_and_activate_windows, default_btn_text="Check and Activate Windows")

    # END threading logic for button tasks

    # if autorun is set to True/On, put each desired task to autorun on a thread that executes after a specified interval
    # and call this function after that interval to repeat the process
    # a reference is created for each task to cancel them when the autorun toggle is turned off
    def autorun_timer(self):
        if self.design_parameters.autorun == True:
            self.autorun_app_check_process_reference = self.root.after(self.design_parameters.autorun_interval_time, self.threading_check_installed_apps)
            self.autorun_package_check_process_reference = self.root.after(self.design_parameters.autorun_interval_time, self.threading_check_installed_packages)
            self.autorun_processes_check_process_reference = self.root.after(self.design_parameters.autorun_interval_time, self.threading_check_running_processes)
            self.root.after(self.design_parameters.autorun_interval_time, self.autorun_timer)
        
    # if toggle is off, turn it on
    # if toggle is on, turn it off and cancel existing autorun threads
    def toggle_autorun_timer(self):
        if self.design_parameters.autorun == False:
            self.design_parameters.autorun = True
            self.autorun_timer()
        else:
            self.design_parameters.autorun = False
            self.root.after_cancel(self.autorun_app_check_process_reference)
            self.root.after_cancel(self.autorun_package_check_process_reference)
            self.root.after_cancel(self.autorun_processes_check_process_reference)

    # create application header menubar containing app info and help
    def construct_menubar(self, frame, version):
        activation_status_help_text = "Clicking 'Check and Activate Windows' will Activate Windows\
                                        \nafter checking it's activation status.\
                                        \nIf activation fails, run this program as an Administrator and try again.\
                                        \nIf still unsuccessful, the computer may not have a Windows OEM product key,\
                                        \npossibly due to a hardware change."
        
        process_help_text = "fc-system-service is the process for 'Connect'\
                            \nfc-authentication-agent is the process for 'School Manager - Authentication Agent'"
        
        autorun_interval_in_minutes = (self.design_parameters.autorun_interval_time / 1000) / 60
        autorun_help_text = "This option enables or disables autorunning\
                            \nthe process, app, and programs checks after an\
                            \ninterval of " + str(autorun_interval_in_minutes) + " minutes\
                            \nGreen = enabled\
                            \nRed = disabled"

        def show_activation_help_message():
            messagebox.showinfo("Activation Help", activation_status_help_text)
        
        def show_license_message():
            messagebox.showinfo("LICENSE", self.design_parameters.license)

        def show_processes_help_message():
            messagebox.showinfo("Processes Help", process_help_text)

        def show_autorun_help_message():
            messagebox.showinfo("Autorun Help", autorun_help_text)

        # parent function for toggling autorun on and off
        # and setting the color of the menu option to reflect being on or off
        def autorun_handler():
            self.toggle_autorun_timer()
            if self.design_parameters.autorun == True:
                options.entryconfigure("Autorun Checks for processes and installed programs/apps", background="green")
            else:
                options.entryconfigure("Autorun Checks for processes and installed programs/apps", background="red")

        # create menubar
        menubar = tk.Menu(frame)

        # create menubar item
        about = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about)
        about.add_command(label=version, command=None)
        about.add_command(label="License", command=show_license_message)

        help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help)
        help.add_command(label="Activation Help", command=show_activation_help_message)
        help.add_command(label="Running Processes Help", command=show_processes_help_message)
        help.add_command(label="Autorun Help", command=show_autorun_help_message)

        options = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Dark Theme", command=lambda:self.change_color_theme(self.root, 'dark'))
        options.add_command(label="Light Theme", command=lambda:self.change_color_theme(self.root, 'light'))
        options.add_command(label="Autorun Checks for processes and installed programs/apps", command=autorun_handler)
        # set initial color of autorun toggle menu option based on status
        if self.design_parameters.autorun == True:
            options.entryconfigure("Autorun Checks for processes and installed programs/apps", background="green")
        else:
            options.entryconfigure("Autorun Checks for processes and installed programs/apps", background="red")

        return menubar

    # call each frame's constructing function (which includes widgets) and place them
    def place_all_frames(self):
        # top left
        frame_col0_row0, frame_col0_row0_header, frame_col0_row0_widgets = self.construct_frame_col0_row0()
        frame_col0_row0.grid(column=0, row=0)
        frame_col0_row0_header.grid(column=0, row=0)

        # top right
        frame_col1_row0, frame_col1_row0_header, frame_col1_row0_widgets = self.construct_frame_col1_row0()
        frame_col1_row0.grid(column=1, row=0)
        frame_col1_row0_header.grid(column=0, row=0)

        # middle left
        frame_col0_row1, frame_col0_row1_header, frame_col0_row1_widgets = self.construct_frame_col0_row1()
        frame_col0_row1.grid(column=0, row=1)
        frame_col0_row1_header.grid(column=0, row=0)

        # middle right
        frame_col1_row1, frame_col1_row1_header, frame_col1_row1_widgets = self.construct_frame_col1_row1()
        frame_col1_row1.grid(column=1, row=1)
        frame_col1_row1_header.grid(column=0, row=0)

        # bottom left
        frame_col0_row2, frame_col0_row2_header, frame_col0_row2_widgets = self.construct_frame_col0_row2()
        frame_col0_row2.grid(column=0, row=2)
        frame_col0_row2_header.grid(column=0, row=0)

        # bottom right
        frame_col1_row2, frame_col1_row2_header, frame_col1_row2_widgets = self.construct_frame_col1_row2()
        frame_col1_row2.grid(column=1, row=2)
        frame_col1_row2_header.grid(column=0, row=0)

        # place grid widget frames
        common_styling_widget_frames = [frame_col0_row0_widgets, frame_col1_row0_widgets, frame_col0_row1_widgets, frame_col1_row1_widgets, frame_col0_row2_widgets, frame_col1_row2_widgets]

        for frame in common_styling_widget_frames:
            frame.grid(row=1, column=0, sticky="nsew")
            frame.columnconfigure(0, weight=1)
        
        # add common stylings to frames
        common_styling_frames = [frame_col0_row0, frame_col1_row0, frame_col0_row1, frame_col1_row1, frame_col0_row2, frame_col1_row2]

        for frame in common_styling_frames:
            frame.grid_configure(sticky='nsew', padx=10, pady=10)
            # row and column '0' of the position frames holds the header
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=0)
            # row '1' of the position frames is the frame that contains the widgets
            frame.rowconfigure(1, weight=1)

            frame.config(highlightbackground="black", highlightthickness=1)


    # begin frame and associated widgets constructing functions #
    # each will return it's frame to be used in place_all_frames() function

    def construct_frame_col0_row0(self):
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        # construct widgets
        frame_widgets = self.windowsupdates_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_col1_row0(self):
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        # construct widgets
        frame_widgets = self.diskcleanup_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_col0_row1(self):
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        frame_widgets = self.installedapps_widgets(frame, frame_header, self.design_parameters.needs_installed_apps, self.design_parameters.title3)

        return frame, frame_header, frame_widgets
    
    def construct_frame_col1_row1(self):
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        frame_widgets = self.installedpackages_widgets(frame, frame_header, self.design_parameters.needs_installed_packages, self.design_parameters.title6)

        return frame, frame_header, frame_widgets
    
    def construct_frame_col0_row2(self):
        # fifth frame
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        frame_widgets = self.runningprograms_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_col1_row2(self):
        # sixth frame
        frame = tk.Frame(self.frame_for_functionality_frames)
        frame_header = tk.Frame(frame)

        frame_widgets = self.windowsactivation_status_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    # begin functions containing widget construction based on task/frame
    # parent frames are the arguments

    # attempt installing and/or changing product key
    # returned result is used to display error message or continue the process
    # attempt to activate windows and after a delay, retrieve and display the result
    def activate_windows_update_widgets(self, lbl_status, btn_check_and_activate_windows):

        # list created to be passed by reference to save result from function called from another function
        self.activation_result = []

        # check if Windows is already activated before attempting activation tasks
        # and update widgets upon a positive activation status
        already_activated = self.app_logic.get_windowsactivation_status()
        if already_activated == "License Status: Licensed":
            # update widgets reflecting the activation status
            self.activation_result.append("True")
            lbl_status.config(text="Windows Already Activated", fg="green")
            btn_check_and_activate_windows.config(text="Check and Activate Windows", state="disabled")
            self.button_tasks_status_dict["activation_status"] = True
            return

        # this status is for the installation of the Windows key
        # True upon success, an error message upon failure
        status = self.app_logic.run_activate_windows_script()
        
        if status != True:
            lbl_status.config(text=status, fg="red")
            btn_check_and_activate_windows.config(text="Check and Activate Windows", state="normal")
            return
        else:
            # update widgets reflecting the activation status
            self.activation_result.append("True")
            self.root.after(5000, lambda:update_widgets())

        # helper function called after the time delay needed to check activation status
        def update_widgets():
            if self.activation_result[len(self.activation_result) - 1] == "True":
                # complete success tasks
                lbl_status.config(text="Successfully Activated Windows", fg="green")
                btn_check_and_activate_windows.config(text="Check and Activate Windows", state="disabled")
                self.button_tasks_status_dict["activation_status"] = True
            else:
                lbl_status.config(text=self.activation_result[len(self.activation_result) - 1], fg="red")
                btn_check_and_activate_windows.config(text="Check and Activate Windows", state="normal")
        

    def windowsactivation_status_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title_windowsactivation_status = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title5)
        lbl_title_windowsactivation_status.grid(column=0, row=0, sticky='n')

        # create label which displays the activation status after button press
        lbl_status = tk.Label(frame_widgets, font=self.main_font, text="Not checked")
        lbl_status.grid(column=0, row=1)

        # activation button
        btn_check_and_activate_windows = tk.Button(frame_widgets, font=self.main_font, bg=self.design_parameters.buttons_color, text="Check and Activate Windows")
        btn_check_and_activate_windows.configure(command=lambda:[self.threading_activate_windows(lbl_status, btn_check_and_activate_windows), self.create_timestamp_widget(frame_widgets, 0, 3)])
        btn_check_and_activate_windows.grid(column=0, row=2, pady=5)

        return frame_widgets

    def windowsupdates_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)
        
        # title
        lbl_title_windowsupdate = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title1)
        lbl_title_windowsupdate.grid(column=0, row=0, sticky='n')

        #button
        btn_open_windowsupdate_gui = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Open",
                                               command=lambda:[self.app_logic.open_windowsupdate(), self.create_timestamp_widget(frame_widgets, 0, 2)])
        btn_open_windowsupdate_gui.grid(column=0, row=1, pady=5)

        return frame_widgets

    def diskcleanup_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title_diskcleaner = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title2)
        lbl_title_diskcleaner.grid(column=0, row=0, sticky="n")

        # button
        btn_open_diskcleaner = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Open", 
                                         command=lambda:[self.app_logic.open_diskcleaner(), self.create_timestamp_widget(frame_widgets, 0, 2)])
        btn_open_diskcleaner.grid(column=0, row=1, pady=5)

        return frame_widgets

    # updates list of currently installed programs and updates checkmark status indicators
    # attached on the btn_find_installed_programs button created in installedapps_widgets function
    def update_app_installstatus_checkmarks(self):
        # retrieve status of desired apps, any value other than [0, 0] indicates app is installed
        # ["app name", "AppID"]

        self.design_parameters.installed_apps_name_and_id_list = self.app_logic.find_installed_apps(self.design_parameters.needs_installed_apps,
                                                                                                    self.design_parameters.duplicate_app_name_unique_id_string)
        
        # populate checkmarks' text with status indicator
        for x in range(len(self.design_parameters.installed_apps_name_and_id_list)):
            if(self.design_parameters.installed_apps_name_and_id_list[x][0]) != 0:
                self.widget_list_app_checkmarks[x].config(text="Yes", fg="green")
            elif(self.design_parameters.installed_apps_name_and_id_list[x][0]) == 0:
                self.widget_list_app_checkmarks[x].config(text="No", fg="red")

        self.button_tasks_status_dict["app_status"] = True

    def installedapps_widgets(self, frame, frame_header, needs_installed_apps_programs_list, title):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title = tk.Label(frame_header, font=self.header_font, text=title)
        lbl_title.grid(column=0, row=0, sticky="n")

        # create widget list of programs
        widget_list_programs = []
        for x in range(len(needs_installed_apps_programs_list)):
            lbl_app_name = tk.Label(frame_widgets, font=self.main_font, text=needs_installed_apps_programs_list[x])
            widget_list_programs.append(lbl_app_name)
            # place labels on grid
            row = x + 1 # to place on grid after header
            widget_list_programs[x].grid(column=0, row=row, sticky="w")
        # end widget list of programs

        # create widget checkmarks for programs
        self.widget_list_app_checkmarks = []
        for x in range(len(widget_list_programs)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            self.widget_list_app_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            self.widget_list_app_checkmarks[x].grid(column=1, row=row, sticky="e", padx=5)
        # end widget checkmarks for programs


        # button updates list of currently installed programs and updates checkmark status indicators
        self.btn_find_installed_apps = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Update", 
                                                command=lambda:[self.threading_check_installed_apps(), 
                                                                self.create_timestamp_widget(frame_widgets, 0, len(self.widget_list_app_checkmarks) + 2)])
        self.btn_find_installed_apps.grid(columnspan=2, row=(len(self.widget_list_app_checkmarks) + 1), pady=5)

        return frame_widgets
        
# updates list of currently installed programs and updates checkmark status indicators and version numbers
    def update_package_installstatus_checkmarks(self):
        # retrieve status of desired apps, any value other than [0, 0] indicates app is installed
        # ["name", "version"]
        self.design_parameters.installed_package_names_and_versions = self.app_logic.find_installed_packages(self.design_parameters.needs_installed_packages)
        
        # populate checkmarks' text with status indicator
        # update version number widget
        for x in range(len(self.design_parameters.installed_package_names_and_versions)):
            if(self.design_parameters.installed_package_names_and_versions[x][0]) != 0:
                self.widget_list_package_checkmarks[x].config(text="Yes", fg="green")
                self.widget_list_package_versions[x].config(text=self.design_parameters.installed_package_names_and_versions[x][1])
            elif(self.design_parameters.installed_package_names_and_versions[x][0]) == 0:
                self.widget_list_package_checkmarks[x].config(text="No", fg="red")
                self.widget_list_package_versions[x].config(text="N/A")

        self.button_tasks_status_dict["package_status"] = True

    def installedpackages_widgets(self, frame, frame_header, needs_installed_apps_programs_list, title):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title = tk.Label(frame_header, font=self.header_font, text=title)
        lbl_title.grid(column=0, row=0, sticky="n")

        # create widget list of programs
        widget_list_programs = []
        for x in range(len(needs_installed_apps_programs_list)):
            lbl_app_name = tk.Label(frame_widgets, font=self.main_font, text=needs_installed_apps_programs_list[x])
            widget_list_programs.append(lbl_app_name)
            # place labels on grid
            row = x + 1 # to place on grid after header
            widget_list_programs[x].grid(column=0, row=row, sticky="w")
        # end widget list of programs

        # create widget list of version numbers
        self.widget_list_package_versions = []
        for x in range(len(widget_list_programs)):
            lbl_version = tk.Label(frame_widgets, font=self.main_font, text="ver.")
            self.widget_list_package_versions.append(lbl_version)
            # place labels on grid
            row = x + 1 # to place on grid after header
            self.widget_list_package_versions[x].grid(column=1, row=row, sticky="w")
        # end widget list of programs

        # create widget checkmarks for programs
        self.widget_list_package_checkmarks = []
        for x in range(len(widget_list_programs)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            self.widget_list_package_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            self.widget_list_package_checkmarks[x].grid(column=2, row=row, sticky="e", padx=5)
        # end widget checkmarks for programs

        

        # button updates list of currently installed programs and updates checkmark status indicators
        self.btn_find_installed_programs = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Update", 
                                                command=lambda:[self.threading_check_installed_packages(), 
                                                                self.create_timestamp_widget(frame_widgets, 0, len(self.widget_list_package_checkmarks) + 2)])
        self.btn_find_installed_programs.grid(columnspan=2, row=(len(self.widget_list_package_checkmarks) + 1), pady=5)

        return frame_widgets
    
# checks running programs against a list and updates widgets according to it's results
    def check_running_programs(self):
        self.design_parameters.currently_running_programs_list = self.app_logic.check_running_processes(self.design_parameters.needs_running_apps)

        # populate checkmarks' text with status indicator
        for x in range(len(self.design_parameters.currently_running_programs_list)):
            if self.design_parameters.currently_running_programs_list[x] != 0:
                self.widget_list_processes_checkmarks[x].config(text="Yes", fg="green")
            elif self.design_parameters.currently_running_programs_list[x] == 0:
                self.widget_list_processes_checkmarks[x].config(text="No", fg="red")

        self.button_tasks_status_dict["processes_status"] = True

    def runningprograms_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)

        lbl_title_diskcleaner = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title4)
        lbl_title_diskcleaner.grid(column=0, row=0, sticky="n")

        # create widget list of apps running #
        widget_list_running_apps = []
        for x in range(len(self.design_parameters.needs_running_apps)):
            lbl_proc_name = tk.Label(frame_widgets, font=self.main_font, text=self.design_parameters.needs_running_apps[x])
            widget_list_running_apps.append(lbl_proc_name)
            # place labels on grid
            row = x + 1
            widget_list_running_apps[x].grid(column=0, row=row, sticky="w")
        # end widget list of apps running

        # create widget checkmarks for programs #
        self.widget_list_processes_checkmarks = []
        for x in range(len(widget_list_running_apps)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            self.widget_list_processes_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            self.widget_list_processes_checkmarks[x].grid(column=1, row=row, sticky="e", padx=5)
        # end widget checkmarks for running apps

        # update button starts process of retrieving status of running processes and updating widgets
        self.btn_check_running_processes = tk.Button(frame_widgets, font=self.main_font, bg=self.design_parameters.buttons_color, text="Update",
                                               command=lambda:[self.threading_check_running_processes(), 
                                                               self.create_timestamp_widget(frame_widgets, 0, len(self.design_parameters.needs_running_apps) + 2)])
        self.btn_check_running_processes.grid(columnspan=2, row=(len(self.design_parameters.needs_running_apps) + 1), pady=5) # makes row last in frame

        return frame_widgets

    # creates a label with the current timestamp
    # the tk widget parent, column, and row are provided as arguments
    def create_timestamp_widget(self, widget_parent, column_value, row_value):
        current_time = self.app_logic.create_timestamp()

        lbl_timestamp = tk.Label(widget_parent, font=self.main_font, text="Last clicked: " + current_time)

        # assign background and foreground color of text based on current color theme
        if(self.design_parameters.theme == 'dark'):
            lbl_timestamp.config(bg=self.design_parameters.dark_theme_background_color, fg=self.design_parameters.accent_color)
        else:
            lbl_timestamp.config(bg=self.design_parameters.light_theme_background_color, fg=self.design_parameters.font_color)

        lbl_timestamp.grid(column=column_value, row=row_value, columnspan=2, sticky="we")

    # update frame background color and label background and foreground/text colors
    # based on dark/light theme colors assigned in wag.py
    def change_color_theme(self, root, theme):
        
        # assign theme variable to be used in other functions that create widgets
        self.design_parameters.theme = theme

        if theme == 'dark':
            for frame in root.winfo_children():
                if isinstance(frame, tk.Frame):
                    frame.config(bg=self.design_parameters.dark_theme_background_color)
                    for frame in frame.winfo_children():
                        if isinstance(frame, tk.Frame):
                            frame.config(bg=self.design_parameters.dark_theme_background_color)
                            for frame in frame.winfo_children():
                                if isinstance(frame, tk.Frame):
                                    frame.config(bg=self.design_parameters.dark_theme_background_color)
                                    for widget in frame.winfo_children():
                                        if isinstance(widget, tk.Label):
                                            if widget.cget('text') == 'Yes' or widget.cget('text') == 'No':
                                                # avoids changing the text color of Yes and No labels which will remain
                                                # green or red respectively
                                                widget.config(bg=self.design_parameters.dark_theme_background_color)
                                                continue

                                            if "License" in widget.cget('text') or "Error" in widget.cget('text') or "Successfully" in widget.cget('text'):
                                                # avoids changing the text color of the windows activation license status label
                                                # so they remain green or red accordingly
                                                widget.config(bg=self.design_parameters.dark_theme_background_color)
                                                continue

                                            widget.config(fg=self.design_parameters.accent_color, bg=self.design_parameters.dark_theme_background_color)
        elif theme == 'light':
            for frame in root.winfo_children():
                if isinstance(frame, tk.Frame):
                    frame.config(bg=self.design_parameters.light_theme_background_color)
                    for frame in frame.winfo_children():
                        if isinstance(frame, tk.Frame):
                            frame.config(bg=self.design_parameters.light_theme_background_color)
                            for frame in frame.winfo_children():
                                if isinstance(frame, tk.Frame):
                                    frame.config(bg=self.design_parameters.light_theme_background_color)
                                    for widget in frame.winfo_children():
                                        if isinstance(widget, tk.Label):
                                            if widget.cget('text') == 'Yes' or widget.cget('text') == 'No':
                                                # avoids changing the text color of Yes and No labels which will remain
                                                # green or red respectively
                                                widget.config(bg=self.design_parameters.light_theme_background_color)
                                                continue

                                            if "License" in widget.cget('text') or "Error" in widget.cget('text') or "Successfully" in widget.cget('text'):
                                                # avoids changing the text color of the windows activation license status label
                                                # so they remain green or red accordingly
                                                widget.config(bg=self.design_parameters.light_theme_background_color)
                                                continue

                                            widget.config(fg=self.design_parameters.font_color, bg=self.design_parameters.light_theme_background_color)     
                    