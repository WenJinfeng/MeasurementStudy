# -*- coding: utf-8 -*-
from zipfile import ZipFile



from conf import *

import time
import json
import os
import decimal
import subprocess






def run_cmd(cmd):
    """
    The simplest way to run an external command
    """
    return os.popen(cmd).read()



def create_function(src_file, func_handler, func_name, memory, runtime, region):
    try:
        run_cmd("gcloud functions deploy %s --entry-point %s --source %s --runtime %s --memory %sMB --timeout 300s --region %s --trigger-http --allow-unauthenticated" % (func_name, func_handler, src_file, runtime, memory, region))
        return True
    except Exception as e:
        print(e)
        return False
    

    

def invoke_function(func_name, region):
    req_para = json.dumps("{}")
    tm_st = time.time() * 1000
        
    resp = run_cmd("gcloud functions call %s --region %s --data %s" % (func_name, region, req_para))
    tm_ed = time.time() * 1000

    # print(resp)
    
    timepoint =  resp.split(",timepoint:")[1].replace("\'","")

    return tm_st, timepoint, tm_ed



def invoke_functionjava(func_name, region):
    req_para = json.dumps("{}")
    tm_st = time.time() * 1000
        
    resp = run_cmd("gcloud functions call %s --region %s --data %s" % (func_name, region, req_para))
    tm_ed = time.time() * 1000

    # print(resp)
    
    timepoint =  resp.split("result: \'")[1].replace("\'","")

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
        print("Function-Name:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("\n")
    
    f.close()



# execute command with added "Y"
def excuteCmd(cmd, addcmd, timeout = 1):
    #print("process delete")
    s = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell = True) 
    s.stdin.write(addcmd+'\n')
    out, err = s.communicate()
    if err is not None:
        return err
    
    return out

def delete_function(func_name, region):
    try:
        cmd = "gcloud functions delete %s --region %s" % (func_name, region)
        excuteCmd(cmd, "Y")
        return True
    except Exception as e:
        return False



def coldstart_measurePythonNodejsCreate(
        func_name,
        runtime,
        mem_size,
        log_file):

    
    # -->for python and nodejs
    func_handler = "handler"
    
    region = CONGIF["func"]["region"]
    src_file = CODE_PATH[runtime]
    

    # create FaaS application
    create_function(src_file, func_handler, func_name, mem_size, runtime, region)
    print("create the FaaS application - finish")


    # # invoke FaaS application 
    # requeststart, timepoint, requestend = invoke_function(func_name, region)
    # print(requeststart, timepoint, requestend)
    # print("invoke FaaS application finish!")
    # log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # delete_function(func_name, region)
    # print("delete FaaS application!")

def coldstart_measurePythonNodejsInvoke(
        func_name,
        runtime,
        mem_size,
        log_file):

    
    # -->for python and nodejs
    func_handler = "handler"
    
    region = CONGIF["func"]["region"]
    src_file = CODE_PATH[runtime]
    

    # # create FaaS application
    # create_function(src_file, func_handler, func_name, mem_size, runtime, region)
    # print("create the FaaS application - finish")


    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_function(func_name, region)
    print(requeststart, timepoint, requestend)
    print("invoke {}-{} finish!".format(func_name, mem_size))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # delete_function(func_name, region)
    # print("delete FaaS application!")



def coldstart_measureJavaCreate(
        func_name,
        runtime,
        mem_size,
        log_file):

 
    # -->for java
    func_handler = "com.example.Example"


    region = CONGIF["func"]["region"]
    src_file = CODE_PATH[runtime]

    # create FaaS application
    create_function(src_file, func_handler, func_name, mem_size, runtime, region)
    print("create the FaaS application - finish")

    # # invoke FaaS application 
    # requeststart, timepoint, requestend = invoke_functionjava(func_name, region)
    # print(requeststart, timepoint, requestend)
    # print("invoke FaaS application finish!")
    # log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # delete_function(func_name, region)
    # print("delete FaaS application!")
   


def coldstart_measureJavaInvoke(
        func_name,
        runtime,
        mem_size,
        log_file):

 
    # -->for java
    func_handler = "com.example.Example"


    region = CONGIF["func"]["region"]
    src_file = CODE_PATH[runtime]

    # # create FaaS application
    # create_function(src_file, func_handler, func_name, mem_size, runtime, region)
    # print("create the FaaS application - finish")

    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_functionjava(func_name, region)
    print(requeststart, timepoint, requestend)
    print("invoke {}-{} finish!".format(func_name, mem_size))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size)

    # # delete FaaS application
    # delete_function(func_name, region)
    # print("delete FaaS application!")
   


def main():
    
    # runtime = "python311"
    # runtime = "nodejs18"
    # runtime = "java17"


    # mem_size = 2048

    # func_name = "ColdStartpython"
    # func_name = "ColdStartnodejs"
    func_name = "ColdStartjava"

    # func_name = "{}-{}".format(func_name, mem_size)

    # log_file = "pythonResult.txt"  
    # log_file = "nodejsResult.txt"  
    # log_file = "javaResult.txt"  

    # coldstart_measurePythonNodejsCreate(func_name, runtime, mem_size, log_file)

    # coldstart_measureJavaCreate(func_name, runtime, mem_size, log_file)

    functions = ["ColdStartpython-128", "ColdStartpython-256", "ColdStartpython-512", "ColdStartpython-1024", "ColdStartpython-2048",
                 "ColdStartnodejs-128", "ColdStartnodejs-256", "ColdStartnodejs-512", "ColdStartnodejs-1024","ColdStartnodejs-2048"]

    runtimes = ["python311", "python311", "python311","python311","python311",
                "nodejs18", "nodejs18", "nodejs18", "nodejs18", "nodejs18"]

    memories=[128, 256, 512, 1024, 2048, 128, 256, 512, 1024, 2048]

    logs = ["pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "pythonResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt", "nodejsResult.txt"]


    javaFunctions = ["ColdStartjava-128", "ColdStartjava-256", "ColdStartjava-512", "ColdStartjava-1024", "ColdStartjava-2048"]
    javaRuntimes = ["java17", "java17", "java17", "java17", "java17"]
    javaMemories = [128, 256, 512, 1024, 2048]
    javaLogs = ["javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt", "javaResult.txt"]




    for i in range(1000):
        print("准备开始第{}次执行".format(i))
        time.sleep(1800)
        for fun_i in range(len(functions)):
            time.sleep(10)
            coldstart_measurePythonNodejsInvoke(functions[fun_i], runtimes[fun_i], memories[fun_i], logs[fun_i])
        for javaFun_i in range(len(javaFunctions)):
            time.sleep(10)
            coldstart_measureJavaInvoke(javaFunctions[javaFun_i], javaRuntimes[javaFun_i], javaMemories[javaFun_i], javaLogs[javaFun_i])


   



if __name__ == '__main__':
    main()