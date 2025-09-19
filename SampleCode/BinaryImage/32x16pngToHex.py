import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image

def convert_image_to_binary(image_path, output_path):
    img = Image.open(image_path).convert('1')
    target_size = (32, 16)
    img.thumbnail(target_size, Image.Resampling.LANCZOS)

    canvas = Image.new('1', target_size, color=1)
    x_offset = (target_size[0] - img.width) // 2
    y_offset = (target_size[1] - img.height) // 2
    canvas.paste(img, (x_offset, y_offset))

    img_data = np.array(canvas)
    binary_data = bytearray()

    for i in range(16):
        row_data = 0
        for j in range(32):
            if img_data[i, j] == 0:
                row_data |= (1 << (31 - j))
        binary_data += row_data.to_bytes(4, byteorder='big')

    with open(output_path, 'wb') as f:
        f.write(binary_data)

def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;"), ("All files", "*.*")]
    )
    if file_path:
        image_path_var.set(file_path)

def save_binary():
    image_path = image_path_var.get()
    if not image_path:
        messagebox.showwarning("警告", "画像ファイルを選択してください。")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin")])
    if output_path:
        try:
            convert_image_to_binary(image_path, output_path)
            messagebox.showinfo("成功", f"バイナリに変換して保存しました。\n{output_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました:\n{e}")

# GUI構築
root = tk.Tk()
root.title("画像 → 32x16バイナリ変換ツール")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

image_path_var = tk.StringVar()

tk.Label(frame, text="画像ファイル:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=image_path_var, width=40).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="参照...", command=select_image).grid(row=1, column=1, padx=5)

tk.Button(frame, text="変換して保存", command=save_binary, bg="green", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
