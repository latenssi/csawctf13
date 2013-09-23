import sysimport telnetlibimport reimport timefrom collections import defaultdictHOST = "128.238.66.216"PORT = "45678"PRINTDEAD, PRINTLIVE = ' *'BORDER = '#'celltable = defaultdict(int, { (1, 2): 1, (1, 3): 1, (0, 3): 1, } ) def remove_shit(round):	nls = 0	new = ""	for c in round:		if c == '\n':			nls += 1		if nls >= 2:			new += c				return new	def remove_round_line(round):	round_line = re.compile('.*(\n##### Round \d{1,3}: (?P<gens>\d{1,3}?) Generations #####).*')	m = re.match(round_line, round)	gens = m.groupdict()	round = re.sub(round_line, '', round)	return round, int(gens['gens'])	def initiate(round1):	nls = 0	width = 0	for c in round1:		if c == '\n':			nls += 1			if nls == 1 and c == BORDER:			width += 1		return width-2, nls-4			def parse_state(round, width, height):	round = round[width+4:]	round = round[:len(round)-width-5]	lines = round.split(BORDER)	clean = []	state = defaultdict(int)	for line in lines:		if line and line != '\n':			clean.append(line)				for y in xrange(len(clean)):		for x in xrange(len(clean[y])):			if clean[y][x] == PRINTLIVE:				state[(x,y)] = 1					return state	def next_generation(universe, width, height):	nextgen = defaultdict(int)	for y in xrange(height):		for x in xrange(width):			nextgen[(x,y)] = celltable[				(universe[(x,y)],				 -universe[(x,y)] + sum(universe[(xn,yn)] 										for yn in range(y-1,y+2)										for xn in range(x-1,x+2) )													) ]	return nextgen	def print_state(state, width, height):	for y in xrange(height):		print "".join(str(state[(x,y)]) for x in xrange(width)).replace('0', PRINTDEAD).replace('1', PRINTLIVE)def format_state(state, round, gens, width, height):	formatted = ""	round_line = "\n##### Round %d: %d Generations #####\n" % (round, gens)	#formatted += round_line	for c in xrange(width+2):		formatted += BORDER		formatted += "\n"		for y in xrange(height):		formatted += BORDER		formatted += "".join(str(state[(x,y)]) for x in xrange(width)).replace('0', PRINTDEAD).replace('1', PRINTLIVE)		formatted += BORDER+"\n"			for c in xrange(width+2):		formatted += BORDER		formatted += "\n"		return formatted	def main():	tn = telnetlib.Telnet(HOST, PORT)	received = tn.read_until('\n\n')	print received	round1, gens = remove_round_line(received)	width, height = initiate(round1)		state1 = parse_state(round1, width, height)		gen_x = state1	rounds = 1	for x in xrange(gens-1):		rounds += 1		gen_x = next_generation(gen_x, width, height)		f_gen_x = format_state(gen_x, rounds, gens, width, height)		tn.write(f_gen_x)		print f_gen_x		#time.sleep(1)		print tn.read_until('\n')	if __name__ == "__main__":	main()