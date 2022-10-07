import numpy as np

class AMBTC(object):
    def __init__(self, image, m):
        self.image = image
        self.height, self.width = image.shape[:2]
        self.m = m
        self.encoding = self.decoding = None
        ## User Requirement defined 2 is symbolic of 2 bit
        self.n = 2

    def encode(self):
        if self.image.ndim == 3:
            self.encode_rgb()
        else:
            self.encode_gray()

    def decode(self):
        if self.image.ndim == 3:
            self.decode_rgb()
        else:
            self.decode_gray()

    def encode_rgb(self):
        self.height, self.width = self.image.shape[:2]
        enData = []
        for i in range(0, self.height, self.m):
            enData_line = []
            for j in range(0, self.width, self.m):
                enData_dim = []
                for k in range(0, 3):
                    block = self.image[i:i+self.m, j:j+self.m, k]
                    enData_dim.append(self.encoded_block(block))
                enData_line.append(enData_dim)
            enData.append(enData_line)
        self.encoding = enData

    def encode_gray(self):
        self.height, self.width = self.image.shape[:2]
        enData = []
        for i in range(0, self.height, self.m):
            enData_line = []
            for j in range(0, self.width, self.m):
                block = self.image[i:i+self.m, j:j+self.m]
                enData_line.append(self.encoded_block(block))
            enData.append(enData_line)
        self.encoding = enData

    def decode_rgb(self):
        inputData = np.array(self.encoding)
        deData = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for i in range (0, inputData.shape[0]):
            for j in range (0, inputData.shape[1]):
                for k in range(0, 3):
                    deData[i*self.m:i*self.m+self.m, j*self.m:j*self.m+self.m, k] = self.decoded_block(inputData[i, j, k, 0], inputData[i, j, k, 1], inputData[i, j, k, 2])
        
        self.decoding = deData

    def decode_gray(self):
        inputData = np.array(self.encoding)
        self.height, self.width = inputData[:, :, 2][0, :].shape[0]*self.m,inputData[:, :, 2][:, 0].shape[0]*self.m
        deData = np.zeros((self.height, self.width), dtype=np.uint8)
        for i in range (0, inputData.shape[0]):
            for j in range (0, inputData.shape[1]):
                deData[i*self.m:i*self.m+self.m, j*self.m:j*self.m+self.m] = self.decoded_block(inputData[i, j, 0], inputData[i, j, 1], inputData[i, j, 2])
        
        self.decoding = deData

    def encoded_block(self, block):
        Ii = np.average(block)
        Bi = np.array(block > Ii, dtype=np.bool)
        ai = np.around(np.mean((Bi*block)[Bi > 0])).astype(np.uint8)
        bi = np.around(np.mean((~Bi*block)[Bi <= 0])).astype(np.uint8)
        return ai if ai is np.nan else bi, bi, Bi

    def decoded_block(self, ai, bi, Bi):
        return ai*Bi + bi*(~Bi)

    def encode2nBitBlocks(self):
        self.height, self.width = self.image.shape[:2]
        blocks = np.zeros((self.height, self.width), dtype=np.uint8)

        for i in range(0, self.height, self.m):
            for j in range(0, self.width, self.m):
                for k in range(0, 3):
                    blocks[i:i+self.m, j:j+self.m, k] = self.encodeing2nBitBlock(self.image[i:i+self.m, j:j+self.m, k])
        self.encoding_blocks = blocks

    def encodeing2nBitBlock(self, block):
        encoded = self.encoded_block(block)
        block = np.zeros((self.m, self.m), dtype=np.uint8)
        block[0, 0:self.m] = self.split2nBitArray(encoded[0])
        block[1, 0:self.m] = self.split2nBitArray(encoded[1])
        block[2:self.m, 0:self.m] = self.flattenBinaryArray2nBitArray(encoded[2]).reshape(self.m-2, self.m)
        return block

    def split2nBitArray(self, num, bit_size=8):
        num_array = np.zeros(bit_size//self.n, dtype=np.uint8)
        for i in range(bit_size//self.n):
            # num_array[bit_size//nbit-i-1]=(num % 2**nbit)
            num_array[i]=(num % 2**self.n)
            num = num >> self.n
        return num_array

    def flattenBinaryArray2nBitArray(self, arr):
        fArr = arr.flatten()
        print(fArr)
        num_array = np.zeros(len(fArr)//self.n, dtype=np.uint8)
        for i in range (len(fArr)):
            num_array[i//self.n] = num_array[i//self.n]*2 + fArr[i]
        return num_array