def aaa():
    info = {"msn":{"data":[{"esn":"op1010sa","line":"line-one","msn":"aaaac","psn":"a001","time":"2020-01-10T01:47:51.370467745Z","wsn":"op1010"},{"esn":"op1010sa","line":"line-one","msn":"aaaac","psn":"a001","time":"2020-01-10T01:47:51.370467745Z","wsn":"op1010"}],"end":"2020-01-10T01:47:51.370467745Z","start":"2020-01-10T01:47:51.370467745Z"}}
    if info is not None:
        if isinstance(info, str):
            print("str")

        elif isinstance(info, list):
            print("list")
            for i in range(len(info)):
                data1 = info[i]["msn"]
                if "start" in data1 and "end" in data1 and "data" in data1:
                    print(data1["start"])
                    print(data1["end"])
                    print(data1["data"])


                    for data in data1["data"]:
                        return data

        elif isinstance(info, dict):
            print("dict")
            data1 = info["msn"]
            if "start" in data1 and "end" in data1 and "data" in data1:
                print(data1["start"])
                print(data1["end"])
                print(data1["data"])


                for data in data1["data"]:
                    return data

a = aaa()
print(a)
