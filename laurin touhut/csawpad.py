import os
from hashlib import sha512
from binascii import hexlify
from binascii import unhexlify
import string

#generates s box and sinverse box, called f and g respectively, using 
#sha 512 as a deterministic random number generator
def genTables(seed="Well one day i'll be a big boy just like manhell"):
    fSub={}
    gSub={}
    i=0
    prng=sha512()
    prng.update(seed)
    seed=prng.digest()
    for el in xrange(256):
        cSeed=""
        for x in xrange(4):
            cSeed+=prng.digest()
            prng.update(str(x))
        prng.update(cSeed)
        fCharSub=[0]*256
        gCharSub=[0]*256
        unused=range(256)
        for toUpdate in xrange(256):
            i+=1
            curInd=ord(cSeed[toUpdate])%len(unused)
            toDo=unused[curInd]
            del unused[curInd]
            fSub[(el,toUpdate)]=toDo
            gSub[(el,toDo )]=toUpdate
    return fSub,gSub
f,g=genTables()

def encrypt(pad, ptext):
    assert(len(ptext)<=len(pad))#if pad < plaintext bail
    ctext = []
    if type(ptext)==type(""):
        ptext=map(ord,ptext)
    if type(pad)==type(""):
        pad=map(ord,pad)
    for padByte,ptextByte in zip(pad,ptext):
        ctext.append(f[padByte,ptextByte])
    return  "".join(map(chr,ctext))

def decrypt(pad, ciphertext):
    assert(len(ciphertext)<=len(pad))#if pad < ciphertext bail
    ptext = []
    if type(ciphertext)==type(""):
        ciphertext=map(ord,ciphertext)
    if type(pad)==type(""):
        pad=map(ord,pad)
    for padByte,ctextByte in zip(pad,ciphertext):
        ptext.append(g[padByte,ctextByte])

    return "".join(map(chr,ptext))

def sanity():
    for x in xrange(256):
        for y in xrange(256):
            enc=f[(x,y)]
            dec=g[(x,enc)]
            assert(y==dec)
    for x in xrange(1000):
        toTest=os.urandom(1000)
        pad=os.urandom(1000)
        enc=encrypt(pad,toTest)
        dec=decrypt(pad,enc)
        assert(dec==toTest)
#sanity()

'''
Recovered texts, hex encoded
 '794d630169441dbdb788337d40fe245daa63c30e6c80151d4b055c18499a8ac3e5f3b3a8752e95cb36a90f477eb8d7aa7809427dde0f00dc11ab1f78cdf64da55cb75924a2b837d7a239639d89fe2b7bc1415f3542dba748dd40',
 '14a60bb3afbca7da0e8e337de5a3a47ae763a20e8e18695f39450353a2c6a26a6d8635694cbdc34b7d1a543af546b94b6671e67d0c5a8b64db12fe32e275',
 '250d83a7ed103faaca9d786f23a82e8e4473a5938eabd9bd03c3393b812643ea5df835b14c8e5a4b36cdcfd210a82e2c3c71d27d3c47091bdb391f2952b261fde94a4b23238137a4897d1631b4e18d63',
 '68a90beb191f13b621747ab46321a491e71c536b71800b8f5f08996bb433838fe56587f171a759cf1c160b4733a3465f5509ad7d1a89d4b41f631f3c600347a8762141095dad3714027dfc7c894d69fd896b810313259b1a0e941ecb43d6ae1857a465b4ddcdf102b7297763acb0281144b0598c326e871c3a1ad047ad4fea2093a1b734d589b8998175b3',
 '0fc304048469137d0e2f3a71885a5a78e749145510cf2d56157939548bfd5dd7e59dcebc75b678cfeac4cf408fce5dda32c9bfcbfd578bdcb801df32ebf64da365df4b285d5068975137990134bd69991695989b322b0849',
 '254c0bb31453badaca9d060ce5faa45fa66378a6716915473579d3743e315dbedf4d8cf78b93c3267d579247e32c8c7cd3e71e7dda6138a2ab015166fa03f2ce6ab74b89ce561eb16a65990189e169f1c457d9af622ba119a66acedb108fae18825bf3efc0428b9dae250791cb0ea018966e257d601a87f9914d646026eeab5c45cbaedd27e4c47643ab4e25193aa64f79',
 '41cd1c01c62883b2ca71e671dce57e5f96b1610e29507b6c03c38211653284576d4d8cdc967764147d1a0578102cb05f32a73065f11009041fa3cc5f60b24d8c7098598627df37322f814525966acabc99be5303c2322b43ecf358ac8b8541bd82214d1cc042cac3869c54e2964fa376229c2563ba3fd03e2d4d4d441721c60b6d817e034965be28b7d463cf2b97baebfe2729ed2aa41ffe',
 '68c50bd5197bfdbdfa887883783d2455a673a685436915bd72d1af74dffdd2b89df335daee93c36d5f57e147e9a35913d3b3bf33'
'''

texts = (
	'794d630169441dbdb788337d40fe245daa63c30e6c80151d4b055c18499a8ac3e5f3b3a8752e95cb36a90f477eb8d7aa7809427dde0f00dc11ab1f78cdf64da55cb75924a2b837d7a239639d89fe2b7bc1415f3542dba748dd40',
	'14a60bb3afbca7da0e8e337de5a3a47ae763a20e8e18695f39450353a2c6a26a6d8635694cbdc34b7d1a543af546b94b6671e67d0c5a8b64db12fe32e275',
	'250d83a7ed103faaca9d786f23a82e8e4473a5938eabd9bd03c3393b812643ea5df835b14c8e5a4b36cdcfd210a82e2c3c71d27d3c47091bdb391f2952b261fde94a4b23238137a4897d1631b4e18d63',
	'68a90beb191f13b621747ab46321a491e71c536b71800b8f5f08996bb433838fe56587f171a759cf1c160b4733a3465f5509ad7d1a89d4b41f631f3c600347a8762141095dad3714027dfc7c894d69fd896b810313259b1a0e941ecb43d6ae1857a465b4ddcdf102b7297763acb0281144b0598c326e871c3a1ad047ad4fea2093a1b734d589b8998175b3',
	'0fc304048469137d0e2f3a71885a5a78e749145510cf2d56157939548bfd5dd7e59dcebc75b678cfeac4cf408fce5dda32c9bfcbfd578bdcb801df32ebf64da365df4b285d5068975137990134bd69991695989b322b0849',	
	'254c0bb31453badaca9d060ce5faa45fa66378a6716915473579d3743e315dbedf4d8cf78b93c3267d579247e32c8c7cd3e71e7dda6138a2ab015166fa03f2ce6ab74b89ce561eb16a65990189e169f1c457d9af622ba119a66acedb108fae18825bf3efc0428b9dae250791cb0ea018966e257d601a87f9914d646026eeab5c45cbaedd27e4c47643ab4e25193aa64f79',	
	'41cd1c01c62883b2ca71e671dce57e5f96b1610e29507b6c03c38211653284576d4d8cdc967764147d1a0578102cb05f32a73065f11009041fa3cc5f60b24d8c7098598627df37322f814525966acabc99be5303c2322b43ecf358ac8b8541bd82214d1cc042cac3869c54e2964fa376229c2563ba3fd03e2d4d4d441721c60b6d817e034965be28b7d463cf2b97baebfe2729ed2aa41ffe',	
	'68c50bd5197bfdbdfa887883783d2455a673a685436915bd72d1af74dffdd2b89df335daee93c36d5f57e147e9a35913d3b3bf33'
)


def get_distinct_products(chars=string.ascii_uppercase, rep=3):
	sys.stdout.write("Getting all distinct character combinations..\n")
	prods =	["".join(t) for t in set(itertools.product(chars, repeat=rep))] 
	sys.stdout.write("Generated %d different combinations.\n" % len(prods))
	return prods

def find_string(pad, string, cipher):
	dc = decrypt(pad*1000, cipher)
	if string in dc:
		return (pad, dc)
	else:
		return False

def print_progress(current, total):
	progress = math.floor(float(current) / float(total) * 100)
	if progress % 5 == 0:
		sys.stdout.write("Progress: %d%% \r" % (progress) )
	
def evaluate_cipher(cipher, prods, text_to_find):
	text = unhexlify(cipher)
	results = []
	for prod in prods:
		result = find_string(prod, text_to_find, text)
		if result:
			results.append(result)
	return results

def main():
	prods = get_distinct_products()
	out_result = open('result.txt', 'w')
	total = len(prods) * len(texts)
	cur = 0
	p = Pool(processes=len(texts))
	result = ""
	for text in texts:
		result = p.apply_async(evaluate_cipher, args=(text,prods,'key'))
	
	print result.get()
#		text = unhexlify(text)
#		for prod in prods:
#			cur += 1
#			print_progress(cur, total)
#			result = find_string(prod, 'flag', text)
#			if result:
#				out_result.write("Pad:{0} Plaintext: {1}\n".format(result[0], result[1]))



		
#		dc = text
#		for x in range(1, rounds+1):
#			dc = decrypt(pad*1000, dc)
		
#		if 'key{' in dc:
#			print dc
			
#	new_texts = []
#	for text in texts:
#		new_texts.append(unhexlify(text))
#	
#	loop = True
#	with open('result.txt', 'w') as output:
#		while loop:
#			pad=os.urandom(1000)
#			for text in new_texts:
#				dec = decrypt(pad, text)
#				if 'key{' in dec:
#					print pad, dec
#					output.write("Pad: {0}\n\n {1}\n".format(pad, dec))
#					loop = False

def test2():
	#pad = "YOS"
	pos = "OSAAT*CY"
	chars = string.ascii_uppercase
	text = unhexlify(texts[3])
	out_result = open('result.txt', 'w')
	all_pads = []
	#add_p = ["".join(c) for c in itertools.product(chars, repeat=2)]
	for c in chars:
		all_pads.append(pos+c)
	
	n_pads = []
	for pad in all_pads:
		for c in chars:
			n_pads.append(pad.replace('*',c))
			
	print n_pads
	all_pads = n_pads
	#perms = []
	#for pad in all_pads:
	#	for perm in itertools.permutations(pad):
	#		perms.append("".join(perm))
	
	#all_pads = perms
	for pad in all_pads:
		result = find_string(pad, 'key=675', text)
		if result:
			out_result.write("Pad:{0} Plaintext: {1}\n".format(result[0], result[1]))
	
	#all_pads = [pad+c for c in chars]
	#for pad in all_pads:
	#	result = find_string(pad, 'key=', text)
	#	if result:
	#		out_result.write("Pad:{0} Plaintext: {1}\n".format(result[0], result[1]))
	#for npad in new_pads:
		#	result = find_string(npad, 'key=', text)
		#	if result:
#				out_result.write("Pad:{0} Plaintext: {1}\n".format(result[0], result[1]))
	
#print find_string('OSCY', 'key', unhexlify(texts[3]))

#text = texts[0]
#print ord(unhexlify(text)[1])
#long_text = ""
#for text in texts:
	#long_text += text

#print "Only unhexlify: "
#for text in texts:
	#print unhexlify(text)

#print "\nConvert to int with base 16:"
#for text in texts:	
	#print int(text, 16)
	
	#print "0x%s" % text
	#print decrypt(pad2, "0x"+text)
	#print decrypt(pad2, long_text)
	#print decrypt(pad2, text)
	#print decrypt(pad2, text.decode("hex"))
	#print decrypt(pad2, unhexlify(text))
	
def temp():
	ciphertext = texts[3]
	import itertools, string, sys, math
	out_prod = open('prod.txt', 'w')
	chars = string.ascii_lowercase
	#perms = itertools.permutations(chars*, r=3)
	prod = set(itertools.product(chars, repeat=1))
	pad_sug = "OSCY"

	new_prod = ["".join(chars)+pad_sug for chars in prod]
	out_prod.write(new_prod)
	values_len = len(prod)
	current = 0
	sys.stdout.write("Start brute forcing. Length of product table: %d \n" % values_len)
	out_result = open('result.txt', 'w')
	for prod in prod:
		current += 1
		last = 0
		progress = math.floor(float(current) / float(values_len) * 100)
		if progress != last and progress % 5 == 0:
			sys.stdout.	write("Progress: %d%% \r" % (progress) )
		pad = "".join(prod)
		
		for text in texts:
			dc = decrypt(pad*100, unhexlify(text))
			if 'key' in dc:
				out_result.write("Pad:{0} Plaintext: {1}\n".format(pad, dc))
				
#pad = "moi"
#print "\nUnhexlify and decrypt with padding: %s" % pad
#for text in texts:
#	print decrypt(pad*1000, unhexlify(text))
	
#print "\nConcatenate all lines, unhexlify and decrypt with padding: %s" % pad1
#print decrypt(pad2, unhexlify(long_text))

#print "\n f table:"
#print g

