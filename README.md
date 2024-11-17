# PyConsoleVideoPlayer

Python控制台视频播放器。

首先使用ExtractVideo提出视频的所有帧，然后使用CompatImageSize.py将图像缩放到控制台大小，再使用BinaryFiles.py对图像进行二值化，最后使用ImagesToChar.py将图像转换为文本。

（或不使用二值化，使用ImagesToChar_Colorful.py生成具有颜色风格的文本。）

然后使用Player.py播放！

## 前置条件

* Python 3
* FFmpeg
* Pillow
* Numpy
* tqdm
* Windows操作系统（由于使用了 `winsound`模块）

## 运行方法

1. 使用 `ExtractVideo.py`从视频文件中提取所有帧。
2. 使用 `CompatImageSize.py`将所有图像缩放到控制台大小。
3. 使用 `ImagesToChar.py`将所有图像转换为二值图像并保存为文本文件。
4. 使用 `Player.py`播放文本文件。
