from tool import json_post,host_graphdbget,host_graphdb,json_requests_post
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