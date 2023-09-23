import subprocess

class ProcessStatus:
    RUNNING = "running"
    INACTIVE = "inactive"
    OTHER = "other"

class SystemMonitoring:
    @staticmethod
    def get_system_uptime():
        try:
            uptime = subprocess.check_output(["uptime"], universal_newlines=True)
            return uptime.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
        
    @staticmethod
    def get_status_sonarr():
        return SystemMonitoring.get_process_status("sonarr")
    
    @staticmethod
    def get_process_status(process_name):
        try:
            cmd = f"sudo systemctl status {process_name}"
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