from __future__ import print_function
import yaml
import random
import errno
import os
import csv
from datetime import datetime
from threading import Timer
import fileinput, string, sys
import boto3 # to import boto3 library

ips = []
global jmeterPath
chrome_script_path = '/scripts/chrome'
chrome_fullpath = os.path.dirname(os.path.realpath(__file__))+chrome_script_path
firefox_script_path = '/scripts/firefox'
firefox_fullpath = os.path.dirname(os.path.realpath(__file__))+firefox_script_path
global reportPath


with open("Input/config.yaml", 'r') as stream:
    try:
        content = yaml.load(stream)
        urlList = content['gitUrl']
        url = urlList[0]
        print(url)

        jmeterVar = content['jmeterPath']
        jmeterPath = jmeterVar[0]
        print(jmeterPath)


    except yaml.YAMLError as exc:
        print(exc)


def timeoutmethod():
    print("Time ended")
    os.chdir(jmeterPath)
    os.system("stoptest")


def jmeter_exection(iteration, rampup, concurrency, filepath):
    #t = Timer(timeout, timeoutmethod)

    os.chdir(jmeterPath)
    #t.start()
    os.system("jmeter.bat -n -t"+ filepath+" -r -Gusers="+str(concurrency)+" -GrampUp="+str(rampup)+" -Gcount="+str(iteration))
    print("executed")




def read_n_write_ip():
    with open(jmeterPath+"\ipconfig.txt", 'r') as stream:
        try:
            content = yaml.load(stream)
            print(content)

        except yaml.YAMLError as exc:
            print(exc)

    text = "remote_hosts="
    x = fileinput.input(files=jmeterPath+"\jmeter.properties",inplace=1)
    for line in x:
        if text in line:
            line = "remote_hosts="+content+"\n"
        print (line)
    x.close()


with open("Input/Input.yaml", 'r') as stream:
    global concurrency
    concurrency = 1
    iteration = 1
    rampup = 0
    try:
        content = yaml.load(stream)
        print(content)

        if 'instance' in content:
            instancevar = content['instance']
            instanceNo = instancevar[0]
            read_n_write_ip()


        if 'execution' in content:
            exection = content['execution']
            for var in exection:
                if "iteration" in var:
                    iteration = var['iteration']
                elif  "concurrency" in var:
                    concurrency = var["concurrency"]
                elif "ramp-up" in var:
                    rampup = var['ramp-up']

                    if(isinstance(rampup,int)):
                        rampup =int(rampup)*60

                    elif "m" in rampup:
                        rampup = rampup.replace("m","")
                        rampup=int(rampup)*60

                    elif "s" in rampup:
                        rampup = rampup.replace("s","")
                        rampup = int(rampup)

            print(concurrency,iteration,rampup)

        if "url" in content:
            urlVar = content['url']
            url = urlVar[0]
            with open(jmeterPath+'\\Inputdatas.csv', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    row[0]=url
                    print (', '.join(row))

        if "time-out" in content:
            timeout = content['time-out'][0]

            if (isinstance(timeout, int)):
                timeout = int(timeout)* 60

            elif "m" in timeout:
                timeout = timeout.replace("m", "")
                timeout = int(timeout) * 60

            elif "s" in rampup:
                timeout = timeout.replace("s", "")
                timeout = int(timeout)


        if "random" in content:
            path = content['random'][0]
            lst = os.listdir(path)
            rand = random.randint(0,len(lst)-1)
            filepath = path+"\\"+lst[rand]
            print(filepath,iteration,rampup,concurrency,iteration,rampup,concurrency)
            jmeter_exection(iteration,rampup,concurrency,filepath)
        else:
            browsers = content['browsers']
            for browser in browsers:
                if "chrome" in browser:
                    path = chrome_fullpath

                elif "firefox" in browser:
                    path = ''
                    path = firefox_fullpath

                scripts = content['scripts']
                for script in scripts:
                    filedir = path
                    print(filedir)
                    lst = os.listdir(filedir)
                    if script in lst:
                        filepath = filedir+"\\"+script
                        print(filepath)
                        print(script,browser,iteration,rampup,concurrency,iteration,rampup,concurrency)
                        jmeter_exection(iteration, rampup, concurrency, filepath)

                    elif os.path.isfile(script):
                        filepath = script
                        jmeter_exection(iteration, rampup, concurrency, filepath)

                    else:
                        print(script+" script is not present for "+browser)


    except yaml.YAMLError as exc:
        print(exc)
