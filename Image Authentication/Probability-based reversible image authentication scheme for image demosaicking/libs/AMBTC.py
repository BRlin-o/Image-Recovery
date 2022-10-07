import numpy as np

class AMBTC(object):
    def __init__(self, image, m):
        self.image = image
        self.height, self.width = image.shape[:2]
        self.m = m
        self.encoding = self.decoding = None

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
        ai = np.around(np.mean((Bi*block)[Bi > 0]))
        bi = np.around(np.mean((~Bi*block)[Bi <= 0]))
        return ai if ai is np.nan else bi, bi, Bi

    def decoded_block(self, ai, bi, Bi):
        return ai*Bi + bi*(~Bi)
