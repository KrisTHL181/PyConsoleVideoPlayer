import os
import argparse
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def binary_image(arg):
    file_path, output_dir, threshold = arg
    try:
        with Image.open(file_path) as img:
            img = img.convert("L")  # 转换为灰度图像
            binary_img = img.point(lambda p: p > threshold and 255)
            output_path = os.path.join(output_dir, os.path.basename(file_path))
            binary_img.save(output_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_images(dir_path, output_dir, threshold):
    os.makedirs(output_dir, exist_ok=True)

    image_files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    with Pool(processes=cpu_count()) as pool:
        tasks = [(file, output_dir, threshold) for file in image_files]
        for _ in tqdm(pool.imap_unordered(binary_image, tasks), total=len(tasks)):
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Binary images in a directory using a given threshold."
    )
    parser.add_argument(
        "-d", "--dir", type=str, required=True, help="Directory containing images"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output directory for binary images",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=128,
        help="Threshold for binarization (0-255)",
    )

    args = parser.parse_args()
    process_images(args.dir, args.output, args.threshold)
