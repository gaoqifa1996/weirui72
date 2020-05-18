

status = "open"
status_list=["open","close"]

if status not in status_list:
    print({"Result": False, "Message": "Error no such status", "Resultint": 2000})

