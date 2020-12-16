import socket
import sys
from thread import *
import time

from thread import *
from server_core import *
from parse import *

'''
Create Socket for server
'''
HOST = ''
PORT = 9999

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print 'Created socket for the server'

except socket.error:
	print 'Failed to create socket for the server.'
	sys.exit() 	


'''
Bind socket to local host and port
'''
try:
	sock.bind((HOST, PORT))
	print 'Bind socket to the server'

except socket.error:
	print 'Failed to bind socket to server'
	sys.exit()


'''
Listen with socket on server
'''
sock.listen(10)
print 'Socket is now listening'


'''
Create Server Core and receive clients on parallel thread
'''
core = Server_Core()
start_new_thread(core.receive_clients, (sock,))


'''
server stats main thread
'''
while 1:
	message = raw_input()

	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'

	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'

	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'

	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'


'''
close server socket
'''
sock.close()





