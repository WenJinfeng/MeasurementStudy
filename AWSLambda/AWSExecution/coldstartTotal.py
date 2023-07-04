# -*- coding: utf-8 -*-
# from zipfile import ZipFile
import zipfile

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




def zip_code_new(zip_name, code_path):
    zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(code_path):
        fpath = path.replace(code_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


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

def log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size, startType):

    duration = fstr(requestend - float(timepoint))
    initDuration = fstr(float(timepoint) - requeststart)
    e2eDuration = fstr(requestend - requeststart)


    with open(log_file,"a") as f:
        print("Function-Name:{}, startType:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, startType, runtime, mem_size, initDuration, duration, e2eDuration))
        f.write("Function-Name:{}, startType:{}, Runtime:{}, MemorySize:{}, ColdStart-Duration:{}, Function-Duration:{}, e2e-Duration:{}".format(func_name, startType, runtime, mem_size, initDuration, duration, e2eDuration))
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


def coldstart_measure(
        func_name,
        inputpayload, 
        tasktype,
        runtime,
        mem_size,
        log_file,
        startType
        ):

    
    zipped_code_path = os.path.join(os.getcwd(), "tmp.zip")

    func_handler = "index.handler"
    

    # print("prepare zip create")
    # src_code_path = os.path.join(os.getcwd(), CODE_PATH[tasktype])
    # zip_code_new(zipped_code_path, src_code_path)

    # # create lambda
    # create_function(zipped_code_path, func_handler, func_name, mem_size, role, runtime)
    # print("create the FaaS application - finish")


    # invoke lambda 
    requeststart, timepoint, requestend = invoke_function(func_name, req_para=inputpayload)
    print(requeststart, timepoint, requestend)
    # print("invoke lambda finish!")
    log_process(requeststart, timepoint, requestend, log_file, func_name, runtime, mem_size, startType)

    # #delete lambda
    # client.delete_function(FunctionName=func_name)
    # print("delete lambda!")

    


def main():


    # tasktype = "cpu"
    # inputpayload = {"n":20}


    # tasktype = "memory"
    # inputpayload = {"index" : 25}


    # tasktype = "diskio"
    # inputpayload = {"file_size":5}

    # tasktype = "network"
    # inputpayload = {"link": "https://jsonplaceholder.typicode.com/users"}


    # tasktype = "image"
    # inputpayload = {"input_bucket":"cynthiaeastbucket", "object_key":"1.jpeg","output_bucket":"cynthiaeastbucket1"}

    # tasktype = "speech"
    # inputpayload = {"batch_size":5,"file_name":"data_smoke_test_LDC93S1.wav"}


    # tasktype = "graph"
    # inputpayload = {"size":1000}


    # tasktype = "trainboto"
    # inputpayload = {"dataset_object_key": "reviews20mb.csv", "dataset_bucket": "cynthiaeastbucket", "model_bucket": "cynthiaeastbucket1", "model_object_key": "lr_model_new.pk"}

    tasktype = "inferenceboto"
    inputpayload = {"x": "The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.", "dataset_object_key": "reviews20mb.csv", "dataset_bucket": "cynthiaeastbucket", "model_bucket": "cynthiaeastbucket1", "model_object_key": "lr_model_new.pk"}


    runtime = "python3.9"
 

    mem_size = 512


    func_index = "faasapp"
    func_name = "{}{}{}".format(tasktype, mem_size, func_index)


    log_file = "AWSResEffResult.txt"

    # start invocations

    functions = ["cpu128faasapp", "memory128faasapp", "diskio128faasapp", "network128faasapp", "image128faasapp", "speech512faasapp", "graph128faasapp", "trainboto512faasapp", "inferenceboto512faasapp"]

    payloads = [{"n":20}, {"index" : 25}, {"file_size":5}, {"link": "https://jsonplaceholder.typicode.com/users"}, {"input_bucket":"cynthiaeastbucket", "object_key":"1.jpeg","output_bucket":"cynthiaeastbucket1"}, {"batch_size":5,"file_name":"data_smoke_test_LDC93S1.wav"}, {"size":1000}, {"dataset_object_key": "reviews20mb.csv", "dataset_bucket": "cynthiaeastbucket", "model_bucket": "cynthiaeastbucket1", "model_object_key": "lr_model_new.pk"}, {"x": "The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.", "dataset_object_key": "reviews20mb.csv", "dataset_bucket": "cynthiaeastbucket", "model_bucket": "cynthiaeastbucket1", "model_object_key": "lr_model_new.pk"}
                ]

    fixedtasktype="seefunctionname"
    fixedruntime = "python3.9"
    fixedmem_size = "seefunctionname"

    

    for i in range(20):
        print("准备开始第{}次执行".format(i))
        time.sleep(1200)
        for fun_index in range(len(functions)):
            coldstart_measure(functions[fun_index], payloads[fun_index], fixedtasktype, fixedruntime, fixedmem_size, log_file, "0")
            for k in range(50):
                print("准备开始第{}次执行函数{}的第{}次热启动迭代".format(i, functions[fun_index], k))
                time.sleep(5)
                coldstart_measure(functions[fun_index], payloads[fun_index], fixedtasktype, fixedruntime, fixedmem_size, log_file, "1")

    
            


    
    # coldstart_measure(func_name, inputpayload, tasktype, runtime, mem_size, log_file, "0")
    



if __name__ == '__main__':
    main()