import ffmpeg
import argparse


def extract_audio(video_path, audio_path):
    try:
        # 使用 ffmpeg 提取音频并保存为 WAV 格式
        ffmpeg.input(video_path).output(audio_path).run()
        print(f"音频已成功提取并保存到 {audio_path}")
    except ffmpeg.Error as e:
        print(f"提取音频时出错: {e.stderr.decode()}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="从视频中提取音频并保存为 WAV 文件")

    parser.add_argument("-f", "--file", type=str, required=True, help="视频文件路径")

    parser.add_argument(
        "-o", "--output", type=str, required=True, help="输出音频文件路径"
    )

    args = parser.parse_args()

    extract_audio(args.file, args.output)
