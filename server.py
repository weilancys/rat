from PIL import ImageGrab
import socket
import struct
import io
import time

# img = ImageGrab.grab()
# img.save(r"c:\Users\Administrator\Desktop" + "\\" + "a.jpg")

IP = "0.0.0.0"
PORT = 4749

socketServer = socket.socket()
socketServer.bind((IP, PORT))
socketServer.listen(1)

print("server is listening on {}:{}".format(IP, PORT))

socketClient, socketClientAddr = socketServer.accept()
socketClientFile = socketClient.makefile("wb")

networkBuffer = io.BytesIO()

timeStart = time.time()

while True:
	img = ImageGrab.grab()
	#img.resize((1280, 720))
	img.save(networkBuffer, "PNG", quality=30)

	imgLength = networkBuffer.tell()
	socketClientFile.write(struct.pack(">L", imgLength))

	networkBuffer.seek(0)
	socketClientFile.write(networkBuffer.read())
	socketClientFile.flush()

	networkBuffer.seek(0)
	networkBuffer.truncate()

	if time.time() - timeStart > 5:
		break

socketClientFile.write(struct.pack(">L", 0))

socketClientFile.close()
socketClient.close()

socketServer.close()
