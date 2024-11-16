import ffmpeg
import os
import argparse

# 隐藏ffmpeg欢迎语
os.environ["FFMPEG_HIDE_banner"] = "1"


def get_total_frames(video_file):
    probe = ffmpeg.probe(video_file)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    if video_stream:
        return int(video_stream["nb_frames"])
    return 0


def extract_frames(video_file, output_directory):
    total_frames = get_total_frames(video_file)
    if total_frames == 0:
        raise ValueError("无法获取视频的总帧数")

    # 计算前缀长度
    prefix_length = len(str(total_frames - 1))

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    (
        ffmpeg.input(video_file)
        .output(
            os.path.join(output_directory, f"%0{prefix_length}d.png"),
            hide_banner=None,
        )
        .run()
    )


def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")

    # 添加参数
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Path to the input video file."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        required=True,
        help="Directory to save the extracted frames.",
    )

    # 解析参数
    args = parser.parse_args()

    # 提取视频帧
    extract_frames(args.file, args.directory)


if __name__ == "__main__":
    main()
