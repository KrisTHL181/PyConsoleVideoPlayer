import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def process_image(input_path: str) -> str:
    with Image.open(input_path) as img:
        gray_img = img.convert("L")
        gray_array = np.array(gray_img)
        binary_array = np.where(gray_array > 128, "1", "0")
        binary_data = "\n".join("".join(row) for row in binary_array)

    return binary_data


def process_file(file_info: tuple[str, str, str]) -> None:
    input_path, output_dir, filename = file_info

    output_filename = os.path.splitext(filename)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_data = process_image(input_path)

    with open(output_path, "w") as f:
        f.write(binary_data)


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(
        description="将文件夹中的图片转换为二值图像并保存为文本文件"
    )
    parser.add_argument("-d", "--dir", type=str, required=True, help="输入文件夹路径")
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="输出文件夹路径"
    )

    args = parser.parse_args()

    input_dir = args.dir
    output_dir = args.output

    os.makedirs(output_dir, exist_ok=True)

    file_infos: list[tuple[str, str, str]] = [
        (os.path.join(input_dir, filepath), output_dir, filepath)
        for filepath in os.listdir(input_dir)
        if filepath.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    with Pool(processes=cpu_count()) as pool:
        for _result in tqdm(pool.imap(process_file, file_infos), total=len(file_infos)):
            pass


if __name__ == "__main__":
    main()
