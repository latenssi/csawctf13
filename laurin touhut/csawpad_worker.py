import re, time
from binascii import unhexlify
from csawpad import decrypt

def print_progress(cur, tot):
	print cur / tot
	
def text_worker(num, text, reg, pads):
	print "Spawned worker #%d" % num
	total = len(pads)
	current = 0
	last = -1
	reg = re.compile(reg)
	for pad in pads:
		current += 1
		progress = int((float(current) / float(total)) * 100)
		if progress > last and progress % 5 == 0:
			last = progress
			print "Worker #%d progress: %d%%\n" % (num, progress)
		dc = decrypt(pad*1000, unhexlify(text))
		keys = reg.findall(dc)
		if keys:
			out = open('result_worker_%d.txt' % num, 'a')
			out.write("Pad: %s\n" % pad)
			for key in keys:
				out.write(key+"\n")
			out.write("\n")
			out.close()
	print "Terminating worker #%d" % num
	return