import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# i=input()
	i='1'
	s.connect((HOST, PORT))
	while i!='q':
		# s.sendall(i.encode())
		data = s.recv(1024)
		print('Received', s.recv(1024))
		# i=input()