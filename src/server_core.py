import socket
import sys
from thread import *
import time


from config import *
from thread import *
from client_core import *
import parse

clients = {}

client_db = {
	"user1": 
	{	"password": "pw1",
		"online": False,
		"messages": [],
	},
	"user2":
	{	"password": "pw2",
		"online": False,
		"messages": [],
	},
	"user3":
	{	"password": "pw3",
		"online": False,
		"messages": [],
	}
}

group_db = {
	"group1": set(),
	"group2": set()
}


class Server_Core:

	def __init__(self, max_attempts = 3):
		self.max_attempts = max_attempts

	def receive_clients(self, sock):	
		while True:
			conn, addr = sock.accept()
			print 'Server has connected with ' + addr[0] + ':' + str(addr[1])
			start_new_thread(self.client_thread, (conn,))

	def login(self, usr, pwd):

		# successful login but user is online
		if usr in client_db and client_db[usr]["password"] == pwd and client_db[usr]["online"] == 1:
			return "exist"
				
		# successful login
		elif usr in client_db and client_db[usr]["password"] == pwd:
			return "valid"

		# incorrect login
		else:
			return "nalid"

	def run_logout(self, usr):
		conn = clients.pop(usr)
		client_db[usr]["online"] = False
		conn.close()
		print 'User ' + usr + ' has logged out'


	# args format: cmd, receiver, message
	def run_msg(self, usr, args):	
		message = usr + ' - ' + args[2]
		receiver = args[1]	
		recv_msg = parse.tupleToString(("msg_recv", message))

		# if nonexistent user, notify sender
		if receiver not in client_db:
			send_msg = parse.tupleToString(("msg_fail", "Recipient does not exist"))
			print 'User ' + usr + ' sent a message to a recipient that does not exist'
		
		# if receiver is online, send immediately
		elif receiver in clients:
			recv_conn = clients[receiver]	
			recv_conn.sendall(recv_msg)		
			send_msg = parse.tupleToString(("msg_pass", "Sent to " + receiver)) 
			print 'User ' + usr + ' sent a message to ' + receiver

		# if receiver is existing offline user, send to unread messages
		elif client_db[receiver]["online"] == False:
			client_db[receiver]["messages"].append(message)
			send_msg = parse.tupleToString(("msg_pass", "Sent to " + receiver + "'s inbox"))
			print "User " + usr + " sent a message to " + receiver + "'s inbox"
		
		# error
		else:
			print 'Server_Core: run_msg error'	

		# let the sender know the status
		send_conn = clients[usr]
		send_conn.sendall(send_msg)


	def run_glist(self, usr):
		message = ["glist"]
		for group in group_db.keys():
			message.append(group)
		send_msg = parse.tupleToString(tuple(message))
		send_conn = clients[usr]
		send_conn.sendall(send_msg)
		
	# args format: cmd, group
	# come back later to add sender status
	def run_gjoin(self, usr, args):
		group = args[1]
		if group in group_db:
			group_db[group].add(usr)
		send_conn = clients[usr]			


	# args format: cmd, group
	# come back later to add sender status
	def run_gquit(self, usr, args):
		group = args[1]
		if group in group_db:
			group_db[group].discard(usr)
		send_conn = clients[usr]

	
	# args format: cmd, group, message
	def run_gmsg(self, usr, args):
		group = args[1]
		message = usr + ' (' + group + ') - ' + args[2]	
		recv_msg = parse.tupleToString(("msg_recv", message))	

		receivers = []		
		if group in group_db:
			receivers = group_db[group]
			send_msg = parse.tupleToString(("msg_pass", "Sent to (" + group + ")"))
			print 'User ' + usr + ' sent a message to group ' + group

		else:
			send_msg = parse.tupleToString(("msg_fail", "Group does not exist"))
			print 'User ' + usr + ' sent a message to a group that does not exist'

		for receiver in receivers:	
			if receiver in clients and receiver != usr:
				recv_conn = clients[receiver]
				recv_conn.sendall(recv_msg)

			elif client_db[receiver]["online"] == False:
				client_db[receiver]["messages"].append(message)
			
			else:
				print 'Server_Core: run_gmsg error'

		# let the sender know the status
		send_conn = clients[usr]
		send_conn.sendall(send_msg)


	# args format: cmd, message
	def run_broadcast(self, usr, args):
		message = usr + ' [Broadcast] - ' + args[1]
		recv_msg = parse.tupleToString(("msg_recv", message))
		send_msg = parse.tupleToString(("msg_pass", "Broadcast to all"))
	
		for receiver in clients:
			if receiver != usr:
				recv_conn = clients[receiver]
				recv_conn.sendall(recv_msg)
		
		send_conn = clients[usr]
		send_conn.sendall(send_msg)
		print 'User ' + usr + ' broadcasted a message'


	def run_unread(self, usr):
		message = ["unread"]	
		for unread_msg in client_db[usr]["messages"]:
			message.append(unread_msg)

		client_db[usr]["messages"] = []		
		send_msg = parse.tupleToString(tuple(message))
		send_conn = clients[usr]
		send_conn.sendall(send_msg)
		print 'User ' + usr + ' received unread messages'
		

	def run_count(self, usr):	
		count = len(client_db[usr]["messages"])
		send_msg = parse.tupleToString(("count", str(count)))
		send_conn = clients[usr]
		send_conn.sendall(send_msg)
		print 'User ' + usr + ' received number of unread messages'


	# args format: cmd, old_pw, new_pw
	def run_changepw(self, usr, args):
		old_pw = args[1]
		new_pw = args[2]

		if client_db[usr]["password"] == old_pw:
			client_bd[usr]["password"] = new_pw
			send_msg = parse.tupleToString(("cpw_pass", "Successfully changed password"))
			print 'User ' + usr + ' successfully changed their password'

		else:
			send_msg = parse.tupleToString(("cpw_fail", "Incorrect old password, no changes made"))
			print 'User ' + usr + ' unsuccessfully tried to change their password'

		# update sender's status
		send_conn = clients[usr]
		send_conn.sendall(send_msg)
		

	def run(self, usr, args=None):
		option = args[0]

		# bad option
		if option not in commands:
			print 'Error receieved bad packet: ' + args[0]

		# client logout	
		elif commands[option] == 1:
			self.run_logout(usr)
			print 'Logging out for user: ' + usr
			
		# message another user
		elif commands[option] == 2:
			self.run_msg(usr, args)
			print 'Messaging for user: ' + usr

		# return group list
		elif commands[option] == 3:
			self.run_glist(usr)
			print 'Returning Group List for user: ' + usr

		# join group
		elif commands[option] == 4:
			self.run_gjoin(usr, args)
			print 'Joining Group for user: ' + usr

		# quit group
		elif commands[option] == 5:
			self.run_gquit(usr, args)
			print 'Quitting Group for user: ' + usr

		# send group message
		elif commands[option] == 6:
			self.run_gmsg(usr, args)
			print 'Sending Group message for user: ' + usr

		# send broadcast
		elif commands[option] == 7:
			self.run_broadcast(usr, args)
			print 'Sending Broadcast for user: ' + usr
		
		# return unread messages
		elif commands[option] == 8:
			self.run_unread(usr)	
			print 'Returning unread messages for user: ' + usr

		# return count of unread messages
		elif commands[option] == 9:
			self.run_count(usr)
			print 'Returning unread messages count for user: ' + usr

		# change password of user
		elif commands[option] == 10:
			self.run_changepw(usr, args)
			print 'Changing password for user: ' + usr

		# error	
		else:
			print 'Server_Core: Command does not exist!'	
			

	def client_thread(self, conn):
		
		# login authentication
		login_attempts = 0	
		login_result = None
		while login_result != "valid":
			userpass = conn.recv(1024)
			userpass = parse.stringToTuple(userpass)
			usr = userpass[0]
			pwd = userpass[1]
			login_result = self.login(usr, pwd)

			# kick user if too many invalid attempts
			if login_attempts >= self.max_attempts and login_result == "nalid":
				conn.sendall("close")
				conn.close()

			login_attempts += 1	
			conn.sendall(login_result)

		# after user logs in, set user to online, and add user to active clients dict
		client_db[usr]["online"] = True
		clients[usr] = conn	

		while client_db[usr]["online"] == True:
			try:
				cmd = conn.recv(1024)
			except: 
				break
			args = parse.stringToTuple(cmd)
			self.run(usr, args)
		
