# image-file-hider
A simple tool to embed encrypted files into an image while preserving the original image data

## Description
This tool contains 4 main files:
 - `enc.py` is the original encoder. It takes an input file and encodes that into an image `key.jpg`
 - `dec.py` is the original decoder. It takes an input image and decodes it into a file as specified by the user
 - `encfast.py` is the chunk-optimized encoder. It takes an input image and input file, encoding the latter into the former. It uses threaded chunk encoders with a modifiable **CHUNKSIZE** variable
 - `decfast.py` is the chunk-optimized decoder. It takes an input image and decodes it. It uses threaded chunk decoders with a modifiable **CHUNKSIZE** variable

## How encoding works
Input: File, Key
 - Read the file as bytes into `Data`
 - Create a copy of the key and reverse it. We will call this `Rkey`
 - Create an empty set of bytes containing our output data. We will call this `Out`
 - Iterate over `[0...len(Data)-1]` such that `Out[i] = Data[i] xor Key[i%len(key)] xor Rkey[i%len(key)]`
 - Save `Out` to a temporary file
 - Write 256 blank bytes to the end of the file
 - In these 256 bytes, write the numeric length of the file you have just encoded
 - Combine the bytes of the image and of the temporary file to get an encoded image file
 - Delete the temporary file

## How decoding works
Input: File, Key
 - Read the file as bytes into `DataRaw`
 - From the last 256 bytes of dataraw, extract the file length as `Flen`
 - Read flen number of bytes from the end file (excluding the block of 256 bytes) and save it as `Data`
 - Create a copy of the key and reverse it. We will call this `Rkey`
 - Create an empty set of bytes containing out output data. We will call this `Out`
 - Iterate over `[0...Flen-1]` such that `Out[i] = Data[i] xor Key[i%len(key)] xor Rkey[i%len(key)]` (The inverse operation of XOR is XOR itself!)
 - Save `Out` to an output file to get the extracted data

## How chunking works
