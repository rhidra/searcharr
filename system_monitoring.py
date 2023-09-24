import subprocess

from log import set_up_logger

class ProcessStatus:
    RUNNING = "running"
    INACTIVE = "inactive"
    OTHER = "other"

class SystemMonitoring:
    def __init__(self, verbose=False, console_logging=False):
        self.logger = set_up_logger("searcharr.system", verbose, console_logging)
    
    def get_system_uptime(self):
        try:
            uptime = subprocess.check_output(["uptime"], universal_newlines=True)
            return uptime.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
        
    def get_status_sonarr(self):
        return self.get_process_status("sonarr")
    
    def get_process_status(self, process_name):
        try:
            cmd = f"sudo systemctl status {process_name}"
            self.logger.info(f"Running: {cmd}")
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

            # Parse the output to determine the status
            if "Active: active (running)" in output:
                return ProcessStatus.RUNNING
            elif "Active: inactive" in output:
                return ProcessStatus.INACTIVE
            else:
                return ProcessStatus.OTHER

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return ProcessStatus.OTHER