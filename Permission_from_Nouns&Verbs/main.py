import mysql.connector
import play_scraper
import nltk
import time
import re
from nlp_analysis import *
from manifest_analysis import *
from static_code_analysis import *
from androguard.core.api_specific_resources import load_permission_mappings

#Starting execution time
start = time.time()

#Connecting to the database with schema="testdb"
mydb=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="password",
	database="testdb",)

my_cursor = mydb.cursor(buffered=True)

#All Permission Groups
all_permissions=['camera','sms','storage','internet', 'phone', 'call log', 'calendar', 'contacts', 'microphone', 'location', 'sensors']

#Output file which displays the application name and extra permissions
f=open("App_Permissions.txt", "w") 										
permission_list=[]

#Retrieving the application id of the applications
lines = [line.rstrip('\n') for line in open('application_id.txt')]


for number_of_applications in range (0,len(lines),2):
	application_details=play_scraper.details(lines[number_of_applications]) #A dictionary that contains multiple fields related to the application
	application_description=application_details['description'] 				#Storing the description
	application_title=application_details['title']							#Storing the title
	application_developer=application_details['developer']			
	application_description=re.sub('[\']','',application_description)	
	sent_tokenize_list = sent_tokenize(application_description) 			#sentence tokenize the description

	permission_from_nlp=nlp_analysis(sent_tokenize_list,all_permissions,my_cursor)
	f.write(application_title + "\n")

	#Name of the APK for the manifest analysis
	apk_name=lines[number_of_applications+1]
	
	#Manifest Analysis
	a = APK("C:/Users/KK/Desktop/Final Year Project/APK/"+apk_name)
	permissions_manifest=a.get_permissions()

	permission_group_from_manifest=[]
	permission_group_from_manifest=manifest_analysis(permissions_manifest)
	f.write("Analysis of Manifest and Description:\n")
	f.write(str(list(set(permission_group_from_manifest)-set(permission_from_nlp))))
	f.write("\n\n")
	
	#Static code analysis

	permissions_from_mapping=[]
	permissions_from_mapping=static_code_analysis(apk_name)

	f.write("Extra permissions (By Static Code Analysis):\n")
	f.write(str(list(set(permissions_manifest)-set(permissions_from_mapping))))
	f.write("\n\n\n")

#Ending execution time
end = time.time()

print("Execution time: ")
print(end - start)

