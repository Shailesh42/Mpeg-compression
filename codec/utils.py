import numpy as np
from scipy.fftpack import dct, idct

def blockify(frame, block_size):
    h, w = frame.shape
    blocks = []
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = frame[y:y+block_size, x:x+block_size]
            # Pad block if edges not exact multiple
            if block.shape != (block_size, block_size):
                padded = np.zeros((block_size, block_size))
                padded[:block.shape[0], :block.shape[1]] = block
                block = padded
            blocks.append(block)
    return blocks

def unblockify(blocks, block_size):
    # Assume blocks cover an exact rectangle frame size
    n_blocks = len(blocks)
    h_blocks = int(np.sqrt(n_blocks))
    w_blocks = h_blocks
    # If input frame shape is unknown, we try to guess by shape of blocks count:
    for i in range(1, n_blocks+1):
        if n_blocks % i == 0:
            h_blocks = i
            w_blocks = n_blocks // i
    # Rebuild frame from blocks
    frame = np.zeros((h_blocks * block_size, w_blocks * block_size))
    idx = 0
    for y in range(0, h_blocks * block_size, block_size):
        for x in range(0, w_blocks * block_size, block_size):
            frame[y:y+block_size, x:x+block_size] = blocks[idx]
            idx += 1
    return frame

def dct2d(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2d(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def quantize(block, Q):
    return np.round(block / Q)

def dequantize(block, Q):
    return block * Q

def zigzag_encode(block):
    # Zigzag scan of 8x8 block
    h, w = block.shape
    result = []
    for s in range(h + w - 1):
        if s % 2 == 0:
            x = min(s, w-1)
            y = s - x
            while x >= 0 and y < h:
                result.append(block[y, x])
                x -= 1
                y += 1
        else:
            y = min(s, h-1)
            x = s - y
            while y >= 0 and x < w:
                result.append(block[y, x])
                x += 1
                y -= 1
    return np.array(result)

def zigzag_decode(arr):
    n = int(np.sqrt(len(arr)))
    result = np.zeros((n, n))
    h, w = n, n
    idx = 0
    for s in range(h + w - 1):
        if s % 2 == 0:
            x = min(s, w-1)
            y = s - x
            while x >= 0 and y < h:
                result[y, x] = arr[idx]
                idx += 1
                x -= 1
                y += 1
        else:
            y = min(s, h-1)
            x = s - y
            while y >= 0 and x < w:
                result[y, x] = arr[idx]
                idx += 1
                x += 1
                y -= 1
    return result

def run_length_encode(arr):
    # Basic RLE for flattened array
    encoded = []
    count = 1
    prev = arr[0]
    for val in arr[1:]:
        if val == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = val
            count = 1
    encoded.append((prev, count))
    return encoded

def run_length_decode(encoded):
    decoded = []
    for val, count in encoded:
        decoded.extend([val]*count)
    return np.array(decoded)

