import tkinter as tk
from tkinter import font
from tkinter import messagebox
from windows_automation_functions import WindowsAutomationFunctions

class Gui:

    def __init__(self, root, design_parameters):
        self.root = root
        self.design_parameters = design_parameters

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

    # create application header menubar containing app info and help
    def construct_menubar(self, frame, version):
        activation_status_help_text = "Click 'Check' to see if Windows is activated.\
                                        \nIf it is not, click 'Activate Windows' to run an Activation script.\
                                        \nIf activation fails, click 'Check' again.\
                                        \nIf unsuccessful, run this program as an Administrator and try again."

        def show_activation_help_message():
            messagebox.showinfo("Activation Help", activation_status_help_text)
        
        def show_license_message():
            messagebox.showinfo("LICENSE", self.design_parameters.license)

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

        options = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Dark Theme", command=lambda:self.change_color_theme(self.root, 'dark'))
        options.add_command(label="Light Theme", command=lambda:self.change_color_theme(self.root, 'light'))

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

    def windowsactivation_status_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title_windowsactivation_status = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title5)
        lbl_title_windowsactivation_status.grid(column=0, row=0, sticky='n')

        # retrieve status of windows activation and display to user
        # if licensed or error, prohibit use of Activate Windows button
        # if not licensed, enable Activate Windows button
        def check_status_update_widget(self):
            status = self.app_logic.get_windowsactivation_status()
            if status == "License Status: Licensed" or status == "Error retrieving status":
                btn_activate_windows.config(state="disabled")
            elif status == "License Status: Not Licensed":
                btn_activate_windows.config(state="normal")
            lbl_status.config(text=status)

        # create label which displays the activation status after button press
        lbl_status = tk.Label(frame_widgets, font=self.main_font, text="Not checked")
        lbl_status.grid(column=0, row=1)

        # attempt installing and/or changing product key
        # returned result is used to display error message or continue the process
        # attempt to activate windows and after a delay, retrieve and display the result
        def activate_windows_update_widgets(self):
            # list created to be passed by reference to save result from function called from another function
            activation_result = []

            status = self.app_logic.run_activate_windows_script()
            if status != True:
                lbl_status.config(text=status)
                return
            else:
                btn_activate_windows.config(text="Activating...", state="disabled")
                self.root.after(
                    5000, lambda:
                    [self.app_logic.run_activate_windows_check_status_script(activation_result), update_widgets()])
                
            # helper function called after the time delay needed to check activation status
            def update_widgets():
                if activation_result[0] == "True":
                    # complete success tasks
                    lbl_status.config(text="Successfully Activated Windows")
                    btn_activate_windows.config(text="Activate Windows", state="disabled")
                else:
                    btn_activate_windows.config(text="Activate Windows")
                    lbl_status.config(text=activation_result[0])

        #button
        btn_check_activation_status = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Check",
                                               command=lambda:[check_status_update_widget(self), self.create_timestamp_widget(frame_widgets, 0, 3)])
        btn_check_activation_status.grid(column=0, row=2, pady=5)

        btn_activate_windows = tk.Button(frame_widgets, font=self.main_font, bg=self.design_parameters.buttons_color, state="disabled", text="Activate Windows")
        btn_activate_windows.configure(command=lambda:activate_windows_update_widgets(self))
        btn_activate_windows.grid(column=0, row=4, pady=5)

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
        widget_list_checkmarks = []
        for x in range(len(widget_list_programs)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            widget_list_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            widget_list_checkmarks[x].grid(column=1, row=row, sticky="e", padx=5)
        # end widget checkmarks for programs

        # updates list of currently installed programs and updates checkmark status indicators
        def update_app_installstatus_checkmarks():
            # retrieve status of desired apps, any value other than [0, 0] indicates app is installed
            # ["app name", "AppID"]
            self.design_parameters.installed_apps_name_and_id_list = self.app_logic.find_installed_apps(needs_installed_apps_programs_list,
                                                                                                        self.design_parameters.duplicate_app_name,
                                                                                                        self.design_parameters.duplicate_app_name_unique_id_string)
            
            # populate checkmarks' text with status indicator
            for x in range(len(self.design_parameters.installed_apps_name_and_id_list)):
                if(self.design_parameters.installed_apps_name_and_id_list[x][0]) != 0:
                    widget_list_checkmarks[x].config(text="Yes", fg="green")
                elif(self.design_parameters.installed_apps_name_and_id_list[x][0]) == 0:
                    widget_list_checkmarks[x].config(text="No", fg="red")

        # button updates list of currently installed programs and updates checkmark status indicators
        btn_find_installed_programs = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Update", 
                                                command=lambda:[update_app_installstatus_checkmarks(), 
                                                                self.create_timestamp_widget(frame_widgets, 0, len(widget_list_checkmarks) + 2)])
        btn_find_installed_programs.grid(columnspan=2, row=(len(widget_list_checkmarks) + 1), pady=5)

        return frame_widgets
        
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
        widget_list_versions = []
        for x in range(len(widget_list_programs)):
            lbl_version = tk.Label(frame_widgets, font=self.main_font, text="ver.")
            widget_list_versions.append(lbl_version)
            # place labels on grid
            row = x + 1 # to place on grid after header
            widget_list_versions[x].grid(column=1, row=row, sticky="w")
        # end widget list of programs

        # create widget checkmarks for programs
        widget_list_checkmarks = []
        for x in range(len(widget_list_programs)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            widget_list_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            widget_list_checkmarks[x].grid(column=2, row=row, sticky="e", padx=5)
        # end widget checkmarks for programs

        # updates list of currently installed programs and updates checkmark status indicators and version numbers
        def update_app_installstatus_checkmarks():
            # retrieve status of desired apps, any value other than [0, 0] indicates app is installed
            # ["name", "version"]
            self.design_parameters.installed_package_names_and_versions = self.app_logic.find_installed_packages(needs_installed_apps_programs_list)
            
            # populate checkmarks' text with status indicator
            # update version number widget
            for x in range(len(self.design_parameters.installed_package_names_and_versions)):
                if(self.design_parameters.installed_package_names_and_versions[x][0]) != 0:
                    widget_list_checkmarks[x].config(text="Yes", fg="green")
                    widget_list_versions[x].config(text=self.design_parameters.installed_package_names_and_versions[x][1])
                elif(self.design_parameters.installed_package_names_and_versions[x][0]) == 0:
                    widget_list_checkmarks[x].config(text="No", fg="red")
                    widget_list_versions[x].config(text="N/A")

        # button updates list of currently installed programs and updates checkmark status indicators
        btn_find_installed_programs = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Update", 
                                                command=lambda:[update_app_installstatus_checkmarks(), 
                                                                self.create_timestamp_widget(frame_widgets, 0, len(widget_list_checkmarks) + 2)])
        btn_find_installed_programs.grid(columnspan=2, row=(len(widget_list_checkmarks) + 1), pady=5)

        return frame_widgets
    
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
        widget_list_checkmarks = []
        for x in range(len(widget_list_running_apps)):
            lbl_checkmarks = tk.Label(frame_widgets, font=self.main_font, text="X")
            widget_list_checkmarks.append(lbl_checkmarks)
            # place checkmarks on grid
            row = x + 1 # to place on grid after header
            widget_list_checkmarks[x].grid(column=1, row=row, sticky="e", padx=5)
        # end widget checkmarks for running apps

        # checks running programs against a list and updates widgets according to it's results
        def check_running_programs():
            self.design_parameters.currently_running_programs_list = self.app_logic.check_running_processes(self.design_parameters.needs_running_apps)

            # populate checkmarks' text with status indicator
            for x in range(len(self.design_parameters.currently_running_programs_list)):
                if self.design_parameters.currently_running_programs_list[x] != 0:
                    widget_list_checkmarks[x].config(text="Yes", fg="green")
                elif self.design_parameters.currently_running_programs_list[x] == 0:
                    widget_list_checkmarks[x].config(text="No", fg="red")

        # update button starts process of retrieving status of running processes and updating widgets
        btn_check_running_programs = tk.Button(frame_widgets, font=self.main_font, bg=self.design_parameters.buttons_color, text="Update",
                                               command=lambda:[check_running_programs(), 
                                                               self.create_timestamp_widget(frame_widgets, 0, len(self.design_parameters.needs_running_apps) + 2)])
        btn_check_running_programs.grid(columnspan=2, row=(len(self.design_parameters.needs_running_apps) + 1), pady=5) # makes row last in frame

        return frame_widgets

    # creates a label with the current timestamp
    # the tk widget parent, column, and row are provided as arguments
    def create_timestamp_widget(self, widget_parent, column_value, row_value):
        current_time = self.app_logic.create_timestamp()

        lbl_timestamp = tk.Label(widget_parent, font=self.main_font, text="Last clicked: " + current_time, bg=widget_parent.cget('bg'), fg=widget_parent.winfo_children()[0].cget('fg'))
        lbl_timestamp.grid(column=column_value, row=row_value, columnspan=2, sticky="we")

    # update frame background color and label background and foreground/text colors
    # based on dark/light theme colors assigned in wag.py
    def change_color_theme(self, root, theme):
        
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
                                            widget.config(fg=self.design_parameters.font_color, bg=self.design_parameters.light_theme_background_color)     
                    