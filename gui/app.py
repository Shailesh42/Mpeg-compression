import tkinter as tk
from tkinter import filedialog, messagebox
from codec.encode import encode_video
from codec.decode import decode_video

class MPEG1CodecApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MPEG-1 Style Video Codec")
        self.geometry("450x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="MPEG-1 Style Video Codec", font=("Arial", 18, "bold")).pack(pady=15)
        tk.Button(self, text="Encode Video File", width=25, height=2, command=self.encode_video).pack(pady=10)
        tk.Button(self, text="Decode Encoded File", width=25, height=2, command=self.decode_video).pack(pady=10)
        self.status = tk.Label(self, text="", fg="blue", font=("Arial", 11))
        self.status.pack(pady=15)

    def encode_video(self):
        file_path = filedialog.askopenfilename(title="Select Video File to Encode", 
                                               filetypes=[("AVI videos", "*.avi"), ("All files", "*.*")])
        if not file_path:
            return
        self.status.config(text="Encoding, please wait...")
        self.update_idletasks()

        try:
            out_file, orig_size, comp_size, psnr = encode_video(file_path)
            msg = (f"Encoding completed!\nOriginal Size: {orig_size/1024:.1f} KB\n"
                   f"Compressed Size: {comp_size/1024:.1f} KB\nPSNR: {psnr:.2f} dB\nSaved encoding: {out_file}")
            self.status.config(text=msg)
        except Exception as e:
            messagebox.showerror("Error in Encoding", str(e))
            self.status.config(text="Encoding failed!")

    def decode_video(self):
        file_path = filedialog.askopenfilename(title="Select Encoded File to Decode", 
                                               filetypes=[("NumPy files", "*.npy"), ("All files", "*.*")])
        if not file_path:
            return
        self.status.config(text="Decoding, please wait...")
        self.update_idletasks()

        try:
            decoded_video_path = decode_video(file_path)
            msg = f"Decoding completed!\nDecoded video saved at:\n{decoded_video_path}"
            self.status.config(text=msg)
        except Exception as e:
            messagebox.showerror("Error in Decoding", str(e))
            self.status.config(text="Decoding failed!")
