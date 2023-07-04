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
    

    

def invoke_function(func_name, region, inputpayload):
    # req_para = json.dumps("{}")
    tm_st = time.time() * 1000
        
    resp = run_cmd("gcloud functions call %s --region %s --data %s" % (func_name, region, inputpayload))
    tm_ed = time.time() * 1000

    # print(resp)
    
    timepoint =  resp.split(",timepoint:")[1].replace("\'","")

    return tm_st, timepoint, tm_ed


   
def fstr(f):
    """
    Convert a float number to string
    """
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')




def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size, startType):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)


    with open(log_file,"a") as f:
        print("Function-Name:{}, startType:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, startType, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, startType:{}, Runtime:{}, MemorySize:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, startType, mem_size, initDuration, duration, e2eDuration))
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



def coldstart_measure(
        func_name,
        inputpayload,
        tasktype,
        runtime,
        mem_size,
        log_file,
        startType):

    
    # -->for python and nodejs
    func_handler = "handler"
    
    region = CONGIF["func"]["region"]
    
    

    # # create FaaS application
    # src_file = CODE_PATH[tasktype]
    # create_function(src_file, func_handler, func_name, mem_size, runtime, region)
    # print("create the FaaS application - finish")


    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_function(func_name, region, inputpayload)
    print(requeststart, timepoint, requestend)
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size, startType)

    # # delete FaaS application
    # delete_function(func_name, region)
    # print("delete FaaS application!")

    

 

def main():
    
    # tasktype = "cpu"
    # inputpayload = json.dumps("{\"n\": 20}")

    # tasktype = "memory"
    # inputpayload = json.dumps("{\"index\": 25}")

    # tasktype = "diskio"
    # inputpayload = json.dumps("{\"filesize\": 5}")

    # tasktype = "network"
    # inputpayload = json.dumps("{\"link\": \"https://jsonplaceholder.typicode.com/users\"}")
   

    # tasktype = "image"
    # inputpayload = json.dumps("{\"input_bucket\":\"cynthiaeastbucket\", \"object_key\": \"1.jpeg\",\"output_bucket\": \"cynthiaeastbucket1\"}")

    # tasktype = "speech"
    # inputpayload = json.dumps("{\"batch_size\": 5,\"file_name\": \"data_smoke_test_LDC93S1.wav\"}")

    tasktype = "graph"
    inputpayload = json.dumps("{\"size\":1000}")

    # tasktype = "trainboto"
    # inputpayload = json.dumps("{\"dataset_object_key\": \"reviews20mb.csv\", \"dataset_bucket\": \"cynthiaeastbucket\", \"model_bucket\": \"cynthiaeastbucket1\", \"model_object_key\": \"lr_model_new.pk\"}")

    # tasktype = "referenceboto"
    # inputpayload = json.dumps("{\"x\": \"The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.\", \"dataset_object_key\": \"reviews20mb.csv\", \"dataset_bucket\": \"cynthiaeastbucket\", \"model_bucket\": \"cynthiaeastbucket1\", \"model_object_key\": \"lr_model_new.pk\"}")


    runtime = "python39"
   


    mem_size = 128

    func_index = "faasapp"
    func_name = "{}{}{}".format(tasktype, mem_size, func_index)

   

    log_file = "GoogleResEffResult.txt"


    functions = ["cpu128faasapp", "memory128faasapp", "diskio128faasapp", "network128faasapp", "image128faasapp", "speech512faasapp", "graph128faasapp", "trainboto512faasapp", "inferenceboto512faasapp"]

   

    

    payloads = [json.dumps("{\"n\": 20}"), json.dumps("{\"index\": 25}"), json.dumps("{\"filesize\": 5}"), json.dumps("{\"link\": \"https://jsonplaceholder.typicode.com/users\"}"), json.dumps("{\"input_bucket\":\"cynthiaeastbucket\", \"object_key\": \"1.jpeg\",\"output_bucket\": \"cynthiaeastbucket1\"}"), json.dumps("{\"batch_size\": 5,\"file_name\": \"data_smoke_test_LDC93S1.wav\"}"), json.dumps("{\"size\":1000}"), json.dumps("{\"dataset_object_key\": \"reviews20mb.csv\", \"dataset_bucket\": \"cynthiaeastbucket\", \"model_bucket\": \"cynthiaeastbucket1\", \"model_object_key\": \"lr_model_new.pk\"}"), json.dumps("{\"x\": \"The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.\", \"dataset_object_key\": \"reviews20mb.csv\", \"dataset_bucket\": \"cynthiaeastbucket\", \"model_bucket\": \"cynthiaeastbucket1\", \"model_object_key\": \"lr_model_new.pk\"}")]

   

    
    
    fixedtasktype="seefunctionname"
    fixedruntime = "python39"
    fixedmem_size = "seefunctionname"

    for i in range(20):
        print("准备开始第{}次执行".format(i))
        time.sleep(1200)
        for fun_index in range(len(functions)):
            coldstart_measure(functions[fun_index], payloads[fun_index], fixedtasktype, fixedruntime, fixedmem_size, log_file, "0")
            for k in range(50):
                print("准备开始第{}次执行函数{}的第{}次热启动迭代".format(i, functions[fun_index], k))
                time.sleep(20)
                try:
                    coldstart_measure(functions[fun_index], payloads[fun_index], fixedtasktype, fixedruntime, fixedmem_size, log_file, "1")
                except Exception as e:
                    print(e)


    
    # startType = "0"

    # coldstart_measure(func_name, inputpayload, tasktype, runtime, mem_size, log_file, startType)
    



if __name__ == '__main__':
    main()