import os

# Read the file to hide
filename = input("File name: ")
data = None
with open(filename,  mode='rb') as fl: data = fl.read()
filesize = len(data)

# Create a secret key
key = input("Add a key: ").encode()
keysize = len(key)

# Create encrypted data using XOR
keydat = b''
for i in range(filesize):
    keydat += (data[i]^key[i%keysize]^key[-1-i%keysize]).to_bytes(1, 'little')

# Write 256 bytes containing filesize
keydat += f"{filesize}".ljust(256).encode()

# Write data to temporary file
with open('temp', mode='wb') as fl: fl.write(keydat)

# Copy data and delete temporary file
os.system(f"copy /b key.jpg+temp out.jpg&&del temp")