
import os
import numpy as np
import cv2
from codec.utils import (
    blockify, unblockify, dct2d, idct2d, quantize, dequantize, 
    zigzag_encode, zigzag_decode, run_length_encode, run_length_decode
)
from motion.block_matching import motion_compensate_using_vectors

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

BLOCK_SIZE = 16


def decode_video(encoded_path):
    # Load encoded data
    encoded_data = np.load(encoded_path, allow_pickle=True)

    decoded_frames = decode_video_from_data(encoded_data)

    # Save decoded video to decoded.avi
    out_path = os.path.join("outputs", "decoded_video.avi")
    os.makedirs("outputs", exist_ok=True)

    # Make video writer
    h, w = decoded_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(out_path, fourcc, 30, (w,h), isColor=False)

    for frame in decoded_frames:
        # Convert single Y channel into 3channel grayscale frame for saving
        frame_uint8 = np.clip(frame, 0, 255).astype(np.uint8)
        # Write grayscale frame (single channel)
        out.write(cv2.cvtColor(frame_uint8, cv2.COLOR_GRAY2BGR))
    out.release()

    return out_path


def decode_video_from_data(encoded_data):
    """
    Decode frames from encoded data list
    Returns list of Y-channel grayscale frames as float32 np.arrays
    """
    decoded_frames = []
    prev_i_p_frame = None

    for frame_info in encoded_data:
        ftype = frame_info['type']

        if ftype == 'I':
            blocks = []
            for rle in frame_info['blocks']:
                zz = run_length_decode(rle)
                quant_block = zigzag_decode(zz)
                idct_block = idct2d(dequantize(quant_block, Q_INTRA))
                blocks.append(idct_block)
            frame = unblockify(blocks, BLOCK_SIZE)
            decoded_frames.append(frame)
            prev_i_p_frame = frame

        elif ftype == 'P':
            # Motion compensation using motion vectors on previous frame
            mv = frame_info['motion_vectors']
            mc_frame = motion_compensate_using_vectors(prev_i_p_frame, mv, BLOCK_SIZE)

            blocks = []
            for rle in frame_info['blocks']:
                zz = run_length_decode(rle)
                quant_block = zigzag_decode(zz)
                idct_block = idct2d(dequantize(quant_block, Q_INTER))
                blocks.append(idct_block)

            diff_frame = unblockify(blocks, BLOCK_SIZE)
            frame = mc_frame + diff_frame
            decoded_frames.append(frame)
            prev_i_p_frame = frame

        else:
            # B-frame in this example: use previous reconstructed frame
            decoded_frames.append(prev_i_p_frame)

    return decoded_frames
