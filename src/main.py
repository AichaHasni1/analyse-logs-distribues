import socket
import time
import json
import random

LOGSTASH_HOST = "localhost"
LOGSTASH_PORT = 5000

levels = ["INFO", "WARNING", "ERROR", "DEBUG"]

def generate_log():
    return {
        "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "level": random.choice(levels),
        "message": "Log message from Python script",
        "service": "my-python-app"
    }

def send_log(log):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        sock.sendall((json.dumps(log) + "\n").encode("utf-8"))
        sock.close()
    except Exception as e:
        print(f"Erreur d'envoi vers Logstash : {e}")

if __name__ == "__main__":
    print("📤 Envoi de logs vers Logstash...")
    while True:
        log = generate_log()
        send_log(log)
        print(f"Envoyé : {log}")
        time.sleep(2)  # envoie un log toutes les 2 secondes
