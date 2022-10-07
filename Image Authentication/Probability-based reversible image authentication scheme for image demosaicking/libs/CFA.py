import numpy as np

def rgb2cfa(img, pattern='rggb'):
    height, width = img.shape[:2]
    _R = np.array([[pattern[0]=='r', pattern[1]=='r'], [pattern[2]=='r', pattern[3]=='r']], dtype=np.uint8)
    _R = np.tile(_R, (height//2, width//2))

    _G = np.array([[pattern[0]=='g', pattern[1]=='g'], [pattern[2]=='g', pattern[3]=='g']], dtype=np.uint8)
    _G = np.tile(_G, (height//2, width//2))

    _B = np.array([[pattern[0]=='b', pattern[1]=='b'], [pattern[2]=='b', pattern[3]=='b']], dtype=np.uint8)
    _B = np.tile(_B, (height//2, width//2))

    _R*=img[:, :, 0]
    _G*=img[:, :, 1]
    _B*=img[:, :, 2]

    new_image = _R + _G + _B
    return new_image

def demosaicked(cfa, pattern='rggb'):
    height, width = cfa.shape[:2]
    _R = np.array([[pattern[0]=='r', pattern[1]=='r'], [pattern[2]=='r', pattern[3]=='r']], dtype=np.uint8)
    _R = np.tile(_R, (height//2, width//2))

    _G = np.array([[pattern[0]=='g', pattern[1]=='g'], [pattern[2]=='g', pattern[3]=='g']], dtype=np.uint8)
    _G = np.tile(_G, (height//2, width//2))

    _B = np.array([[pattern[0]=='b', pattern[1]=='b'], [pattern[2]=='b', pattern[3]=='b']], dtype=np.uint8)
    _B = np.tile(_B, (height//2, width//2))

    _R*=cfa
    _G*=cfa
    _B*=cfa
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            _R[i, j+1] = _R[i, j]
            _R[i+1, j] = _R[i, j]
            _R[i+1, j+1] = _R[i, j]

            _G[i, j] = _G[i, 1+j]
            _G[i+1, j+1] = _G[i, j-1]

            _B[i, j+1] = _B[i+1, j+1]
            _B[i+1, j] = _B[i+1, j+1]
            _B[i, j] = _B[i+1, j+1]

    new_image = np.zeros((height, width, 3), dtype=np.uint8)
    new_image[:, :, 0] = _R
    new_image[:, :, 1] = _G
    new_image[:, :, 2] = _B

    return new_image