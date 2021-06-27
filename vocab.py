#!/usr/bin/python
import asyncio
import aiohttp
from tqdm import tqdm  
import sys, getopt, requests, cgi, os, csv  
  
MA3_DOWNLOAD_URL = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/%s--_gb_1.mp3"  
buffer_size = 1024  
  
async def main(argv):  
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
		await downloadMp3FromCSV(csv, output)  
	else:  
		downloadMp3(vocabulary, output)  
  
async def downloadMp3(vocab, output):  
	if not vocab:  
		showInstruction()  
  
	downloadURL = MA3_DOWNLOAD_URL % vocab
	async with aiohttp.ClientSession() as session:  
		async with session.get(downloadURL) as response:

			try:
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
	  
				progress = tqdm(desc=f"Downloading {filename}", total=file_size, unit="", unit_scale=True, unit_divisor=1024)  
				with open(filename, "wb") as f:  
					async for chunk in response.content.iter_chunked(buffer_size): 
						f.write(chunk)  
						progress.update(len(chunk))

			except NameError as erroe:
				print('Sorry %s is not exist in database.' % vocab)
				print(error.__class__.__name__)
				exit()

	  
  
async def downloadMp3FromCSV(input, output):  
	vocabList = getVocabularyList(input)  
  
	for vocab in vocabList:  
		await downloadMp3(vocab, output)  
  
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
	print('vocab.py [-c <csv_file_path>] -d <vocabulary> -o <output_directory>')  
	sys.exit()  
  
if __name__ == "__main__":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  
	asyncio.run(main(sys.argv[1:]))
