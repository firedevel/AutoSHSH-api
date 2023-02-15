import SHSHdata as sd
import os,shutil,filecmp
import requests
import json,sys

if (not os.path.exists('./saved')):
    os.mkdir('./saved')

#fetchone(): ('11d02e4c-7946-462a-9f96-daff19ae178b', 'iTest1,1', 'testap', '000000000000002E', '0.0', '{}')
def saveOnce(id):
    #用于备份一次指定设备
    data = sd.getDevice(id)
    if (not os.path.exists(f'./saved/{id}')):
        os.mkdir(f'./saved/{id}')
    downloadConfig()
    with open('/tmp/firmware.json','r') as j:
        fjson = json.loads(j.read())['devices'][data[1]]
    for i in fjson['firmwares']:
        #如果验证开着且没有备份过
        if ((i['signed'] == True) and (not os.path.exists(f'./saved/{id}/{i["version"]}'))):
            os.mkdir(f'./saved/{id}/{i["version"]}')
            os.system(f'./tsschecker -d {data[1]} -B {data[2]} -e {data[3]} -i {i["version"]} --save-path ./saved/{id}/{i["version"]} -s')
            try:
                sd.writeSHSH(id,i["version"],f'./saved/{id}/{i["version"]}/%s'%os.listdir(f"./saved/{id}/{i['version']}/")[0])
            except:
                #当没签名没文件时
                os.removedirs(f'./saved/{id}/{i["version"]}')
    max = fjson['firmwares'][0]["version"]#最高版本
    sd.writeMax(id,max)


    
    
    

def downloadConfig():
    if (os.path.exists('./firm.json')):
        shutil.move('./firm.json','./oldfirm.json')
    downloadFile('http://app4.i4.cn/getFirmwareiosList.xhtml','./firm.json')#爱思所有iOS版本接口
    if ((not os.path.exists('/tmp/firmware.json')) or (not filecmp.cmp('./firm.json','oldfirm.json'))):
        downloadFile('https://api.ipsw.me/v2.1/firmwares.json/condensed','./tmp/firmware.json')
        return True
    else:
        return False
    
def downloadFile(url,out):
    r = requests.get(url, stream = True)
    with open(out, "wb") as f:
        for chunk in r.iter_content(chunk_size = 1024): # 1024 bytes
            if chunk:
                f.write(chunk)  

def saveAll():
    downloadConfig()
    with open('/tmp/firmware.json','r') as aj:
        alljson = json.loads(aj.read())
        for nowData in sd.getAll():
            #用于备份一次指定设备
            fjson = alljson['devices'][nowData[1]]

            if (not os.path.exists(f'./saved/{nowData[0]}')):
                os.mkdir(f'./saved/{nowData[0]}')
                #上文with open
            for i in fjson['firmwares']:
                #如果验证开着且没有备份过
                if ((i['signed'] == True) and (not os.path.exists(f'./saved/{nowData[0]}/{i["version"]}'))):
                    os.mkdir(f'./saved/{nowData[0]}/{i["version"]}')
                    os.system(f'./tsschecker -d {nowData[1]} -B {nowData[2]} -e {nowData[3]} -i {i["version"]} --save-path ./saved/{nowData[0]}/{i["version"]} -s')
                    sd.writeSHSH(nowData[0],i["version"],f'./saved/{nowData[0]}/{i["version"]}/%s'%os.listdir(f"./saved/{nowData[0]}/{i['version']}/")[0])
            if (not fjson['firmwares'][0]["version"] == nowData[4]):
                #如果最高版本不对
                max = fjson['firmwares'][0]["version"]#最高版本
                sd.writeMax(nowData[0],max)

if __name__ == '__main__':
    #如果被手动运行
    def showHelp():
        for info in [
            ("-a, --all","Save all devices's SHSH in database."),
            ("-u, --uuid","Save devices who has uuid match."),
            ("-h, --help","Show this page.")
        ]:
            print('    %-30s%-0s' %info) #'%-30s' 含义是 左对齐，且占用30个字符位 
    for index,val in enumerate(sys.argv):
        match val:
            case '-a' | '--all':
                saveAll()
                print("=========================\n  Succes!\n=========================")
                os._exit(0)
            case '-u' | '--uuid':
                #获取-u后面的参数
                saveOnce(sys.argv[index+1])
                print("=========================\n  Succes!\n=========================")
                os._exit(0)
            case '-h' | '--help':
                showHelp()
    #当匹配不成功，没有exit时
    print("Unknown argument!")
    showHelp()


    
