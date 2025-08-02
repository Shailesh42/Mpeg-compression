MPEG-1 Style Video Compression System with GUI
📽️ Project Overview
This project implements a simple MPEG-1 style video compression and decompression system in Python. It demonstrates the core concepts of video compression using:

Intra-frame compression (I-frames): Compresses individual frames using block-based DCT, quantization, and run-length encoding.

Inter-frame compression (P-frames): Uses motion estimation and compensation to encode differences between frames.

Scalability and performance metrics: Includes evaluation using PSNR and compression ratio.

A simple GUI (built with Tkinter) allows users to:

Select a video file to compress.

View compression size and quality metrics.

Decode an encoded file back to video.
✨ Features
✅ I-frame and P-frame based compression
✅ Block-based motion estimation (for P-frames)
✅ DCT, quantization, zigzag scan, and run-length encoding
✅ Save and load encoded videos
✅ Shows PSNR and compression ratio in the GUI
✅ Simple user-friendly interface

Install requirements:

pip install -r requirements.txt

Run the application:
python main.py
To Encode:

Click Encode Video File

Choose an .avi file to compress

Wait for the process to complete

The GUI will show original size, compressed size, and PSNR

To Decode:

Click Decode Encoded File

Select the saved .npy encoded file

The decoded video will be saved as an .avi in the outputs/ folder
├── main.py                 # Launches the GUI
├── gui/                    # GUI logic (Tkinter)
├── codec/                  # Encoding and decoding logic
├── motion/                 # Motion estimation and compensation
├── outputs/                # Output folder (encoded + decoded videos)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
Requirements
Python 3.x

Required packages:
numpy
opencv-python
scipy
tk (usually pre-installed with Python)

This project is a basic demonstration of video compression concepts.
B-frames and chroma subsampling are not implemented.
Possible improvements:
Add B-frame support
Implement chroma channel compression (YUV)
Improve entropy coding (e.g., Huffman)
Enhance the GUI/UX
