import requests
import re

def clean(text):
	text = text.replace("&nbsp;", " ")
	text = text.replace("<br />", "\n")
	text = re.sub(r'<[^<]+?>', "", text)
	text = re.sub(r'[\\s \\t\\r\\n]+', " ", text)
	text = text.replace("&#162;", "cents")
	return text.strip()

landingPage = requests.get("http://www.metro.ca/en/flyer")
eflyer = str(re.findall(r'/MTR/MTRO/en/.+/Page/PDF', landingPage.content)[0]).replace("Page/PDF", "Text")

webpage = requests.get("http://eflyer.metro.ca"+eflyer)
content = webpage.content

thing = re.findall(r'\<b>(.*?)\</b>', content)
stuff = re.findall(r'\</b>((.|\n)*?)\<b>', content)

items = []
price = []
i = 0

for each in stuff:
	each = clean(str(each))
	if " ea." not in each:
		ppu = re.search(r'[0-9]\.[0-9][0-9]/kg', each)
		if ppu:
			ppu = re.sub(r'/kg', "", ppu.group(0))
			ppu = float(ppu)/10

			items.insert(len(items), thing[i])
			price.insert(len(price), ppu)
	i = i+1

json = "{"
i=0
for item in items:
	json = json+'"'+str(item)+'": '+str(price[i])
	if i < len(items)-1:
		json = json+", "
	i=i+1
json=json+"}"

print json
