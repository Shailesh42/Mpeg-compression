import os
import cv2
import numpy as np
from codec.utils import (
    blockify, unblockify, dct2d, idct2d, quantize, dequantize, 
    zigzag_encode, zigzag_decode, run_length_encode, run_length_decode
)
from motion.block_matching import block_matching

# Quantization matrices (8x8) for intra and inter frames
Q_INTRA = np.array([
    [8,16,19,22,26,27,29,34],
    [16,16,22,24,27,29,34,37],
    [19,22,26,27,29,34,34,38],
    [22,22,26,27,29,34,37,40],
    [22,26,27,29,32,35,40,48],
    [26,27,29,32,35,40,48,58],
    [26,27,29,34,38,46,56,89],
    [27,29,35,38,46,56,69,83],
])

Q_INTER = np.ones((8,8)) * 16

BLOCK_SIZE = 16  # macroblocks 16x16 for motion estimation
SEARCH_RANGE = 4
SKIP_THRESHOLD = 5

def encode_video(video_path):
    # Read video frames in YCrCb color space
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        frames.append(frame_ycrcb)
    cap.release()

    num_frames = len(frames)
    height, width, _ = frames[0].shape

    # Frame types using repeating GOP pattern (I P B B P B B)
    frame_types = ['I', 'P', 'B', 'B', 'P', 'B', 'B'] * ((num_frames // 7) + 1)
    frame_types = frame_types[:num_frames]

    encoded_data = []
    prev_i_p_frame = None

    # Process frames
    for i, (frame, ftype) in enumerate(zip(frames, frame_types)):
        Y = frame[:,:,0].astype(np.float32)
        if ftype == 'I':
            # Encode I-frame (intra) blocks: DCT + Quantization + Zigzag + RLE
            blocks = blockify(Y, BLOCK_SIZE)
            encoded_blocks = []
            for b in blocks:
                dct_block = dct2d(b)
                quant_block = quantize(dct_block, Q_INTRA)
                zz = zigzag_encode(quant_block)
                rle = run_length_encode(zz)
                encoded_blocks.append(rle)
            encoded_data.append({'type': 'I', 'blocks': encoded_blocks})
            prev_i_p_frame = Y
        elif ftype == 'P':
            # Motion estimation and compensation
            motion_vectors, mc_frame = block_matching(Y, prev_i_p_frame, BLOCK_SIZE, SEARCH_RANGE)

            # Difference frame
            diff = Y - mc_frame
            # Encode difference blocks
            blocks_diff = blockify(diff, BLOCK_SIZE)
            encoded_blocks = []
            for b in blocks_diff:
                dct_block = dct2d(b)
                quant_block = quantize(dct_block, Q_INTER)
                zz = zigzag_encode(quant_block)
                rle = run_length_encode(zz)
                encoded_blocks.append(rle)

            encoded_data.append({'type': 'P', 'motion_vectors': motion_vectors, 'blocks': encoded_blocks})
            prev_i_p_frame = Y
        else:
            # B-frame not implemented in this basic example: store empty
            encoded_data.append({'type': 'B', 'blocks': []})

    # Save encoded data to .npy file
    output_path = os.path.join("outputs", "encoded_video.npy")
    os.makedirs("outputs", exist_ok=True)
    np.save(output_path, encoded_data)

    # Compression size
    original_size = os.path.getsize(video_path)
    compressed_size = os.path.getsize(output_path)

    # Calculate PSNR between first decoded frame and original first frame as quick quality metric
    from codec.decode import decode_video_from_data
    decoded_frames = decode_video_from_data(encoded_data)
    psnr_val = calculate_psnr(frames[0][:,:,0].astype(np.float32), decoded_frames[0])

    return output_path, original_size, compressed_size, psnr_val


def calculate_psnr(original, decoded):
    mse = np.mean((original - decoded) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 10 * np.log10((PIXEL_MAX ** 2) / mse)
