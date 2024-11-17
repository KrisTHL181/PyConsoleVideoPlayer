import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def process_image(input_path):
    with Image.open(input_path) as img:
        gray_img = img.convert('L')
        gray_array = np.array(gray_img)

        # 定义区间边界
        bins = [0, 32, 64, 128, 160, 192, 224, 256]
        # 使用 np.digitize 将灰度值分配到相应的区间
        digitized_array = np.digitize(gray_array, bins) - 1

        binary_array = np.where(digitized_array == 0, '0', '0')
        binary_array = np.where(digitized_array == 1, '3', binary_array)
        binary_array = np.where(digitized_array == 2, '6', binary_array)
        binary_array = np.where(digitized_array == 3, '8', binary_array)
        binary_array = np.where(digitized_array == 4, '9', binary_array)
        binary_array = np.where(digitized_array == 5, '6', binary_array)
        binary_array = np.where(digitized_array == 6, '1', binary_array)

    return '\n'.join(''.join(row) for row in binary_array)

def process_file(file_info):
    input_path, output_dir, filename = file_info

    output_filename = os.path.splitext(filename)[0] + '.txt'
    output_path = os.path.join(output_dir, output_filename)

    binary_data = process_image(input_path)

    with open(output_path, 'w') as f:
        f.write(binary_data)

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='将文件夹中的图片转换为二值图像并保存为文本文件')
    parser.add_argument('-d', '--dir', type=str, required=True, help='输入文件夹路径')
    parser.add_argument('-o', '--output', type=str, required=True, help='输出文件夹路径')

    args = parser.parse_args()

    input_dir = args.dir
    output_dir = args.output

    os.makedirs(output_dir, exist_ok=True)

    file_infos = [(os.path.join(input_dir, f), output_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    with Pool(processes=cpu_count()) as pool:
        for result in tqdm(pool.imap(process_file, file_infos), total=len(file_infos)):
            pass

if __name__ == '__main__':
    main()
