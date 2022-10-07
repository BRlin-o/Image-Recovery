import numpy as np
from scipy.signal import convolve, correlate

## 雙線性內插演算法（Bilinear interpolation）
def rgb2cfa(RGB, pattern='RGGB'):
    height, width = RGB.shape[:2]
    
    _R = RGB[:, :, 0]
    _G = RGB[:, :, 1]
    _B = RGB[:, :, 2]

    bayer = np.array(list(pattern)).reshape(2, 2)
    bayerArray = np.tile(bayer, (height//2, width//2))

    cfa = np.zeros((height, width), dtype=np.uint8)
    cfa[bayerArray=='R'] = _R[bayerArray=='R']
    cfa[bayerArray=='G'] = _G[bayerArray=='G']
    cfa[bayerArray=='B'] = _B[bayerArray=='B']

    return cfa

## 雙線性內插演算法（Bilinear interpolation）, convolve(mode = 'same')可能導致PSNR降低
def demosaic(CFA, pattern='RGGB'):
    height, width = CFA.shape[:2]
    bayer = np.array(list(pattern)).reshape(2, 2)
    bayerArray = np.tile(bayer, (height//2, width//2))
    R_m, G_m, B_m = [bayerArray == c for c in ['R', 'G', 'B']]

    H_G = np.array([
        [0, 1, 0],
        [1, 4, 1],
        [0, 1, 0]
    ]) / 4
    H_RB = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]) / 4

    # R = convolve(CFA*R_m, H_RB, mode='same')
    # G = convolve(CFA*G_m, H_G, mode='same')
    # B = convolve(CFA*B_m, H_RB, mode='same')
    R = correlate(CFA*R_m, H_RB, mode='same')
    G = correlate(CFA*G_m, H_G, mode='same')
    B = correlate(CFA*B_m, H_RB, mode='same')

    R[bayerArray=='r']=CFA[bayerArray=='r']
    G[bayerArray=='g']=CFA[bayerArray=='g']
    B[bayerArray=='b']=CFA[bayerArray=='b']

    return np.dstack([R, G, B]).astype(np.uint8)