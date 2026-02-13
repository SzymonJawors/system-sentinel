import psutil
import datetime
import time
import logging

def setup_logger(name, log_file, level=logging.INFO):

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)


    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger


process_logger = setup_logger('process_monitor', 'processes.log')
network_logger = setup_logger('network_monitor', 'network.log')

def check_process(threshold=5.0):
    process_logger.info(f"--- Process Audit: {datetime.datetime.now()} ---")
    
    for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            process_name = proc.info['name']
            process_pid = proc.info['pid'] #process id
            cpu_usage = proc.info['cpu_percent']
            
            if cpu_usage > threshold:
                process_logger.warning(f"[WARNING] High CPU: {process_name} (PID: {process_pid}) - Usage: {cpu_usage}%")
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
def check_network():
    network_logger.info(f"--- Network Audit: {datetime.datetime.now()} ---")
    
    connections = psutil.net_connections(kind="inet") #ipv4 ipv6
    
    for conn in connections:
        if conn.status == 'LISTEN':
            port = conn.laddr.port # (local addres )(laddr)
            ip = conn.laddr.ip
            network_logger.info(f"[OK] Port Listening: {port} on IP: {ip}")
            if port == 4444:
                network_logger.error("!!! [CRITICAL] Potential Malicious Port 4444 detected!")
                
def main():
    print("System Sentinel Started.")
    
    try:
        while True:
            check_process(threshold=10.0)
            check_network()
            print("\nWaiting 10 s for next scan... \n")
            time.sleep(10)
    
    except KeyboardInterrupt: # ctrl c
        print("\nSentinel shutting down.")

if __name__ == "__main__":
    main()