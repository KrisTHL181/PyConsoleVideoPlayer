import os
import argparse
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def process_image(args):
    image_path, output_dir, console_size = args
    try:
        with Image.open(image_path) as img:
            img = img.resize(console_size, Image.LANCZOS)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            img.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Resize images in a directory to console size and save to output directory."
    )
    parser.add_argument(
        "-d", "--dir", type=str, required=True, help="Directory containing images"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output directory to save resized images",
    )
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print(f"Error: Directory {args.dir} does not exist.")
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    console_size = (os.get_terminal_size().columns, os.get_terminal_size().lines)
    print(f"控制台长宽: {console_size}")

    image_paths = [
        os.path.join(args.dir, f)
        for f in os.listdir(args.dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    with Pool(processes=cpu_count()) as pool:
        results = list(
            tqdm(
                pool.imap(
                    process_image,
                    [(img_path, args.output, console_size) for img_path in image_paths],
                ),
                total=len(image_paths),
            )
        )

    print(f"Processed {sum(results)} images successfully.")


if __name__ == "__main__":
    main()
