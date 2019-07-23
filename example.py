#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:06:55 2019

@author: busra
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import requests
from bs4 import BeautifulSoup

chunk_size = 256

class ButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Demo")
        self.set_size_request(300, 150)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        
        hbox1 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox1, True, True, 0)
        
        hbox2 = Gtk.Box(spacing=6)
        vbox.pack_start(hbox2, True, True, 0)
        
        self.label1 = Gtk.Label("Video Link: ")
        hbox1.pack_start(self.label1, True, True, 0)
        
        self.entrylink = Gtk.Entry()
        self.entrylink.set_text("")
        hbox1.pack_start(self.entrylink, True, True, 0)
        
        self.label2 = Gtk.Label("Video Name:")
        hbox2.pack_start(self.label2, True, True, 0)
        
        self.entryname = Gtk.Entry()
        self.entryname.set_text("")
        hbox2.pack_start(self.entryname, True, True, 0)
                
        button = Gtk.Button.new_with_label("download")
        button.connect("clicked", self.on_click_me_clicked)
        vbox.pack_start(button, True, True, 0)
        
        button = Gtk.Button.new_with_label("close")
        button.connect("clicked", self.on_close_clicked)
        vbox.pack_start(button, True, True, 0)
   
    def on_click_me_clicked(self, button):
        #print(self.entrylink.get_text())
        self.source_code(self.entrylink.get_text())
        self.entrylink.set_text("DONE!")
         
    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()
    
    def change_char(self,name):
        liste = str.maketrans("ÇĞİÖŞÜçğıöşü\n ","CGIOSUcgiosu _")
        name = name.translate(liste)
        return name.lower()
    
    def source_code(self, url):
        req = requests.get(url)
        
        if(req.status_code == 200):
            req = req.text
        else:
            print("Not Found")
        
        soup = BeautifulSoup(req,'lxml')
        data = soup.find("meta",property="og:video")['content']
        #print(self.entryname.get_text())
        name = self.entryname.get_text()
        
        name = self.change_char(name)
        #print(name)
        self.entryname.set_text(name)
        r = requests.get(data, stream=True)
        
        with open(name+".mp4","wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                

win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()