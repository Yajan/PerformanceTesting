from __future__ import print_function

import requests
import json
ips = []
global jmeterPath
from os import listdir
from os.path import isfile, join
import socket


def get_link(path):

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link"

    headers = {
        "Authorization": "Bearer 7la5zgquXUAAAAAAAAAAOPGjvDT7X9-7WT150rlbmoh1A6kt9WBgC-zE6fOz_gji",
        "Content-Type": "application/json"
    }

    data = {
        "path": path
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    jsonurl = r.json()
    link = jsonurl['url']
    print(link)
    return link

def create_folder(foldername):
    foldername="/"+str(foldername)
    url = "https://api.dropboxapi.com/2/files/create_folder"

    headers = {
        "Authorization": "Bearer 7la5zgquXUAAAAAAAAAALRj2iFdh2VMWqawMbi_ahnU1oBKrINqz4TlzJd_OUoWC",
        "Content-Type": "application/json"
    }
    data = {
        "path": foldername
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("Folder created")
    print(r.json())

def file_upload(filepath,filename,foldername):

    foldername = "/"+str(foldername)
    filename = "/"+str(filename)



    url = "https://content.dropboxapi.com/2/files/alpha/upload"

    headers = {
        "Authorization": "Bearer 7la5zgquXUAAAAAAAAAALRj2iFdh2VMWqawMbi_ahnU1oBKrINqz4TlzJd_OUoWC",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": "{\"path\":\""+str(foldername)+str(filename)+"\"}"
    }

    data = open(filepath+filename, "rb").read()
    r = requests.post(url, headers=headers, data=data)
    print("File uploaded")
    print(r.json())







def store_data():
    testname = socket.gethostbyname(socket.gethostname())
    logpath = "C:/Users/Administrator/Documents/apache-jmeter-3.3/bin/TimestampsFolder"
    onlyfiles = [f for f in listdir(logpath) if isfile(join(logpath, f))]
    #print(onlyfiles)
    create_folder(testname)
    for file in onlyfiles:
        #print(file)
        file_upload(logpath,file,testname)

store_data()











