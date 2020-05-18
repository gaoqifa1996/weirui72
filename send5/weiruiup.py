from tool import json_post,host_graphdbget,host_graphdb,host_machine,json_requests_post,read_cfg,write_cfg,host_timedb
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
            "n": tab,
            "obj": "*",
            "opt": {
                "limit": 1
            }
        })

    else:
        info = json_post(client, host_timedb(), {
            "n": tab,
            "obj": "*",
            "opt": {
                "and": [{
                    "ge": "time",
                    "v": st
                }],
                "limit": 20
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
                    for data in data1["data"]:
                        return data

        elif isinstance(info, dict):
            print("dict")
            data1 = info[tab]
            if "start" in data1 and "end" in data1 and "data" in data1:
                print(data1["start"])
                print(data1["end"])
                print(data1["data"])

                cfg[tab] = data1["end"]
                for data in data1["data"]:
                    return data
    return None
######################## get to MES ########################
def get_plan(rec):

    line = get_item(rec, "ProdLineCode")
    sn = get_item(rec, "WorkOrderNo")
    pnum = get_item(rec, "Qty")
    tsn = get_item(rec, "TechnologyNo")
    pstart = get_item(rec, "StartTime")
    pend = get_item(rec, "EndTime")

    print(tsn,sn,pnum,pstart,pend)

    if tsn and sn and pnum and pstart and pend:
        print(tsn,sn,pnum,pstart,pend)
    else:
        return {"Result":False,"Message":"has null value","Resultint":2000}

    if tsn :
        uidinfo = json_requests_post(host_graphdbget(),{
            "n":"tech",
            "obj":"uid,sn",
            "opt":{
                "and":[{
                    "eq":"sn",
                    "v":tsn
                }]
            }
        })
        uid = uidinfo[0]["uid"]
        if not uid:
            return {"Result": False, "Message": "no such Technology", "Resultint": 2000}
        info = json_requests_post(host_graphdb(), {
            "a":[{
            "u":"line-one",
            "n":"task",
            "v":[[
                {"k":"sn","v":sn},
                {"k":"tech","u":uid},
                {"k":"pstart","v":pstart},
                {"k":"pend","v":pend},
                {"k":"pnum","v":pnum},
                {"k":"state","v":"open"},
                {"k":"linecode","v":line}
            ]]
            }]})
        if info == "Success":
            return {"Result": True, "Message": info , "Resultint": 1000}
        else:
            return {"Result": False, "Message": "info error", "Resultint": 2000}


def get_module(rec):
    for i in range(len(rec)):
        prodlinecode = get_item(rec[i], "ProdLineCode")
        modulesn = get_item(rec[i], "ModuleSn")
        voltage = get_item(rec[i],"Voltage")
        maxvoltage = get_item(rec[i], "MaxVoltage")
        minvoltage = get_item(rec[i], "MinVoltage")
        resistance = get_item(rec[i], "Resistance")
        maxresistance = get_item(rec[i], "MaxResistance")
        minresistance = get_item(rec[i], "MinResistance")
        insulationvalue = get_item(rec[i], "InsulationValue")
        leakcurrent = get_item(rec[i], "LeakCurrent")
        singlevoltage = get_item(rec[i], "SingleVoltage")
        voltagediffer = get_item(rec[i], "VoltageDiffer")
        differntc = get_item(rec[i], "DifferNTC")
        resultmsg = get_item(rec[i], "ResultMsg")
        userno = get_item(rec[i], "UserNo")
        timein = get_item(rec[i], "Time")

        if modulesn and resultmsg and timein and voltage and prodlinecode and maxvoltage and minvoltage and resistance and maxresistance and minresistance and insulationvalue and leakcurrent and singlevoltage and voltagediffer and differntc and userno :
            print(modulesn, resultmsg)
        else:
            return {"Result": False, "Message": "has null value", "Resultint": 2000}
        # global recresult
        recresult = json_requests_post(host_machine(),{
            "op010_op010_psn":modulesn,
            "op010_op010_moduleinfo":
                [{
                    "prodlinecode":prodlinecode,
                    "voltage":voltage,
                    "maxvoltage":maxvoltage,
                    "minvoltage":minvoltage,
                    "resistance":resistance,
                    "maxresistance":maxresistance,
                    "minresistance":minresistance,
                    "insulationvalue":insulationvalue,
                    "leakcurrent":leakcurrent,
                    "singlevoltage":singlevoltage,
                    "voltagediffer":voltagediffer,
                    "differntc":differntc,
                    "resultmsg":resultmsg,
                    "userno":userno,
                    "timein":timein
                }]
        })
        # print(recresult)
        if recresult["code"]==1000:
            if i >= len(rec)-1:
                print(recresult)
                return {"Result": True, "Message": "ok", "Resultint": 1000}
        else:
            return {"Result": False, "Message": "send error", "Resultint": 2000}


def get_psn(rec):
    for i in range(len(rec)):
        sn = get_item(rec[i],"WorkOrderNo")
        psn = get_item(rec[i],"SerialNumber")

        if sn and psn:
            print(sn,psn)
        else:
            return {"Result": False, "Message": "has null value", "Resultint": 2000}

        uidinfo = json_requests_post(host_graphdbget(),{

            "n":"task",
            "obj":"uid,sn",
            "opt":{
                "and":[{
                    "eq":"sn",
                    "v":sn
                }]
            }
        })
        uid = uidinfo[0]["uid"]
        # psnresult = json_requests_post("http://47.96.151.120/graphdb/md",{
        psnresult = json_requests_post(host_graphdb(), {
            "a":[{
                "v":[[{
                    "k":"sn",
                    "v":psn
                }]],
            "u":uid,
            "n":"pcode"
            }]
        })
        print(psnresult)
        if psnresult == "Success":
            if i >= len(rec)-1:
                print(i)
                return {"Result": True, "Message": "ok", "Resultint": 1000}
        else:
            return {"Result": False, "Message": "send error", "Resultint": 2000}


def get_snstatus(rec):
    for i in range(len(rec)):
        sn = get_item(rec[i], u"WorkOrderNo")
        status = get_item(rec[i], u"Status")

        status_list=["open","close"]   # only support such
        if status not in status_list:
            print(status)
            return {"Result": False, "Message": "Error no such status", "Resultint": 2000}
        # info = json_requests_post("http://47.96.151.120/graphdb/get/line-two",{
        info = json_requests_post(host_graphdbget(), {
            "n": "task",
            "obj": "sn,uid,state",
            "opt": {
    	    "and":  [
            {
                "eq": "sn",
                "v": sn
            }]
            }
        })
        print(info)
        state = get_item(info[0],"state")
        uid = get_item(info[0],"uid")
        if status == state:
            if i >= len(rec)-1:
                return {"Result": True, "Message": "ok", "Resultint": 1000}
        else:
            # data = json_requests_post("http://47.96.151.120/graphdb/md",{
            data = json_requests_post(host_graphdb(), {
            "m": [
             {
            "u": uid,
            "v": [
                {
                    "k": "sn",
                    "v": sn
                },
                {
                    "k": "state",
                    "v": status
                }
                ]}
            ]
            })
            print(data)
            if data == "Success":
                if i >= len(rec)-1:
                    return {"Result": True, "Message": "ok", "Resultint": 1000}
            else:
                return {"Result": False, "Message": "error", "Resultint": 2000}





####################### post to MES ########################
def post_packstation(client,cfg):
    data = get_data(client,"stnstatus",cfg)
    if data is None:
        return
    prodLineCode = "PL02"
    
    workOrderNo = get_item(data, u"sn")
    partNo = ""
    serialNumber = get_item(data, u"psn")
    stationCode = get_item(data, u"wsn")
    stationPassType = get_item(data, u"qa")
    userNo = get_item(data, u"usn")
    time = get_item(data, u"time")

    info = json_post(client,"http://10.106.11.42:8049/restful/prod-exec/station-pass-pull/insert/ames",[{
    # info = json_post(client, "http://10.40.9.8/send/server/test", [{
        "prodLineCode":prodLineCode,
        "workOrderNo":workOrderNo,
        "partNo":partNo,
        "serialNumber":serialNumber,
        "stationCode":stationCode,
        "stationPassType":stationPassType,
        "userNo":userNo,
        "time":time
    }])

    if info["result"] == True:
        print("stnstatus success")
    else:
        print("stnstatus error")

def post_snstatus(client,cfg):
    info = json_post(client,host_graphdbget(),{
    # info = json_post(client, "http://47.96.151.120/graphdb/get/line-two", {
    "n": "task",
    "obj": "sn,uid,state",
    "opt": {
        "has":"sn"
    }
    })
    print(info)
    if info == None:
        return
    for i in info:
        sn = get_item(i, "sn")
        state = get_item(i ,"state")
        snstatus = cfg["snstatus"]
        if i in range(len(snstatus)):
            if sn == snstatus[i]["sn"] and state == snstatus[i]["state"]:
                continue
            else:
                now_time = datetime.datetime.now()
                Tim = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')

                info = json_requests_post("http://10.106.11.42:8049/restful/prod-plan/work-order-service/sync/status",[{
                "workOrderNo":sn,
                "prodLineCode":"PL02",
                "status":state,
                "siteCode":"3310",
                "userNo":"AMES",
                "time":Tim
                }])
                if info["result"]:
                    print(info)
                    snstatus[i]["state"] = state





######################### PREPARE ##########################


def do_post_cmd(cmd, n):
    client = tornado.httpclient.HTTPClient()
    cfg = read_cfg()

    if cfg is None:
        cfg = {}

    if cmd == "packstation":
        post_packstation(client, cfg)
    if cmd == "snstatus":
        post_snstatus(client, cfg)

    client.close()
    write_cfg(cfg)


def do_task():
    do_post_cmd("packstation", None)
    do_post_cmd("snstatus", None)


cfg_host = host = "http://dockerhost/cfg"

http_client = tornado.httpclient.HTTPClient()
model = json_post(http_client, cfg_host, {
        "cmd": "get",
        "key": "client"
        })
 
http_client.close()




do_task()