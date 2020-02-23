import spacy
import mysql.connector
import play_scraper
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation

#List of stopwords and punctuations
stopword_list=set(stopwords.words('english')+list(punctuation))

lancaster_stemmer = LancasterStemmer()

#Connecting to the database with schema="testdb"
mydb=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="password",
	database="testdb",)

my_cursor = mydb.cursor()

#Retrieving the application id of the applications
lines = [line.rstrip('\n') for line in open('application_id.txt')]

#To retrieve the Nouns and permissions from the database
dictionary_noun={}
my_cursor.execute("select stemmed_noun, permissions from testdb.semantic_analysis;")
result_noun=my_cursor.fetchall()
dictionary_noun=dict(result_noun)

#List of all permissions
all_permissions=['camera','sms','storage','internet', 'phone', 'call log', 'calendar', 'contacts', 'microphone', 'location', 'sensors']
f=open("App_Permissions.txt", "w")

#Traversing all the applications
for number_of_applications in range(len(lines)):
	application_details=play_scraper.details(lines[number_of_applications]) #A dictionary that contains multiple fields related to the application
	application_description=application_details['description'] 				#Storing the description
	application_title=application_details['title']							#Storing the title
	application_developer=application_details['developer']					#Storing the developer
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(application_description)

	permission_list=[]

	for token in doc:
		if token.text not in stopword_list:
			stemmed_token=lancaster_stemmer.stem(token.text)
			if stemmed_token in dictionary_noun.keys() and (token.pos_=="noun" or dictionary_noun[stemmed_token] in all_permissions):
				permissions_app=dictionary_noun[stemmed_token].split(",")
				for i in range (len(permissions_app)):
						if permissions_app[i] not in permission_list:
								permission_list.append(permissions_app[i])
	f.write(application_title + "\n")
	f.write(str(list(set(permission_list))))
	f.write("\n\n---------------------------------------------------------------------------\n\n")