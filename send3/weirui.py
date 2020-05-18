from tool import host_graphdbget,host_graphdb,host_machine,json_requests_post
import tornado.httpclient

def get_item(data, key):
    if key in data:
        return data[key]
    return None

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
        print(recresult)
    if recresult["code"]==1000:
        return {"Result": True, "Message": "ok", "Resultint": 1000}
    else:
        return {"Result": False, "Message": "send error", "Resultint": 2000}