# -*- coding: utf-8 -*-
from zipfile import ZipFile

import fc2

from conf import *

import time
import json
import os
import decimal


def get_config_basic():
    """
    Get the credentials and basic setting from the config file
    """
    endpoint = CONGIF["creds"]["endpoint"]
    aliyun_id = CONGIF["creds"]["aliyun_id"]
    aliyun_key = CONGIF["creds"]["aliyun_key"]
    service = CONGIF["func"]["service"]
    region = CONGIF["func"]["region"]
    role = CONGIF["func"]["role_1"]

    return endpoint, aliyun_id, aliyun_key, service, region, role

endpoint, aliyun_id, aliyun_key, service, region, role = get_config_basic()


client = fc2.Client(endpoint = endpoint, accessKeyID = aliyun_id, accessKeySecret = aliyun_key)

def zip_code(zip_name, code_path):
    """
    Zip the source function files to a deployment package
    """
    with ZipFile(zip_name, 'w') as functioncompute_zip:
        if not os.path.isdir(code_path):
            functioncompute_zip.write(code_path)
        else:
            for root, dirs, fs in os.walk(code_path):
                for f in fs:
                    abs_path = os.path.join(root, f)
                    functioncompute_zip.write(abs_path, f)




def create_function(src_file, func_handler, func_name, memory, role, runtime):
    
    try:
        response = client.create_function(
            serviceName = service,
            functionName = func_name, 
            description = "",
            runtime = runtime,
            memorySize = memory,
            timeout = 300, 
            handler = func_handler,
            codeZipFile = src_file
        )
        return True
    except Exception as e:
        print(e)
        return False
    

def invoke_function(service, func_name, req_para={}):
    tm_st = time.time() * 1000
    resp = client.invoke_function(
        serviceName=service, 
        functionName=func_name,
        # logType='Tail',
        payload=json.dumps(req_para)
    )
    tm_ed = time.time() * 1000
    # print(tm_st)
    # print(tm_ed)


    timepoint = resp.data.decode('utf-8')
    return tm_st, timepoint, tm_ed


   
def fstr(f):
    """
    Convert a float number to string
    """
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')




def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)


    with open(log_file,"a") as f:
        # print("Function-Name:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("\n")
    
    f.close()


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

    # # create FaaS application
    create_function(zipped_code_path, func_handler, func_name, mem_size, role, runtime)
    print("create the FaaS application - finish")


    # # invoke FaaS application 
    # requeststart, timepoint, requestend = invoke_function(service, func_name, req_para={})
    # print(requeststart, timepoint, requestend)
    # print("invoke FaaS application finish!")
    # log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # client.delete_function(serviceName=service, functionName=func_name)
    # print("delete FaaS application!")

    
def coldstart_measureInvoke(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for python and nodejs
    zipped_code_path = os.path.join(os.getcwd(), "tmp.zip")
    
    # -->for python and nodejs
    func_handler = "index.handler"
    



    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_function(service, func_name, req_para={})
    print(requeststart, timepoint, requestend)
    print("invoke {}-{} finish!".format(func_name, mem_size))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # client.delete_function(serviceName=service, functionName=func_name)
    # print("delete FaaS application!")

   

def coldstart_measureJavaCreate(
        func_name,
        runtime,
        mem_size,
        log_file):

    # -->for java
    zipped_code_path = os.path.join(os.getcwd(), "java.zip")
    

    # -->for java
    func_handler = "example.App::handleRequest"


    print("prepare create")
    # create FaaS application
    create_function(zipped_code_path, func_handler, func_name, mem_size, role, runtime)
    print("create the FaaS application - finish")


    # # invoke FaaS application
    # requeststart, timepoint, requestend = invoke_function(service, func_name, req_para={})
    # print(requeststart, timepoint, requestend)
    # print("invoke FaaS application finish!")
    # log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # client.delete_function(serviceName=service, functionName=func_name)
    # print("delete FaaS application!")

   

def main():
    
    # runtime = "python3.9"
    # runtime = "nodejs14"
    runtime = "java11"


    mem_size = 2048

    # func_name = "ColdStartpython"
    # func_name = "ColdStartnodejs"
    func_name = "ColdStartjava"

    func_name = "{}-{}".format(func_name, mem_size)

    # log_file = "pythonResult.txt"  
    # log_file = "nodejsResult.txt"  
    log_file = "javaResult.txt"  

    # coldstart_measurePythonNodejsCreate(func_name, runtime, mem_size, log_file)
    # coldstart_measureJavaCreate(func_name, runtime, mem_size, log_file)


    functions = ["ColdStartpython-128", "ColdStartpython-256", "ColdStartpython-512", "ColdStartpython-1024", "ColdStartpython-2048",
                "ColdStartnodejs-128", "ColdStartnodejs-256", "ColdStartnodejs-512", "ColdStartnodejs-1024","ColdStartnodejs-2048", "ColdStartjava-128", "ColdStartjava-256", "ColdStartjava-512", "ColdStartjava-1024", "ColdStartjava-2048"]
    
    runtimes = ["python3.9", "python3.9", "python3.9","python3.9","python3.9", "nodejs14", "nodejs14", "nodejs14", "nodejs14", "nodejs14", "java11", "java11", "java11", "java11", "java11"]
    
    memories=[128, 256, 512, 1024, 2048, 128, 256, 512, 1024, 2048, 128, 256, 512, 1024, 2048]

    logs = ["pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", 
            "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt"]


    for i in range(800):
        print("准备开始第{}次执行".format(i))
        time.sleep(1800)
        for fun_i in range(len(functions)):
            coldstart_measureInvoke(functions[fun_i], runtimes[fun_i], memories[fun_i], logs[fun_i])
        

    # coldstart_measureInvoke(func_name, runtime, mem_size, log_file)
    
    


if __name__ == '__main__':
    main()