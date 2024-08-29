import subprocess
from datetime import datetime

class WindowsAutomationFunctions:
    def __init__(self):
        pass

    # get windows activation status
    # cscript runs command in CLI environment
    def get_windowsactivation_status(self):
        try:
            status = subprocess.Popen(["powershell", "cscript", "c:\\Windows\\System32\\slmgr.vbs", "/dli"], stdout=subprocess.PIPE)
            result_status_lines = status.communicate()[0].splitlines()
            for item in result_status_lines:
                if "License Status" in str(item):
                    return item
        except:
            return "Error retrieving status"

        return "Error retrieving status"

    # open windows update gui using powershell
    def open_windowsupdate(self):
        process = subprocess.Popen(["powershell", "start", "ms-settings:windowsupdate"])

    # open disk cleaner application using powershell
    def open_diskcleaner(self):
        process = subprocess.Popen(["powershell", "cleanmgr.exe"]) # takes arguments from additional list items
        #result = process.communicate()[0]
        #print("Result: " + str(result))

    # returns a list with the status of the apps that need installed (0 - installed, 1 - not installed)
    # in the same order as the list of apps that need installed retrieved from data.py (needs_installed_apps var)
    def find_installed_apps(self, needs_installed_apps, duplicate_app_name):

        # executes powershell command to get currently installed start apps
        process_names = subprocess.Popen(["powershell", "get-StartApps | select -Expand Name"], stdout=subprocess.PIPE)
        process_appid = subprocess.Popen(["powershell", "get-StartApps | select -Expand AppID"], stdout=subprocess.PIPE)
        # retrieve list of app names and id from stdout of powershell command
        result_names = process_names.communicate()[0].splitlines()
        result_appid = process_appid.communicate()[0].splitlines()

        # initialize list with same length as the amount of apps that need installed
        installed_apps_name_and_id_list = [[0,0]] * len(needs_installed_apps)
        
        # toggle for ensuring TWO applications with the same name can get checked for by comparing AppID later
        # check wag.py to initialize data to assign the application with a duplicate name to a var
        toggle = False
        # check installed apps against needed apps
        # a match (no match remains value of 0) is recorded in the same index position as the needs_installed_apps list
        for x in range(len(needs_installed_apps)):
            for i in range(len(result_names)):
                if needs_installed_apps[x] in str(result_names[i]).strip("b'"):
                    # skip this loop iteration if the duplicate app name was already iterated on
                    # this allows the loop to keep iterating and find the second duplicate app name
                    # allowing accurate status of the apps
                    if toggle == True and str(result_names[i]).strip("b'") in duplicate_app_name:
                        toggle = False
                        continue

                    # debug info: lists found installed apps in console
                    # print("Installed App: " + str(result_names[i]).strip("b'") + " - AppID: " + str(result_appid[i]).strip("b'"))

                    # saves name and appid to corresponding needs_installed_apps index
                    installed_apps_name_and_id_list[x] = [str(result_names).strip("b'"), str(result_appid).strip("b'")]
                    if str(result_names[i]).strip("b'") in duplicate_app_name:
                        toggle = True
                    break

        # returns a list of lists containing app names and ids; one element in format: ['name', 'id'] or [0, 0] if no matches
        return installed_apps_name_and_id_list

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

