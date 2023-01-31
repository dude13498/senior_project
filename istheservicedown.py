import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib.request #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 
import os

def istheservicedown():
	conf=open(os.path.expanduser("~/FCC/senior_project/config.txt"),"r")
	conf_data=conf.readlines()
	print (conf_data)
	path=conf_data[0].split(":")
	print (path)
	path=path[1][:-1]
	f=open(os.path.expanduser(path+"providers.txt"),"r")
	#opens a file with the list of providers 
	data=f.readlines()
	date=time.time()

	for provider in data:
			try:
				provider=provider.replace("\n","")#removes to new line for the providers 
				#print provider
				content = requests.get("https://istheservicedown.com/problems/"+provider)
				content = content.text    #opens the website to grab that data in it
				soup = BeautifulSoup(content,"html5lib")
				data=soup.findAll("dl", class_="inline-list-bullet")#finds the html element with the percent data
				data=str(data[0])
				data=data.replace('<dl class="inline-list-bullet">',"")
				data=data.replace(" ","")
				data=data.replace("</dt><dd>",";")
				data=data.replace(")","")
				data=data.replace("(","")#cleans up the data
				data=data.replace("\n","")
				data=data.replace("</dd><dt>", ",")
				data=data.replace("</dd></dl>","")
				data=data.replace("<dt>","")
				data=data.split(",")
				percent_data=data
				percent_dic={}
				for data in percent_data:
					#print data
					data=data.split(";")
					data[1]=data[1].replace(" ","")
					percent_dic[data[0]]=data[1]
				status_data=soup.findAll("div", {"class": "service-status-alert"})#finds the html element with the sites status
				status_data=str(status_data)
				status_data=status_data.split("</i>")
				status_data=status_data[1] #cleans the data
				status_data=status_data.split("at")
				status_data=status_data[0]
				status_data=status_data.replace(u'\\xa0', u'')
				percent_dic["Status"]=status_data
				percent_dic["Provider"]=provider #saves the data to a table
				percent_dic["Source"]="Is the service down"
				current_time=time.strftime("%H:%M:%S",time.localtime(date))
				current_date=time.strftime("%a %d %b %Y",time.localtime(date))
				#gets the current time and date
				percent_dic["Date collected"]=current_date
				percent_dic["Time collected"]=current_time
				content = requests.get("https://istheservicedown.com/problems/"+provider+"/map")
				tables = pd.read_html(content.text,header=0)
				tables=tables[0]
				for headers in percent_dic:
					tables[headers]=percent_dic[headers]
				tables.to_csv(os.path.expanduser(path+"data/istheservicedown-"+provider+"_"+str(date)+".csv"),index=False)
				tables.to_csv(os.path.expanduser(path+"data/istheservicedown_current-"+provider+".csv"),index=False)
				#save the data to csv
				#print tables
			except IndexError:
				#print provider
				pass
#istheservicedown()