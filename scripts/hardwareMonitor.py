import threading
import time
import psutil


def check_cpu_usage(interval: int) -> float:
    return psutil.cpu_percent(interval=interval)


def check_ram_usage() -> float:
    return psutil.virtual_memory().percent


def hw_monitor():
    while True:
        cpu_usage = check_cpu_usage(1)
        ram_usage = check_ram_usage()
        print(f'Cpu usage: {cpu_usage}')
        print(f'Ram usage: {ram_usage}')
        time.sleep(1)


def start_hw_mon_thread():
    hw_mon_thread = threading.Thread(target=hw_monitor)
    hw_mon_thread.daemon = True
    hw_mon_thread.start()
