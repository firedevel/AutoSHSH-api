import SHSHdata as sd #封装数据库操作
import SHSHsaver as ss #封装文件操作
import UserManager as um
from fastapi import FastAPI
from starlette.responses import FileResponse
from pydantic import BaseModel
import re,json
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class iDevices(BaseModel):
    model: str = "iTest1,1"
    board: str = "testap"
    ecid: str = "000000000000002E"
    token = ""

@app.post("/new_device")
def new_device(dev: iDevices):
    if(um.verify(dev.token,1)):
        if (
            #判断输入是否合规，防止注入
            #dev.board.lower(),dev.ecid.upper() 统一大/小写格式
            re.search('^[a-z,A-Z]*[0-9]*,[0-9]$', dev.model) and
            re.search('^[a-z,0-9]*$', dev.board.lower()) and 
            re.search('^[A-Z,0-9]{16}$', dev.ecid.upper())
        ):
            print(dev)
            if (sd.isDevice(dev.model,dev.board.lower(),dev.ecid.upper()) == False):
                #如果数据库中没有
                uuid = sd.addDevice(dev.model,dev.board.lower(),dev.ecid.upper())
                ss.saveOnce(uuid)
                return {"status": "success", "uuid": uuid}
            else:
                #如果已存在
                return {"status": "failed","reason":"alredy"}
        else:
            #如果输入不合法
            return {"status": "failed","reason":"input-invalid"}
    else:
        return {"result": "error", "reason":"access-denied"}


@app.get("/device_info")
def device_info(model: str, baord: str, ecid: str, token=""):
    if(um.verify(token,1)):
        result = sd.getDevice(model,baord.lower(),ecid.upper())
        if result != "not found":
            return {
                "status": "success",
                "id": result[0],
                "model": result[1],
                "board": result[2],
                "ecid": result[3],
                "max_version": result[4],
                "file_json": result[5]
            }
        else:
            return{
                "status": "error", "reason": result
            }
    else:
        return {"result": "error", "reason":"access-denied"}
@app.get("/down_shsh/{id}_{version}")
def device_info(id: str, version: str, token=""):
    if(um.verify(token,1)):
        print(id)
        result = sd.getID(id)
        if result != "not found":
            return FileResponse(json.loads(result[5])[version]['path'])
        else:
            return{
                "status": "error", "reason": result
            }
    else:
        return {"result": "error", "reason":"access-denied"}

@app.get("/delete_device")
def delete_device(id: str, key=""):
    if(um.verify(key,2)):
        sd.delDevice(id)
        return {"result": "success"}
    else:
        return {"result": "error", "reason":"access-denied"}
    

@app.get("/device_list")
def device_list(key=""):
    list = []
    if(um.verify(key,2)):
        for d in sd.getAll():
            list.append({
                "id": d[0],
                "model": d[1],
                "board": d[2],
                "ecid": d[3],
                "max_version": d[4]
            })
        return {"result": "success", "deviceList": list}
    else:
        return {"result": "error", "reason":"access-denied"}


