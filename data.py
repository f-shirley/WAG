# contains the parameters for the gui design, *most* are assignable
# parameters with an "Edited internally" comment after it should NOT be changed
class GuiDesignParameters:
    def __init__(self):
        self.app_title = None
        self.start_dimensions = None
        self.font_family_name = None
        self.font_size = None
        self.header_font_size_adjuster = None # this value is added to font_size to create the header
        self.font_color = None
        self.buttons_color = None
        self.accent_color = None
        # title names for each of four workspaces/frames
        self.title1 = None
        self.title2 = None
        self.title3 = None
        self.title4 = None
        self.title5 = None
        self.needs_installed_apps = None # Will be list
        self.installed_apps_name_and_id_list = None # Edited internally, [0, 0] if uninstalled and content if installed
        self.duplicate_app_name = "" # assign this var the name for an app who's Name (from powershell - get-StartApps) ...
        # ... is listed twice. This allows the program to properly track both apps installation status
        self.needs_running_apps = None # Will be list
        self.currently_running_programs_list = None # Edited internally
