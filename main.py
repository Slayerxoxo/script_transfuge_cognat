#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Authors:
	Cora

:Date:
	2014/9/8
"""

import sys
import os
import codecs
import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#####################################################
#                     FUNCTIONS                     #
#####################################################

def removeAccent (string):
	string = string.replace(u"é", "e")
	string = string.replace(u"è", "e")
	string = string.replace(u"ê", "e")
	string = string.replace(u"ë", "e")
	string = string.replace(u"à", "a")
	string = string.replace(u"â", "a")
	string = string.replace(u"ä", "a")
	string = string.replace(u"î", "i")
	string = string.replace(u"ï", "i")
	string = string.replace(u"ô", "o")
	string = string.replace(u"ö", "o")
	string = string.replace(u"ù", "u")
	string = string.replace(u"û", "u")
	string = string.replace(u"ü", "u")
	string = string.replace(u"ç", "c")
	return string

"""
def removeAcc (s):
    s = re.sub(u"[éèëê]", u"e", s)
    s = re.sub(u"[ïî]", u"i", s)
    s = re.sub(u"[àâ]", u"a", s)
    s = re.sub(u"[ô]", u"o", s)
    s = re.sub(u"[ç]", u"c", s)
    s = re.sub(u"[û]", u"u", s)
    s = re.sub(u"[œ]", u"oe", s)

    return s
"""

def isNotAWord (string):
	bad_lst = [u"__endfile", u"__ENDFILE", u".", u",", u"?", u";", u"/", u":", u"!", u"<", u">", u"#", u"%", u"\"", u"-", u"\'", u"\r\n", u"\n", u"(", u")", u"=", u"[", u"]", u"+", u"«", u"»"]
	if string in bad_lst or "__file" in string or "0" in string or "1" in string or "2" in string or "3" in string or "4" in string or "5" in string or "6" in string or "7" in string or "8" in string or "9" in string or "." in string or "," in string or "%" in string:
		return 1
	else:
		return 0 

#####################################################
#                       MAIN                        #
#####################################################


if __name__ == "__main__":
	if len(sys.argv) > 2:
		for arg in [1, 2]:
			if not os.path.isfile(sys.argv[arg]):
				raise SystemExit, "[ERROR] " + sys.argv[arg] + ": file not found !"
	else:
		raise SystemExit, "[ERROR] "+sys.argv[0]+" expected at least 2 arguments !"

	#TODO write your script here.

	corpus_source = codecs.open(sys.argv[1], "r", "utf-8")	# ouverture des fichiers
	corpus_target = codecs.open(sys.argv[2], "r", "utf-8")
	
	result_source = codecs.open("resultat_source", "w", "utf-8")
	result_target = codecs.open("resultat_target", "w", "utf-8")
	result_transfuge = codecs.open("resultat_transfuges", "w", "utf-8")
	result_cognat_4gram = codecs.open("resultat_cognats_4gram", "w", "utf-8")
	result_cognat_5gram = codecs.open("resultat_cognats_5gram", "w", "utf-8")
	result_stat = codecs.open("resultat_stats", "w", "utf-8")
	random_4gram = codecs.open("random_4gram", "w", "utf-8")
	random_5gram = codecs.open("random_5gram", "w", "utf-8")

	
	corpus_source_str = corpus_source.read()	# lecture de l'intégralité du fichier
	corpus_target_str = corpus_target.read()

	corpus_source_lst = corpus_source_str.split(" ")	# chaque élément séparé par un " " est mis dans une liste
	corpus_target_lst = corpus_target_str.split(" ")

	final_source_dico = {}
	final_target_dico = {}
	final_source_lst = []
	final_target_lst = []
	transfuge_lst = []
	cognat_4gram_lst = []
	cognat_5gram_lst = []


	# nettoyage de la liste source
	print color.BOLD +"\n\nNETTOYAGE DE LA LISTE SOURCE ..." + color.END
	for elt in corpus_source_lst:
		elt = elt.split("/")[-1].split(":")[0]		# on récupère le dernier élément avant le "/" et avant un ":"			
		elt = removeAccent(elt)		# on supprime les accents
		if not isNotAWord(elt):
			if not elt.lower() in final_source_dico.keys():
				final_source_dico[elt.lower()]=1
				
			else:
				final_source_dico[elt.lower()] += 1
	for elt in final_source_dico:
		result_source.write(elt + " = " + str(final_source_dico[elt]) + "\n")
		if final_source_dico[elt] >= 2:
			final_source_lst.append(elt)

	print color.GREEN + "                  DONE" + color.END


	# nettoyage de la liste target
	print color.BOLD +"NETTOYAGE DE LA LISTE TARGET ..." + color.END
	for elt in corpus_target_lst:
		elt = elt.split("/")[-2]
		if not isNotAWord(elt):
			if not elt.lower() in final_target_dico.keys():
				final_target_dico[elt.lower()]=1
			else:
				final_target_dico[elt.lower()] += 1
	for elt in final_target_dico:
		result_target.write(elt + " = " + str(final_target_dico[elt]) + "\n")
		if final_target_dico[elt] >= 2:
			final_target_lst.append(elt)
	
	print color.GREEN + "                  DONE" + color.END


	# recherche de transfuges
	print color.BOLD +"RECHERCHE DE TRANSFUGES ..." + color.END
	for elt in final_source_lst:
		if elt in final_target_lst:
			transfuge_lst.append(elt)
			result_transfuge.write(elt + "\n")
	print color.GREEN + "                  DONE" + color.END


	# recherche de  cognats 4-gram
	print color.BOLD +"RECHERCHE DE COGNATS ..." + color.END
	for elt_source in final_source_lst:
		if len(elt_source) > 4:		
			source_4gram = elt_source[:4]
			for elt_target in final_target_lst:
				target_4gram = elt_target[:4]
				if source_4gram == target_4gram:
					cognat_4gram_lst.append((elt_source,elt_target))	
					result_cognat_4gram.write(elt_source + " " + elt_target + "\n")

	for elt_source in final_source_lst:
		if len(elt_source) > 5:		
			source_5gram = elt_source[:5]
			for elt_target in final_target_lst:
				target_5gram = elt_target[:5]
				if source_5gram == target_5gram:
					cognat_5gram_lst.append((elt_source,elt_target))	
					result_cognat_5gram.write(elt_source + " " + elt_target + "\n")
	print color.GREEN + "                  DONE" + color.END


	# génération des listes de tests aléatoires
    	for i in range(0,100):
   		r = random.randint(0, len(cognat_4gram_lst)-1)
   		random_4gram.write(cognat_4gram_lst[r][0]+" <-> "+cognat_4gram_lst[r][1]+"\n")

	for i in range(0,100):
   		r = random.randint(0, len(cognat_5gram_lst)-1)
   		random_5gram.write(cognat_5gram_lst[r][0]+" <-> "+cognat_5gram_lst[r][1]+"\n")
	

	# affichage des statistiques
	print str(len(final_source_lst)) + " mots français"
	print str(len(final_target_lst)) + " mots anglais"
	print str(len(transfuge_lst)) + " transfuges"
	print str(len(cognat_4gram_lst)) + " cognats 4-gram"
	print str(len(cognat_5gram_lst)) + " cognats 5-gram"

	result_stat.write(str(len(final_source_lst)) + u" mots français \n" + str(len(final_target_lst)) + " mots anglais \n" + str(len(transfuge_lst)) + " transfuges \n" + str(len(cognat_4gram_lst)) + " cognats 4-gram \n" + str(len(cognat_5gram_lst)) + " cognats 5-gram \n")
		
	result_source.close()	# fermeture des fichiers résultats
	result_target.close()
	result_transfuge.close()
	result_cognat_4gram.close()
	result_cognat_5gram.close()
	result_stat.close()
	random_4gram.close()
	random_5gram.close()

	corpus_source.close()	# fermeture des fichiers
	corpus_target.close()

	
