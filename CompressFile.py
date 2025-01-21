import os
import argparse
import random
import struct
from tqdm import tqdm


def binary_text_to_bytes(binary_text: str, chunk_size: int = 16) -> bytes:
    binary_chunks = [
        binary_text[i : i + chunk_size] for i in range(0, len(binary_text), chunk_size)
    ]

    integers = [int(chunk, 2) for chunk in binary_chunks]

    return struct.pack(f">{len(integers)}H", *integers)


def bytes_to_binary_text(binary_data) -> str:
    binary_chunks = [format(byte, "08b") for byte in binary_data]
    binary_text = "".join(binary_chunks)
    return binary_text


def compress_lzw(text: str) -> str:
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    result = []
    current_string = ""

    for char in text:
        new_string = current_string + char
        if new_string in dictionary:
            current_string = new_string
        else:
            result.append(dictionary[current_string])
            dictionary[new_string] = next_code
            next_code += 1
            current_string = char

    if current_string:
        result.append(dictionary[current_string])

    binary_result = "".join(format(code, "016b") for code in result)

    return binary_result


def process_file_lzw(filepath: str, output_dir: str) -> None:
    with open(filepath, "r", encoding="utf-8") as file:
        txt_content = file.read()
    output_filename = os.path.splitext(filepath)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_data = binary_text_to_bytes(compress_lzw(txt_content))

    with open(output_path, "wb") as f:
        f.write(binary_data)


def decompress_lzw(binary_text: str) -> str:
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    result = []
    current_code = int(binary_text[:16], 2)
    result.append(dictionary[current_code])
    previous_string = dictionary[current_code]

    for i in range(16, len(binary_text), 16):
        current_code = int(binary_text[i : i + 16], 2)
        if current_code in dictionary:
            current_string = dictionary[current_code]
        elif current_code == next_code:
            current_string = previous_string + previous_string[0]
        else:
            raise ValueError("Invalid compressed data")

        result.append(current_string)

        dictionary[next_code] = previous_string + current_string[0]
        next_code += 1
        previous_string = current_string

    return "".join(result)


def process_file_lzw_decompress(filepath: str, output_dir: str) -> None:
    with open(filepath, "rb") as file:
        binary_data = file.read()

    output_filename = os.path.splitext(filepath)[0] + ".txt"
    output_path = os.path.join(output_dir, output_filename)

    binary_text = bytes_to_binary_text(binary_data)
    decompressed_text = decompress_lzw(binary_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decompressed_text)


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(
        description="将文件夹中的txt文件使用给定的算法压缩或解压"
    )
    parser.add_argument("-d", "--dir", type=str, required=True, help="输入文件夹路径")
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="输出文件夹路径"
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        choices=["lzw", "lzw_decompress"],
        default="lzw",
        help="选择压缩算法(lzw)或解压缩算法(lzw_decompress)",
    )
    parser.add_argument(
        "-s", "--sample", type=int, default=10, help="压缩率计算样本个数"
    )

    args = parser.parse_args()

    input_dir = args.dir
    output_dir = args.output

    os.makedirs(output_dir, exist_ok=True)

    filelist: list[str] = [
        filepath for filepath in os.listdir(input_dir) if filepath.endswith(".txt")
    ]

    if args.algorithm == "lzw":
        for filepath in tqdm(filelist):
            process_file_lzw(filepath, output_dir)
            compression_ratios: list[float] = []
            sample_size = min(args.sample, len(filelist))  # 默认抽10个样本
            samples = random.sample(filelist, sample_size)

            for sample in samples:
                original_file_path = os.path.join(input_dir, sample)
                compressed_file_path = os.path.join(
                    output_dir, os.path.splitext(sample)[0] + ".txt"
                )

                original_size = os.path.getsize(original_file_path)
                compressed_size = os.path.getsize(compressed_file_path)

                compression_ratio = (
                    (original_size - compressed_size) / original_size * 100
                )
                compression_ratios.append(compression_ratio)

            print(
                f"压缩率: {sum(compression_ratios) / len(compression_ratios) * 100:.3f}%"
            )
    elif args.algorithm == "lzw_decompress":
        for filepath in tqdm(filelist):
            process_file_lzw_decompress(filepath, output_dir)


if __name__ == "__main__":
    main()
