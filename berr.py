from flask import Flask
import threading, json, os, time, requests, datetime
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

#Read the database file if there is one
if os.path.isfile("keyholderstats.json"):
	stats = json.loads(open("keyholderstats.json").read())
else:
	stats = {}

def crawlStats():
	global stats
	i = 0
	while True:
		time.sleep(30) #Not nice, to lazy for a threading Timer here. TODO
		global stats
		i += 1
		r = requests.get("http://portal.shack:8088/status")
		result = r.json()
		
		if result["status"] == "open": #Dont count closed hours		
			if result["keyholder"] in stats:
				stats[result["keyholder"]] += 30
			else:
				stats[result["keyholder"]] = 30

			f = open("keyholderstats.json", "w")
			f.write(json.dumps(stats))
			f.close()
			
		#Backup the file once a day
		if i == 2*60*24:
			i = 0
			now = datetime.datetime.now()
			backupFile = open("keyholderstats.json." + now.strftime("%Y-%m-%d"), "w")
			backupFile.write(json.dumps(stats))
			backupFile.close()

#Webserver
@app.route('/')
def get_stats():
	global stats
	return json.dumps(stats)

threading.Thread(target=crawlStats).start()

if __name__ == '__main__':
	app.run("0.0.0.0", port=8088)
