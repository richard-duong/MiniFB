import sys

from config import commands
from config import recv_cmds
import parse



class Client_Core:
	
	def __init__(self, usr, pwd, conn):
		self.usr = usr
		self.pwd = pwd
		self.conn = conn

	def receive_thread(self, sock):
		conn = self.conn
		while True:
			cnt = 0
			try:
				server_msg = conn.recv(4096)
				server_msg = parse.stringToTuple(server_msg)
				option = server_msg[0]
				args = server_msg[1:]

				# display group list
				if recv_cmds[option] == 0:	
					print "Group List"
					print "-------------------------------"	
					for group in args:
						print str(cnt) + ' - ' + group
						cnt += 1
					
				# display unread messages
				elif recv_cmds[option] == 1:
					print "Unread Messages"
					print "-------------------------------"
					for msg in args:
						print str(cnt) + ' - ' + msg	
						cnt += 1
			
				# display number of unread messages
				elif recv_cmds[option] ==  2:
					print "Number of unread messages: " + args[0]

				# display received message
				elif recv_cmds[option] == 3:
					print "Incoming message from " + args[0]
					 
				elif recv_cmds[option] == 4:
					print "Message failed to send " + args[0]

				elif recv_cmds[option] == 5:
					print "Message successfully sent " + args[0]

				elif recv_cmds[option] == 6:
					print "Change password failed, incorrect password " + args[0]

				elif recv_cmds[option] == 7:
					print "Change password success " + args[0]

				elif recv_cmds[option] == 8:
					print "Group join failed: " + args[0]

				elif recv_cmds[option] == 9:
					print "Group join success: " + args[0]

				elif recv_cmds[option] == 10:
					print "Group quit fail: " + args[0]
 
				elif recv_cmds[option] == 11:
					print "Group quit success: " + args[0]

			except:
				print 'Connection with server closed'
				break
			
		
	def run(self, args):
		option = args[0]		
		args = args[1:]

		# display menu
		if commands[option] == 0:
			self.run_menu()

		# client logout
		elif commands[option] == 1:
			self.run_logout()

		# private message
		elif commands[option] == 2:
			self.run_msg(args)

		# display group list
		elif commands[option] == 3:
			self.run_glist()

		# join group
		elif commands[option] == 4:
			self.run_gjoin(args)

		# quit group
		elif commands[option] == 5:
			self.run_gquit(args)

		# group message
		elif commands[option] == 6:
			self.run_gmsg(args)

		# broadcast to all online
		elif commands[option] == 7:
			self.run_broadcast(args)
	
		# display unread messages
		elif commands[option] == 8:
			self.run_unread()

		# display count of unread messages
		elif commands[option] == 9:
			self.run_count()

		# change password
		elif commands[option] == 10:
			self.run_changepw(args)
		
		# error
		else:
			print 'Client_Core: Command does not exist!'		


	# get command from prompt
	def prompt(self):
		print ""
		print "For commands menu, type /help"
		args = raw_input("> ")
		return parse.stringToArgs(args)

	# displays the menu
	def run_menu(self):
		print "\n\n"
		print "Help Menu and Commands"
		print "===================================================================================="
		print "/help or /menu".ljust(30) + 					"Display the help menu"
		print "/logout".ljust(30) + 						"Log user out"
		print "/msg [user] [message]".ljust(30) + 			"Sends a private message to the user"
		print "/glist".ljust(30) + 							"Displays the groups and members"
		print "/gjoin [group]".ljust(30) + 					"Request to join a group"
		print "/gquit [group]".ljust(30) + 					"Request to quit a group"
		print "/gmsg [group] [message]".ljust(30) + 		"Sends a message to all group members"
		print "/broadcast [message]".ljust(30) + 			"Sends a message to all online users"
		print "/unread".ljust(30) + 						"Displays all unread messages"
		print "/count".ljust(30) +							"Displays how many unread messages"
		print "/changepw [oldpw] [newpw]".ljust(30) +		"Change old password"

	def run_logout(self):
		conn = self.conn
		conn.sendall("logout")	
		conn.close()
		print 'Sent logout request to server'
		print 'Bye!'
		sys.exit()

	def run_msg(self, args):	
		conn = self.conn
		args = args[0].split(" ", 1)
		if len(args) == 2:
			receiver = args[0]
			message = parse.tupleToString(tuple(args[1:]))
			send_msg = parse.tupleToString(("msg", receiver, message))
			conn.sendall(send_msg)	
			print 'Sent private message'
		else:
			print 'Not enough arguments to send message!'

	def run_glist(self):
		conn = self.conn
		conn.sendall("glist")
		print 'Display group list'

	def run_gjoin(self, args):
		conn = self.conn
		args = args[0].split(" ", 1)
		if len(args) == 1:
			group = args[0]
			send_msg = parse.tupleToString(("gjoin", group))
			conn.sendall(send_msg)
			print 'Join Group'
		else:
			print 'Not the right number of arguments to join group!'


	def run_gquit(self, args):
		conn = self.conn
		args = args[0].split(" ", 1)
		if len(args) == 1:
			group = args[0]
			send_msg = parse.tupleToString(("gquit", group))
			conn.sendall(send_msg)
			print 'Quit Group'
		else:
			print 'Not the right number of arguments to quit group!'
			

	def run_gmsg(self, args):
		conn = self.conn
		args = args[0].split(" ", 1)
		if len(args) >= 2:
			group = args[0]
			message = parse.tupleToString(tuple(args[1:]))
			send_msg = parse.tupleToString(("gmsg", group, message))
			conn.sendall(send_msg)	
			print 'Sent message to group'
		else:
			print 'Not enough arguments to send message to group!'


	def run_broadcast(self, args):
		conn = self.conn
		if len(args) >= 1:
			message = parse.tupleToString(args)
			send_msg = parse.tupleToString(("broadcast", message))
			conn.sendall(send_msg)
			print 'Broadcasted message'
		else:	
			print 'Not enough args to broadcast!'


	def run_unread(self):
		conn = self.conn
		conn.sendall("unread")
		print 'Display unread messages'


	def run_count(self):
		conn = self.conn
		conn.sendall("count")
		print 'Display count of unread messages'

	
	def run_changepw(self, args):
		conn = self.conn
		args = args[0].split(" ", 1)
		if len(args) == 2:
			old_pw = args[0]
			new_pw = args[1]
			send_msg = parse.tupleToString(("changepw", old_pw, new_pw))
			conn.sendall(send_msg)
			print 'Sent request to change password'
		else:
			print 'Needs exact args to make password change request'
				
