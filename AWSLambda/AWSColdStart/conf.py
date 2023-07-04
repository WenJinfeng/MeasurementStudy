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
            "role_1": "YOUR ROLE"
        }
}


# The default path for function code

CODE_PATH = {
    "python3.10": "./code/python",
    "nodejs18.x": "./code/nodejs",
    "java11": "./code/java"
}



