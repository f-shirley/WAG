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
        self.dark_theme_background_color = None
        self.light_theme_background_color = None
        # title names for each of four workspaces/frames
        self.title1 = None
        self.title2 = None
        self.title3 = None
        self.title4 = None
        self.title5 = None
        self.title6 = None
        self.needs_installed_apps = None # Will be list
        self.needs_installed_packages = None # Will be list
        self.installed_apps_name_and_id_list = None # Edited internally, [0, 0] if uninstalled and content if installed
        self.installed_package_names_and_versions = None # Edited internally, [0, 0] if uninstalled and content if installed
        self.duplicate_app_name = "" # assign this var the name for an app who's Name (from powershell - get-StartApps) ...
        # ... is listed twice. This allows the program to properly track both apps installation status
        self.duplicate_app_name_unique_id_string = "" # if app/package shows up twice in get-Startapps command due to duplicate installations,
        # assign this variable a unique value found in the PACKAGE appid; in the Check Installed Apps section,
        # that package will be skipped,allowing accurate installation check for the actual app
        self.needs_running_apps = None # Will be list
        self.currently_running_programs_list = None # Edited internally
        self.license = None # Edited internally
        self.version = None # Will be assigned current application version number
