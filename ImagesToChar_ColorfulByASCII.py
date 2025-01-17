import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

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
        height, width = img_array.shape[0], img_array.shape[1]

        closest_colors = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                pixel = img_array[y, x]
                closest_color_index = find_closest_color(pixel)
                # 检查 closest_color_index 是否在 COLORS 数组中
                if closest_color_index < len(COLORS):
                    closest_colors[y, x] = closest_color_index
                else:
                    # 如果不在，选择一个默认值或者跳过这个像素
                    closest_colors[y, x] = 0  # 示例：选择第

        binary_array = np.vectorize(lambda x: COLOR_TO_LETTER[tuple(COLORS[x])])(
            closest_colors
        )

    return "\n".join("".join(row) for row in binary_array.astype(str))


def process_file(file_info):
    input_path, output_dir, filename = file_info

    output_filename = os.path.splitext(filename)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_data = process_image(input_path)

    with open(output_path, "w") as f:
        f.write(binary_data)


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

    with Pool(processes=cpu_count()) as pool:
        for result in tqdm(pool.imap(process_file, file_infos), total=len(file_infos)):
            pass


if __name__ == "__main__":
    main()
