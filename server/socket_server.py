import socket
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", type=int, metavar='<#port>',
                    help="server port number", required=True)
args = parser.parse_args()
pnumber = args.p

HOST, PORT = "", pnumber
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("The web server has already established, running on port %i" % pnumber)

while(True):
    s.listen(0)

    client, address = s.accept()
    print(str(address) + " connected")
    request = client.recv(1024).decode('utf-8')
    print(request)
    try:
        fileName = request.split()[1]
        if fileName == '/' or fileName == '/favicon.ico':
            fileName = '/index.html'

        print('opening %s' % fileName)
        f = open(fileName[1:])
        outputdata = f.read()
        f.close()
        client.send(b'HTTP/1.1 200 OK\r\n\r\n')
        client.send(bytes(outputdata,'utf-8'))
        client.close()
        
    except:
        print("exception raise")
        client.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        client.send(bytes('404 Not Found','utf-8'))
        client.close()
