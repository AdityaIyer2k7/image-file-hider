import math
import threading

# Set a chunk size of 16 mb = 16*1024 kb = 16*1024*1024 bytes
CHUNKSIZE = 16*1024*1024

# Read the image with hidden file
filename = input("Image to extract: ")
datain = None
with open(filename, mode='rb') as fl: datain = fl.read()

# Obtain the secret key
key = input("Enter the key: ").encode()
keysize = len(key)
keytemp = [0]*keysize
for i in range(keysize): keytemp[i] = key[i]^key[-1-i]
key = bytes(keytemp)    # This secret key is double encoded using a front-back XOR cipher

# Last 256 bytes are filesize
filesize = int(datain[-256:])
print(f"Filesize: {filesize}")
chunkcount = math.ceil(filesize/CHUNKSIZE)

# Get hidden data
data = datain[-filesize-256 : -256]

# Create buffers for chunks to raed and write
databuffer = [0]*filesize
statbuffer = [False]*chunkcount

# Create a chunk decoder
def chunkDecode(id):
    print(f"Created chunk id {id}")
    start = CHUNKSIZE*id
    stop = min(CHUNKSIZE+start, filesize)
    for i in range(start, stop):
        databuffer[i] = data[i]^key[i%keysize]
    statbuffer[id] = True
    print(f"Chunk {id} finished")

# Create threads for all chunks
for i in range(chunkcount):
    threading.Thread(target=chunkDecode, args=(i,)).start()

# Create a waiter loop to wait for chunks to finish
while not all(statbuffer): pass

# Create the output file
dataout = bytes(databuffer)
outfilename = input("Output file: ")
with open(outfilename, mode='wb') as fl: fl.write(dataout)