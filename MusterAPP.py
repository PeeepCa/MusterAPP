import tkinter as tk
import socket
import time
from PIL import ImageTk, Image

sleep = 0.7
init = b"UTF-8$"
login = b"regLogin"
logout = b"regLogout"
registrationType = b"S"
systemIdentifier = b"testlogin"
crmuster = b"attribAppendAttributeValues"


class ITAC:
    def init():
##        TCP_IP = socket for ITAC
        TCP_IP = ''
        TCP_PORT = 4711
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(init)
        time.sleep(sleep)
        data = s.recv(BUFFER_SIZE)
        print("init " + str(data))

        return [s , BUFFER_SIZE]
        
        if data != b'0$':
            ctypes.windll.user32.MessageBoxA(0, data, "iTAC Message", 1)

    def login(s , BUFFER_SIZE , stationNumber):
        loginString = stationNumber + b",,,,," + registrationType + b"," + systemIdentifier
        
        s.send(login + b",stationNumber,stationPassword,user,password,client,registrationType,systemIdentifier," + loginString + b"$")
        time.sleep(sleep)
        sessionId = s.recv(BUFFER_SIZE)
        sessionId = sessionId.replace(b"$", b"", 1)
        sessionId = sessionId.replace(b"0", b"", 1)
        print(sessionId)
        
        return sessionId

    def musterFunc(s , BUFFER_SIZE , sessionId , stationNumber , attributeCode):
        e2 = GUI.E2.get() ##serialNumber
        print(e2)
        e4 = GUI.E4.get() ##attributeValue
        print(e4)
        s.send(crmuster + sessionId + b"," + stationNumber +  b",0," + e2.encode() + b",-1,-1,1,2,attribute_code,attribute_value,2," + attributeCode + b"," + e4.encode() + b"$")
        time.sleep(sleep)
        data = s.recv(BUFFER_SIZE)
        print("odesilani " + str(data))

    def logout(s , BUFFER_SIZE , sessionId):
        s.send(logout + sessionId + b"$")
        time.sleep(sleep)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print("logout " + str(data))
        
        if data != b'0$':
            ctypes.windll.user32.MessageBoxA(0, data, "iTAC Message", 1)

def readConfig():
    file = open("config.ini", "r")
    temp = file.readlines()
    stationNumber = temp[0].split("=")
    stationNumber = stationNumber[1]
    stationNumber = stationNumber.replace("\n","")

    attributeCode = temp[1].split("=")
    attributeCode = attributeCode[1]
    attributeCode = attributeCode.replace("\n","")

    return [stationNumber.encode() , attributeCode.encode()]

def mainFunc():
    ret = readConfig()
    attributeCode = ret[1]
    stationNumber = ret[0]
    ret = ITAC.init()
    s = ret[0]
    BUFFER_SIZE = ret[1]
    sessionId = ITAC.login(s , BUFFER_SIZE , stationNumber)
    ITAC.musterFunc(s , BUFFER_SIZE , sessionId , stationNumber , attributeCode)
    ITAC.logout(s , BUFFER_SIZE , sessionId)

class GUI:
    top = tk.Tk()
    top.title("Muster APP")
    top.geometry("300x145")
    top.config(bg = "#FFFFFF")

    img = Image.open("apag logo.bmp")
    img = img.resize((80,50), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    I1 = tk.Label(top , image = photoImg , height = 50 , width = 80 , borderwidth = 0)
    I1.place(x=210 , y=5)
    
    T2 = tk.Label(top , text = "serialNumber" , bg = "#FFFFFF")
    T2.place(x=5, y=65)
    T4 = tk.Label(top , text = "attributeValue" , bg = "#FFFFFF")
    T4.place(x=5, y=90)

    E2 = tk.Entry(top , width = 31)
    E2.place(x=100, y=65)
    E4 = tk.Entry(top , width = 31)
    E4.place(x=100, y=90)

    B = tk.Button(top , text = "Send" , command = mainFunc , width = 40)
    B.place(x=5, y=115)

GUI.top.mainloop()

