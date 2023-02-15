import os
import json

security = "public"
password = "21232f297a57a5a743894a0e4a801fc3"
if os.path.exists('./config.json'):
    with open('./config.json','rb') as j:
        jsond = j.read()
        security = json.loads(jsond)['security']
        password = json.loads(jsond)['passwd']
else:
    with open('./config.json','w+') as j:
        j.write('''{"security": "public","passwd": "21232f297a57a5a743894a0e4a801fc3"}''')
        

    

def verify(key,mode):
    #mode: 1:不需要验证管理员，2:需要验证管理员
    if mode == 1:
        return True
    else:
        if mode == 2:
            if security == "nas":
                return True
            else:
                if key == password:
                    return True
                else:
                    return False
        return False# 不匹配默认拒绝




