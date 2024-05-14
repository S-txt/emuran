from fastapi import FastAPI
import os
import subprocess
import threading

app = FastAPI()

base_cmd = '../UERANSIM/build/'
base_ue_config = '../UERANSIM/config/free5gc-ue.yaml'

cli = f'{base_cmd}nr-cli'
ue = f'{base_cmd}nr-ue'

@app.get("/ue/info/{ue_imsi}")
async def get_ue_info(ue_imsi):
    result = subprocess.Popen([cli, ue_imsi, '--exec', '"info"'], stdout = subprocess.PIPE)
    output = str(result.communicate()) 
    return {"message": output}

@app.get("/ue/set/{ue_imsi}")
async def create_ue(ue_imsi: str, n: int = 0):
    if n <= 0:
        n = 1
    def startUE():
        print(f'starting UEs {n}')
        print(['sudo', ue, '-c', base_ue_config, '-n', str(n), '-i', ue_imsi])
        result = subprocess.Popen([f'sudo {ue} -c {base_ue_config} -n {n} -i {ue_imsi}'], shell=True)
    print('start Thread')
    threading.Thread(target=startUE).start()
    print('all UE started')
    return {"message": 'all UE started'}