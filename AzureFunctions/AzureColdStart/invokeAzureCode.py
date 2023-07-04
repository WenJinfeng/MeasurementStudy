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
    

    
def create_functionNodejs(func_name, runtime, version, region):
    try:
        print(run_cmd("az functionapp create --resource-group %s --consumption-plan-location %s --runtime %s --runtime-version %s --functions-version 3 --name %s --storage-account %s --os-type linux" % ("ColdStartResourceGroup1", region, runtime, version, func_name, "coldstartstorage1")))
        time.sleep(20)
        text = run_cmd("func azure functionapp publish %s" % (func_name))
        text = text.split("Invoke url: ")[1].split("==")[0]
        returntext = "{}==".format(text)
        print("create app: {}".format(func_name))
        return returntext
    except Exception as e:
        print(e)
        return False
    


def invoke_functionPython(func_name):
    # req_para = json.dumps("{}")
    resp = "no_change"
    socket.setdefaulttimeout(600)
    url = "https://%s.azurewebsites.net/api/httpexample" % (func_name)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    tm_st = time.time() * 1000
    req = urllib2.Request(url, headers=hdr)
    resp = urllib2.urlopen(req, None, 600)
    tm_ed = time.time() * 1000
    
    resp =resp.read()

    print(resp)
    
    timepoint =  resp.split(",timepoint:")[1]

    return tm_st, timepoint, tm_ed

# each nodejs is different

def invoke_functionNodejs(func_name):
    # f = open("textsave.txt",'r')
    # url = f.read()
    # f.close()
    resp = "no_change"
    socket.setdefaulttimeout(600)
    url = "https://%s.azurewebsites.net/api/httpexample?code=9Of26vJJsMK-uNaFA8jbwp3Te8e_b_kEu3ydWkkvCzcaAzFup6WOng==" % (func_name)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    tm_st = time.time() * 1000
    req = urllib2.Request(url, headers=hdr)
    resp = urllib2.urlopen(req, None, 600)
    tm_ed = time.time() * 1000
    
    resp =resp.read()

    print(resp)
    
    timepoint =  resp.split(",timepoint:")[1]

    return tm_st, timepoint, tm_ed

def invoke_functionJava(func_name):
    # req_para = json.dumps("{}")
    resp = "no_change"
    socket.setdefaulttimeout(600)
    url = "https://%s.azurewebsites.net/api/httpexample" % (func_name)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    tm_st = time.time() * 1000
    try:
        req = urllib2.Request(url, headers=hdr)
        resp = urllib2.urlopen(req, None, 600)
    except Exception as e:
        print(e)

    tm_ed = time.time() * 1000
    
    resp =resp.read()

    print(resp)
    
    timepoint =  resp
    

    return tm_st, timepoint, tm_ed




   
def fstr(f):
    """
    Convert a float number to string
    """
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')




def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)


    with open(log_file,"a") as f:
        print("Function-Name:{}, Runtime:{}, runtimeVersion:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, version, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, Runtime:{}, runtimeVersion:{}, Init-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, runtime, version, initDuration, duration, e2eDuration))
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
        runtime,
        version,
        log_file):

    region = "eastus"
    

    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_functionPython(func_name)
    print(requeststart, timepoint, requestend)
    print("invoke {} finish!".format(func_name))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version)


def coldstart_measureNodejs(
        func_name,
        runtime,
        version,
        log_file):
    
    region = "eastus"
    
    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_functionNodejs(func_name)
    print(requeststart, timepoint, requestend)
    print("invoke {} finish!".format(func_name))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version)

def coldstart_measureJava(
        func_name,
        runtime,
        version,
        log_file):
    
    region = "eastus"
    


    # invoke FaaS application 
    requeststart, timepoint, requestend = invoke_functionJava(func_name)
    print(requeststart, timepoint, requestend)
    print("invoke {} finish!".format(func_name))
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, version)

    
 

def main():
    
    # runtime = "python"
    # version = "3.9"

    # runtime = "node"
    # version = "14"
    
    # runtime = "java"
    # version ="11"

    # azure needs to allocate the specific memory size
    # mem_size = 128

    # func_name = "ColdStartpython"
    # func_name = "ColdStartnodejs"
    # func_name = "ColdStartjava"

    # log_file = "pythonResult.txt"  
    # log_file = "nodejsResult.txt"  
    # log_file = "javaResult.txt"  

    # coldstart_measurePython(func_name, runtime, version, log_file)
    # coldstart_measureNodejs(func_name, runtime, version, log_file)
    # coldstart_measureJava(func_name, runtime, version, log_file)

    functions = ["ColdStartpython", "ColdStartnodejs", "ColdStartjava"]
    
    runtimes = ["python", "node", "java"]

    versions = ["3.9", "14", "11"]

    logs = ["pythonResult.txt", "nodejsResult.txt", "javaResult.txt" ]

    for i in range(1000):
        print("准备开始第{}次执行".format(i))
        time.sleep(1800)
        coldstart_measurePython(functions[0], runtimes[0], versions[0], logs[0])
        time.sleep(20)
        coldstart_measureNodejs(functions[1], runtimes[1], versions[1], logs[1])
        time.sleep(20)
        coldstart_measureJava(functions[2], runtimes[2], versions[2], logs[2])



 



if __name__ == '__main__':
    main()