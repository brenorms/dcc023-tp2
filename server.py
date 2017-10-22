import select
import socket
import sys
from multiprocessing import Queue
from struct import pack,unpack

clienteId = 0

class Serveridor:

	def __init__(self,server_address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.setblocking(0)
		self.con.bind(server_address)
		self.con.listen(5)
		self.readable = [self.con]
		self.writable = []
		self.id = 0xFFFF
		self.connected_sockets = {}
		self.message_queues = {}

	def verificarConexao(self, clienteId):
		if clienteId in self.connected_sockets:
			return self.connected_sockets[clienteId]
		else:
			return -1

	def sendOk(self, clienteId, sequencia):
		tipoMensagem = pack("!H", 1)
		s = self.verificarConexao(clienteId)
		origem = pack("!H", self.id)
		destino = pack("!H", clienteId)
		sequencia = pack("!H", sequencia)
		msg_final = tipoMensagem + origem + destino + sequencia
		print("ID = ", clienteId)
		if s not in self.writable:
			self.writable.append(s)
		self.message_queues[s].put(tipoMensagem + origem + destino + sequencia)
		print("Mensagem Salva = ", self.message_queues[s].get())
		#s.send(msg_final)
		print("Enviando MSG OK, BOA SORTE SOLDADO!")

	def con_socket(self):
		connection, client_address = self.con.accept()
		connection.setblocking(0)
		self.readable.append(connection)
		self.message_queues[connection] = Queue()
		return connection,client_address

def main():
	PORT = int(sys.argv[1])
	ADRESS = ('localhost', PORT)
	servidor = Serveridor(ADRESS)
	broadcast = 0
	clienteId = 0
	while servidor.readable:
		readable, writable, exceptional = select.select(servidor.readable, servidor.writable,
            servidor.readable)
		for s in readable:
			if s is servidor.con:
				servidor.con_socket()
			else:
				print("Entrei aqui")
				data = s.recv(8)
				tipoMensagem = unpack("!H", data[0:2])[0]
				origem = unpack("!H", data[2:4])[0]
				destino = unpack("!H", data[4:6])[0]
				sequencia = unpack("!H", data[6:8])[0]
				if destino == 0:
					broadcast = 1
				elif destino != 0:
					try:
						servidor.connected_sockets[destino]
					except:
						destino = -1
				if tipoMensagem == 3:
					print("Recebi mensagem hi")
					if(origem == 0):
						servidor.connected_sockets[clienteId] = s
						servidor.sendOk(clienteId,sequencia)
						clienteId = clienteId + 1


if __name__ == "__main__":
	main()