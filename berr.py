from flask import Flask
import threading, json, os, time, requests
app = Flask(__name__)

#Read the database file if there is one
if os.path.isfile("keyholderstats.json"):
	stats = json.loads(open("keyholderstats.json").read())
else:
	stats = {}

def crawlStats():
	global stats
	while True:
		time.sleep(120) #Not nice, to lazy for a threading Timer here. TODO
		global stats
		r = requests.get("http://portal.shack:8088/status")
		result = r.json()
	
		if result["keyholder"] in stats:
			stats[result["keyholder"]] += 120
		else:
			stats[result["keyholder"]] = 120
	
		f = open("keyholderstats.json", "w")
		f.write(json.dumps(stats))
		f.close()

#Webserver
@app.route('/')
def get_stats():
	global stats
	return json.dumps(stats)

threading.Thread(target=crawlStats).start()

if __name__ == '__main__':
    app.run("0.0.0.0", port=8088)
