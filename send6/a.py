
import datetime
def post_creatsn(client, cfg):
    info1 = json_post(client, host_graphdbget(), {
        "n": "task",
        "obj": "sn,uid,state",
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
        snstatus = tabname
        if state == "open":
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
        else:
            break