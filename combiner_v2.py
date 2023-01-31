import time
import pandas as pd
import os#imports the needed modules
import glob
import re
import sys

def file_opener(path): #opens all of the csv files in a folder 
	master_index={}
	path=os.path.expanduser(path+"data/") #creates the path to work for any computer
	for filename in glob.glob(path+'*.csv'): #combines the path and the filename
		#print filename
		df = pd.read_csv(filename)#opens the file
		filename=str(filename)
		filename=filename.split("\\")#remove the path and leaves only the filename
		filename=filename[-1]
		#print filename
		master_index[filename]=df
	return master_index 
	#returns the a list of all of the csv file and the data in it 
		
def combiner(path):
#goes throught the list of cvs file and combines them into one file
	master_index=file_opener(path)
	table_headers=master_index.keys()
	#get list of key which has the filename 
	unique_header=[]
	for header in table_headers:
		#cleans up the file name remove provider and time infor
		header=header.split("-")
		header=header[0]
		unique_header.append(header)
	unique_header=list(set(unique_header))
	header_dic={}
	#makes a empty dic
	for header in unique_header:
	#creates a list of all the files from the same site 
		r = re.compile(header+".+")
		header_match=list(filter(r.match, table_headers))
		header_dic[header]=header_match
	data_frame_dic={}
	for header in header_dic:
		#creates a dictonary with source name as the header and data as the key
		data_frame_list=[]
		for file in header_dic[header]:
			data_frame_list.append(master_index[file])
		data_frame_dic[header]=data_frame_list
	#print (data_frame_dic)
	for header in data_frame_dic:
		#combines the data dic from the same source using the dictonary 
		combine_frame=pd.concat(data_frame_dic[header],sort=True)
		#print combine_frame
		#combine_frame= combine_frame.fillna(0)
		header = header.split("/")[-1]
		combine_frame.to_csv(os.path.expanduser(path+"data/combined_data/"+str(header)+".csv"),index=False)
		#save the data as a csv
now = time.time()
conf=open(os.path.expanduser("~/FCC/senior_project/config.txt"),"r")
conf_data=conf.readlines()
#print (conf_data)
path=conf_data[0].split(":")
#print (path)
path=path[1][:-1]
combiner(path)
path_2=os.path.expanduser(path+"data/")
#print os.listdir(path)
for f in os.listdir(path_2):
	#gets a list of files in a folder and delete the file that are older than a year 
	f=os.path.expanduser(path+"data/"+str(f))
	if "csv" in f:
		#get only csv files 
		if os.stat(f).st_mtime < now - 1 * 365 * 86400:
			if os.path.isfile(f):
				os.remove(f)
	#opens the created file so the powerbi can uses them 
#down_detector=pd.read_csv(os.path.expanduser("~/Documents\senior_project\data\combined_data\downdetector.csv"))
#internet_traffic_report=pd.read_csv(os.path.expanduser("~/Documents\senior_project\data\combined_data\internettrafficreport.csv"))
is_it_down_right_now=pd.read_csv(os.path.expanduser(path+"data/combined_data/isitdownrightnow.csv"))
is_the_service_down=pd.read_csv(os.path.expanduser(path+"data/combined_data/istheservicedown.csv"))
outage_report=pd.read_csv(os.path.expanduser(path+"data/combined_data/outage_report.csv"))