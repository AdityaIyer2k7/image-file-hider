# Read the image with hidden file
filename = input("Image to extract: ")
data = None
with open(filename, mode='rb') as fl: data = fl.read()

# Obtain the secret key
key = input("Add a key: ").encode()
keysize = len(key)

# Last 256 bytes are filesize
datsize = int(data[-256:])
print(datsize)

# Get hidden data
data = data[-datsize-256 : -256]

# Decrypt hidden data
decrypted = b''
for i in range(datsize):
    decrypted += (data[i]^key[i%keysize]^key[-1-i%keysize]).to_bytes(1, 'little')

# Create the output file
outfilename = input("Output file: ")
with open(outfilename, mode='wb') as fl: fl.write(decrypted)