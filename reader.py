from __future__ import print_function
import yaml
import random
import errno
import os
import csv
from datetime import datetime
from threading import Timer
import fileinput, string, sys

global jmeterPath
global chrome_script_path
global firefox_script_path
global reportPath

def filecreation():
    reportdir = os.path.join(
        reportPath,
        datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),"HTML")
    try:
        os.makedirs(reportdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # This was not a "directory exist" error..

    return reportdir


with open("config.yaml", 'r') as stream:
    try:
        content = yaml.load(stream)
        #print(content)
        urlList = content['gitUrl']
        url = urlList[0]
        print(url)

        jmeterVar = content['jmeterPath']
        jmeterPath = jmeterVar[0]
        print(jmeterPath)

        reportVar = content['reports']
        reportPath = reportVar[0]
        print(reportPath)

        scriptVar = content['scripts']
        for scriptpath in scriptVar:
            if "chrome" in scriptpath:
                chrome_script_path = scriptpath['chrome']
            elif "firefox" in scriptpath:
                firefox_script_path = scriptpath['firefox']

        print(chrome_script_path,firefox_script_path)

    except yaml.YAMLError as exc:
        print(exc)


def timeoutmethod():
    print("Time ended")
    os.chdir(jmeterPath)
    os.system("stoptest")


def jmeter_exection(iteration, rampup, concurrency, filepath):
    t = Timer(timeout, timeoutmethod)

    os.chdir(jmeterPath)
    reportdir = filecreation()
    t.start()
    os.system("jmeter.bat -n -t"+ filepath+" -l "+reportdir+"\log.csv -e -o "+reportdir+"\HTML -R -Gusers="+str(concurrency)+" -GrampUp="+str(rampup)+" -Gcount="+str(iteration))
    print("executed")


def create_instance(instance_number):
    print("Need to create "+str(instance_number)+" Instance(s)")

    with open("aws-config.yaml", 'r') as stream:
        try:
            content = yaml.load(stream)
            print(content)
            ami = content['ami']
            print(ami)


        except yaml.YAMLError as exc:
            print(exc)


def read_n_write_ip():
    with open(jmeterPath+"/ipconfig.txt", 'r') as stream:
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


with open("input.yaml", 'r') as stream:
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
            create_instance(instanceNo)
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
                        pass

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
                    # row is a list of strings
                    # use string.join to put them together
                    row[0]=url
                    print (', '.join(row))

        if "time-out" in content:
            timeout = content['time-out'][0]

            if (isinstance(timeout, int)):
                pass

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
                    path = chrome_script_path

                elif "firefox" in browser:
                    path = firefox_script_path

                scripts = content['scripts']
                for script in scripts:
                    lst = os.listdir(path)
                    if script in lst:
                        filepath = path+"\\"+script
                        print(script,browser,iteration,rampup,concurrency,iteration,rampup,concurrency)
                        jmeter_exection(iteration, rampup, concurrency, filepath)

                    elif os.path.isfile(script):
                        filepath = script
                        jmeter_exection(iteration, rampup, concurrency, filepath)

                    else:
                        print(script+" script is not present for "+browser)


    except yaml.YAMLError as exc:
        print(exc)
