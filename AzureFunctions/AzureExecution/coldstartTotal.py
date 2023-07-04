# -*- coding: utf-8 -*-
from zipfile import ZipFile

import time
import json
import os
import decimal
import subprocess

import urllib2
import socket




def run_cmd(cmd):
    """
    The simplest way to run an external command
    """
    return os.popen(cmd).read()



def create_functionPython(func_name, runtime, version, region):
    try:
        print(run_cmd("az functionapp create --resource-group %s --consumption-plan-location %s --runtime %s --runtime-version %s --functions-version 3 --name %s --storage-account %s --os-type linux" % ("ColdStartResourceGroup1", region, runtime, version, func_name, "coldstartstorage1")))
        time.sleep(20)
        print(run_cmd("func azure functionapp publish %s" % (func_name)))
        print("create app: {}".format(func_name))
        return True
    except Exception as e:
        print(e)
        return False
    

    


def invoke_functionPython(func_name, req_para):
    # req_para = json.dumps("{}")
    resp = "no_change"
    socket.setdefaulttimeout(600)
    url = "https://%s.azurewebsites.net/api/httpexample?name=%s" % (func_name, req_para)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    tm_st = time.time() * 1000
    req = urllib2.Request(url, headers=hdr)
    resp = urllib2.urlopen(req, None, 600)
    tm_ed = time.time() * 1000
    
    resp =resp.read()

    print(resp)
    
    timepoint =  resp.split(",timepoint:")[1]

    return tm_st, timepoint, tm_ed



   
def fstr(f):
    """
    Convert a float number to string
    """
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')




def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version, startType):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)

    with open(log_file,"a") as f:
        print("Function-Name:{}, startType:{}, Runtime:{}, runtimeVersion:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, startType, runtime, version, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, startType:{}, Runtime:{}, runtimeVersion:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, startType, runtime, version, initDuration, duration, e2eDuration))
        f.write("\n")
    
    f.close()




def delete_function(func_name):
    try:
        cmd = "az functionapp delete --name %s --resource-group ColdStartResourceGroup1" % (func_name)
        run_cmd(cmd)
        return True
    except Exception as e:
        return False


def coldstart_measurePython(
        func_name,
        inputpayload,
        runtime,
        version,
        log_file,
        startType):

    region = "eastus"
    

    # # create FaaS application
    # create_functionPython(func_name, runtime, version, region)
    # print("create the FaaS application - finish")


    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_functionPython(func_name, inputpayload)
    print(requeststart, timepoint, requestend)
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version, startType)

    # # delete FaaS application
    # delete_function(func_name)
    # print("delete FaaS application!")




def main():
    
   

    tasktype = "graph"
    inputpayload = ""


    runtime = "python"
    version = "3.9"

    # runtime = "node"
    # version = "14"
    
    # runtime = "java"
    # version ="11"

    # azure needs to allocate the specific memory size
    # mem_size = xx

    func_index = "faasapp"
    func_name = "{}{}".format(tasktype, func_index)

 
    log_file = "AzureResEffResult1.txt"
 

    functions = ["cpufaasapp", "memoryfaasapp", "diskiofaasapp", "networkfaasapp", "imagefaasapp", "speechfaasapp", "graphfaasapp", "trainbotofaasapp", "inferencebotofaasapp"]


    payloads = [20, 25, 5, "https://jsonplaceholder.typicode.com/users", "", "", "", "", ""]



    # startType = "0"

    
    fixedruntime = "python"
    fixedversion = "3.9"
    

    for i in range(20):
        print("准备开始第{}次执行".format(i))
        time.sleep(1200)
        for fun_index in range(len(functions)):
            coldstart_measurePython(functions[fun_index], payloads[fun_index], fixedruntime, fixedversion, log_file, "0")
            for k in range(50):
                print("准备开始第{}次执行函数{}的第{}次热启动迭代".format(i, functions[fun_index], k))
                time.sleep(20)
                try:
                    coldstart_measurePython(functions[fun_index], payloads[fun_index], fixedruntime, fixedversion, log_file, "1")
                except Exception as e:
                    print(e)




    # coldstart_measurePython(func_name, inputpayload, runtime, version, log_file, startType)
    
    



if __name__ == '__main__':
    main()