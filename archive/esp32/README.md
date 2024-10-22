# IEEE ReRo Lab

<br />

### ESP32 DevKit

- The ESP32 flash storage contains two important files : `boot.py` and `main.py`
- `boot.py` is the file that is run when the ESP32 is powered on.
- `main.py` is run right after `boot.py`

- Using `ampy`, we can upload files to the ESP32 flash storage :
	- Upload `boot.py` : `ampy --port <PORT> put boot.py`
	- Upload `main.py` : `ampy --port <PORT> put main.py`

<br />

### TCP Server

- The program `server.py` is run on the server system.
- The ESP32 acts as a TCP client and communication is established.