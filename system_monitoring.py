import subprocess

from log import set_up_logger

PROCESSES = [{
        "id": "sonarr",
        "systemctl": "sonarr",
        "display": "Sonarr"
    },{
        "id": "radarr",
        "systemctl": "radarr",
        "display": "Radarr"
    }, {
        "id": "prowlarr",
        "systemctl": "prowlarr",
        "display": "Prowlarr"
    }, {
        "id": "bazarr",
        "systemctl": "bazarr",
        "display": "Bazarr"
    }, {
        "id": "plex",
        "systemctl": "plexmediaserver",
        "display": "Plex"
    }, {
        "id": "jellyfin",
        "systemctl": "jellyfin",
        "display": "Jellyfin"
    }, {
        "id": "ombi",
        "systemctl": "ombi",
        "display": "Ombi"
    }, {
        "id": "searcharr",
        "systemctl": "searcharr",
        "display": "Searcharr"
    }, {
        "id": "nzbget",
        "systemctl": "nzbget",
        "display": "NZBGet"
    }, {
        "id": "transmission",
        "systemctl": "transmission-deamon",
        "display": "Transmission"
    }, {
        "id": "openvpn",
        "systemctl": "openvpn",
        "display": "OpenVPN"
    }, {
        "id": "readarr",
        "systemctl": "readarr",
        "display": "Readarr"
    }]

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
    
    def generate_processs_status_report(self):
        report = ''
        for p in PROCESSES:
            status = self.get_process_status(p['systemctl'])
            report += f"{p['display']}: {status}\n"
        return report

    # Before adding a new process to check, add the command to visudo, like:
    # rhidra ALL=(ALL) NOPASSWD: /bin/systemctl status sonarr
    def get_process_status(self, process_name):
        try:
            cmd = ['systemctl', 'status', process_name]
            self.logger.info(f"Running: {' '.join(cmd)}")
            output = subprocess.check_output(cmd, universal_newlines=True)

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