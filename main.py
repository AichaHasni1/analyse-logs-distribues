import time
import random

log_file = "C:/Users/user/Desktop/master fs/sysDIS/project/analyse-logs-distribues/ssh_logs.log"

ips = ["192.168.1.1", "10.0.0.1", "172.16.0.5", "8.8.8.8"]
statuses = ["Accepted", "Failed", "Invalid user"]

while True:
    ip = random.choice(ips)
    status = random.choice(statuses)
    log_line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} SSH {status} for user from {ip}\n"
    
    with open(log_file, "a") as file:
        file.write(log_line)
    
    print(f"Written: {log_line.strip()}")
    time.sleep(2)  # toutes les 2 secondes
