import subprocess

class SystemMonitoring:
    @staticmethod
    def get_system_uptime():
        try:
            uptime = subprocess.check_output(["uptime"], universal_newlines=True)
            return uptime.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    @staticmethod
    def get_cpu_usage():
        try:
            top_output = subprocess.check_output(["top", "-bn1"], universal_newlines=True)
            cpu_usage = [line for line in top_output.splitlines() if line.startswith("%Cpu(s):")]
            return cpu_usage[0]
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    @staticmethod
    def get_memory_usage():
        try:
            free_output = subprocess.check_output(["free", "-m"], universal_newlines=True)
            memory_usage = [line for line in free_output.splitlines() if line.startswith("Mem:")]
            return memory_usage[0]
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
