import requests_unixsocket
import json
import time

CONTAINER_LOGS_FILE = 'container_logs.txt'
DOCKER_API_VERSION = 'v1.41'  # Change this to match your Docker API version

def get_containers():
    url = f'http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/json?all=1'
    session = requests_unixsocket.Session()
    response = session.get(url)
    containers = response.json()
    return containers

def monitor_containers():
    while True:
        containers = get_containers()
        # print(containers)
        for container in containers:
            container_id = container['Id'][:12]
            container_name = container['Names'][0]
            container_status = container['State']
            if container_status != 'running':
                print(container)
            # break
            if "nginx" not in container_name:
                with open(CONTAINER_LOGS_FILE, 'a') as log_file:
                    if container_status != 'running':
                        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        log_file.write(f"Container {container_name} (ID: {container_id}) started at {start_time}\n")
                    else:
                        end_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        log_file.write(f"Container {container_name} (ID: {container_id}) stopped at {end_time}\n")
            
        # time.sleep(10)  # Adjust the interval as needed

if __name__ == "__main__":
    monitor_containers()
