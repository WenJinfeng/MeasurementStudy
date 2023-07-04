from collections import OrderedDict

CONGIF = {
    "creds":
        {
            "aws_id": "YOUR AWS ID",
            "aws_key": "YOUR AWS Key"
        },
    "func":
        {
            "name_prefix": "TestCode",
            "region": "us-east-1",
            "role_1": "YOUR Role"
        }
}


# The default path for function code

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



