#!/usr/bin/python

import sys, getopt, urllib

MA3_DOWNLOAD_URL = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/%s--_gb_1.mp3"


def main(argv):
   vocabulary = ''

   try:
      opts, args = getopt.getopt(argv, "hd:", ["vocab="])
   except getopt.GetoptError:
      showInstruction()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
        showInstruction()
        sys.exit()
      elif opt in ("-d", "--vocab"):
        vocabulary = arg
   		print('Vocabulary is ', vocabulary)

def downloadMp3(vocab):
	   		

def showInstruction():
	print('test.py -d <vocabulary>')


if __name__ == "__main__":
   main(sys.argv[1:])