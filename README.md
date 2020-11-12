
## About This Repository:

YO! Machine Terminator is a multiprocess hacking tool. It uses FTP for sending the generated files. It handles the following processes:

   * Keylogging.
   * Screen recording.
   * Voice recording.
   * Grabbing the machine info.
   * Tracking and saving the clipboard history.

The following video illustrates how the program works:

## Installation:

#### 1. Install dependencies:

 	pip install -r requirements.txt
 
#### 2. Create a config.py file as follows:

	ftp_authentication = dict(
		user = "<value>",
		password = "<value>",
		port = <value>,
		address = "<value>",
		directory = "<value>",
	)
	
#### 3. Running the FTP server:

	python ftpserver.py
	
#### 4. Running the The Machine Terminator (TMT):

	python machineterminator.py

 	
	









