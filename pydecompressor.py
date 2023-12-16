import gzip
from os.path import exists 
import argparse
# this is a gzip decompression tool 
parser = argparse.ArgumentParser("pydecompressor")
parser.add_argument('file', help="specifies the gzip compressed file")
args =  parser.parse_args()
path = args.file

if exists(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rb') as content:
            decompressed_content = content.read()
            final = open(path[:-3], "x")
            final.write(decompressed_content.decode('utf-8'))
            final.close()
    else:
        print("File does not end with .gz extension"), exit(1)
else:
    print("File does not exist"), exit(1)


