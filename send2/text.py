import requests
from tool import json_post,host_graphdbget,host_graphdb,json_requests_post
import tornado.httpclient

def get_item(data, key):
    if key in data:
        return data[key]
    return None

# r = requests.post("http://10.40.9.1/machine/dj/line-one",json={"op010_op010_unmsn":1,"op010_op010_msn":"21021021"})
# print(r.text)


def get_plan(rec):

    line = get_item(rec, "ProdLineCode")
    sn = get_item(rec, "WorkOrderNo")
    pnum = get_item(rec, "Qty")
    tsn = get_item(rec, "TechnologyNo")
    pstart = get_item(rec, "StartTime")
    pend = get_item(rec, "EndTime")

    print(tsn,sn,pnum,pstart,pend)

    if not tsn and sn and pnum and pstart and pend:
        return {"Result":False,"Message":"has null value","Resultint":2000}
    # client = tornado.httpclient.HTTPClient()
    if tsn :
        # uidinfo = json_requests_post(host_graphdbget(),{
        uidinfo = json_requests_post("http://47.96.151.120/graphdb/get/line-two", {
            "n":"tech",
            "obj":"uid,sn",
            "opt":{
                "and":[{
                    "eq":"sn",
                    "v":tsn
                }]
            }
        })
        print(uidinfo)
        uid = uidinfo[0]["uid"]
        # print(uid)
        if not uid:
            return {"Result": False, "Message": "no such Technology", "Resultint": 2000}
        info = json_requests_post("http://47.96.151.120/graphdb/md", {
            "a":[{
            "u":"line-two",
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
            return {"Result": True, "Message": "info error", "Resultint": 1000}