import subprocess

from log import set_up_logger

MOUNT_POINT = '/mnt/media'

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
        "systemctl": "transmission-daemon.service",
        "display": "Transmission"
    }, {
        "id": "openvpn",
        "systemctl": "openvpn@cdg-001.service",
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

    def map2emoji(status):
        emoji_mapping = {
            ProcessStatus.RUNNING: "🟢",
            ProcessStatus.INACTIVE: "⚫",
            ProcessStatus.OTHER: "🔴",
        }
        return emoji_mapping.get(status, "🔴")


class SystemMonitoring:
    def __init__(self, verbose=False, console_logging=False):
        self.logger = set_up_logger("searcharr.system", verbose, console_logging)

    def generate_processs_status_report(self):
        report = 'Media Server Dashboard\n\n'
        report += f"Uptime: {self.get_system_uptime()}\n\n"
        report += 'Process Status:\n'

        for p in PROCESSES:
            status = self.get_process_status(p['systemctl'])
            report += f"- {ProcessStatus.map2emoji(status)} {p['display']}\n"
        
        report += '\nDisk Status:\n'
        if not self.check_disk_mounted():
            report += '- 🔴 Disk not mounted correctly !\n'
        else:
            report += '- 🟢 Disk mounted\n'
            total, used, available, percent_used = self.get_disk_usage()
            report += f"- Disk space usage: {used} / {total} ({percent_used})\n"
            report += f"- Disk space available: {available}\n"
        return report
    
    def get_system_uptime(self):
        try:
            cmd = ["uptime", "-p"]
            self.logger.info(f"Running: {' '.join(cmd)}")
            uptime = subprocess.check_output(cmd, universal_newlines=True).strip()[3:]
            return uptime
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error: {e}")
            return 'Error'
        
    def check_disk_mounted(self):
        try:
            cmd = ['findmnt', '-n', '-o', 'SOURCE', '--target', MOUNT_POINT]
            self.logger.info(f"Running: {' '.join(cmd)}")
            output = subprocess.check_output(cmd, universal_newlines=True)
            return "/dev/sdc2" in output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error check_disk_mounted: {e}")
            return False
    
    def get_disk_usage(self):
        try:
            cmd = ['df', '-h', MOUNT_POINT]
            self.logger.info(f"Running: {' '.join(cmd)}")
            output = subprocess.check_output(cmd, universal_newlines=True).strip().split('\n')
            fields = output[1].split()
            if len(fields) != 6:
                self.logger.error("Unexpected 'df' output format")
                raise Exception("Unexpected 'df' output format")
            
            filesystem, total, used, available, percent_used, mounted_on = fields
            return total, used, available, percent_used
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error get_disk_usage: {e}")
            raise e
    
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
            self.logger.error(f"Error get_process_status: {e}")
            return ProcessStatus.OTHER

    def run_start_script(self):
        try:
            cmd = ['sh', '/home/rhidra/start.sh']
            self.logger.info(f"Running: {' '.join(cmd)}")
            subprocess.check_output(cmd, universal_newlines=True)
            self.logger.info("Done running the start script")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error: {e}")
            return False