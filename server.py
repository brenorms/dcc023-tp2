import select
import socket
import sys
import queue as Queue
from struct import pack,unpack

clienteId = 0
mensagem_queue = {}

class Serveridor:

	def __init__(self,server_address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.bind(server_address)
		self.con.listen(5)
		self.con.setblocking(0)
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
		#mensagem_queues[s].put(tipoMensagem + origem + destino + sequencia)
		#print("Mensagem Salva = ", self.message_queues[s].get())
		#s.send(msg_final)
		print("Enviando MSG OK, BOA SORTE SOLDADO!")

	def sendOk2(self, clienteId, sequencia):
		tipoMensagem = pack("!H", 1)
		s = self.verificarConexao(clienteId)
		origem = pack("!H", self.id)
		destino = pack("!H", clienteId)
		sequencia = pack("!H", sequencia)
		msg_final = tipoMensagem + origem + destino + sequencia
		print("ID = ", clienteId)
		print("Mensagem Nova Salva = ", (tipoMensagem + origem + destino + sequencia))
		if s not in self.writable:
			self.writable.append(s)
		self.message_queues[s].put(tipoMensagem + origem + destino + sequencia)
		#mensagem_queues[s].put(tipoMensagem + origem + destino + sequencia)
		#print("Mensagem Salva = ", self.message_queues[s].get())
		#s.send(msg_final)
		print("SENDOK2");

	def sendMessage(self, clienteId, dados, socket, message_pack, msg):
		if socket not in self.writable:
			self.writable.append(socket)
		self.message_queues[socket].put(dados + message_pack + msg)

	def conexao(self):
		connection, client_address = self.con.accept()
		connection.setblocking(0)
		self.readable.append(connection)
		self.message_queues[connection] = Queue.Queue()
		return connection,client_address

def main():
	PORT = int(sys.argv[1])
	ADRESS = ('localhost', PORT)
	servidor = Serveridor(ADRESS)
	broadcast = 0
	clienteId = 0
	i = 0
	while servidor.readable:
		#print("ENTREI AQUI")
	#	print(sys.stderr, '\nwaiting for the next event')
		readable, writable, exceptional = select.select(servidor.readable, servidor.writable,
            servidor.readable)
		for s in readable:
			#print("Dentro1")	
			if s is servidor.con:
				print("Conectando socket")
				servidor.conexao()
			else:
				#print("S = ", s)
				#print("Entrei aqui")
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
				if tipoMensagem == 4:
					continue
				if tipoMensagem == 5:
					#print("TO HERE")
					if destino == 20:
						broadcast = 1
					else:
						broadcast = 0
						msg_len = s.recv(2)
						msg_len_u = unpack("!H", msg_len)[0]
						print("MSG-LEN = ", msg_len_u)
						mensagem = s.recv(msg_len_u)
						print("MENSAGEM = ", mensagem)
						servidor.sendOk(origem,sequencia)
						#print("VERIFIQUEI CONEXAO")
						v = servidor.verificarConexao(destino)
						if v == -1:
							#print("uai?")
							#sendErro
							pass
						else:
							#print("entrei no else")
							servidor.sendMessage(origem, data, v, msg_len, mensagem)
					#print("Nova funcao")
					#print("origem = ", origem)
				if tipoMensagem == 6:
					servidor.sendOk(origem, sequencia)
					novo_tipo_mensagem = pack("!H", 7)
					dados_restantes = data[2:8]
					dados_restantes = novo_tipo_mensagem + dados_restantes
					dados_restantes = dados_restantes + pack("!H", len(servidor.connected_sockets))
					socket_destino = servidor.verificarConexao(destino)
					if socket_destino not in servidor.writable:
						servidor.writable.append(socket_destino)
					servidor.message_queues[socket_destino].put(dados_restantes)
					for clientes_ids, val in servidor.connected_sockets.items():
						print(clientes_ids)
						ids = pack("!H", clientes_ids)
						servidor.message_queues[socket_destino].put(ids)
		for s in writable:
			#print("Dentro2")
			try:
			#	print("dentro do Try")
				#print("S = ", s)
				print("mandando msg")
				next_msg = servidor.message_queues[s].get_nowait()#se coloco get(True) ou get(), funciona.
				print(next_msg)
				print("FOI")
			except:
			#	print("Except")
				servidor.writable.remove(s)
			else:
			#	print("Else!")
				s.send(next_msg)
		for s in exceptional:
			#print("Dentro3")
			servidor.readable.remove(s)
			if s in servidor.writable:
				servidor.writable.remove(s)
			s.close()
			del servidor.message_queues[s]


if __name__ == "__main__":
	main()