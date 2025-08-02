MPEG-1 Style Video Compression System with GUI
Project Overview
This project implements a simple MPEG-1 style video compression and decompression system in Python. It uses common video compression techniques like:

Intra-frame compression (I-frames): Compresses individual frames using block-based Discrete Cosine Transform (DCT), quantization, and run-length encoding.

Inter-frame compression (P-frames): Uses motion estimation and compensation to encode differences between frames.

Basic scalability and performance metrics: Evaluates compression quality using PSNR and compression ratio.

A Graphical User Interface (GUI) built with Tkinter allows users to:

Select a video file to encode (compress).

See compression size and quality metrics.

Select an encoded file to decode back to video.

Features
Supports I-frame and P-frame based compression.

Motion Estimation using block matching for P-frames.

DCT, Quantization, Zigzag scanning, and Run-Length Encoding for compression.

Encode and decode videos with saved files.

Shows PSNR (quality metric) and compression size in the GUI.

User-friendly simple interface for encoding and decoding.

How to Use
Run the application:

bash
python main.py
Click Encode Video File to pick an input .avi video to compress.

Wait for encoding to finish; the GUI will display original size, compressed size, and PSNR.

Click Decode Encoded File to pick the saved encoded file (.npy) to reconstruct the video.

Decoded video will be saved as an .avi file in the outputs/ folder.

Project Structure
main.py — Launches the GUI.

gui/ — User interface code.

codec/ — Core encoding and decoding logic.

motion/ — Motion estimation and compensation code.

outputs/ — Folder for encoded data and decoded videos.

requirements.txt — Lists required Python packages.

Requirements
Python 3.x

Packages: numpy, opencv-python, scipy, tk (install via pip install -r requirements.txt)

Notes
This project is a basic demonstration of video compression concepts.

Currently, B-frame support and chroma channel compression are not implemented.

You can extend the project by adding support for more frame types, color channels, better entropy coding, or a more advanced GUI.

If you have any questions or need help, feel free to ask!

You can copy-paste this text into your README.md. It’s designed for simplicity and good understanding by users new to video compression or Python projects. Let me know if you want it more technical or with additional sections!
