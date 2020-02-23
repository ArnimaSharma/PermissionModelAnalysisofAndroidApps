import spacy
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
lancaster_stemmer = LancasterStemmer()
permission_from_nlp=[]
def nlp_analysis(sent_tokenize_list, all_permissions,my_cursor):
	for i in range (len(sent_tokenize_list)):
		nlp = spacy.load('en_core_web_sm')
		doc = nlp(sent_tokenize_list[i])
		noun_list=[]
		verb_list=[]

		#To prepare a NOUN and VERB list
		for token in doc:
				if token.pos_=="NOUN":
					if token.text in all_permissions:
						permission_from_nlp.append(token.text)
					noun_list.append(lancaster_stemmer.stem(token.text))
				elif token.pos_=="VERB" :
					verb_list.append(lancaster_stemmer.stem(token.text))

		#To retrieve permissions for corresponding Verbs and Nouns
		for i in range (len(verb_list)):
			for j in range (len(noun_list)):
				my_cursor.execute("select permissions from testdb.semantic_analysis where stemmed_noun='%s' AND stemmed_verb='%s';" %(noun_list[j],verb_list[i]))
				res=my_cursor.fetchall()
				y=[x.split(',') for t in res for x in t]
				res1=[item for sublist in y for item in sublist]
				for k in range(len(res1)):
					permission_from_nlp.append(res1[k].strip(' ').upper())
	return permission_from_nlp