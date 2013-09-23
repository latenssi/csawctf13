import socket
import sys
import re
import time
from collections import defaultdict

remote_host = "128.238.66.216"
remote_port = 45678


#======== Solving methods ==========#

PRINTDEAD, PRINTLIVE = ' *'
BORDER = '#'
celltable = defaultdict(int, {
 (1, 2): 1,
 (1, 3): 1,
 (0, 3): 1,
 } )
 
def remove_shit(round):
	nls = 0
	new = ""
	for c in round:
		if c == '\n':
			nls += 1
		if nls >= 2:
			new += c
			
	return new
	
def remove_round_line(round):
	round_line = re.compile('.*(\n##### Round \d{1,3}: (?P<gens>\d{1,3}?) Generations #####).*')
	m = re.match(round_line, round)
	gens = m.groupdict()
	round = re.sub(round_line, '', round)
	return round, int(gens['gens'])
	
def initiate(round1):
	nls = 0
	width = 0
	for c in round1:
		if c == '\n':
			nls += 1
	
		if nls == 0 and c == BORDER:
			width += 1
	
	return width-2, nls-2
			
def parse_state(round, width, height):
	round = round[width+4:]
	round = round[:len(round)-width-5]
	lines = round.split(BORDER)
	clean = []
	state = defaultdict(int)
	for line in lines:
		if line and line != '\n':
			clean.append(line)
			
	for y in xrange(len(clean)):
		for x in xrange(len(clean[y])):
			if clean[y][x] == PRINTLIVE:
				state[(x,y)] = 1
				
	return state
	
def next_generation(universe, width, height):
	nextgen = defaultdict(int)
	for y in xrange(height):
		for x in xrange(width):
			nextgen[(x,y)] = celltable[
				(universe[(x,y)],
				 -universe[(x,y)] + sum(universe[(xn,yn)] 
										for yn in range(y-1,y+2)
										for xn in range(x-1,x+2) )
										
			) ]
	return nextgen
	
def print_state(state, width, height):
	for y in xrange(height):
		print "".join(str(state[(x,y)]) for x in xrange(width)).replace('0', PRINTDEAD).replace('1', PRINTLIVE)

def format_state(state, round, gens, width, height):
	formatted = ""
	round_line = "\n##### Round %d: %d Generations #####\n" % (round, gens)
	#formatted += round_line
	for c in xrange(width+2):
		formatted += BORDER
	
	formatted += "\n"
	
	for y in xrange(height):
		formatted += BORDER
		formatted += "".join(str(state[(x,y)]) for x in xrange(width)).replace('0', PRINTDEAD).replace('1', PRINTLIVE)
		formatted += BORDER+"\n"
		
	for c in xrange(width+2):
		formatted += BORDER
	
	formatted += "\n"
	
	return formatted



#========= Handle TCP traffic ===========#


sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((remote_host, remote_port))

#def read(_socket, _buffer):
round1 = None
gens = None
width = None
height = None
state1 = None
rounds = 1


try:
	while 1:
		data = sock.recv(1024*2)
		#print(data)
		if("Generations" in data):
			kikki, gens = remove_round_line(data)
			#print "\n\n==========gens========\n"+str(gens)+"\n==============\n\n"
		if("#\n###" in data):
			round1 = data
			width, height = initiate(round1)
			#print width, height
			state1 = parse_state(round1, width, height)
			gen_x = state1
			for x in xrange(gens):
				rounds += 1
				gen_x = next_generation(gen_x, width, height)
			f_gen_x = format_state(gen_x, rounds, gens, width, height)
			#print "\n\n==========round1========\n"+repr(f_gen_x)+"\n==============\n\n"
				#sock.sendall("\n##### Round 150: %d Generations #####\n" %(gens,))
				#print("\n##### Round %d: %d Generations #####\n" %(rounds, gens))
			sock.sendall(f_gen_x)
				#print (f_gen_x)
				#time.sleep(0.3)
				#resp = sock.recv(1024*2)
				#print repr(resp)
		#print (data)
		if(len(data) == 0):
			break
		

finally:
	print >>sys.stderr, 'closing socket'
	sock.close()
#data = sock.recv(4096)

#print repr(data)
