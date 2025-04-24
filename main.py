from scripts.promptConnection import start_server_thread, start_prompts
from scripts.hardwareMonitor import start_hw_mon_thread

start_server_thread()
start_hw_mon_thread()
start_prompts()

