from tool import json_post,read_cfg,write_cfg,host_timedb
import tornado.httpclient
import datetime

def get_item(data, key):
    if key in data:
        return data[key]
    return None

def get_data(client, tab, cfg):
    st = None
    if tab in cfg:
        st = cfg[tab]

    if st is None:
        info = json_post(client, host_timedb(), {
            "cmd": "get/first",
            "data": {
                "tab": tab,
                "orig": "true",
                "obj": "*"
            }
        })
    else:
        info = json_post(client, host_timedb(), {
            "cmd": "get/start",
            "data": {
                "tab": tab,
                "limit": 20,
                "start": st,
                "orig": "true",
                "nostart": "true",
                "obj": "*"
            }
        })

    if info is not None:
        if isinstance(info, str):
            print("str")

        elif isinstance(info, list):
            print("list")
            for i in range(len(info)):
                data1 = info[i][tab]
                if "start" in data1 and "end" in data1 and "data" in data1:
                    print(data1["start"])
                    print(data1["end"])
                    print(data1["data"])

                    cfg[tab] = data1["end"]
                    return data1["data"]

        elif isinstance(info, dict):
            print("dict")
            data1 = info[tab]
            if "start" in data1 and "end" in data1 and "data" in data1:
                print(data1["start"])
                print(data1["end"])
                print(data1["data"])

                cfg[tab] = data1["end"]
                return data1["data"]

    return None

def post_stnstatusdata(client, cfg):
    data = get_data(client, "IPC_OP220_H", cfg)

    return

    serialNumber = get_item(data,u"psn")
    partNo = get_item(data,u"msn")
    workOrderNo = get_item(data, u"sn")
    ProndLineCode = "PL02"
    stationCode = get_item(data, u"wsn")
    stationPassType = 1
    siteCode = "3310"
    userNo = "AMES"
    time = datetime

    senddata = {

    }

def do_post_cmd(cmd,n):
    client = tornado.httpclient.HTTPClient()

    cfg = read_cfg()
    if cfg is None:
        cfg = {}
    if cmd == "stnstatus":
        post_stnstatusdata(client, cfg)
    # elif cmd == "packtighten":
    #     post_packtighten(client, cfg)
    # elif cmd == "packleaktest":
    #     post_packleaktest(client, cfg)
    # elif cmd == "packweight":
    #     post_packweight(client, cfg)
    client.close()
    write_cfg(cfg)

def do_task():
    do_post_cmd("stnstatus", None)