import os
import argparse
import numpy as np
from PIL import Image
from tqdm.contrib.concurrent import process_map
import time

# 定义16种基本颜色
COLORS = np.array(
    [
        [0, 0, 0],
        [255, 255, 255],
        [170, 170, 170],
        [85, 85, 85],
        [254, 0, 0],
        [0, 254, 0],
        [0, 0, 254],
        [254, 254, 0],
        [0, 254, 254],
        [254, 0, 254],
        [170, 0, 0],
        [0, 170, 0],
        [0, 0, 170],
        [170, 170, 0],
        [0, 170, 170],
        [170, 0, 170],
    ]
)

# 定义颜色到字母的映射
COLOR_TO_LETTER = {tuple(color): chr(65 + i) for i, color in enumerate(COLORS)}


def find_closest_color(pixel):
    """找到最接近的16色色彩"""
    distances = np.sum((COLORS[:, None] - pixel) ** 2, axis=2)
    closest_color_index = np.argmin(distances, axis=0)
    return closest_color_index


def process_image(input_path):
    with Image.open(input_path) as img:
        img_array = np.array(img)
        height, width, _ = img_array.shape

        img_array = img_array.reshape(-1, 3)  # 展平图像数组
        closest_color_indices = find_closest_color(img_array)

        binary_array = np.vectorize(lambda x: COLOR_TO_LETTER[tuple(COLORS[x])])(
            closest_color_indices
        )
        binary_array = binary_array.reshape(height, width)

    return "\n".join("".join(row) for row in binary_array.astype(str))


def process_file(file_info):
    input_path, output_dir, filename = file_info

    output_filename = os.path.splitext(filename)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_data = process_image(input_path)

    with open(output_path, "w") as f:
        f.write(binary_data)

    return filename  # 返回文件名用于进度条显示


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="将文件夹中的图片转换为文本文件")
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

    # 使用 process_map 处理多进程任务，并显示进度条
    return process_map(
        process_file, file_infos, max_workers=os.cpu_count(), chunksize=128
    )


if __name__ == "__main__":
    main()
