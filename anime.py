#!/usr/bin/env python

import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import requests
from robobrowser.forms.form import Form

browser = RoboBrowser(history=True)
print("enter the anime you want to download")
inp = input()
anime = inp.split(" ")
ur = ""
for x in anime:
	ur = ur+x+"%"
url = "http://www1.gogoanime.tv//search.html?keyword="+ur
print(url)
browser.open(url)
anchors = browser.get_links(inp)
links=[]
titles=[]
for x in anchors:
	links.append(x['href'])
	titles.append(x['title'])

print("enter the no. of anime you want to download")
i = 1
for t in titles:
	print(str(i)+"> "+t)
	i+=1

base_url = "http://www1.gogoanime.tv"
selec = int(input())
#selection = links[selec-1]
#url = base_url+selection
#browser.open(url)
#print(selection)
#resp = browser.session.get(url, params={'value': 'cat'})
browser.follow_link(anchors[selec-1])

selected = titles[selec-1].split(" ")
inter = ""
for x in selected:
	inter=inter+x.lower()+"-"
selected = inter[0:len(inter)-1]
print(selected)
z = browser.parsed
z = str(z)
soup = BeautifulSoup(z , 'html.parser')

movie_id = soup.find_all("input" , class_="movie_id")
default_ep = soup.find_all("input" , class_="default_ep")
a = soup.find_all("a" ,class_="active")
movie_id=movie_id[0]
default_ep=default_ep[0]
a=a[0]
movie_id=movie_id['value']
default_ep=default_ep['value']
ep_start=a['ep_start']
ep_end=a['ep_end']
print(movie_id + " " + default_ep + " " + ep_start + " " + ep_end)
url = base_url + '/load-list-episode?ep_start='+ep_start+'&ep_end='+ep_end+'&id='+movie_id+'&default_ep='+default_ep 
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
episodes = soup.find_all("a")

#for x in range(24,-1,-1)
link=((episodes[4])['href'])
url = base_url+link
url = re.sub('[\s+]', '', url)
print(url)
browser.open(url)
soup = BeautifulSoup(str(browser.parsed),'html.parser')
dl = soup.find_all("div" ,class_="download-anime")
soup = BeautifulSoup(str(dl[0]),'html.parser')
dl = soup.find_all("a")
browser.follow_link(dl[0])
soup = BeautifulSoup(str(browser.parsed),'html.parser')
mirror_link = soup.find_all("div" ,class_="mirror_link")
lin = []
source = []
for x in mirror_link:
	sap = BeautifulSoup(str(x),'html.parser')
	tag = str(sap.find("h6").string)
	if(tag == "Mirror Link"):
		sp = BeautifulSoup(str(x),'html.parser')
		anchs = sp.find_all("a")
		for y in anchs:
			lin.append(y['href'])
			source.append(y.string)
l = len(lin)
dl = l-1
for x in range(l-1,-1,-1):
	if(source[x] == "Download mp4upload"):
		dl = x
		break
	elif(source[x] == "Download openload"):
		dl = x
		break
	else:
		print("Sorry no script supported download link found")

dlselected = lin[dl]
browser.open(dlselected)
print(source)


if(source[dl] == "Download mp4upload"):
	form = browser.get_forms()
	num = 0
	i = 0
	for f in form:
		if(f['op'].value=="download2"):
			num = i
		i+=1
	form = form[num]
	#print(form)
	data = form.serialize()
	print(data)
	#func = getattr(requests.session, form.method.lower())
    #response = func(dlselected, **data)
    #print(response)
	#browser.submit_form(form)




#z = str(browser.parsed)
#target = open('hello','w')
#target.truncate()
#target.write(str(z))
#target.close()
#dl = browser.find_all("	a", string="http://vidstream.co")
#print(dl)

#print(z)
	#print(str(re.search(selected,x)))

