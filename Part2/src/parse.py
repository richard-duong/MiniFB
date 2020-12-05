from config import commands

def stringToTuple(s):
	t = s.split("<>")
	return t

def tupleToString(t):
	s = ""
	for item in t:
		s += str(item) + "<>"
	return s[:-2]

def stringToArgs(s):
	
	# check to see if command is prefixed
	if s[0] != "/":
		print 'Parser: Needs "/" prefix'
		return None
	
	# check to see if command exists
	args = s[1:].split(" ", 1)
	if args[0] in commands:	
		return args

	print "Parser: Not a valid command"
	return None

