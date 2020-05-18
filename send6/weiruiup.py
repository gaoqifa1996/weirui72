from tool import json_post, host_graphdbget, host_graphdb, host_machine, json_requests_post, read_cfg, write_cfg, \
    host_timedb
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
                    "gt": "time",
                    "v": st
                }],
                "limit": 1
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
                    # cfg[tab] = data1["end"]
                    for data in data1["data"]:
                        return data
        elif isinstance(info, dict):
            print("dict")
            data1 = info[tab]
            if "start" in data1 and "end" in data1 and "data" in data1:
                print(data1["start"])
                print(data1["end"])
                print(data1["data"])
                #cfg[tab] = data1["end"]
                for data in data1["data"]:
                    return data
    return None




######################## get to MES ########################
def get_plan(rec):
    line = get_item(rec, "ProdLineCode")
    sn = get_item(rec, "WorkOrderNo")
    pnum = get_item(rec, "Qty")
    tsn = get_item(rec, "PartNo")
    pstart = get_item(rec, "StartTime")
    pend = get_item(rec, "EndTime")

    print(tsn, sn, pnum, pstart, pend)

    if tsn and sn and pnum and pstart and pend:
        print(tsn, sn, pnum, pstart, pend)
    else:
        return {"Result": False, "Message": "has null value", "Resultint": 2000,"TaskID":"IF-46"}

    if tsn:
        uidinfo = json_requests_post(host_graphdbget(), {
            "n": "tech",
            "obj": "uid,sn",
            "opt": {
                "and": [{
                    "eq": "sn",
                    "v": tsn
                }]
            }
        })
        uid = uidinfo[0]["uid"]
        if not uid:
            return {"Result": False, "Message": "no such Technology", "Resultint": 2000,"TaskID":"IF-46"}
        info = json_requests_post(host_graphdb(), {
            "a": [{
                "u": "line-one",
                "n": "task",
                "v": [[
                    {"k": "sn", "v": sn},
                    {"k": "tech", "u": uid},
                    {"k": "pstart", "v": pstart},
                    {"k": "pend", "v": pend},
                    {"k": "pnum", "v": pnum},
                    {"k": "state", "v": "open"},
                    {"k": "linecode", "v": line}
                ]]
            }]})
        if info == "Success":
            return {"Result": True, "Message": info, "Resultint": 1000,"TaskID":"IF-46"}
        else:
            return {"Result": False, "Message": "info error", "Resultint": 2000,"TaskID":"IF-46"}


def get_module(rec):
    for i in range(len(rec)):
        prodlinecode = get_item(rec[i], "ProdLineCode")
        modulesn = get_item(rec[i], "ModuleSn")
        voltage = get_item(rec[i], "Voltage")
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

        if modulesn and resultmsg and timein and voltage and prodlinecode and maxvoltage and minvoltage and resistance and maxresistance and minresistance and insulationvalue and leakcurrent and singlevoltage and voltagediffer and differntc and userno:
            print(modulesn, resultmsg)
        else:
            return {"Result": False, "Message": "has null value", "Resultint": 2000,"TaskID":"IF-50"}
        # global recresult
        recresult = json_requests_post(host_machine(), {
            "op010_op010_psn": modulesn,
            "op010_op010_moduleinfo":
                [{
                    "prodlinecode": prodlinecode,
                    "voltage": voltage,
                    "maxvoltage": maxvoltage,
                    "minvoltage": minvoltage,
                    "resistance": resistance,
                    "maxresistance": maxresistance,
                    "minresistance": minresistance,
                    "insulationvalue": insulationvalue,
                    "leakcurrent": leakcurrent,
                    "singlevoltage": singlevoltage,
                    "voltagediffer": voltagediffer,
                    "differntc": differntc,
                    "resultmsg": resultmsg,
                    "userno": userno,
                    "timein": timein
                }]
        })
        # print(recresult)
        if recresult["code"] == 1000:
            if i >= len(rec) - 1:
                print(recresult)
                return {"Result": True, "Message": "ok", "Resultint": 1000,"TaskID":"IF-50"}
        else:
            return {"Result": False, "Message": "send error", "Resultint": 2000,"TaskID":"IF-50"}


def get_psn(rec):
    for i in range(len(rec)):
        sn = get_item(rec[i], "WorkOrderNo")
        psn = get_item(rec[i], "SerialNumber")

        if sn and psn:
            print(sn, psn)
        else:
            return {"Result": False, "Message": "has null value", "Resultint": 2000,"TaskID":"IF-51"}

        uidinfo = json_requests_post(host_graphdbget(), {

            "n": "task",
            "obj": "uid,sn",
            "opt": {
                "and": [{
                    "eq": "sn",
                    "v": sn
                }]
            }
        })
        uid = uidinfo[0]["uid"]
        # psnresult = json_requests_post("http://47.96.151.120/graphdb/md",{
        psnresult = json_requests_post(host_graphdb(), {
            "a": [{
                "v": [[{
                    "k": "sn",
                    "v": psn
                }]],
                "u": uid,
                "n": "pcode"
            }]
        })
        print(psnresult)
        if psnresult == "Success":
            if i >= len(rec) - 1:
                print(i)
                return {"Result": True, "Message": "ok", "Resultint": 1000,"TaskID":"IF-51"}
        else:
            return {"Result": False, "Message": "send error", "Resultint": 2000,"TaskID":"IF-51"}


def get_snstatus(rec):
    for i in range(len(rec)):
        sn = get_item(rec[i], u"WorkOrderNo")
        status = get_item(rec[i], u"Status")

        status_list = ["open", "close"]  # only support such
        if status not in status_list:
            print(status)
            return {"Result": False, "Message": "Error no such status", "Resultint": 2000,"TaskID":"IF-48"}
        # info = json_requests_post("http://47.96.151.120/graphdb/get/line-two",{
        info = json_requests_post(host_graphdbget(), {
            "n": "task",
            "obj": "sn,uid,state",
            "opt": {
                "and": [
                    {
                        "eq": "sn",
                        "v": sn
                    }]
            }
        })
        print(info)
        state = get_item(info[0], "state")
        uid = get_item(info[0], "uid")
        if status == state:
            if i >= len(rec) - 1:
                return {"Result": True, "Message": "ok", "Resultint": 1000,"TaskID":"IF-48"}
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
                if i >= len(rec) - 1:
                    return {"Result": True, "Message": "ok", "Resultint": 1000,"TaskID":"IF-48"}
            else:
                return {"Result": False, "Message": "error", "Resultint": 2000,"TaskID":"IF-48"}


####################### post to MES ########################
def post_packstation(client, cfg):
    # cfg["stnstatus"] = "2020-01-01T10:10:10.123456789Z"
    data = get_data(client, "stnstatus", cfg)
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

    info = json_post(client, "http://10.106.11.42:8049/restful/prod-exec/station-pass-pull/insert/ames", [{
        # info = json_post(client, "http://10.40.9.8/send/server/test", [{
        "prodLineCode": prodLineCode,
        "workOrderNo": workOrderNo,
        "partNo": partNo,
        "serialNumber": serialNumber,
        "stationCode": stationCode,
        "stationPassType": stationPassType,
        "userNo": userNo,
        "time": time
    }])
    print(info)
    if info["result"] == True:
        print("stnstatus success")
        cfg["stnstatus"] = data["time"]
    else:
        print("stnstatus error")

def post_snstatus(client, cfg):
    info1 = json_post(client, host_graphdbget(), {
        # info1 = json_post(client, "http://47.96.151.120/graphdb/get/line-two", {
        "n": "task",
        "obj": "sn,uid,state",
        "opt": {
            "has": "sn"
        }
    })
    print(info1)
    tabname = None
    if "snstatus" in cfg:
        tabname = cfg["snstatus"]

    for i in info1:
        sn = get_item(i, "sn")
        state = get_item(i, "state")
        snstatus = tabname
        if snstatus == None:
            now_time = datetime.datetime.now()
            Tim = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
            info = json_requests_post("http://10.106.11.42:8049/restful/prod-plan/work-order-service/sync/status", [{
                "workOrderNo": sn,
                "prodLineCode": "PL02",
                "status": state,
                "siteCode": "3310",
                "userNo": "AMES",
                "time": Tim}])
            print(info)
            if info["result"]:
                snstatus[i]["state"] = state
                print("snstatus post success")
                return
            else:
                print("snstatus post error")
                return
        else:
            snlen = len(snstatus)
            if i in range(snlen):
                if sn == snstatus[i]["sn"] and state == snstatus[i]["state"]:
                    continue
                else:
                    now_time = datetime.datetime.now()
                    Tim = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')

                    info = json_requests_post(
                        "http://10.106.11.42:8049/restful/prod-plan/work-order-service/sync/status", [{
                            "workOrderNo": sn,
                            "prodLineCode": "PL02",
                            "status": state,
                            "siteCode": "3310",
                            "userNo": "AMES",
                            "time": Tim
                        }])
                    print(info)
                    if info["result"]:
                        print("snstatus post success")
                        snstatus[i]["state"] = state
                        return
                    else:
                        print("snstatus post error")
                        return

def post_creatsn(client, cfg):
    # info1 = json_post(client, host_graphdbget(), {
    info1 = json_post(client, "http://10.106.160.10/graphdb/get/line-one", {
        "n": "task",
        "obj": "sn,uid,state,pstart,pend",
        "opt": {
            "has": "sn"
        }
    })
    print(info1)
    tabname = None
    if "creatsn" in cfg:
        tabname = cfg["creatsn"]

    for i in info1:
        sn = get_item(i, "sn")
        state = get_item(i, "state")
        qty = "1"
        starttime = get_item(i, "pstart")
        endtime = get_item(i, "pend")

        snstatus = tabname
        if state == "open":
            if snstatus == None:
                info = json_requests_post("http://10.106.11.42:8049/restful/prod-plan/work-order-service/insert/ames", [{
                    "workOrderNo": sn,
                    "prodLineCode": "PL02",
                    "partNo": "",
                    "qty":qty,
                    "siteCode": "3310",
                    "userNo": "AMES",
                    "startTime": starttime,
                    "endTime": endtime
                    }])
                print(info)
                if info["result"]:
                    snstatus[i]["sn"] = sn
                    print("creatsn post success")
                    return
                else:
                    print("creatsn post error")
                    return
            else:
                snlen = len(snstatus)
                if i in range(snlen):
                    if sn == snstatus[i]["sn"] and state == snstatus[i]["state"]:
                        continue
                    else:
                        info = json_requests_post("http://10.106.11.42:8049/restful/prod-plan/work-order-service/insert/ames", [{
                                "workOrderNo": sn,
                                "prodLineCode": "PL02",
                                "partNo": "",
                                "qty":qty,
                                "siteCode": "3310",
                                "userNo": "AMES",
                                "startTime": starttime,
                                "endTime": endtime
                            }])
                        print(info)
                        if info["result"]:
                            print("creatsn post success")
                            snstatus[i]["state"] = state
                            return
                        else:
                            print("creatsn post error")
                            return
        else:
            break

def post_pipmsn(client,cfg):
    data = get_data(client,"msn",cfg)
    if data is None:
        return
    psn = get_item(data,u"psn")
    sn = get_item(data,u"sn")
    wsn = get_item(data,u"wsn")
    stepnum = get_item(data,u"stepnum")
    msn = get_item(data,u"msn")
    msnpart = msn[0:10]
    resultinfo = get_item(data,"result")
    if resultinfo == "pass":
        result = 1
    else:
        result = 0
    Tim1 = get_item(data,"time")
    Tim = Tim1[0:19]
    tim = str(datetime.datetime.strptime(Tim,"%Y-%m-%dT%H:%M:%S"))
    info = json_post(client,"http://10.106.11.42:8049/restful/prod-exec/sn-bind-detail-service/insert/ames",[{
        "serialNumber":psn,
        "workOrderNo":sn,
        "partNo":"",
        "prodLineCode":"PL02",
        "stationCode":wsn,
        "stepNo":stepnum,
        "componentPartNo":msnpart,
        "componentSN":msn,
        "resultMsg":result,
        "siteCode":"3310",
        "userNo":"AMES",
        "time":tim
    }])
    print(info)
    if info["result"]:
        print("pipmsn post success")
        cfg["msn"] = data["time"]
    else:
        print("pipmsn post fail")

def post_tight(client,cfg):
    data = get_data(client,"atlas",cfg)
    if data is None:
        return
    psn = get_item(data,u"psn")
    sn = get_item(data,u"sn")
    wsn = get_item(data,u"wsn")
    stepnum = get_item(data,u"stepnum")
    sleeve = get_item(data,u"sleeve")
    device = get_item(data,u"deviceid")
    contorl = get_item(data,u"contorlid")
    pset = get_item(data,u"pset")
    fintorque = get_item(data,u"finaltorque")
    finangle = get_item(data, u"finalangle")
    maxAngle = get_item(data, u"maxangle")
    maxtoeque = get_item(data, u"maxtorque")
    minangle = get_item(data, u"minangle")
    mintorque = get_item(data, u"mintorque")
    resultinfo = get_item(data,"result")
    if resultinfo == "pass":
        result = 1
    else:
        result = 0
    Tim1 = get_item(data,"time")
    Tim = Tim1[0:19]
    tim = str(datetime.datetime.strptime(Tim,"%Y-%m-%dT%H:%M:%S"))
    info = json_post(client,"http://10.106.11.42:8049/restful/prod-exec/product-torque-detail-service/insert/ames",[{
        "serialNumber":psn,
        "workOrderNo":sn,
        "partNo":"",
        "prodLineCode":"PL02",
        "stationCode":wsn,
        "stepNo":stepnum,
        "sleeve":sleeve,
        "deviceID":device,
        "contorlID":contorl,
        "pSET":pset,
        "finalTorque":fintorque,
        "finalAngle":finangle,
        "maxTorque":maxtoeque,
        "minTorque":mintorque,
        "maxAngle":maxAngle,
        "minAngle":minangle,
        "resultMsg":result,
        "siteCode":"3310",
        "userNo":"AMES",
        "time":tim
    }])
    print(info)
    if info["result"]:
        print("torque post success")
        cfg["atlas"] = data["time"]
    else:
        print("torque post fail")

def post_airtight(client,cfg):
    data = get_data(client,"ateq",cfg)
    if data is None:
        return
    psn = get_item(data,u"psn")
    sn = get_item(data,u"sn")
    wsn = get_item(data,u"wsn")
    device = get_item(data,u"deviceid")
    testProID = get_item(data,u"testproid")
    testCount = get_item(data,u"testnum")
    testPressure = get_item(data,u"testpressure")
    testData = get_item(data, u"testrate")
    testRate = get_item(data, u"testrate")

    resultinfo = get_item(data,"result")
    if resultinfo == "pass":
        result = 1
    else:
        result = 0
    Tim = get_item(data,"time")
    pt1 = Tim[0:19]
    pstar = datetime.datetime.strptime(pt1, "%Y-%m-%dT%H:%M:%S")
    nedtime = datetime.timedelta(seconds=int(get_item(data,u"stepbeat")))
    pen = (pstar + nedtime).strftime("%Y-%m-%d %H:%M:%S")
    startim = str(pstar.strftime("%Y-%m-%d %H:%M:%S"))
    endtim = str(pen)

    info = json_post(client,"http://10.106.11.42:8049/restful/prod-battery/divulge-data/insert/ames",[{
        "serialNumber":psn,
        "workOrderNo":sn,
        "partNo":"",
        "prodLineCode":"PL02",
        "stationCode":wsn,
        "deviceID":device,
        "testProID":testProID,
        "testCount":testCount,
        "testPressure":testPressure,
        "testData":testData,
        "testRate":testRate,
        "resultMsg":result,
        "siteCode":"3310",
        "userNo":"AMES",
        "startTime":startim,
        "endTime":endtim
    }])
    print(info)
    if info["result"]:
        print("airtight post success")
        cfg["atlas"] = data["time"]
    else:
        print("airtight post fail")


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
    if cmd == "pipmsn":
        post_pipmsn(client,cfg)
    if cmd == "tight":
        post_tight(client,cfg)
    if cmd == "airtight":
        post_airtight(client,cfg)
    if cmd == "creatsn":
        post_creatsn(client,cfg)

    client.close()
    write_cfg(cfg)

def do_task():
    #do_post_cmd("packstation", None)
    do_post_cmd("creatsn", None)
    #do_post_cmd("snstatus", None)
    #do_post_cmd("pipmsn", None)
    #do_post_cmd("tight", None)
    #do_post_cmd("airtight", None)



do_task()
