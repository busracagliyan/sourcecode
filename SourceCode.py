#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:45:28 2019

@author: busra
"""

from bs4 import BeautifulSoup
import requests
from sys import argv

chunk_size = 256

def change_char(name):
    liste = str.maketrans("ÇĞİÖŞÜçğıöşü\n","CGIOSUcgiosu ")
    name = name.translate(liste)
    return name.lower()

def source_code(url):
    req = requests.get(url)
    
    if(req.status_code == 200):
        req = req.text
    else:
        print("Not Found")
    
    soup = BeautifulSoup(req,'lxml')
    data = soup.find("meta",property="og:video")['content']
    
    lst = soup.title.text
    lst = change_char(lst)
    lst = lst.split(" ")
    
    name = ""
    video_name = ""
    
    for i in lst:
        name += i
    print(name)
    
    for j in range(0,20):
        video_name += name[j]
    
    print(video_name)
    
    r = requests.get(data, stream=True)
    
    with open(video_name+".mp4","wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)

script,x=argv

print("the name of the script: ",script)
print("url of the video:",x)
source_code(x)
