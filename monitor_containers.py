import docker
import datetime
import pytz
import secrets
import string,random

client = docker.DockerClient(base_url='unix://var/run/docker.sock')



def convert_to_local_time(utc_time):
    # Convert UTC time to datetime object
    utc_time = utc_time[:26]  # Truncate the string to 26 characters
    datetime_obj = datetime.datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%f')

    # Convert to UTC timezone
    utc_timezone = pytz.timezone('UTC')
    datetime_obj = utc_timezone.localize(datetime_obj)

    # Convert to local timezone
    local_timezone = pytz.timezone('Asia/Kolkata')  # Replace with your local timezone
    local_time = datetime_obj.astimezone(local_timezone)
    return local_time

def generate_random_password(length=20):
    characters = string.digits  # This includes numbers 0-9
    print(characters)
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_container_start_stop_events():
    for container in client.containers.list(filters={"status": "exited"}):
        print(container.name)
        container_info = container.attrs

        start_time = container_info['State']['StartedAt']
        end_time = container_info['State']['FinishedAt']

        local_start_time = convert_to_local_time(start_time)
        local_end_time = convert_to_local_time(end_time)

        time_diff = local_end_time - local_start_time
        
        print(f"Start time (local) of container '{container.name}': {local_start_time.strftime('%Y-%m-%d %I:%M:%S')}")
        print(f"End time (local) of container '{container.name}': {local_end_time.strftime('%Y-%m-%d %I:%M:%S')}")
        print(f"Duration of container '{container.name}': {round(time_diff.total_seconds() / 60)} MINUTE")
        # break




if __name__ == "__main__":
    get_container_start_stop_events()
