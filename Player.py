import os
import sys
import time
import argparse
import ctypes
import winsound

if os.name == "nt":

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    def goto(y, x):
        console_handle = ctypes.windll.kernel32.GetStdHandle(-11)

        coord = COORD(x, y)
        ctypes.windll.kernel32.SetConsoleCursorPosition(console_handle, coord)

else:
    import curses

    def goto(y, x):
        curses.setsyx(y, x)


def load_txt_files(directory):
    """加载指定目录下的所有txt文件的内容"""
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                txt_files.append(f"{file.read()}\n")
    return txt_files


def play_txt_files(txt_files, fps, sound):
    """按照指定的帧率逐行打印txt文件的内容"""
    frame_duration = 1 / fps
    total_files = len(txt_files)
    dropped_frames = 0
    estimated_total_time = len(txt_files) / fps
    estimated_finish_time = time.time() + estimated_total_time

    winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    for idx, txt_content in enumerate(txt_files, start=1):
        start_time = time.time()

        sys.stdout.write(txt_content)

        elapsed_time = time.time() - start_time
        if elapsed_time < frame_duration:
            time.sleep(frame_duration - elapsed_time)
        else:
            dropped_frames += 1

        # 打印状态信息
        try:
            real_fps = 1 / elapsed_time
        except ZeroDivisionError:
            real_fps = fps
        remaining_time = estimated_finish_time - time.time()
        sys.stdout.write(
            f"\n{idx}/{total_files} FPS: {real_fps:.2f} (预期FPS: {fps}) DROPS: {dropped_frames} 剩余时间: {remaining_time:.2f}s      "
        )

        # 移动光标到文本起始位置
        goto(0, 0)


def main():
    parser = argparse.ArgumentParser(description="播放文件夹中的txt文件")
    parser.add_argument(
        "-d", "--dir", type=str, required=True, help="txt文件所在的文件夹路径"
    )
    parser.add_argument(
        "-f", "--fps", type=float, required=True, help="播放速度（帧率）"
    )
    parser.add_argument("-m", "--music", type=str, required=True, help="音乐文件路径")

    args = parser.parse_args()
    goto(0, 0)
    sys.stdout.write("加载文件中...\r")
    txt_files = load_txt_files(args.dir)
    play_txt_files(txt_files, args.fps, args.music)


if __name__ == "__main__":
    main()