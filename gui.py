import tkinter as tk
from tkinter import font
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

        # give each column and row in root equal weight
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # call function which constructs the gui
        self.place_all_frames()

    # call each frame's constructing function (which includes widgets) and place them
    def place_all_frames(self):
        # top left
        frame_topleft, frame_topleft_header, frame_topleft_widgets = self.construct_frame_topleft()
        frame_topleft.grid(column=0, row=0)
        frame_topleft_header.grid(column=0, row=0)

        # top right
        frame_topright, frame_topright_header, frame_topright_widgets = self.construct_frame_topright()
        frame_topright.grid(column=1, row=0)
        frame_topright_header.grid(column=0, row=0)

        # bottom left
        frame_bottomleft, frame_bottomleft_header, frame_bottomleft_widgets = self.construct_frame_bottomleft()
        frame_bottomleft.grid(column=0, row=1)
        frame_bottomleft_header.grid(column=0, row=0)

        # bottom right
        frame_bottomright, frame_bottomright_header, frame_bottomright_widgets = self.construct_frame_bottomright()
        frame_bottomright.grid(column=1, row=1)
        frame_bottomright_header.grid(column=0, row=0)

        # last
        frame_last, frame_last_header, frame_last_widgets = self.construct_frame_last()
        frame_last.grid(column=0, row=2)
        frame_last_header.grid(column=0, row=0)

        # place grid widget frames
        common_styling_widget_frames = [frame_topleft_widgets, frame_topright_widgets, frame_bottomleft_widgets, frame_bottomright_widgets, frame_last_widgets]

        for frame in common_styling_widget_frames:
            frame.grid(row=1, column=0, sticky="nsew")
            frame.columnconfigure(0, weight=1)
        
        # add common stylings to frames
        common_styling_frames = [frame_topleft, frame_topright, frame_bottomleft, frame_bottomright, frame_last]

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

    def construct_frame_topleft(self):
        frame = tk.Frame(self.root)
        frame_header = tk.Frame(frame)

        # construct widgets
        frame_widgets = self.windowsupdates_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_topright(self):
        frame = tk.Frame(self.root)
        frame_header = tk.Frame(frame)

        # construct widgets
        frame_widgets = self.diskcleanup_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_bottomleft(self):
        frame = tk.Frame(self.root)
        frame_header = tk.Frame(frame)

        frame_widgets = self.installedprograms_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_bottomright(self):
        frame = tk.Frame(self.root)
        frame_header = tk.Frame(frame)

        frame_widgets = self.runningprograms_widgets(frame, frame_header)

        return frame, frame_header, frame_widgets
    
    def construct_frame_last(self):
        # fifth frame
        frame = tk.Frame(self.root)
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
        def check_status_update_widget(self):
            status = self.app_logic.get_windowsactivation_status()
            lbl_status.config(text=status)

        # create label which displays the activation status after button press
        lbl_status = tk.Label(frame_widgets, font=self.main_font, text="Not checked")
        lbl_status.grid(column=0, row=1)

        #button
        btn_check_activation_status = tk.Button(frame_widgets, font=self.main_font,bg=self.design_parameters.buttons_color, text="Check",
                                               command=lambda:[check_status_update_widget(self), self.create_timestamp_widget(frame_widgets, 0, 3)])
        btn_check_activation_status.grid(column=0, row=2, pady=5)

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

    def installedprograms_widgets(self, frame, frame_header):
        frame_widgets = tk.Frame(frame)

        # title
        lbl_title_diskcleaner = tk.Label(frame_header, font=self.header_font, text=self.design_parameters.title3)
        lbl_title_diskcleaner.grid(column=0, row=0, sticky="n")

        # create widget list of programs
        widget_list_programs = []
        for x in range(len(self.design_parameters.needs_installed_apps)):
            lbl_app_name = tk.Label(frame_widgets, font=self.main_font, text=self.design_parameters.needs_installed_apps[x])
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
            self.design_parameters.installed_apps_name_and_id_list = self.app_logic.find_installed_apps(self.design_parameters.needs_installed_apps,
                                                                                                        self.design_parameters.duplicate_app_name)
            
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

        lbl_timestamp = tk.Label(widget_parent, font=self.main_font, text="Last clicked: " + current_time)
        lbl_timestamp.grid(column=column_value, row=row_value, columnspan=2, sticky="we")