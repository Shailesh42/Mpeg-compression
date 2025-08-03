import numpy as np

def block_matching(current, reference, block_size, search_range):
    """
    For each block in current frame, search within reference frame to find best match.
    Returns motion_vectors list [(dy, dx)] and motion compensated frame.
    """
    h, w = current.shape
    mc_frame = np.zeros_like(current)
    motion_vectors = []

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            cur_block = current[y:y+block_size, x:x+block_size]
            best_mse = float('inf')
            best_mv = (0, 0)
            best_block = cur_block

            for dy in range(-search_range, search_range + 1):
                for dx in range(-search_range, search_range + 1):
                    ref_y = y + dy
                    ref_x = x + dx
                    if (0 <= ref_y < h - block_size) and (0 <= ref_x < w - block_size):
                        ref_block = reference[ref_y:ref_y+block_size, ref_x:ref_x+block_size]
                        mse = np.mean((cur_block - ref_block) ** 2)
                        if mse < best_mse:
                            best_mse = mse
                            best_mv = (dy, dx)
                            best_block = ref_block

            mc_frame[y:y+block_size, x:x+block_size] = best_block
            motion_vectors.append(best_mv)
    return motion_vectors, mc_frame

def motion_compensate_using_vectors(reference, motion_vectors, block_size):
    """
    Apply motion vectors to reference frame to construct predicted frame.
    """
    h, w = reference.shape
    predicted = np.zeros_like(reference)
    idx = 0

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            dy, dx = motion_vectors[idx]
            ref_y = y + dy
            ref_x = x + dx
            # Clamp inside boundaries
            ref_y = min(max(0, ref_y), h - block_size)
            ref_x = min(max(0, ref_x), w - block_size)
            predicted[y:y+block_size, x:x+block_size] = reference[ref_y:ref_y + block_size, ref_x:ref_x + block_size]
            idx += 1

    return predicted

