from struct import pack, unpack
import socket
import sys

servidor_dst = 0xFFFF
#num_sequencia = 0

class Cliente:
	
	def __init__(self, connection_address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.connect(connection_address)
		self.id = 0
		self.num_sequencia = 0

	def oiMessage(self):
		tipoMensagem = pack("!H", 3)
		origem = pack("!H", 0)
		destino = pack("!H", servidor_dst)#destino do cliente e' o servidor
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + sequencia
		print(msg_final)
		self.con.send(msg_final)
		data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		self.id = testeDestino
		self.num_sequencia = self.num_sequencia + 1
		print("id", self.id)

	def flwMessage(self):
		pass

	def teste(self):
		pass


def main():
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
	connection_address = (IP, PORT)
	clientezim = Cliente(connection_address)
	clientezim.oiMessage()

if __name__ == "__main__":
	main()