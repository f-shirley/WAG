import subprocess
from datetime import datetime
import os
import time

class WindowsAutomationFunctions:
    def __init__(self):
        self.windows_drive_dir = self.get_windows_drive_letter()

    # retrieve drive letter for installation location of windows
    # to properly execute certain scripts
    def get_windows_drive_letter(self):
        try:
            windir = os.path.expandvars('%windir%')
            return str(windir[0])
        except:
            return "Error retrieving installation directory"

    # get windows activation status
    # cscript runs command in CLI environment
    def get_windowsactivation_status(self):
        # error handling for drive letter
        # if constructor retrieved error message instead of a letter, return the error message
        if len(self.windows_drive_dir) != 1:
            return self.windows_drive_dir

        try:
            status = subprocess.Popen(["powershell", "cscript", self.windows_drive_dir + ":\\Windows\\System32\\slmgr.vbs", "/dli"], stdout=subprocess.PIPE)
            result_status_lines = status.communicate()[0].splitlines()

            for item in result_status_lines:
                if "License Status: Licensed" in str(item):
                    # return the string, as opposed to the item, because the item does not == "License Status: Licensed"
                    # despite it appearing to be the same string. And it needs to be checked for equality later
                    return "License Status: Licensed"
            
            return "License Status: Not Licensed"
                    
        except:
            return "Error retrieving status"
        
    # attempt to get the original key, install that key, and then activate windows
    # returns error messages or True if a complete success occurs
    def run_activate_windows_script(self):
        # error handling for drive letter
        # if constructor retrieved error message instead of a letter, return the error message
        if len(self.windows_drive_dir) != 1:
            return self.windows_drive_dir

        try:
            # gets original key
            get_key_process = subprocess.Popen(["wmic", "path", "softwarelicensingservice", "get", "OA3xOriginalProductkey", "/value"], stdout=subprocess.PIPE)
            result_getkey_lines = get_key_process.communicate()[0]

            key = str(result_getkey_lines).split(sep="=")
            key_formatted = key[1][:29]

            # installs key
            install_key_process = subprocess.Popen(["powershell", "cscript", self.windows_drive_dir + ":\\Windows\\System32\\slmgr.vbs", "/ipk", key_formatted], stdout=subprocess.PIPE)
            result_installkey_lines = install_key_process.communicate()[0].splitlines()

            # check for key install success
            # if no success and retrieved key is correct format:
            # try changing the key a different way
            if not (str(result_installkey_lines[len(result_installkey_lines) - 2]).endswith(" successfully.'")):
                if len(key_formatted) == 29:
                    change_key_process = subprocess.Popen(["powershell", self.windows_drive_dir + ":\\Windows\\System32\\changepk.exe", "/ProductKey", key_formatted], stdout=subprocess.PIPE)
                else:
                    return "Installing key failed\nThis feature requires running\nthis program as an Admin\nError retrieving product key"
            
            # return True on complete success
            return True
            
        except:
            # if key_formatted has been assigned display this message in gui
            if len(key_formatted) == 29:
                return "Error Activating Windows\nTry activating manually using this key:\n" + key_formatted
            else:
                return "Error Activating Windows"
            
    def run_activate_windows_check_status_script(self, activation_result):
        # attempt activating windows and saving result
        # result is stored in a list (so it is pased by reference)
        activate_process = subprocess.Popen(["powershell", "cscript", self.windows_drive_dir + ":\\Windows\\System32\\slmgr.vbs", "/ato"], stdout=subprocess.PIPE)
        result_activate_lines = activate_process.communicate()[0].splitlines()
        # check for activation success
        if not (str(result_activate_lines[len(result_activate_lines) - 2]).endswith("Product activated successfully.'")):
            activation_result.append("Error Activating Windows")
            return
        
        activation_result.append("True")
        return

    # open windows update gui using powershell
    def open_windowsupdate(self):
        process = subprocess.Popen(["powershell", "start", "ms-settings:windowsupdate"])

    # open disk cleaner application using powershell
    def open_diskcleaner(self):
        process = subprocess.Popen(["powershell", "cleanmgr.exe"]) # takes arguments from additional list items
        #result = process.communicate()[0]
        #print("Result: " + str(result))

    # returns a list of lists containing app names and ids; one element in format: ['name', 'id'] or [0, 0] if no matches
    # in the same order as the list of apps that need installed retrieved from data.py (needs_installed_apps var)
    def find_installed_apps(self, needs_installed_apps, duplicate_app_name, duplicate_app_name_unique_id_string):

        # executes powershell command to get currently installed start apps and packages
        startapps_names = subprocess.Popen(["powershell", "get-StartApps | select -Expand Name"], stdout=subprocess.PIPE)
        process_appid = subprocess.Popen(["powershell", "get-StartApps | select -Expand AppID"], stdout=subprocess.PIPE)
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
        # executes powershell command to get currently installed packages
        # retrieve list of package names, version from stdout of powershell command
        package_names_and_version = subprocess.Popen(["powershell", "Get-Package | select -Property Name, Version | Format-List"], stdout=subprocess.PIPE)
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

        # returns a list of lists containing package names and versions; one element in format: ['name', 'version'] or [0, 0] if no matches
        return installed_package_name_and_version_list

    # saves all processes with argument[n] in list
    # returns a list of the actual process names in the same order as the needs_running_apps list
    # with 0 in the appropiate index if no match
    def check_running_processes(self, needs_running_apps):
        # initialize list
        process_list = [0] * len(needs_running_apps)

        process_names = subprocess.Popen(["powershell", "Get-Process | select -Expand ProcessName"], stdout=subprocess.PIPE)
        result_names_list = process_names.communicate()[0].splitlines()

        # loop through all processes
        for x in range(len(needs_running_apps)):
            for proc in result_names_list:
                if needs_running_apps[x].lower() in str(proc).lower():
                    process_list[x] = str(proc)
                    break

        return process_list
    
    # returns a formatted timestamp string for current time
    def create_timestamp(self):
        current_time = datetime.now().strftime("%m/%d/%y, %I:%M:%S %p")
        return current_time

