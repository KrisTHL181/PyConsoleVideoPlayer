import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def process_image(input_path):
    pixel_array = []
    with Image.open(input_path) as img:
        img_array = np.array(img.convert("RGB"))
        height, width = img_array.shape[0], img_array.shape[1]

        for y in range(height):
            for x in range(width):
                pixel = img_array[y, x]
                pixel_array.append(
                    "{:02x}{:02x}{:02x}".format(pixel[0], pixel[1], pixel[2])
                )
            pixel_array.append("\n")
        pixel_array.append("\n")

    return "\n".join(pixel_array)


def process_file(file_info):
    input_path, output_dir, filename = file_info

    output_filename = os.path.splitext(filename)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_data = process_image(input_path)

    with open(output_path, "w") as f:
        f.write(binary_data)


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(
        description="将文件夹中的图片转换为带有RGB真彩色的文本文件"
    )
    parser.add_argument("-d", "--dir", type=str, required=True, help="输入文件夹路径")
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="输出文件夹路径"
    )

    args = parser.parse_args()

    input_dir = args.dir
    output_dir = args.output

    os.makedirs(output_dir, exist_ok=True)

    file_infos = [
        (os.path.join(input_dir, f), output_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    with Pool(processes=cpu_count()) as pool:
        for result in tqdm(pool.imap(process_file, file_infos), total=len(file_infos)):
            pass


if __name__ == "__main__":
    main()
