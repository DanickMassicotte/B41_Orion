# -*- coding: utf-8 -*-
from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp
from Vue import *
from Modele import *
from ObjetsJeu import *
from Controleur import *
from PIL import Image, ImageTk

if __name__=="__main__":
    c=Controleur()
    print("End Orion_mini")