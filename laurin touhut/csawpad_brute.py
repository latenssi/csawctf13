import string, sys, math, itertools, re, multiprocessing
import csawpad_worker
from binascii import unhexlify

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

if __name__ == "__main__":
	chars = string.ascii_uppercase
	length = 4
	
	print "Generating all possible pads of length %d" % length
	pads = ["".join(pad) for pad in itertools.product(chars, repeat=length)]
	print "Done."

	#key_reg = ".+key=(?P<key>.+?).+"
	key_reg = ".*{(?P<key>\w{32}?)}.*$"

	jobs = []
	for x in xrange(len(texts)):
		p = multiprocessing.Process(target=csawpad_worker.text_worker, args=(x+1, texts[x], key_reg, list(pads)))
		jobs.append(p)
		p.start()
	
	print "Spawned all workers."