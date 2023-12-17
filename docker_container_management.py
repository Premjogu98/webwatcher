import requests_unixsocket,datetime,logging,time,datetime,re
from main.db_connection import DbConnection
from main.env_handler import EnvHandler
from main.db_connection.query_handler import QueryHandler
from main.logger import console_logger
import random

class DockerManagement:

    def __init__(self) -> None:
        DATABASE_DETAILS = EnvHandler.DB_CONNECTION
        self.dbconnection = DbConnection(CONNECTION_DETAILS=DATABASE_DETAILS)
        QUERY_HANDLER = QueryHandler(
            connection=self.dbconnection.connection, cur=self.dbconnection.cur
        )
        query = f"SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy,data.CompareChangedOn, data.LastCompareChangedOn,links.tender_link FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';"
        status, data = QUERY_HANDLER.getQueryAndExecute(query=query, fetchall=True)
        if not status:
            raise Exception
        self.data_count = len(data)
        console_logger.info(f"DATA COUNT : {self.data_count}")
        self.session = requests_unixsocket.Session()
        self.docker_api_url = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
        self.container_running_details = {}
        self.container_stoped_details = {}
        self.startime = None
        self.batch_size = None
        self.group_id = random.randint(1000000000000000, 9999999999999999)
        console_logger.debug(self.group_id)

    def createContainer(self,container_count,offset, limit,threads,frozen=False):
        if frozen:
            container_name = f"{container_count}-{offset}-{limit}-frozen-restored"
        else:
            container_name = f"{container_count}-{offset}-{limit}"
        console_logger.debug(f"container Name: {container_name}")

        volumes = [
            "/home/gts/web-watcher/htmldocs:/home/gts/code/htmldocs",
            "/home/gts/web-watcher/main:/home/gts/code/main",
            "/home/gts/web-watcher/logs:/home/gts/code/logs",
            "/home/gts/web-watcher/run.py:/home/gts/code/run.py",
            "/etc/localtime:/etc/localtime:ro",
            "/etc/timezone:/etc/timezone:ro",
            "/dev/shm:/dev/shm"
        ]
        envs = [
            f"DB_DATA_LIMIT={limit}",
            f"DB_DATA_OFFSET={offset}",
            f"THREAD={threads}",
            f"GROUP_ID={self.group_id}",
            f"CONTAINER_NAME={container_name}"
        ]
        container_create_data = {
            # "Image": "playwight:0.0.1", #web-watcher:0.0.1
            "Image": "web-watcher:0.0.1", #
            # "Cmd": ["pip3","install", "cdifflib","python", "run.py"],
            "Cmd": ["/bin/bash", "-c", "pip3 install cdifflib && python run.py"],
            
            "Env": envs,
            "HostConfig": {
                "Binds": volumes,
                # "Memory": 524288000,  # 500mb
                "Memory": 1073741824,  # 1GB
                # "MemorySwap": 0,
                # "NanoCpus": 900000000,
                
                "NetworkMode":"host"
            },
        }
        
        response = self.session.post(f"{self.docker_api_url}/containers/create?name={container_name}", json=container_create_data)
        console_logger.debug(response.status_code)
        console_logger.debug(response.json())
        container_id = response.json()["Id"]
        self.session.post(f"{self.docker_api_url}/containers/{container_id}/start")
        console_logger.debug(f"{offset}-{limit} STARTED")
        # time.sleep(10)
        self.container_running_details[container_id] = {"start_time":self.getCurrentTime(),"end_time":""}
    
    def remove_from_dict(self,container_id):
        if self.container_running_details.get(container_id):
            self.container_running_details.pop(container_id)
            
    def stop_and_remove_all_containers(self,container_id=None):
        if not container_id:
            response = self.session.get(f"{self.docker_api_url}/containers/json?all=1")
            containers = response.json()
            for container in containers:
                container_id = container["Id"]
                if "nginx" not in container["Names"][0]:
                    console_logger.debug(container["Names"])
                    self.stop_container(container_id)
                    self.delete_container(container_id)
                console_logger.info(f"STOPED AND DELETED CONTAINER {container_id}")
                # container_info = self.get_container_start_end_time(container_id)
                # self.container_stoped_details[container_id] = container_info
                # console_logger.info(f"Stopping and removing container: {container_id}")
                # self.stop_container(container_id)
                # self.delete_container(container_id)

            console_logger.info("All containers stopped and removed.")
            console_logger.info(self.container_stoped_details)
        else:
            container_data = self.get_container_start_end_time(container_id)
            self.delete_container(container_id)
            if self.container_running_details.get(container_id):
                self.remove_from_dict(container_id)
            self.container_stoped_details[container_id] = container_data

    def is_container_running(self,container_id):
        container_info = self.get_container_info(container_id)
        if container_info:
            if not container_info["State"]["Running"]:
                self.stop_and_remove_all_containers(container_id)
            else:
                if self.is_container_frozen(container_id):
                    self.get_docker_container_logs_and_create_new_container(container_id)
        else:
            console_logger.debug(f"Failed to inspect container with ID {container_id}.")
    
    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_process(self,container_limit,batch_size,total_thread):
        self.startime = self.getCurrentTime()
        self.batch_size = batch_size
        container_count = 0
        offset = 0
        while True:
            if container_count != container_limit:
            # if offset <= self.data_count:
                self.createContainer(container_count=container_count,offset=offset,limit=batch_size,threads=total_thread)
                offset += batch_size
                console_logger.info(f"OFFSET = {offset} | TOTAL DATA: {self.data_count}")
                container_count += 1
                continue
            else:
                break
        
    def monitor_containers(self):
        while True:
            try:
                response = self.session.get(f"{self.docker_api_url}/containers/json?all=1")
                containers = response.json()
                for container in containers:
                    self.is_container_running(container["Id"])
                if len(self.container_running_details) == 0:
                    console_logger.info(self.container_stoped_details)
                    self.update_webwatcher_monitor_log()
                    break
            except KeyboardInterrupt:
                break

    def insert_webwatcher_monitor_log(self):
        query = f"""INSERT INTO dms_wpw_bot_run_log (total_data, batch_run, docker_containers, start_time) VALUES ({self.data_count},{self.batch_size},{len(self.container_running_details)},"{self.startime}");"""
        self.dbconnection.executeQuery(query=query)
        console_logger.info("*** DB INSERTED ***")

    def update_webwatcher_monitor_log(self):
        status,data = self.dbconnection.getQueryAndExecute("SELECT * FROM dms_wpw_bot_run_log ORDER BY entry_date DESC LIMIT 1;",fetchall=True)
        if status:
            query = f"""UPDATE dms_wpw_bot_run_log SET end_time="{self.getCurrentTime()}";"""
            self.dbconnection.executeQuery(query=query)
            console_logger.info("*** DB UPDATED ***")
        else:
            console_logger.debug(f"Data Not found {status} {data}")

    def stop_container(self,container_id):
        self.session.post(f"{self.docker_api_url}/containers/{container_id}/stop")
    
    def delete_container(self,container_id):
        self.session.delete(f"{self.docker_api_url}/containers/{container_id}")

    def get_docker_container_logs_and_create_new_container(self,container_id):
        num_lines = 20
        params = {
            'stdout': True,
            'stderr': True,
            'tail': num_lines,
            'follow': False,
        }
        response = self.session.get(f'{self.docker_api_url}/containers/{container_id}/logs', params=params)
        
        if response.status_code == 200:
            logs = response.text
            onlytext = re.sub("\s\s+" , " ",logs.replace('\n',' ').replace('\t',' '))
            count = re.findall(r"Total : (.*?) \|", onlytext, re.DOTALL)
            if count:
                console_logger.debug(f"LOGS Total : {count}")
                remaining = int(count[-1].partition("/")[0].strip())
                total = int(count[-1].partition("/")[2].strip())
                console_logger.debug(f"remaining : {remaining}")
                console_logger.debug(f"total : {total}")
                if total == remaining:
                    self.stop_container(container_id)
                    self.delete_container(container_id)
                    self.remove_from_dict(container_id)
                    console_logger.info(f"Stopping and removing container: {container_id}")
                    return True
                response = self.session.get(f"{self.docker_api_url}/containers/{container_id}/json")
                DB_DATA_OFFSET = next((int(i.replace("DB_DATA_OFFSET=","")) for i in response.json()["Config"]["Env"] if "DB_DATA_OFFSET" in i),False)
                DB_DATA_LIMIT = next((int(i.replace("DB_DATA_LIMIT=","")) for i in response.json()["Config"]["Env"] if "DB_DATA_LIMIT" in i),False)
                MAIN_DB_DATA_OFFSET = remaining - DB_DATA_OFFSET
                if MAIN_DB_DATA_OFFSET < 0:
                    MAIN_DB_DATA_OFFSET = DB_DATA_OFFSET - remaining
                MAIN_DB_DATA_LIMIT = DB_DATA_LIMIT - remaining
                if MAIN_DB_DATA_LIMIT < 0:
                    MAIN_DB_DATA_LIMIT = remaining - DB_DATA_LIMIT
                console_logger.debug(f"DB_DATA_OFFSET : {DB_DATA_OFFSET}")
                console_logger.debug(f"DB_DATA_LIMIT : {DB_DATA_LIMIT}")
                console_logger.debug(f"MAIN_DB_DATA_OFFSET : {MAIN_DB_DATA_OFFSET}")
                console_logger.debug(f"MAIN_DB_DATA_LIMIT : {MAIN_DB_DATA_LIMIT}")
                self.createContainer(offset=MAIN_DB_DATA_OFFSET,limit=MAIN_DB_DATA_LIMIT,threads=2,frozen=True)
                if self.container_running_details.get(container_id,None):
                    self.remove_from_dict(container_id) # old container log delete
                try:
                    self.stop_container(container_id)
                    self.delete_container(container_id)
                    self.remove_from_dict(container_id)
                except :
                    console_logger.debug(f"Failed to stop or delete container {container_id}")
        else:
            console_logger.error(f"Failed to retrieve logs. Status code: {response.status_code}")
        return False

    def convert_to_local_time(self,time_str, time_format):
        input_time = datetime.datetime.strptime(time_str, time_format)
        local_timezone = datetime.timezone(datetime.timedelta(seconds=-time.timezone))
        local_time = input_time.replace(tzinfo=datetime.timezone.utc).astimezone(local_timezone)
        return local_time
    
    def get_container_info(self,container_id):
        response = self.session.get(f"{self.docker_api_url}/containers/{container_id}/json")
        if response.status_code == 200:
            container_info = response.json()
            return container_info
        return None
    
    def get_container_start_end_time(self,container_id):
        container_info = self.get_container_info(container_id)
        if container_info['State']['OOMKilled']:
            if not self.get_docker_container_logs_and_create_new_container(container_id):
                return {}
        start_time_str = container_info['State']['StartedAt']
        end_time_str = container_info['State']['FinishedAt']
        console_logger.debug(f'{container_info["Name"]} start_time_str : {start_time_str}')
        console_logger.debug(f'{container_info["Name"]} end_time_str : {end_time_str}')
        if start_time_str:
            start_time_str = start_time_str.partition(".")[0].replace("T"," ").replace("Z","")
            console_logger.debug(f'{container_info["Name"]} start_time_str : {start_time_str}')
            start_time = self.convert_to_local_time(start_time_str, "%Y-%m-%d %H:%M:%S")
        if end_time_str:
            end_time_str = end_time_str.partition(".")[0].replace("T"," ").replace("Z","")
            console_logger.debug(f'{container_info["Name"]} end_time_str : {end_time_str}')
            end_time = self.convert_to_local_time(end_time_str, "%Y-%m-%d %H:%M:%S")
            time_difference = end_time - start_time

        return {"container_name":container_info["Name"],"start_time":datetime.datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S"),"end_time":datetime.datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S"),"difference":str(time_difference)}

    def get_container_stats(self,container_id):
        response = self.session.get(f"{self.docker_api_url}/containers/{container_id}/stats?stream=false")
        stats = response.json()
        return stats

    def is_container_frozen(self,container_id, interval=10, threshold=5):
        prev_cpu = 0
        prev_mem = 0
        try:
            for _ in range(threshold):
                stats = self.get_container_stats(container_id)
                console_logger.debug(stats)
                if stats['cpu_stats'].get('system_cpu_usage'):
                    cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
                elif stats['precpu_stats'].get("system_cpu_usage"):
                    cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['precpu_stats']['system_cpu_usage'] * 100
                else:
                    self.delete_container(container_id)
                    self.remove_from_dict(container_id)
                    console_logger.info(f"Container Removed {stats['name']} had no system_cpu_usage used stats")
                    return False
                if stats['memory_stats'].get('usage'):
                    mem_usage = stats['memory_stats']['usage']
                else:
                    self.delete_container(container_id)
                    self.remove_from_dict(container_id)
                    console_logger.info(f"Container Removed {stats['name']} had no memory used stats")
                    return False
                console_logger.info(f"{stats['name']} cpu_percent {cpu_percent}")
                console_logger.info(f"{stats['name']} mem_usage {mem_usage}")
                console_logger.info(abs(cpu_percent - prev_cpu))
                console_logger.info(abs(mem_usage - prev_mem))
                console_logger.info((50 * 1024 * 1024))
                if round(abs(cpu_percent - prev_cpu),2) > 0.05 or abs(mem_usage - prev_mem) > (60 * 1024 * 1024): # less than 50 mb 
                    return False
                prev_cpu = cpu_percent
                prev_mem = mem_usage
                time.sleep(interval)
            console_logger.info(f"The {stats['name']} container is frozen")
            return True
        except Exception as e:
            console_logger.error(f"\n\n{e}\n\n")
            return False

if __name__ == "__main__":
    ObjDockerManagement = DockerManagement()
    ObjDockerManagement.stop_and_remove_all_containers()
    # time.sleep(5)
    # ObjDockerManagement.start_process(container_limit=50,batch_size=1000,total_thread=2)
    # time.sleep(60)
    # # ObjDockerManagement.insert_webwatcher_monitor_log()
    # # console_logger.debug("1 hr sleep after monitor")
    # time.sleep(3600)
    # ObjDockerManagement.monitor_containers()
    
