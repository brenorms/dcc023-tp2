from struct import pack, unpack
import socket
import sys
import select

servidor_dst = 0xFFFF
#num_sequencia = 0

class Cliente:
	
	def __init__(self, connection_address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.connect(connection_address)
		self.id = 0
		self.num_sequencia = 0
		self.message_queues = {}
		self.input = [self.con]
		self.output = []

	def oiMessage(self):
		tipoMensagem = pack("!H", 3)
		origem = pack("!H", 0)
		destino = pack("!H", servidor_dst)#destino do cliente e' o servidor
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + sequencia
		print(msg_final)
		self.con.send(msg_final)
		print("To aqui")
		data = self.con.recv(8)
		print("To aqui2222")
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		self.id = testeDestino
		self.num_sequencia = self.num_sequencia + 1
		print("id", self.id)

	def flwMessage(self):
		pass

	def receiveOk(self):
		data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		if testeTipo == 1:
			print("OK RECEBIDO!")
			return True
		else:
			return False

	def receiveMessage(self):
		data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		data2 = self.con.recv(2)
		print("DATA = ", data2)
		len_msg = unpack("!H", data2)[0]
		print("LEN = ", len_msg)
		data3 = self.con.recv(len_msg)
		print(data3.decode()) 

	def receiveCList(self):
		data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		data2 = self.con.recv(2)
		print("DATA = ", data2)
		len_msg = unpack("!H", data2)[0]
		print("LEN = ", len_msg)
		for i in range(0,len_msg):
			data3 = self.con.recv(2)
			unpack_int = unpack("!H", data3)[0]
			print(unpack_int)

	def testeInf(self):
		while 1:
			teste = 0
			while teste != 6:
				teste = int(input("novo teste: "))
				msg = input("mensagem: ")
			tipoMensagem = pack("!H", teste)
			origem = pack("!H", self.id)
			destino = pack("!H", self.id)#destino do cliente e' o servidor
			sequencia = pack("!H", self.num_sequencia)
			msg_final = tipoMensagem + origem + destino + sequencia
			#msg_final = msg_final + pack("!H", len(msg))
			print("LEN-MSG = ", len(msg))
			#msg_final = msg_final + msg
			msg = msg.encode()
			print(msg)
			print(self.id)
			#self.con.send(msg_final + msg)
			self.con.send(msg_final)
			print("vim parar aqui")
			testeSucess = self.receiveOk()
			self.receiveCList()

def main():
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
	connection_address = (IP, PORT)
	clientezim = Cliente(connection_address)
	clientezim.oiMessage()
	clientezim.testeInf()


if __name__ == "__main__":
	main()