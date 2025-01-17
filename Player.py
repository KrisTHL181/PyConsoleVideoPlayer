import os
import sys
import time
import argparse
from PyScreenUtils.cursor_util import goto  # type: ignore
import winsound
import keyboard  # 引入keyboard库
import colorama

colorama.just_fix_windows_console()

colorama_colors = {
    "A": colorama.Fore.BLACK,
    "B": colorama.Fore.WHITE,
    "C": colorama.Fore.LIGHTBLACK_EX,
    "D": colorama.Fore.LIGHTBLACK_EX,
    "E": colorama.Fore.RED,
    "F": colorama.Fore.GREEN,
    "G": colorama.Fore.BLUE,
    "H": colorama.Fore.YELLOW,
    "I": colorama.Fore.CYAN,
    "J": colorama.Fore.MAGENTA,
    "K": colorama.Fore.RED,
    "L": colorama.Fore.GREEN,
    "M": colorama.Fore.BLUE,
    "N": colorama.Fore.YELLOW,
    "O": colorama.Fore.CYAN,
    "P": colorama.Fore.MAGENTA,
}


def load_txt_files(directory: str, color: bool = False) -> list[str]:
    """加载指定目录下的所有txt文件的内容"""
    txt_files: list[str] = []
    if not color:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(
                    os.path.join(directory, filename), "r", encoding="utf-8"
                ) as file:
                    txt_files.append(f"{file.read()}\n")
        return txt_files

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                data = file.read()
            for key, value in colorama_colors.items():
                data = data.replace(key, value + "0")
            txt_files.append(f"{data}{colorama.Style.RESET_ALL}\n")
    return txt_files


def play_txt_files(txt_files: list[str], fps: int, sound: str):
    """按照指定的帧率逐行打印txt文件的内容"""
    frame_duration = 1 / fps
    total_files = len(txt_files)
    dropped_frames = 0
    estimated_total_time = len(txt_files) / fps
    estimated_finish_time = time.time() + estimated_total_time

    winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    idx = 0
    paused = False

    while idx < total_files:
        if not paused:
            txt_content = txt_files[idx]
            start_time = time.time()

            sys.stdout.write(txt_content)

            elapsed_time = time.time() - start_time
            if elapsed_time < frame_duration:
                time.sleep(frame_duration - elapsed_time)
            else:
                dropped_frames += 1
                idx += 1

            sys.stderr.write(
                f"\n{idx + 1}/{total_files}({((idx+1)/total_files)*100:.2f}%) FPS: {min(1 / max(elapsed_time, frame_duration), fps):.2f} (预期FPS: {fps}) DROPS: {dropped_frames} 剩余时间: {estimated_finish_time - time.time():.2f}s      "
            )

            goto(0, 0)

        if keyboard.is_pressed("left"):
            if idx > 0:
                idx -= 1
                continue
            else:
                idx = 0

        if keyboard.is_pressed("right"):
            if idx < total_files - 1:
                idx += 3
                continue
            else:
                idx = total_files - 1

        if keyboard.is_pressed("space"):
            paused = not paused
            goto(0, 0)
            sys.stderr.write("已暂停\r")
            while keyboard.is_pressed("space"):
                time.sleep(0.01)

        if not paused:
            idx += 1


def main():
    parser = argparse.ArgumentParser(description="播放文件夹中的txt文件")
    parser.add_argument(
        "-d", "--dir", type=str, required=True, help="txt文件所在的文件夹路径"
    )
    parser.add_argument(
        "-f", "--fps", type=float, required=True, help="播放速度（帧率）"
    )
    parser.add_argument("-m", "--music", type=str, required=True, help="音乐文件路径")
    parser.add_argument(
        "-a", "--ascii", action="store_true", required=False, help="使用ASCII颜色"
    )

    args = parser.parse_args()
    goto(0, 0)
    sys.stdout.write("加载文件中...\r")

    txt_files = load_txt_files(args.dir, color=args.ascii)
    play_txt_files(txt_files, args.fps, args.music)


if __name__ == "__main__":
    main()
