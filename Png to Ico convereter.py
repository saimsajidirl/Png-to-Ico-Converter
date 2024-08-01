import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
import threading
import queue
import random
import string

class PNGToICOConverter:
    def __init__(self, master):
        self.master = master
        master.title("Advanced PNG to ICO Converter")

        self.stack = queue.Queue()
        self.conversion_thread = None

        # Input Frame
        self.input_frame = ttk.Frame(master)
        self.input_frame.pack(padx=10, pady=10)

        self.select_button = ttk.Button(self.input_frame, text="Select PNG Files", command=self.select_files)
        self.select_button.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self.input_frame, width=40)
        self.listbox.pack(side=tk.LEFT)

        # Preview Frame
        self.preview_frame = ttk.Frame(master)
        self.preview_frame.pack(padx=10, pady=10)

        self.preview_label = ttk.Label(self.preview_frame, text="Preview:")
        self.preview_label.pack()

        self.preview_canvas = tk.Canvas(self.preview_frame, width=128, height=128)
        self.preview_canvas.pack()

        # Output Frame
        self.output_frame = ttk.Frame(master)
        self.output_frame.pack(padx=10, pady=10)

        self.output_label = ttk.Label(self.output_frame, text="Output ICO File Path:")
        self.output_label.pack(side=tk.LEFT, padx=10)

        self.output_entry = ttk.Entry(self.output_frame)
        self.output_entry.pack(side=tk.LEFT)

        self.browse_button = ttk.Button(self.output_frame, text="Browse", command=self.browse_output)
        self.browse_button.pack(side=tk.LEFT)

        # Conversion Frame
        self.conversion_frame = ttk.Frame(master)
        self.conversion_frame.pack(padx=10, pady=10)

        self.convert_button = ttk.Button(self.conversion_frame, text="Convert PNG to ICO", command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(self.conversion_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT)

        self.status_label = ttk.Label(self.conversion_frame, text="")
        self.status_label.pack(side=tk.LEFT)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(title="Select PNG Files", filetypes=[("PNG Files", "*.png")])
        for file_path in file_paths:
            self.stack.put(file_path)
            self.listbox.insert(tk.END, file_path)
            self.update_preview(file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ico", filetypes=[("ICO Files", "*.ico")])
        if not file_path:
            file_path = self.generate_random_filename(".ico")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def generate_random_filename(self, extension):
        random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        return f"{random_name}{extension}"

    def start_conversion(self):
        if self.conversion_thread is None:
            self.conversion_thread = threading.Thread(target=self.convert_files)
            self.conversion_thread.start()

    def convert_files(self):
        total_files = self.stack.qsize()
        converted_files = 0

        while not self.stack.empty():
            file_path = self.stack.get()
            try:
                self.convert_single_file(file_path)
                converted_files += 1
                progress = (converted_files / total_files) * 100
                self.progress_bar["value"] = progress
                self.status_label["text"] = f"Converting {converted_files}/{total_files}..."
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {file_path}: {e}")

        self.conversion_thread = None
        self.progress_bar["value"] = 0
        self.status_label["text"] = "Conversion complete!"

    def convert_single_file(self, file_path):
        image = Image.open(file_path)

        output_path = self.output_entry.get()
        if not output_path:
            output_path = os.path.splitext(file_path)[0] + ".ico"

        image.save(output_path, format="ICO")

    def update_preview(self, file_path):
        try:
            image = Image.open(file_path)
            image = image.resize((128, 128))
            photo = ImageTk.PhotoImage(image)
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.preview_canvas.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preview: {e}")

root = tk.Tk()
converter = PNGToICOConverter(root)
root.mainloop()