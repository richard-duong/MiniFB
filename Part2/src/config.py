# this config file is explicitly just for servers to access
import sys
sys.dont_write_bytecode = True


commands = 	{	
	"menu": 		0,		# prints menu / commands (alias)
	"help": 		0,		# prints menu / commands
	"logout": 		1,		# logs user out
	"logoff": 		1,		# logs user out (alias)
	"msg": 			2,		# private messages a user
	"glist": 		3,		# list groups / members
	"gjoin": 		4,		# joins group
	"gquit": 		5,		# quits group
	"gmsg": 		6,		# group messages a group_id
	"broadcast": 	7,		# broadcasts to all online users
	"unread": 		8,		# view unread messages
	"count": 		9,		# display count unread messages
	"changepw": 	10		# change password
}

recv_cmds = {
	"glist": 		0,		# receiving grouplist
	"unread": 		1,		# receiving unread messages
	"count":		2,		# receiving count of messages
	"msg_recv": 	3,		# receiving incoming message
	"msg_fail": 	4,		# receiving message from server fail
	"msg_pass": 	5,		# receiving message from server pass
	"cpw_fail": 	6,		# receiving change password fail
	"cpw_pass": 	7,		# receiving change password success
	"gjoin_fail": 	8,		# receiving join group fail
	"gjoin_pass": 	9,		# receiving join group pass
	"gquit_fail": 	10,		# receiving quit group fail
	"gquit_pass": 	11		# receiving quit group pass
}
