import sqlite3
import uuid
import copy
import json
import time

sql = sqlite3.connect('main.db', check_same_thread=False)
cur=sql.cursor()

sql.execute('''
CREATE TABLE IF NOT EXISTS idevices(
    ID     TEXT,
    Model  TEXT,
    Board  TEXT,
    ECID   TEXT,
    Latest TEXT,
    Data   TEXT
);
''')


def addDevice(model, board ,ecid):
    id4 = copy.deepcopy(uuid.uuid4())
    cur.execute(f"SELECT * FROM idevices WHERE ID='{id4}'")
    #不堆屎，防止uuid重复
    if(cur.fetchall().__len__() == 0):
        cur.execute(f"INSERT INTO idevices VALUES ('{id4}','{model}', '{board}' ,'{ecid}', '0.0','{{}}')")
        sql.commit()
        return id4
    else:
        #递归，有可能造成问题，未测试
        addDevice(model, board ,ecid)

def isDevice(model, board ,ecid):
    cur.execute(f"SELECT * FROM idevices WHERE Model='{model}' AND Board='{board}' AND ECID='{ecid}'")
    if (cur.fetchall().__len__() == 0):
        return False
    else:
        return True

def getDevice(model,board,ecid):
    cur.execute(f"SELECT * FROM idevices WHERE ECID='{ecid}' AND Board='{board}' AND Model='{model}'")
    try:
        return cur.fetchall()[0]
    except:
        #找不到时
        return "not found"
def getID(id):
    cur.execute(f"SELECT * FROM idevices WHERE ID='{id}'")
    try:
        return cur.fetchall()[0]
    except:
        #找不到时
        return "not found"


def getAll():
    cur.execute("SELECT * FROM idevices")
    return cur.fetchall()

def writeSHSH(id,ver,path):
    #fetchone(): ('11d02e4c-7946-462a-9f96-daff19ae178b', 'iTest1,1', 'testap', '000000000000002E', '0.0', '{}')
    cur.execute(f"SELECT * FROM idevices WHERE ID='{id}'")
    data = json.loads(cur.fetchall()[0][5]) #所有的第一个，防止取多次导致报错, 5: Data
    data[ver] = {
        #比如："16.3":{"path": "./saved/[uuid]/16.3.shsh2", "time": "2023/2/13 9:41"}
        "path": path,
        "time": time.strftime('%Y-%m-%d %H:%M', time.localtime())
    }
    cur.execute(f"UPDATE iDevices SET Data = '{json.dumps(data)}' WHERE ID = '{id}' ")
    sql.commit()
def writeMax(id,ver):
    cur.execute(f"UPDATE iDevices SET Latest = '{ver}' WHERE ID = '{id}' ")

def delDevice(id):
    pass