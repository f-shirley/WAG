import subprocess
from datetime import datetime
import os
import time

class WindowsAutomationFunctions:
    def __init__(self):
        self.windows_drive_dir = self.get_windows_drive_letter()

    def get_windows_drive_letter(self):
        """ Returns drive letter for installation location of windows to properly execute certain scripts.
         Returns error message string if exception is thrown. """
        try:
            windir = os.path.expandvars('%windir%')
            return str(windir[0])
        except:
            return "Error retrieving installation directory"

    def get_windowsactivation_status(self):
        """ Returns Windows activation status of the host machine as a string: License Status: Licensed, 
        License Status: Not Licensed, or Error retrieving status """

        # error handling for drive letter
        # if constructor retrieved error message instead of a letter, return the error message
        if len(self.windows_drive_dir) != 1:
            return self.windows_drive_dir

        try:
            # cscript runs command in CLI environment
            status = subprocess.Popen(["powershell", "cscript", self.windows_drive_dir + ":\\Windows\\System32\\slmgr.vbs", "/dli"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
            result_status_lines = status.communicate()[0].splitlines()

            for item in result_status_lines:
                if "License Status: Licensed" in str(item):
                    # return the string, as opposed to the item, because the item does not == "License Status: Licensed"
                    # despite it appearing to be the same string. And it needs to be checked for equality later
                    return "License Status: Licensed"
            
            return "License Status: Not Licensed"
                    
        except:
            return "Error retrieving status"

    def run_activate_windows_script(self):
        """ Attempt to get the OEM Windows activation key stored from the computer's hardware, install that key, and then activate windows. 
        Returns error message string or boolean True if successful. """

        # error handling for drive letter
        # if constructor retrieved error message instead of a letter, return the error message
        if len(self.windows_drive_dir) != 1:
            return self.windows_drive_dir

        try:
            # gets original key
            # wmic command is deprecated and inconsistent among Windows versions

            get_key_process = subprocess.Popen(["powershell", "(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductkey"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
            result_getkey_line = get_key_process.communicate()[0]

            print("Get key result: " + str(result_getkey_line))

            key_formatted = result_getkey_line.rstrip().decode()

            if(len(key_formatted) == 29):
                change_key_process = subprocess.Popen(["powershell", self.windows_drive_dir + ":\\Windows\\System32\\changepk.exe", "/ProductKey", key_formatted], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
                result_change_key_process = change_key_process.communicate()[0].splitlines()

                for item in result_change_key_process:
                    if "Access denied" in str(item) or "failed" in str(item):
                        return "Installing key failed\nThis feature may require admin privileges\nTry activating manually using:\n" + key_formatted
                
            # return True on complete success
            return True
            
        except:
            # if key_formatted has been assigned display this message in gui
            if len(key_formatted) == 29:
                return "Error Activating Windows\nTry activating manually using this key:\n" + key_formatted
            else:
                return "Error Activating Windows"

    def open_windowsupdate(self):
        """ Open the windows update gui using powershell. """
        process = subprocess.Popen(["powershell", "start", "ms-settings:windowsupdate"], creationflags=subprocess.CREATE_NO_WINDOW)

    def open_diskcleaner(self):
        """ Open the Disk Cleanup application gui using powershell. """
        process = subprocess.Popen(["powershell", "cleanmgr.exe"], creationflags=subprocess.CREATE_NO_WINDOW) # takes arguments from additional list items

    # returns in the same order as the list of apps that need installed retrieved from data.py (needs_installed_apps var)
    # which is important to update the associated check marks in gui.py
    def find_installed_apps(self, needs_installed_apps, duplicate_app_name_unique_id_string):
        """ Returns a list of lists containing app names and ids; one element in format: ['name', 'id'] or [0, 0] if no matches. """

        # executes powershell command to get currently installed start apps and packages
        subprocess.CREATE_NO_WINDOW
        startapps_names = subprocess.Popen(["powershell", "get-StartApps | select -Expand Name"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
        process_appid = subprocess.Popen(["powershell", "get-StartApps | select -Expand AppID"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
        # retrieve list of app and package names, version, and appid from stdout of powershell command
        result_startapps_names = startapps_names.communicate()[0].splitlines()
        result_appid = process_appid.communicate()[0].splitlines()

        # initialize list with same length as the amount of apps that need installed
        installed_apps_name_and_id_list = [[0,0]] * len(needs_installed_apps)
        
        # check installed apps against needed apps
        # a match (no match remains value of 0) is recorded in the same index position as the needs_installed_apps list
        for x in range(len(needs_installed_apps)):
            for i in range(len(result_startapps_names)):
                if needs_installed_apps[x] in str(result_startapps_names[i]).strip("b'"):

                    # just skips the duplicate app name that does not need to be checked for here
                    # use case: when the app is installed as an app and a package
                    if duplicate_app_name_unique_id_string != "":
                        if duplicate_app_name_unique_id_string in str(result_appid[i]).strip("b'"):
                            continue

                    # debug info: lists found installed apps in console
                    # print("Installed App: " + str(result_startapps_names[i]).strip("b'") + " - AppID: " + str(result_appid[i]).strip("b'"))

                    # saves name and appid to corresponding needs_installed_apps index
                    installed_apps_name_and_id_list[x] = [str(result_startapps_names[i]).strip("b'"), str(result_appid[i]).strip("b'")]
                    break

        # returns a list of lists containing app names and ids; one element in format: ['name', 'id'] or [0, 0] if no matches
        return installed_apps_name_and_id_list

    def find_installed_packages(self, needs_installed_packages):
        """ Returns a list of lists containing package names and versions; one element in format: ['name', 'version'] or [0, 0] if no matches. """

        # executes powershell command to get currently installed packages
        # retrieve list of package names, version from stdout of powershell command
        package_names_and_version = subprocess.Popen(["powershell", "Get-Package | select -Property Name, Version | Format-List"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
        # splits each line into a list in format:
            # b'Name    : Package Name'
            # b'Version : 1.2.3'
        result_package_names_and_version = package_names_and_version.communicate()[0].splitlines()

        # initialize list with same length as the amount of apps that need installed
        installed_package_name_and_version_list = [[0,0]] * len(needs_installed_packages)
        
        # check installed apps against needed apps
        # a match (no match remains value of 0) is recorded in the same index position as the needs_installed_apps list
        for x in range(len(needs_installed_packages)):
            for i in range(len(result_package_names_and_version)):
                if needs_installed_packages[x] in str(result_package_names_and_version[i]):

                    # saves name and version to corresponding needs_installed_packages index
                    installed_package_name_and_version_list[x] = [str(result_package_names_and_version[i]).split(":", maxsplit=1)[1].strip(" '"), str(result_package_names_and_version[i + 1]).split(":", maxsplit=1)[1].strip(" '")]
                    break

        return installed_package_name_and_version_list

    def check_running_processes(self, needs_running_apps):
        """ Returns a list of all running processes of the host machine in the same order that matches the elements of the
         provided list-type argument. A value of 0 is assigned to any index with no match. """

        # initialize list
        process_list = [0] * len(needs_running_apps)

        process_names = subprocess.Popen(["powershell", "Get-Process | select -Expand ProcessName"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE)
        result_names_list = process_names.communicate()[0].splitlines()

        # loop through all processes
        for x in range(len(needs_running_apps)):
            for proc in result_names_list:
                if needs_running_apps[x].lower() in str(proc).lower():
                    process_list[x] = str(proc)
                    break

        return process_list
    
    def create_timestamp(self):
        """ Return a formatted timestamp string for the current time on the host machine. """
        current_time = datetime.now().strftime("%m/%d/%y, %I:%M:%S %p")
        return current_time

