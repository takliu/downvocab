#!/usr/bin/python
from tqdm import tqdm
import sys, getopt, requests, cgi

MA3_DOWNLOAD_URL = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/%s--_gb_1.mp3"
buffer_size = 1024


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
        downloadMp3(vocabulary)

def downloadMp3(vocab):
   downloadURL = MA3_DOWNLOAD_URL % vocab
   response = requests.get(downloadURL, stream=True)
   file_size = int(response.headers.get("Content-Length", 0))
   content_disposition = response.headers.get("Content-Disposition")

   default_filename = "%s.mp3" % vocab 
   
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
   	   	

def showInstruction():
	print('vocab.py -d <vocabulary>')


if __name__ == "__main__":
   main(sys.argv[1:])