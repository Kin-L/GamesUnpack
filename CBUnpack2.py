import os
import shutil
from os import path,makedirs, chdir
import subprocess
from convert import convert_to_png, convert_spine, png_convert


def activity_ui(rootpath):
    _path = r"Game\Content\Plot\CgPlot"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "CgPlot")
    if not path.exists(_p2):
        makedirs(_p2)
    all_entries = os.listdir(_p1)
    # 筛选出目录
    directories = [entry for entry in all_entries if os.path.isdir(os.path.join(_p1, entry))]
    for i in directories:
        pdp1 = path.join(_p1, i)
        pdp2 = path.join(_p2, i)
        if os.path.exists(path.join(pdp1, "PoltAsset")):
            bg_path1 = path.join(pdp1, "PoltAsset", "Bg")
            bg_path2 = path.join(pdp2, "Bg")
            convert_to_png(bg_path1, bg_path2)
            sp_path1 = path.join(pdp1, "PoltAsset", "Spine")
            convert_spine(sp_path1, pdp2)
        else:
            convert_to_png(pdp1, pdp2)
            convert_spine(pdp1, pdp2)


def chara(rootpath):
    _path = r"Game\Content\Spine\Hero"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "Hero")
    if not path.exists(_p2):
        makedirs(_p2)
    all_entries = os.listdir(_p1)
    # 筛选出目录
    directories = [entry for entry in all_entries if os.path.isdir(os.path.join(_p1, entry))]
    for i in directories:
        pdp1 = path.join(_p1, i)
        pdp2 = path.join(_p2, i)
        convert_to_png(pdp1, pdp2)
        convert_spine(pdp1, pdp2)


def ser(rootpath):
    _path = r"Game\Content\UI\Pose\Ser"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "Ser")
    if not path.exists(_p2):
        makedirs(_p2)
    convert_to_png(_p1, _p2)


def fashion(rootpath):
    _path = r"Game\Content\UI\Pose\Fashion"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "Fashion")
    if not path.exists(_p2):
        makedirs(_p2)
    convert_to_png(_p1, _p2)


def dialogue(rootpath):
    _path = r"Game\Content\UI\Picture\Dialogue"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "Dialogue")
    if not path.exists(_p2):
        makedirs(_p2)
    convert_to_png(_p1, _p2)


def bgm(rootpath):
    _path = r"Game\Content\Wwise\Windows"
    _p1 = path.join(rootpath, _path)
    _p2 = path.join(rootpath, "BGM")
    if not path.exists(_p2):
        makedirs(_p2)
    all_entries = os.listdir(_p1)
    # 筛选出目录
    directories = [entry for entry in all_entries if os.path.join(_p1, entry).endswith(".wem")]
    for i in directories:
        pdp1 = path.join(_p1, i)
        pdp2 = path.join(_p2, i)
        shutil.copy(pdp1, pdp2)

    _list = []
    for filename in os.listdir(_p2):
        if ".wem" in filename:
            _list += [filename.removesuffix(".wem")]
    print(_list)
    _path = path.join(rootpath, r"Game\Content\Wwise\Windows\BGM.txt")
    _m3u = open(_path, 'r+', encoding='utf-8')
    _sheet = []
    for _line in _m3u:
        for i in _list:
            if i in _line:
                _sheet += [_line.split("\t")[1] + "\t" +
                      _line.split("\t")[2] + "\t" + _line.split("\t")[2].replace("_", "\t")]
    with open(path.join(rootpath, "sheet.txt"), 'w', encoding='utf-8') as f:
        for i in _sheet:
            f.write(i+"\n")
    for name in _list:
        try:
            # 1. 用 vgmstream 解码为 WAV
            wav_path = path.join(_p2, f"{name}.wav")
            wem_path = path.join(_p2, f"{name}.wem")
            subprocess.run([r"D:\Kin-project\PythonProjects\GamesUnpack\vgmstream-win64\vgmstream-cli.exe", "-o", wav_path, wem_path], check=True)

            # 2. 用 FFmpeg 转 WAV 为 FLAC
            subprocess.run([
                r"D:\Program Files\ffmpeg\ffmpeg.exe",
                "-i", wav_path,
                "-c:a", "flac",
                path.join(_p2, f"{name}.flac")
            ])

        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)
            if os.path.exists(wem_path):
                os.remove(wem_path)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 总体资源提取
    root_path = r"E:\Unpack\尘白禁区\step1"
    activity_ui(root_path)
    bgm(root_path)
    chara(root_path)
    ser(root_path)
    fashion(root_path)
    dialogue(root_path)
