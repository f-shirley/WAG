import tkinter as tk
from gui import Gui
from data import GuiDesignParameters

# version 0.0.1-beta
# last modified 8-28-2024

# colors
peach = "#EFC5B9" # accent
lightblue = "#B9E3EF" # buttons

# adjustable parameters for the gui design
# see data.py for all parameters
gui_design_parameters = GuiDesignParameters()
gui_design_parameters.app_title = "Windows Automation Gui"
gui_design_parameters.start_dimensions = "550x550"
gui_design_parameters.font_family_name = "Calibri"
gui_design_parameters.font_size = 11
gui_design_parameters.header_font_size_adjuster = 3
gui_design_parameters.font_color = "black"
gui_design_parameters.buttons_color = lightblue
gui_design_parameters.accent_color = peach
gui_design_parameters.title1 = "Windows Update"
gui_design_parameters.title2 = "Disk Cleaner"
gui_design_parameters.title3 = "Check Installed Programs"
gui_design_parameters.title4 = "Check Running Programs"
gui_design_parameters.title5 = "Activation Status"
gui_design_parameters.needs_installed_apps = ["Firefox", "Microsoft Teams", "Minecraft"]
gui_design_parameters.duplicate_app_name = "N/A"
gui_design_parameters.needs_running_apps = ["spooler", "Firefox"]

# start application
root = tk.Tk()
root.geometry(gui_design_parameters.start_dimensions)
root.title(gui_design_parameters.app_title)
gui = Gui(root, gui_design_parameters)
root.mainloop()
