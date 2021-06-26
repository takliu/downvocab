#!/usr/bin/python  
from tqdm import tqdm  
import sys, getopt, requests, cgi, os, csv  
  
MA3_DOWNLOAD_URL = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/%s--_gb_1.mp3"  
buffer_size = 1024  
  
def main(argv):  
	vocabulary = ''  
	output = ''  
	csv = ''  
  
	try:  
		opts, args = getopt.getopt(argv, "hd:o:c:", ["vocab=", "ofile=", "csv="])  
	except getopt.GetoptError:  
		showInstruction()  
	for opt, arg in opts:  
		if opt == '-h':  
			showInstruction()  
		elif opt in ("-d", "--vocab"):  
		 	vocabulary = arg  
		elif opt in ("-o", "--ofile"):  
			output = arg  
		elif opt in ("-c", "--csv"):  
			csv = arg  
  
	if csv:  
		downloadMp3FromCSV(csv, output)  
	else:  
		downloadMp3(vocabulary, output)  
  
def downloadMp3(vocab, output):  
	if not vocab:  
		showInstruction()  
  
	downloadURL = MA3_DOWNLOAD_URL % vocab  
	response = requests.get(downloadURL, stream=True)  
	file_size = int(response.headers.get("Content-Length", 0))  
	content_disposition = response.headers.get("Content-Disposition")  
  
	default_filename = "%s.mp3" % vocab  
	if output:  
		makedirIfNeeded(output)  
		default_filename = output + "/" + default_filename  
	  
	if content_disposition:  
		value, params = cgi.parse_header(content_disposition)  
		filename = params.get("filename", default_filename)  
	else:  
		filename = default_filename  
  
	progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)  
	with open(filename, "wb") as f:  
		for data in progress.iterable:  
			f.write(data)  
			progress.update(len(data))  
  
def downloadMp3FromCSV(input, output):  
	vocabList = getVocabularyList(input)  
  
	for vocab in vocabList:  
		downloadMp3(vocab, output)  
  
def getVocabularyList(csvPath):  
	vocabList = []  
  
	with open(csvPath, newline='') as csvFile:  
		csvFile = csv.reader(csvFile)  
		rows = list(csvFile)  
  
		for row in rows:  
			for item in row:  
				vocabList.append(item)  
  
	return vocabList  
  
def makedirIfNeeded(output):  
	if not os.path.isdir(output):  
		os.makedirs(output)		  
  
def showInstruction():  
	print('vocab.py -d <vocabulary> -o <output_path>')  
	sys.exit()  
  
if __name__ == "__main__":  
	main(sys.argv[1:])