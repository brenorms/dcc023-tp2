from struct import pack, unpack
import socket
import sys
import select
import time

servidor_dst = 0xFFFF
#num_sequencia = 0

class Cliente:
	
	def __init__(self, connection_address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.connect(connection_address)
		self.id = 0
		self.num_sequencia = 0
		self.message_queues = {}
		self.readable = [self.con, sys.stdin]
		self.writable = []

	def oiMessage(self):
		tipoMensagem = pack("!H", 3)
		origem = pack("!H", 0)
		destino = pack("!H", servidor_dst)#destino do cliente e' o servidor
		self.num_sequencia = self.num_sequencia%65536
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + (sequencia)
		#print(msg_final)
		self.con.send(msg_final)
		#print("To aqui")
		data = self.con.recv(8)
		#print("To aqui2222")
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		self.id = testeDestino
		#self.num_sequencia = self.num_sequencia + 1
		print("id", self.id)

	def send_message_1(self):
		tipoMensagem = pack("!H", 1)
		origem = pack("!H", self.id)
		destino = pack("!H", self.id)
		self.num_sequencia = (self.num_sequencia + 1)%65536
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + (sequencia)
		#time.sleep(6)
		self.con.send(msg_final)

	def send_message_2(self):
		pass

	def send_message_3(self):
		pass

	def send_message_4(self):
		#print(self.id)
		tipoMensagem = pack("!H", 4)
		origem = pack("!H", self.id)
		destino = pack("!H", self.id)
		self.num_sequencia = (self.num_sequencia + 1)%65536
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + (sequencia)
		self.con.send(msg_final)

	def send_message_5(self, msg, destination):
		#print(self.id)
		tipoMensagem = pack("!H", 5)
		origem = pack("!H", self.id)
		destino = pack("!H", destination)
		self.num_sequencia = (self.num_sequencia + 1)%65536
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + (sequencia)
		msg_final = msg_final + pack("!H", len(msg))
		msg = msg.encode()
		self.con.send(msg_final + msg)

	def send_message_6(self):
		#print(self.id)
		#print("DIGITE QUAL MENSAGEM DESEJA ENVIAR: ")
		#msg = sys.stdin.readline()
		tipoMensagem = pack("!H", 6)
		origem = pack("!H", self.id)
		destino = pack("!H", self.id)#destino do cliente e' o servidor
		self.num_sequencia = (self.num_sequencia + 1)%65536
		sequencia = pack("!H", self.num_sequencia)
		msg_final = tipoMensagem + origem + destino + (sequencia)
		#msg_final = msg_final + pack("!H", len(msg))
		#print("LEN-MSG = ", len(msg))
		#msg_final = msg_final + msg
		#print(msg)
		#print(isinstance(msg,str))
		#msg = msg.encode()
		#print(msg)
		#print(self.id)
		#self.con.send(msg_final + msg)
		#print(msg_final)
		self.con.send(msg_final)
		#self.readable.append(s)
		#print("vim parar aqui")

	def flwMessage(self):
		pass

	def receiveOk(self):
		print("tentando receber")
		data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		if testeTipo == 1:
			print("OK")
			return True
		else:
			print("Nao OK")
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

	def receive5(self, data):
		#data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		data2 = self.con.recv(2)
		#print("DATA = ", data2)
		len_msg = unpack("!H", data2)[0]
		#print("LEN = ", len_msg)
		data3 = self.con.recv(len_msg)
		print("Dados recebidos: "+data3.decode()) 
		self.send_message_1()

	def receive4(self):
		#print("Fechando conexao com cliente!")
		print("FLW")
		self.con.close()

	def receiveCList(self, data):
		#print("Ja e um bom avanco")
		#data = self.con.recv(8)
		testeTipo = unpack("!H", data[:2])[0]
		testeOrigem = unpack("!H", data[2:4])[0]
		testeDestino = unpack("!H", data[4:6])[0]#id estara aqui pq o destino do servidor foi o cliente
		testeSequencia = unpack("!H", data[6:8])[0]
		#print(data)
		data2 = self.con.recv(2)
		#print("DATA = ", data2)
		len_msg = unpack("!H", data2)[0]
		#print("LEN = ", len_msg)
		for i in range(0,len_msg):
			data3 = self.con.recv(2)
			unpack_int = unpack("!H", data3)[0]
			print(unpack_int)

	def testeInf(self):
		inicial = True
		while 1:
			scoket_list = [self.con, sys.stdin]
			if inicial == True:
				print("Digite qual tipo de mensagem deseja enviar: 4/5/6")
			readable, _, _ = select.select(scoket_list, [], [])
			for s in readable:
				if s == self.con:
					data = self.con.recv(8)
					#print(data)
					msg_type = unpack("!H", data[:2])[0]
					if msg_type == 7:
						self.receiveCList(data)
					elif msg_type == 5:
						self.receive5(data)
					elif msg_type == 4:
						self.receive4()
					elif msg_type == 1:
						print("OK")
					elif msg_type == 2:
						print("ERRO")
				elif s == sys.stdin:
					#if inicial != True:
						#pass
					inicial = False
					if inicial == False:
						print("Digite qual tipo de mensagem deseja enviar 4/5/6")
					tipo = int(sys.stdin.readline())
					if tipo == 5:
						print("Qual mensagem deseja enviar? ")
						msg = sys.stdin.readline()
						print("Digite qual o id do destino da mensagem: ")
						destination = int(sys.stdin.readline())
						self.send_message_5(msg, destination)
					if tipo == 6:
						self.send_message_6()
					if tipo == 4:
						self.send_message_4()
						self.receiveOk()
						exit()

				# print("to dentro")
				# print(s)
				# if s==sys.stdin.fileno():
				# 	continue
				# teste = 0
				# while teste != 6:
				# 	teste = int(input("novo teste: "))
				# 	msg = input("mensagem: ")
				# print(teste)
				# print(self.id)
				# print(self.id)
				# tipoMensagem = pack("!H", teste)
				# origem = pack("!H", self.id)
				# destino = pack("!H", self.id)#destino do cliente e' o servidor
				# sequencia = pack("!H", self.num_sequencia)
				# msg_final = tipoMensagem + origem + destino + sequencia
				# #msg_final = msg_final + pack("!H", len(msg))
				# print("LEN-MSG = ", len(msg))
				# #msg_final = msg_final + msg
				# print(msg)
				# print(isinstance(msg,str))
				# #msg = msg.encode()
				# print(msg)
				# print(self.id)
				# #self.con.send(msg_final + msg)
				# print(msg_final)
				# self.con.send(msg_final)
				# self.readable.append(s)
				# print("vim parar aqui")
			# for s in exceptional:
			# 	pass
				# self.readable.remove(s)
				# if s in servidor.writable:
				# 	servidor.writable.remove(s)
				# s.close()
				# del servidor.message_queues[s]
			
def main():
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
	connection_address = (IP, PORT)
	clientezim = Cliente(connection_address)
	clientezim.oiMessage()
	#testeSucess = clientezim.receiveOk()
	clientezim.testeInf()


if __name__ == "__main__":
	main()