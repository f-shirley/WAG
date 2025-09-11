import tkinter as tk
from gui import Gui
from data import GuiDesignParameters
import sys
import os

# version 2.0.1
# last modified 9-11-2025

# colors
peach = "#EFC5B9" # accent
lightblue = "#B9E3EF" # buttons
darkblue = "#1c384f" # dark mode background

# adjustable parameters for the gui design
# see data.py for all parameters
gui_design_parameters = GuiDesignParameters()
gui_design_parameters.app_title = "Windows Automation Gui"
gui_design_parameters.version = "v2.0.1"
gui_design_parameters.font_family_name = "Calibri"
gui_design_parameters.font_size = 11
gui_design_parameters.header_font_size_adjuster = 3
gui_design_parameters.font_color = "black"
gui_design_parameters.buttons_color = lightblue
gui_design_parameters.accent_color = peach
gui_design_parameters.dark_theme_background_color = darkblue
gui_design_parameters.light_theme_background_color = "white"
gui_design_parameters.title1 = "Windows Update"
gui_design_parameters.title2 = "Disk Cleaner"
gui_design_parameters.title3 = "Check Installed Apps"
gui_design_parameters.title4 = "Check Running Processes"
gui_design_parameters.title5 = "Activation Status"
gui_design_parameters.title6 = "Check Installed Programs"
gui_design_parameters.needs_installed_apps = ["Microsoft Teams", "Word", "Excel", "Access", "Minecraft"]
gui_design_parameters.needs_installed_packages = ["balenaEtcher", "VLC media player"]
#gui_design_parameters.duplicate_app_name_unique_id_string = "" # can comment out this line of code if no duplicate apps are installed
gui_design_parameters.needs_running_apps = ["msedge"]
gui_design_parameters.autorun = True
gui_design_parameters.autorun_interval_time = 2700000 # 45 minutes == 2.7 * 10**6 or 2,700,000 milliseconds

# begin code for loading license file as string to display in gui
# many thanks to James on stackoverflow for this function 'resource_path'
# allows using external files in a single exe after building
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

license = ""
license_path = resource_path('LICENSE')

try:
    with open(license_path, 'r', encoding='utf-8') as file:
        license = file.read()
except Exception:
    license = "Error loading LICENSE"

gui_design_parameters.license = license
# end code for loading license file

# start application
root = tk.Tk()

# fullscreen windowed mode if no starting dimensions are set
if gui_design_parameters.start_dimensions == None:
    root.state("zoomed")

root.title(gui_design_parameters.app_title)
root.iconbitmap(default=resource_path("wag-logo.ico"))
gui = Gui(root, gui_design_parameters)
root.mainloop()