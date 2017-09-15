import urllib, json, array, datetime, time, sys, urllib2, os
from datetime import datetime, timedelta

url = "https://reserve-prime.apple.com/HK/zh_HK/reserve/iPhone/availability.json"

shopList = ["R409","R499","R485","R428","R610","R673"]
shopListNameMap = {"R409":"CWB","R499":"TST","R485":"FW","R428":"IFC","R610":"NTP","R673":"APM"}

modelList8 = ["MQ6K2ZP/A","MQ6L2ZP/A","MQ6M2ZP/A","MQ7F2ZP/A","MQ7G2ZP/A","MQ7H2ZP/A"]
modelList8Plus = ["MQ8D2ZP/A","MQ8E2ZP/A","MQ8F2ZP/A","MQ8G2ZP/A","MQ8H2ZP/A","MQ8J2ZP/A"]
modelListX = ["MQA52ZP/A","MQA62ZP/A","MQA82ZP/A","MQA92ZP/A"]
modelListShortColourMap8 = {"MQ6K2ZP/A":"iPhone 8 Black 64GB","MQ6L2ZP/A":"iPhone 8 Silver 64GB","MQ6M2ZP/A":"iPhone 8 Gold 64GB","MQ7F2ZP/A":"iPhone 8 Black 256GB","MQ7G2ZP/A":"iPhone 8 Silver 256GB","MQ7H2ZP/A":"iPhone 8 Gold 256GB"}
modelListShortColourMap8Plus = {"MQ8D2ZP/A":"iPhone 8 Plus Black 64GB","MQ8E2ZP/A":"iPhone 8 Plus Silver 64GB","MQ8F2ZP/A":"iPhone 8 Plus Gold 64GB","MQ8G2ZP/A":"iPhone 8 Plus Black 256GB","MQ8H2ZP/A":"iPhone 8 Plus Silver 256GB","MQ8J2ZP/A":"iPhone 8 Plus Gold 256GB"}
modelListShortColourMapX = {"MQA52ZP/A":"iPhone X Plus Black 64GB","MQA62ZP/A":"iPhone X Plus Silver 64GB","MQA82ZP/A":"iPhone 8 X Black 256GB","MQA92ZP/A":"iPhone 8 X Silver 256GB"}


token="271726306:AAHaRAV9hUu4tj5FeDhS4VHUQI41cSTux3k"
#TODO: comment below for production
isTest="_test"
telegram_web_service = "https://api.telegram.org/bot(token)/sendMessage?chat_id=@iphonehkprice"+isTest+"&parse_mode=markdown"
telegram_web_service = telegram_web_service.replace("(token)", token)

def recordStock(model, hasStock):
	"record the model has stock in last minute, return true if previously has no stock"
	needUpdate = 0
	model = model.replace("/","")
	my_file = "tmp_record/"+model
	if hasStock == 1:
		if os.path.exists(my_file):
			print my_file + " exist"
		else:
			print my_file + " not exist"
			f = open(my_file, 'w')
			f.write("1")
			f.close()
			needUpdate = 1
	else:
		if os.path.exists(my_file):
			os.remove(my_file)

	return needUpdate;


def sendTelegramMessage(message):
	"send telegram message to iphonehkprice_test"
	values = {'text' : message}
	html_data = urllib.urlencode(values)
	req = urllib2.Request(telegram_web_service, html_data)
	print telegram_web_service
	response = urllib2.urlopen(req)
	return json.loads(response.read());

def readDataFromURL(url):
	"read json from apple"
	response = urllib.urlopen(url)
	return json.loads(response.read());
	
def createLink(model, shop):
   "create direct ireserve buying link"
   return "https://reserve-prime.apple.com/HK/zh_HK/reserve/iPhone?partNumber="+model+"&channel=1&sourceID=&iPP=N&appleCare=N&carrier=&store="+shop;

for looptime in ["1"]:
	print "working on " + looptime + " time\n"
	output = ""
	needSendMessage = 0
	data = ""
	for x in range(1, 10):
		try:
			data = readDataFromURL(url)
			break
		except IOError:
			time.sleep(3)

#	with open('../stores.json') as data_file:    
#		data = json.load(data_file)
			
	if data == "" or not data.has_key("stores"):
		continue

	for model in modelList8:
		for shop in shopList:
			found = 0
			if data['stores'][shop][model]['availability']['unlocked'] == True:
				found = 1
				if recordStock(model, 1) == 1:
					needSendMessage = 1
				output += "["+shopListNameMap[shop] + " - " + modelListShortColourMap8[model]+"]("+createLink(model, shop) + ")\n"   
				break
		if found == 0:
			recordStock(model, 0)

	for model in modelList8Plus:
		for shop in shopList:
			found = 0
			if data['stores'][shop][model]['availability']['unlocked'] == True:
				found = 1
				if recordStock(model, 1) == 1:
					needSendMessage = 1
				output += "["+shopListNameMap[shop] + " - " + modelListShortColourMap8Plus[model]+"]("+createLink(model, shop) + ")\n"   
				break
		if found == 0:
			recordStock(model, 0)

			
	if output == "":
		print "no change"
		continue

	current_datetime = datetime.now() + timedelta(hours=15);

	output += "\n\nLast updated:" + current_datetime.strftime("%Y-%m-%d %H:%M:%S") 

	header = open('header.txt', 'r').read()
	footer = open('footer.txt', 'r').read()

	if needSendMessage == 1:
		print sendTelegramMessage(header+"\n"+output+"\n"+footer)
print "completed all\n."