import socket
import sys
from thread import *
from getpass import getpass
import os

'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.2.15'
port = 9999
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
print ''

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
usr = raw_input("Enter your username: ")
pwd = getpass("Enter your password: ")
s.sendall(usr + '<>' + pwd)


'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
reply = s.recv(5)
if reply == 'valid': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :

		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
			
		message = raw_input("\n\nChoose an option (type the number): \n 1. Logout \n 2. Post a message \n 3. Change Password \n")	
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				print 'Logout'
				s.sendall('1')
				s.close()
				sys.exit()

			# TODO: add logout operation
			elif message == str(2):
				print 'Post a message'
				message = raw_input("Type a message and hit enter: ")
				print "Sent: " + message
				s.sendall('2')
				s.sendall(message)
				

			# Add other operations, e.g. change password
			elif message == str(3):
				old_pwd = getpass("Old Password: ")
				new_pwd = getpass("New Password: ")
				s.sendall('3')
				s.sendall(old_pwd + '<>' + new_pwd)
					
				"""
				# faililng to receive message from server again
				rcv_msg = s.recv(5)
				print 'received message from server' + rcv_msg
				
				if rcv_msg == "valid":
					print "Successfully changed password"
				else:
					print "Incorrect old password, No changes were made"
				"""

		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'

s.close()
