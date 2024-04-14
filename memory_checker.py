import psutil
import requests
import time
import uuid
import os

API_URL = 'http://localhost:8080/flaskapp/api/data'
MEMORY_THRESHOLD = 70
UUID_FILE = "UUID.txt"


def check_memory_usage():
    memory_percent = psutil.virtual_memory().percent
    return memory_percent

def get_uuid_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                try:
                    return str(uuid.UUID(line.strip()))
                except ValueError:
                    pass
    return None

def generate_and_save_uuid(filename):
    new_uuid = str(uuid.uuid4())
    with open(filename, 'a') as file:
        file.write(new_uuid + '\n')
    return new_uuid


def send_alarm(host_id):
    data = {"key": host_id, "value": f"Memory usage exceeded threshold {MEMORY_THRESHOLD}%"}

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            print("Alarm sent successfully!")
        else:
            print("Failed to send alarm. Status code:", response.status_code)
    except Exception as e:
        print("Failed to send alarm:", e)

def main():
    while True:
        memory_percent = check_memory_usage()
        print(memory_percent)
        if memory_percent > MEMORY_THRESHOLD:
            uuid = get_uuid_from_file(UUID_FILE)
            if uuid is None:
               uuid = generate_and_save_uuid(UUID_FILE)
            send_alarm(host_id=uuid)

        time.sleep(10)

if __name__ == "__main__":
    main()
