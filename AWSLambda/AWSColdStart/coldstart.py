# -*- coding: utf-8 -*-
from zipfile import ZipFile

import boto3
from botocore.client import Config
from conf import *

import time
import json
import os
import base64
import decimal

def get_config_basic():
    """
    Get the credentials and basic setting from the config file
    """
    aws_id = CONGIF["creds"]["aws_id"]
    aws_key = CONGIF["creds"]["aws_key"]
    region = CONGIF["func"]["region"]
    role = CONGIF["func"]["role_1"]

    return aws_id, aws_key, region, role


aws_id, aws_key, region, role = get_config_basic()

session = boto3.Session(aws_access_key_id=aws_id,
                                aws_secret_access_key=aws_key,
                                region_name=region)
config = Config(connect_timeout=300, read_timeout=300)
client = session.client(service_name='lambda', config=config)



def zip_code(zip_name, code_path):
    """
    Zip the source function files to a deployment package
    """
    with ZipFile(zip_name, 'w') as lambda_zip:
        if not os.path.isdir(code_path):
            lambda_zip.write(code_path)
        else:
            for root, dirs, fs in os.walk(code_path):
                for f in fs:
                    abs_path = os.path.join(root, f)
                    lambda_zip.write(abs_path, f)




def create_function(src_file, func_handler, func_name, memory, role, runtime):
    try:     
        with open(src_file, "rb") as zip_blob:
            response = client.create_function(
                Code={'ZipFile': zip_blob.read()},
                Description='',
                FunctionName=func_name,
                Handler=func_handler,
                MemorySize=memory,
                Publish=True,
                Role=role,
                Runtime=runtime,
                Timeout=300,
            )
        return True
    except Exception as e:
        print(e)
        print("kk")
        return False
    

# def invoke_function(func_name, req_para={}):
#     tm_st = time.time() * 1000
#     resp = client.invoke(
#         FunctionName = func_name,
#         InvocationType = "RequestResponse",
#         LogType="Tail",
#         Payload = json.dumps(req_para)
#     )
#     tm_ed = time.time() * 1000
#     out = base64.b64decode(resp['LogResult'])
    
#     return out, tm_st, tm_ed

def invoke_function(func_name, req_para={}):
    tm_st = time.time() * 1000
    resp = client.invoke(
        FunctionName = func_name,
        InvocationType = "RequestResponse",
        # LogType="Tail",
        Payload = json.dumps(req_para)
    )
    tm_ed = time.time() * 1000
    timepoint = str(resp['Payload'].read(), 'utf-8')

    
    # timepoint = resp.data.decode('utf-8')
    # out = base64.b64decode(resp['LogResult'])
    
    return tm_st, timepoint, tm_ed


def invoke_functionJava(func_name, req_para={}):
    tm_st = time.time() * 1000
    resp = client.invoke(
        FunctionName = func_name,
        InvocationType = "RequestResponse",
        # LogType="Tail",
        Payload = json.dumps(req_para)
    )
    tm_ed = time.time() * 1000
    timepoint = json.loads(str(resp['Payload'].read(),'utf-8'))["body"]
    

    # timepoint = resp.data.decode('utf-8')
    # out = base64.b64decode(resp['LogResult'])
    
    return tm_st, timepoint, tm_ed



# def update_function(func_name, zip_name):
#     try:     
#         with open(zip_name, "rb") as zip_blob:
#             client.update_function_configuration(
#                 FunctionName=func_name,
#                 Code={'ZipFile': zip_blob.read()})
#         return True
#     except Exception as e:
#         print(e)
#         print("kk")
#         return False
    


# def log_process(out, tm_st, tm_ed, log_file, func_name, runtime, mem_size):

#     duration = str(out).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Duration:")[1].split(" ")[1]
#     addDuration = ""

#     initDuration = 0
#     if ",Init Duration:" in str(out).split('REPORT RequestId:')[1].replace("\\t", ","):
#         initDuration = str(out).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Init Duration:")[1].split(" ")[1]
    
#     e2eDuration = fstr(tm_ed - tm_st)

#     with open(log_file,"a") as f:
#         print("Function-Name:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}{}".format(func_name, runtime, mem_size, initDuration, duration, addDuration))
#         f.write("Function-Name:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}{}".format(func_name, runtime, mem_size, initDuration, duration, addDuration))
#         f.write("\n")
    
#     f.close()


def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)


    with open(log_file,"a") as f:
        # print("Function-Name:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("\n")
    
    f.close()

def fstr(f):
    """
    Convert a float number to string
    """
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def coldstart_measurePythonNodejsCreate(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for python and nodejs
    zipped_code_path = os.path.join(os.getcwd(), "tmp.zip")
    
    # -->for python and nodejs
    func_handler = "index.handler"
    

    print("prepare create")
    src_code_path = os.path.join(os.getcwd(), CODE_PATH[runtime])
    zip_code(zipped_code_path, src_code_path)

    # create lambda
    create_function(zipped_code_path, func_handler, func_name, mem_size, role, runtime)
    print("create the FaaS application - finish")


    # # invoke lambda 
    # requeststart, timepoint, requestend = invoke_function(func_name, req_para={})
    # print(requeststart, timepoint, requestend)
    # print("invoke lambda finish!")
    # log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # #delete lambda
    # client.delete_function(FunctionName=func_name)
    # print("delete lambda!")

    
def coldstart_measurePythonNodejsInvoke(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for python and nodejs
    zipped_code_path = os.path.join(os.getcwd(), "tmp.zip")
    
    # -->for python and nodejs
    func_handler = "index.handler"
    

    # invoke lambda 
    requeststart, timepoint, requestend = invoke_function(func_name, req_para={})
    print(requeststart, timepoint, requestend)
    print("invoke {}-{} finish!".format(func_name, mem_size))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)




def coldstart_measureJavaCreate(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for java
    zipped_code_path = os.path.join(os.getcwd(), "java.zip")
    

    # -->for java
    func_handler = "example.Hello::handleRequest"


    print("prepare create")
    # create lambda
    create_function(zipped_code_path, func_handler, func_name, mem_size, role, runtime)
    print("create the FaaS application - finish")



   
def coldstart_measureJavaInvoke(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for java
    zipped_code_path = os.path.join(os.getcwd(), "java.zip")
    

    # -->for java
    func_handler = "example.Hello::handleRequest"

    #invoke lambda 
    requeststart, timepoint, requestend = invoke_functionJava(func_name, req_para={})
    print(requeststart, timepoint, requestend)
    print("invoke {}-{} finish!".format(func_name, mem_size))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)



    # delete lambda
    # client.delete_function(FunctionName=func_name)
    # print("delete lambda!")


def main():
    
    # runtime = "python3.10"
    # runtime = "nodejs18.x"
    # runtime = "java11"


    # mem_size = 2048

    # func_name = "ColdStartpython"
    # func_name = "ColdStartnodejs"
    # func_name = "ColdStartjava"

    # func_name = "{}-{}".format(func_name, mem_size)
    

    # log_file = "pythonResult.txt"  
    # log_file = "nodejsResult.txt"  
    # log_file = "javaResult.txt"  


    # coldstart_measurePythonNodejsCreate(func_name, runtime, mem_size, log_file)
    # coldstart_measureJavaCreate(func_name, runtime, mem_size, log_file)

    # start invocations

    functions = ["ColdStartpython-128", "ColdStartpython-256", "ColdStartpython-512", "ColdStartpython-1024", "ColdStartpython-2048",
                "ColdStartnodejs-128", "ColdStartnodejs-256", "ColdStartnodejs-512", "ColdStartnodejs-1024","ColdStartnodejs-2048"]

    
    
    runtimes = ["python3.10", "python3.10", "python3.10","python3.10","python3.10", "nodejs18.x", "nodejs18.x", "nodejs18.x", "nodejs18.x", "nodejs18.x"]
    
    memories=[128, 256, 512, 1024, 2048, 128, 256, 512, 1024, 2048]


    logs = ["pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", 
            "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt"]


    javaFunctions = ["ColdStartjava-128", "ColdStartjava-256", "ColdStartjava-512", "ColdStartjava-1024", "ColdStartjava-2048"]
    javaRuntimes = ["java11", "java11", "java11", "java11", "java11"]
    javaMemories = [128, 256, 512, 1024, 2048]
    javaLogs = ["javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt"]

    for i in range(600):
        print("准备开始第{}次执行".format(i))
        time.sleep(600)
        for fun_i in range(len(functions)):
            coldstart_measurePythonNodejsInvoke(functions[fun_i], runtimes[fun_i], memories[fun_i], logs[fun_i])
        for javaFun_i in range(len(javaFunctions)):
            coldstart_measureJavaInvoke(javaFunctions[javaFun_i], javaRuntimes[javaFun_i], javaMemories[javaFun_i], javaLogs[javaFun_i])


    



if __name__ == '__main__':
    main()