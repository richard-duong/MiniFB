import time
import socket
import sys
from thread import *
from getpass import getpass
import os

from thread import *
from client_core import *


'''
Create Socket
'''

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Created socket for the client'

except socket.error:
	print 'Failed to create socket for the client'
	sys.exit()



'''
Resolve Hostname
'''

HOST = 'localhost'
PORT = 9999

try:
	remote_ip = socket.gethostbyname(HOST)
	print 'IP address of ' + HOST + ' on ip ' + remote_ip
except socket.error:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()


'''
Connect to remote server
'''
sock.connect((remote_ip, PORT))
print 'Socket connected to ' + HOST + ' on ip ' + remote_ip + ' through port ' + str(PORT)



'''
Login user
'''

login_count = 0
reply = None

while reply != "valid":
	usr = raw_input("Enter your username: ")
	pwd = getpass("Enter your password: ")
	print 'Sent username and password ' + usr + ' ' + pwd
	sock.sendall(usr + '<>' + pwd)
	reply = sock.recv(5)
	
	# if successful login
	if reply == 'valid':
		print 'Login successful!'
		print 'Welcome back ' + usr
		break
	
	# if successful login but another user is logged into account	
	elif reply == 'exist':
		print 'Existing user is logged in!'
		print 'Please contact us for tech support'
		print ''
	
	# if invalid authentication, try again
	elif reply == 'nalid':
		print 'We could not find your username / password combination'
		print 'Please try again'
		print ''

	# if too many attempts, quit
	elif reply == 'close':
		print 'Too many attempts have been made'
		print 'Exiting the app'
		print ''
		sock.close()
		sys.exit()

	# error case
	else:
		print 'Received: ' + reply
		print 'Client Login: Invalid response from server'
		print 'Exiting the app'
		sock.close()
		sys.exit()
		

'''
Log client "into" the server
'''
# generate client core for processing commands
core = Client_Core(usr, pwd, sock)

# start receiving thread
start_new_thread(core.receive_thread, (sock,))

# display count of unread messages on login
core.run_count()

# run app while logged in
while True:
	args = core.prompt()
	if args != None:
		core.run(args)
	time.sleep(1)
