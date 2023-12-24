# MeasurementStudy

**UPDATE！！！**
实现在不同主流平台下的微基准测试程序和宏基准测试程序分别提供在相应平台下探究执行性能的文件夹中（即AWSLambda/AWSExecution、GoogleCloudFunctions/GoogleExecution、AzureFunctions/AzureExecution和AlibabaFunctionCompute/AlibabaExecution）。



关于四个服务器无感知平台进行运行时性能探究的代码脚本。创建、部署和执行的FaaS应用根据每个平台的编写格式特点进行微调。同时，也包括我们设计的每组实验获得的1,000次性能数据结果。

## 亚马逊Lambda -- 对应文件夹“AWSLambda”
- 冷启动性能实验：文件夹“AWSColdStart”
    - 文件夹“code”里面包含三种语言的Hello World应用代码: Python、JavaScript（也可称为nodejs）和Java
    - coldstart.py是对各种语言应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括亚马逊Lambda的凭证信息、部署应用的文件位置

- 执行性能实验：文件夹“AWSExecution”
    - 文件夹“micro”是所使用的亚马逊Lambda编写格式下的微基准测试程序代码：CPU密集型任务、磁盘IO密集型任务、内存密集型任务、网络密集型任务
    - 文件夹“macro”是所使用的亚马逊Lambda编写格式下的宏基准测试程序代码：图计算graph、图片处理image、机器学习推理inferenceboto、语音合成speech、机器学习训练trainboto
    - coldstartTotal.py是对不同类型应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括平台的凭证信息、部署应用的文件位置


## 谷歌Cloud Functions -- 对应文件夹“GoogleCloudFunctions”
- 冷启动性能实验：文件夹“GoogleColdStart”
    - 文件夹“code”里面包含三种语言的Hello World应用代码: Python、JavaScript（也可称为nodejs）和Java
    - coldstart.py是对各种语言应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括部署应用的文件位置


- 执行性能实验：文件夹“GoogleExecution”
    - 文件夹“micro”是所使用的谷歌Cloud Functions编写格式下的微基准测试程序代码：CPU密集型任务、磁盘IO密集型任务、内存密集型任务、网络密集型任务
    - 文件夹“macro”是所使用的谷歌Cloud Functions编写格式下的宏基准测试程序代码：图计算graph、图片处理image、机器学习推理inferenceboto、语音合成speech、机器学习训练trainboto
    - coldstartTotal.py是对不同类型应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括部署应用的文件位置


## 微软Azure Functions -- 对应文件夹“AzureFunctions”
- 冷启动性能实验：文件夹“AzureColdStart”
    - 文件夹“Azurejava” - coldstart.py是Java语言应用创建部署、调用、删除
    - 文件夹“Azurenodejs” - coldstart.py是JavaScript语言应用创建部署、调用、删除
    - 文件夹“Azurepython” - coldstart.py是JavaScript语言应用创建部署、调用、删除
    - invokeAzureCode.py是对三种应用进行多次调用执行的代码


- 执行性能实验：文件夹“AzureExecution”
    - 微基准测试程序创建部署和调用代码：
        - 文件夹“AzureCPU” - coldstart.py是CPU密集型应用创建部署、调用、删除
        - 文件夹“Azurediskio” - coldstart.py是磁盘IO密集型应用创建部署、调用、删除
        - 文件夹“Azurememory” - coldstart.py是内存密集型应用创建部署、调用、删除
        - 文件夹“Azurenetwork” - coldstart.py是网络密集型应用创建部署、调用、删除
    - 宏基准测试程序创建部署和调用代码：
        - 文件夹“Azureimage” - coldstart.py是图片处理应用创建部署、调用、删除
        - 文件夹“Azuregraph” - coldstart.py是图计算应用创建部署、调用、删除
        - 文件夹“Azurespeech” - coldstart.py是语音合成应用创建部署、调用、删除
        - 文件夹“Azuretrainboto” - coldstart.py是机器学习训练应用创建部署、调用、删除
        - 文件夹“Azureinferenceboto” - coldstart.py是机器学习推理应用创建部署、调用、删除
     - coldstartTotal.py是对所有不同类型应用的多次调用执行的代码
    

## 阿里巴巴Function Compute -- 对应文件夹“AlibabaFunctionCompute”
- 冷启动性能实验：文件夹“AlibabaColdStart”
    - 文件夹“code”里面包含三种语言的Hello World应用代码: Python、JavaScript（也可称为nodejs）和Java
    - coldstart.py是对各种语言应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括阿里巴巴Function Compute的凭证信息、部署应用的文件位置

- 执行性能实验：文件夹“AlibabaExecution”
    - 文件夹“micro”是所使用的阿里巴巴Function Compute编写格式下的微基准测试程序代码：CPU密集型任务、磁盘IO密集型任务、内存密集型任务、网络密集型任务
    - 文件夹“macro”是所使用的阿里巴巴Function Compute编写格式下的宏基准测试程序代码：图计算graph、图片处理image、机器学习推理inferenceboto、语音合成speech、机器学习训练trainboto
    - AlicoldstartTotal.py是对不同类型应用的操作：创建部署、调用、删除
    - conf.py是设置的全局信息，包括阿里巴巴Function Compute的凭证信息、部署应用的文件位置


## 度量的性能数据
- TotalAnalysisColdStart.xlsx表示四个平台在不同语言、不同内存下分别获得的1,000次冷启动性能结果
- TotalAnalysisExecution.xlsx表示四个平台在不同任务类型下分别获得的1,000次冷启动性能结果
