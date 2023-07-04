from collections import OrderedDict

CONGIF = {
    "creds":
        {
            "endpoint": "YOUR Aliyun Endpoint",
            "aliyun_id": "YOUR Aliyun ID",
            "aliyun_key": "YOUR Aliyun key"
        },
    "func":
        {
            "name_prefix": "TestCode",
            "service": "MeasureService",
            "region": "us-east-1",
            "role_1": "YOUR ROLE"
        }
}



CODE_PATH = {
    "cpu": "./micro/cpu",
    "memory": "./micro/memory",
    "diskio": "./micro/diskio",
    "network": "./micro/network",
    "image": "./macro/image",
    "speech": "./macro/speech",
    "graph": "./macro/graph",
    "trainboto": "./macro/trainboto",
    "inferenceboto": "./macro/inferenceboto"
}

