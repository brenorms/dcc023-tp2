import select
import socket
import sys
try:
	import queue as Queue
except:
	import Queue as Queue
from struct import pack,unpack

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
		self.clienteId = 1#talvez comecar com 1 porque quando a mensagem tem destino 0 deve ser boradcast e nao o cliente 0


	def verificarConexao(self, clienteId):
		if clienteId in self.connected_sockets:
			#print("consegui achar")
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
		#print("ID = ", clienteId)
		if s not in self.writable:
			self.writable.append(s)
		self.message_queues[s].put(tipoMensagem + origem + destino + sequencia)
		#mensagem_queues[s].put(tipoMensagem + origem + destino + sequencia)
		#print("Mensagem Salva = ", self.message_queues[s].get())
		#s.send(msg_final)
		#print("Enviando MSG OK, BOA SORTE SOLDADO!")
		print("OK "+str(clienteId))

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

	def sendErro(self, clienteId, sequencia):
		s = self.verificarConexao(clienteId)
		tipoMensagem = pack("!H", 2)
		destino = pack("!H", clienteId)
		sequencia = pack("!H", sequencia)
		msg = tipoMensagem + destino + destino + sequencia
		if s not in self.writable:
			self.writable.append(s)
		self.message_queues[s].put(msg)
		print("ERRO ", destino)

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
	i = 0
	while servidor.readable:
		readable, writable, exceptional = select.select(servidor.readable, servidor.writable,
            servidor.readable)
		for s in readable:
			#print("Dentro1")	
			if s is servidor.con:
				#print("Conectando socket")
				servidor.conexao()
			else:
				#print("recebendo")
				data = s.recv(8)
				#print(data)
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
				if tipoMensagem == 1:
					print("Received OK "+str(origem))
				if tipoMensagem == 3:
					#print("Recebi mensagem hi")
					print("OI "+str(origem))
					if(origem == 0):
						servidor.connected_sockets[servidor.clienteId] = s
						servidor.sendOk(servidor.clienteId,sequencia)
						#print("Passei or aqui")
						servidor.clienteId = servidor.clienteId + 1
				if tipoMensagem == 4:
					if origem == destino:
						socket = servidor.verificarConexao(origem)
						servidor.sendOk(origem, sequencia)
						servidor.readable.remove(s)#socket ou s
						print("FLW "+str(origem))
					else:
						print("Origem != Destino, seu idiota!")
					
				if tipoMensagem == 5:
					if destino == 0:
						broadcast = True
					else:
						broadcast = False
					msg_len = s.recv(2)
					msg_len_u = unpack("!H", msg_len)[0]
					#print("MSG-LEN = ", msg_len_u)
					mensagem = s.recv(msg_len_u)
					#print("MENSAGEM = ", mensagem)
					servidor.sendOk(origem,sequencia)
					print("MSG from "+str(origem)+" to "+str(destino)+": "+str(mensagem))
					if destino==0:
						for i in range(1, servidor.clienteId):
							v = servidor.verificarConexao(i)
							servidor.sendMessage(origem, data, v, msg_len, mensagem)
					else:
						v = servidor.verificarConexao(destino)
						if v == -1:
							servidor.sendErro(origem, sequencia)
							pass
						else:
							servidor.sendMessage(origem, data, v, msg_len, mensagem)
				if tipoMensagem == 6:
					#print("entrei!!")
					servidor.sendOk(origem, sequencia)
					novo_tipo_mensagem = pack("!H", 7)
					dados_restantes = data[2:8]
					dados_restantes = novo_tipo_mensagem + dados_restantes
					dados_restantes = dados_restantes + pack("!H", len(servidor.connected_sockets))
					#print("Dados restantes =", dados_restantes)
					socket_destino = servidor.verificarConexao(destino)
					#print("socket Dest = ", socket_destino)
					# if socket_destino not in servidor.connected_sockets:
					# 	print("entrei")
					# 	print(socket_destino)
					# 	print(servidor.connected_sockets)
					# 	continue
					print("CREQ"+str(origem))
					if socket_destino not in servidor.writable:
						#print("entrei tb")
						servidor.writable.append(socket_destino)
					servidor.message_queues[socket_destino].put(dados_restantes)
					for clientes_ids, val in servidor.connected_sockets.items():
						#print("Id cliente = ", clientes_ids)
						ids = pack("!H", clientes_ids)
						servidor.message_queues[socket_destino].put(ids)
						#print("coloquei a mensagem na queue!!")
		for s in writable:
			try:
				print("Enviando...")
				next_msg = servidor.message_queues[s].get_nowait()#se coloco get(True) ou get(), funciona.
				#print(next_msg)
				#print("FOI")
			except:
				servidor.writable.remove(s)
			else:
				print("sent")
				print(next_msg)
				s.send(next_msg)
		for s in exceptional:
			servidor.readable.remove(s)
			if s in servidor.writable:
				servidor.writable.remove(s)
			s.close()
			del servidor.message_queues[s]

if __name__ == "__main__":
	main()