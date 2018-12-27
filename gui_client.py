from PIL import Image, ImageTk
import tkinter as tk 
import socket
import struct
import io

class guiRatClient(tk.Tk):
	"""docstring for guiRatClient"""
	def __init__(self):
		super(guiRatClient, self).__init__()
		self.title("rat client")
		self.server_addr = ("127.0.0.1", 4749)

		self.__initUI()

	def __initUI(self):
		self.ref_reserve = {}
		self.ref_reserve["temp_pic"] = ImageTk.PhotoImage(Image.open("patlabor.jpg"))

		self.canvas = tk.Canvas(self, width=1280, height=720, bg="black")
		self.canvas.create_image(0, 0, anchor="nw", image=self.ref_reserve["temp_pic"])
		self.canvas.pack()

		self.btn = tk.Button(self, text="play!", command=self.play)
		self.btn.pack()

	def play(self):
		socketClient = socket.socket()
		socketClient.connect(self.server_addr)

		socketClientFile = socketClient.makefile('rb')

		imageBuffer = io.BytesIO()
		while True:
			imageLength = struct.unpack(">L" ,socketClientFile.read(struct.calcsize(">L")))[0]
			if imageLength == 0:
				break

			rawImageData = socketClientFile.read(imageLength)		
			imageBuffer.write(rawImageData)
			imageBuffer.seek(0)
			# image = ImageTk.PhotoImage(Image.frombytes("RGBA", (800, 600) ,rawImageData))
			self.ref_reserve["image"] = ImageTk.PhotoImage(Image.open(imageBuffer).resize((1280, 720)))

			self.canvas.create_image(0, 0, anchor="nw", image=self.ref_reserve["image"])
			self.canvas.update()
			
			imageBuffer.seek(0)
			imageBuffer.truncate()

		#self.canvas.create_text((int(1280/2), int(720/2)), anchor="nw", text="play over.")
		self.canvas.delete(tk.ALL)
		self.canvas.create_text(((1280/2), (720/2)), anchor="nw", text="play over.", fill="white")
		self.canvas.update()

		socketClientFile.close()
		socketClient.close()

	def run(self):
		self.mainloop()


if __name__ == "__main__":
	client = guiRatClient()
	client.run()

		