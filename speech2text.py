import speech_recognition as sr
import random
import nltk
from nltk.corpus import stopwords
import datetime
import pyttsx3
import shutil

def say(s):
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(s)
    engine.runAndWait()
    
def listen_input(s, t):
    r = sr.Recognizer()
    r.energy_threshold = 1000
    r.pause_threshold = t
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print(s, end="")
        audio = r.listen(source)
    text = r.recognize_google(audio)
    return text

def execute():
    keywords_dict = {"ATM and e-facilities":["debit card", "cards", "credit card", "ATM", "net banking", "password", "pin"], "Personnel":["manager", "teller", "guard", "accountant"], "Loan and lending":["loan"], "Cashier":["deposit", "withdraw","transaction", "cheque", "bounce", "currency"]}
    folders = list(keywords_dict.keys())
    say("Input last 4 digits of your account number")
    ac_num = listen_input("Input last 4 digits of your A/c No. = ", 0.8)
    print(ac_num)

    t = datetime.datetime.now()
    filename = "E:/project_awaaz/awaaz_input/" + ac_num + "_" + str(t.year) + "_" + str(t.month) + "_" + str(t.day) + "_" + str(t.hour) + "_" + str(t.minute) + ".txt"

    complaint = ""
    say("Input your complaint")
    complaint = listen_input("Input your complaint = ", 3)
    say("registered")
        
    fobj = open(filename, "w")
    fobj.write(complaint)
    fobj.close()
    sort_into_folders(complaint, keywords_dict, filename, folders)

def KMPSearch(pat, txt, found): 
	M = len(pat) 
	N = len(txt) 

	# create lps[] that will hold the longest prefix suffix 
	# values for pattern 
	lps = [0]*M 
	j = 0 # index for pat[] 

	# Preprocess the pattern (calculate lps[] array) 
	computeLPSArray(pat, M, lps) 

	i = 0 # index for txt[] 
	while i < N: 
		if pat[j] == txt[i]: 
			i += 1
			j += 1

		if j == M: 
			found.append(i-j)
			j = lps[j-1]

		# mismatch after j matches 
		elif i < N and pat[j] != txt[i]: 
			# Do not match lps[0..lps[j-1]] characters, 
			# they will match anyway 
			if j != 0: 
				j = lps[j-1] 
			else: 
				i += 1

def computeLPSArray(pat, M, lps): 
	len = 0 # length of the previous longest prefix suffix 

	lps[0] # lps[0] is always 0 
	i = 1

	# the loop calculates lps[i] for i = 1 to M-1 
	while i < M: 
		if pat[i]== pat[len]: 
			len += 1
			lps[i] = len
			i += 1
		else: 
			# This is tricky. Consider the example. 
			# AAACAAAA and i = 7. The idea is similar 
			# to search step. 
			if len != 0: 
				len = lps[len-1] 

				# Also, note that we do not increment i here 
			else: 
				lps[i] = 0
				i += 1

def sort_into_folders(complaint, keywords_dict, filename, folders):
    found = list()
    category_count = list()
    for category in folders:
        keywords = keywords_dict[category]
        for pat in keywords:
            KMPSearch(pat, complaint, found)
        category_count.append(len(found))
        found.clear()
    folder_num = category_count.index(max(category_count))
    newfilename = "E:/project_awaaz/" + folders[folder_num] + "/" + filename[29:]
    shutil.move(filename, newfilename)


#main
execute()
