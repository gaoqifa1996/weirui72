import xmltodict
import json

# xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><env:Envelope xmlns:env="http://pdps.in.audi.vwg/legacy_schema/20.7.3/envelope"><Header><Sender><Location assembly_cycle="" assembly_line="" assembly_line_section="" assembly_subline="" plant="C4" plant_segment="BODY"/><Device name="" hostname="" ipaddress="10.228.202.97" macaddress="" manufacturer="" type="" operating_state="" model=""/><Application name="MES" minorversion="0" majorversion="1" manufacturer=""/></Sender><Telegraminfo minorversion="0" majorversion="1" dataguid="" timestamp="2020-02-07T10:45:45" datatype="MODULES"/><Communicationtype type="SEND"/></Header><Body><VehicleData><BodyIdent plant="C4" id="1128001" productionyear="2019" checkdigit="9"/></VehicleData><Data><Raw><Detail><Key>STA</Key><Value>X000</Value></Detail><Detail><Key>TIM</Key><Value>20191205135529000</Value></Detail></Raw></Data></Body></env:Envelope>'
def xml2dict(xml):
    # file_object = open('t.xml',encoding = 'utf-8')
       # try:
    #     all_the_xmlStr = file_object.read()
    # finally:
    #     file_object.close()
    #xml To dict
    convertedDict = xmltodict.parse(xml)
    #ensure_ascii = False chinese can be used
    jsonStr = json.dumps(convertedDict,ensure_ascii=False)
    print(jsonStr)
    jsonDict = eval(jsonStr)
    # recv = jsonDict["env:Envelope"]["Body"]["Data"]["Raw"]["Detail"]
    # d = {}
    # for a in range(len(recv)):
    #     # print(detail[a])
    #     d[recv[a]["Key"]] = recv[a]["Value"]
    # print(d)
    return jsonDict
    # with open('./1111111018378_20181203214626.json', 'w',encoding = 'utf-8') as f:
    #xmltodict value can move to @
        # f.write(jsonStr.replace('@', ''))

def dict2xml(dict):
    #2.Json to Xml
    convertedXml = xmltodict.unparse(dict)
    print ("convertedXml=",convertedXml)


def readjson(json):

    env = json["env:Envelope"]
    xmlns = env["@xmlns:env"]
    header = env["Header"]

    body = env["Body"]
    vehicledata = body["VehicleData"]
    data = body["Data"]
    raw = data["Raw"]
    detail = raw["Detail"]
    d = {}
    for a in range(len(detail)):
        # print(detail[a])
        d[detail[a]["Key"]] = detail[a]["Value"]
    print(d)
    del env["Body"]["Data"]["Raw"]
    # print(env)
    return d,env

# jsonStr = {"env:Envelope": {"@xmlns:env": "http://pdps.in.audi.vwg/legacy_schema/20.7.3/envelope", "Header": {"Sender": {"Location": {"@assembly_cycle": "", "@assembly_line": "", "@assembly_line_section": "", "@assembly_subline": "", "@plant": "C4", "@plant_segment": "BODY"}, "Device": {"@name": "", "@hostname": "", "@ipaddress": "10.228.202.97", "@macaddress": "", "@manufacturer": "", "@type": "", "@operating_state": "", "@model": ""}, "Application": {"@name": "MES", "@minorversion": "0", "@majorversion": "1", "@manufacturer": ""}}, "Telegraminfo": {"@minorversion": "0", "@majorversion": "1", "@dataguid": "", "@timestamp": "2020-02-07T10:45:45", "@datatype": "MODULES"}, "Communicationtype": {"@type": "SEND"}}, "Body": {"VehicleData": {"BodyIdent": {"@plant": "C4", "@id": "1128001", "@productionyear": "2019", "@checkdigit": "9"}}, "Data": {"Raw": {"Detail": [{"Key": "STA", "Value": "X000"}, {"Key": "TIM", "Value": "20191205135529000"}]}}}}}
#
# readjson(jsonStr)


