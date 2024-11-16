import subprocess


def extract_frames(video_file, output_directory):
    subprocess.run(
        ["python", "ExtractVideo.py", "-f", video_file, "-d", output_directory]
    )


def extract_sound(video, output_file):
    subprocess.run(["python", "ExtractSound.py", "-f", video, "-o", output_file])


def resize_images(input_directory, output_directory):
    subprocess.run(
        ["python", "CompatImageSize.py", "-d", input_directory, "-o", output_directory]
    )


def convert_images_to_text(input_directory, output_directory):
    subprocess.run(
        ["python", "ImagesToChar.py", "-d", input_directory, "-o", output_directory]
    )


def main():
    video_file = input("请输入视频文件名（包括路径）：")
    sound_file = "music.wav"
    frames_directory = "extracted_frames"
    images_directory = "resized_images"
    texts_directory = "text_files"

    extract_sound(video_file, sound_file)
    extract_frames(video_file, frames_directory)
    resize_images(frames_directory, images_directory)
    convert_images_to_text(images_directory, texts_directory)

    print(
        "使用:\npython Player.py -d text_files -f <视频帧率|一般输入60> -m music.wav\n播放视频。"
    )


if __name__ == "__main__":
    main()
