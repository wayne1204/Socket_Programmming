from socket import *
import sys

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-ip", metavar='<IP>',
                    help="It is the IP Address Of Proxy Server", required=True)
parser.add_argument("-p", type=int, metavar='<#port>',
                    help="It is the port number of Proxy Server", required=True)
parser.add_argument("-destip", metavar='<IP>',
                    help="It is the IP Address of the Server", required=True)
parser.add_argument("-destp", type=int, metavar='<#port>',
                    help="It is the port number of the Server", required=True)

args = parser.parse_args()
proxyIP = args.ip
proxyPort = args.p
serverIP = args.destip
serverPort = args.destp

# import threading

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
HOST, PORT = proxyIP, proxyPort
print("running proxy server at IP address: %s on port#%i" % (proxyIP, proxyPort))
tcpSerSock.bind((HOST,PORT))
tcpSerSock.listen(5)
connections = []


# Fill in end.
while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	# cThread = threading.Thread(target=handler, args=(tcpCliSock, addr))
	# cThread.daemon = True
	# cThread.start()
	# connections.append(tcpCliSock)
	print('Received a connection from:', addr)
	request = tcpCliSock.recv(1024).decode('utf-8') # Fill in start.		# Fill in end.
	print('=======[request]=======')
	print(request)
	# Extract the filename from the given message
	filename = request.split()[1]
	if filename == '/' or filename == '/favicon.ico':
		filename = '/index.html'

	print('request for filename %s' % filename)
	fileExist = "false"
	try:
		# Check wether the file exist in the cache
		f = open(filename[1:], 'r')
		outputdata = f.read()
		f.close()
		# ProxyServer finds a cache hit and generates a response message
		# Fill in start.
		fileExist = "true"
		tcpCliSock.send(b'HTTP/1.1 200 OK\r\n\r\n')
		tcpCliSock.send(bytes(outputdata,'utf-8'))
		tcpCliSock.close()
		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			print('create a new socket for proxy server')
			c = socket(AF_INET, SOCK_STREAM)
			try:
				# Connect to the socket to port 80
				# Fill in start.
				c.connect((serverIP, serverPort))
				# Fill in end.
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile("wb", 0)
				string = "GET " + filename + " HTTP/1.1\r\n\r\n"
				fileobj.write(bytes(string,'utf-8'))
				# Read the response into buffer
				# Fill in start.
				
				receive = c.recv(2048)
				print(receive)
				receive = (receive.partition(b'\r\n\r\n'))[2]
				# Fill in end.
				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				# Fill in start.
				tmpFile = open("./" + filename,"wb")
				tmpFile.write(receive)
				tcpCliSock.send(b'HTTP/1.1 200 OK\r\n\r\n')
				tcpCliSock.send(receive)
				tcpCliSock.close()
				# Fill in end.
			except:
				print("Illegal request")
				tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n\r\n")
				tcpCliSock.send(b"404 Not Found\r\n\r\n")
		else:
			# HTTP response message for file not found
			# Fill in start.
			tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n\r\n")
			tcpCliSock.send(b"404 Not Found\r\n\r\n")
			# Fill in end.
	# Close the client and the server sockets
	tcpCliSock.close()
# Fill in start.
# Fill in end.
