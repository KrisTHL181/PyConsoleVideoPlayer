import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# 预生成十六进制查找表
hex_table = ["{:02x}".format(i) for i in range(256)]

def process_image(input_path: str) -> str:
    with Image.open(input_path) as img:
        img_array = np.array(img.convert("RGB"))
        height, width = img_array.shape[:2]
        
        # 一次性处理所有像素
        hex_pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = img_array[y, x]
                row.append(hex_table[r] + hex_table[g] + hex_table[b])
            hex_pixels.append(''.join(row))
        
        return '\n'.join(hex_pixels)

def process_file(file_info: tuple[str, str, str]):
    input_path, output_dir, filename = file_info
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
    
    try:
        hex_data = process_image(input_path)
        with open(output_path, "w") as f:
            f.write(hex_data)
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert images to RGB hex text files")
    parser.add_argument("-d", "--dir", type=str, required=True, help="Input directory")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    
    file_list = [
        (os.path.join(args.dir, f), args.output, f
        for f in os.listdir(args.dir) 
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    with Pool(cpu_count()) as pool:
        list(tqdm(pool.imap(process_file, file_list), total=len(file_list)))

if __name__ == "__main__":
    main()