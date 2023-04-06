import os
import math
import threading

# Set a chunk size of 16 mb = 16*1024 kb = 16*1024*1024 bytes
CHUNKSIZE = 16*1024*1024

# Get the original image
imgname = input("Original image: ")

# Read the file to hide
filename = input("File name: ")
datain = None
with open(filename,  mode='rb') as fl: datain = fl.read()
filesize = len(datain)
chunkcount = math.ceil(filesize/CHUNKSIZE)

# Create a secret key
key = input("Add a key: ").encode()
keysize = len(key)
keytemp = [0]*keysize
for i in range(keysize): keytemp[i] = key[i]^key[-1-i]
key = bytes(keytemp)    # This secret key is double encoded using a front-back XOR cipher

# Create buffers for threaded chunks to read and write
databuffer = [0]*filesize
statbuffer = [False]*chunkcount

# Create a chunk encoder
def chunkEncode(id):
    print(f"Created chunk id {id}")
    start = CHUNKSIZE*id
    stop = min(filesize, start+CHUNKSIZE)
    for i in range(start, stop):
        databuffer[i] = datain[i]^key[i%keysize]
    statbuffer[id] = True
    print(f"Chunk {id} finished")

# Create threads for all chunks
for i in range(chunkcount):
    threading.Thread(target=chunkEncode, args=(i,)).start()

# Create a waiter loop to wait for chunks to finish
while not all(statbuffer): pass

# Write 256 bytes containing filesize
dataout = bytes(databuffer)
dataout += f"{filesize}".ljust(256).encode()

# Write data to temporary file
with open('temp', mode='wb') as fl: fl.write(dataout)

# Copy data and delete temporary file
os.system(f"copy /b {imgname}+temp out.jpg&&del temp")