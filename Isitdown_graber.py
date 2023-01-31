import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib.request #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 
import os.path

def isitdown():
	conf=open(os.path.expanduser("~/FCC/senior_project/config.txt"),"r")
	conf_data=conf.readlines()
	print (conf_data)
	path=conf_data[0].split(":")
	print (path)
	path=path[1][:-1]
	f=open(os.path.expanduser(path+"providers.txt"),"r")
	data=f.readlines()
	date=time.time()
	#print data
	for provider in data:
		#print provider
		try:
			provider=provider.replace("\n","")
			#print provider
			content = requests.get("https://www.isitdownrightnow.com/"+provider+".com.html")
			#content = content.text    #opens the website to grab that data in it
			tables = pd.read_html(content.text,header=0) #Using pandas automatically find all the table on a website 
			df1 = tables[0].iloc[:, :3]
			df2 = tables[0].iloc[:, 4:7]
			#splits the table in half
			df2.columns = ["Date reported","Time reported(PT)","Ping Time(ms.)"]
			df1.columns = ["Date reported","Time reported(PT)","Ping Time(ms.)"]
			#changes the headers for the tables 
			combine_tables=pd.concat([df1,df2],ignore_index=True)
			#combines the two table
			current_timedate=time.strftime("%a %d %b %Y %H:%M:%S",time.localtime(date))
			#gets the current time and date
			#current_date=time.strftime("%a %d %b %Y",time.localtime(date))
			combine_tables["Time collected"]=current_timedate
			#adds time collected to the final table
			#combine_tables["date collected"]=current_date
			combine_tables["Source"]="Is it down right now?"
			#adds the source to the table
			combine_tables["Provider"]=provider
			#add =s the provider to the table
			combine_tables['Ping Time(ms.)'] = combine_tables['Ping Time(ms.)'].str.extract('(\d*\.?\d*)', expand=False).astype(float)
			#adds the rest of the data to hte final table
			#print combine_tables
			combine_tables.to_csv(os.path.expanduser(path+"data/isitdownrightnow-"+provider+"_"+str(date)+".csv"),index=False)
			#save the data as a csv for trend anaysis 
			combine_tables.to_csv(os.path.expanduser(path+"data/isitdownrightnow_current-"+provider+".csv"),index=False)
			#save the data for current data 
		except ValueError:
			#print provider
			pass
#isitdown()