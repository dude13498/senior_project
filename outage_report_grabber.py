import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib.request #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 
import os

def outage():
	conf=open(os.path.expanduser("~/FCC/senior_project/config.txt"),"r")
	conf_data=conf.readlines()
	path=conf_data[0].split(":")
	print (path)
	path=path[1][:-1]
	f=open(os.path.expanduser(path+"providers.txt"),"r") #opens the file with the list of providers
	data=f.readlines()
	date=time.time()
	for provider in data:
		try:
			provider=provider.replace("\n","")
			content = requests.get("https://outage.report/us/"+provider)
			content = content.text    #opens the website to grab that data in it
			soup = BeautifulSoup(content,"html5lib")
			for ul in soup.find_all("ul", {'class':'post-list'}): #removes comment section
				ul.decompose()
			site_data=soup.get_text() #gets the websie section for the number of report
			reg_exp=r"[0-9]+ ?Reports? in last 20 minutes?" #gets the number of reports in the last 20 min
			reports_matcher=re.compile(reg_exp)
			reports_numb=reports_matcher.search(str(site_data.encode('utf-8')))
			if str(reports_numb) != "None":
				reports_numb=reports_numb.group()
			#print data.encode('utf-8')
			reg_exp_2=r"[0-9]+"
			reports_exp=re.compile(reg_exp_2)
			reports_result=reports_exp.search(reports_numb)
			if str(reports_numb) != "None":
				reports_result=reports_result.group() #turns position of the data into text data
				report_time=reports_result
			current_time=time.strftime("%H:%M:%S",time.gmtime(date)) #creates the filed for time and date
			current_date=time.strftime("%a %d %b %Y",time.localtime(date))
			#print current_date
			d = {'Reports in last 20 minutes':[report_time]}
			df=pd.DataFrame(data=d)
			 #gets issues list
			issue_list=["Landline problems","WiFi down","WiFi speed issues","DSL internet out","DSL speed Internet down","Internet speed issues","TV pixilation","Email reading issues","Email sending issues","Mobile app not working","Mobile app crashes","Power out","Cell service down","Website down","TV freezing","channels not working","4G LTE not working","4G LTE speed issues","Text sending problems","Dial-up internet down","Everything is down","Other",]
			#list of issues to look for 
			issue_dic={}
			for issue in issue_list:#finds the issues and the value
				percent_ex=issue+" - [0-9]+%"
				percent_ex=re.compile(percent_ex)#makes a regulor expression to look for the issues
				percent_ex=percent_ex.search(str(site_data.encode('utf-8')))
				if str(percent_ex) != "None":
					percent_data=percent_ex.group()
					percent_num_ex="[0-9]+%"#gets only the percentage value
					percent_num_dat=re.compile(percent_num_ex)
					percent_num_dat=percent_num_dat.search(str(percent_data))
					percent_num_result=percent_num_dat.group()
					issue_dic[issue]=percent_num_result
				else:
					issue_dic[issue]="0%"
			percent_dic=issue_dic
			#print percent_dic
			#print provider
			map_data=soup.findAll("ul",{"class":"RecentReports__Row-q9gvkj-1 gjMiDF"})#gets the location data from the site
			list_data=[]
			for string in soup.stripped_strings:
				list_data.append(repr(string))
			string_data='---'.join(list_data)
			reg_ex=r"'United States'.+u'Outage Map'" #reg expression to find the location data 
			results=re.search(reg_ex,string_data,re.IGNORECASE)
			provider=provider
			if str(results) != "None":
				provider=results.group()
				provider=provider.split("'---u'")
				provider=provider[1]
			issue_list.append("Internet down")
			issue_list.append("Everything is down")
			
			#print results
			string_no_comm=re.sub(r"Discussion.+",'',string_data) #removes the comment section 
			string_no_comm=re.sub(r".+Live'---",'',string_no_comm)
			string_no_comm=re.sub(r".adsbygoogle.+---",'',string_no_comm)
			string_no_comm=string_no_comm.replace("'","")
			#print (string_no_comm)
			parsed_data=string_no_comm.split("-")
			parsed_data = list(filter(None, parsed_data)) #remove empty items
			#print (parsed_data)
			found=1
			for issues in issue_list:
				if issues in parsed_data[0]:
					d={"Location":["unknown"],"Issue":[parsed_data[0]],"How long ago":[parsed_data[1]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date":[current_date],"Time":[current_time],'Source':"Outage Report"}
					parsed_data.pop(0)
					parsed_data.pop(0)
					found=0
					break
			if found == 1:
				d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date":[current_date],"Time":[current_time],'Source':"Outage Report"}
				parsed_data.pop(0)
				parsed_data.pop(0) #removes usesless data 
				parsed_data.pop(0)
			location_DataFrame=pd.DataFrame(data=d) #creates a data frame using panda
			while len(parsed_data)>2:

				found=1
				for issues in issue_list:
					if issues in parsed_data[0]:

						d={"Location":["unknown"],"Issue":[parsed_data[0]],"How long ago":[parsed_data[1]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date":[current_date],"Time":[current_time],'Source':"Outage Report"}
						parsed_data.pop(0)
						parsed_data.pop(0)
						found=0
						break
				if found==1:
					d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date":[current_date],"Time":[current_time],'Source':"Outage Report"}
					parsed_data.pop(0)
					parsed_data.pop(0)
					parsed_data.pop(0)
				temp_DataFrame=pd.DataFrame(data=d) #creates a second data frame 
				try:
					location_DataFrame=pd.concat([temp_DataFrame,location_DataFrame],sort=True)#combines the two data frame
				except ValueError:
					pass 
			for headers in percent_dic:
				location_DataFrame[headers]=percent_dic[headers]
			#print (location_DataFrame)
			location_DataFrame.to_csv(os.path.expanduser(path+"data/"+"outage_report-"+provider+"_"+str(time.time())+".csv"),index=False) #save the data to a csv
			location_DataFrame.to_csv(os.path.expanduser(path+"data/"+"outage_report_current-"+provider+".csv"),index=False) #save the data to a csv
			#return location_DataFrame
		except TypeError:
			pass



#outage()
