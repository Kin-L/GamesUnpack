import os
import shutil
from os import path,makedirs, chdir
import subprocess
from convert import convert_to_png, convert_spine, png_convert


def activity_ui():
    _path = r"Game\Content\Plot\CgPlot"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    path_out = path.join(unpath_path, "活动界面spine")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            pdp1 = path.join(_p2, i)
            pdp2 = path.join(path_out, i)
            if os.path.exists(path.join(pdp1, "PoltAsset")):
                bg_path1 = path.join(pdp1, "PoltAsset", "Bg")
                bg_path2 = path.join(pdp2, "Bg")
                convert_to_png(bg_path1, bg_path2)
                sp_path1 = path.join(pdp1, "PoltAsset", "Spine")
                convert_spine(sp_path1, pdp2)
            else:
                convert_to_png(pdp1, pdp2)
                convert_spine(pdp1, pdp2)
    _path = r"Game\Content\UI\Picture"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[1]:
        for i in _list[1]:
            if "DLC" in i:
                inp = path.join(_p2, i)
                outp = path.join(path_out, i)
                convert_to_png(inp, outp)


def login_ui():
    path_out = path.join(unpath_path, "登录界面spine")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
    _path = r"Game\Content\Plot\CgPlot\Login_Plots\PoltAsset\Bg"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            if i.endswith(".uexp"):
                png_convert(os.path.join(_p2, i), path_out)

    _path = r"Game\Content\Plot\CgPlot\Login_Plots\PoltAsset\Spine"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            pdp = path.join(_p2, i)
            path_out = path.join(unpath_path, f"登录界面spine\\{i}")
            convert_spine(pdp, path_out)


def ser():
    path_out = path.join(unpath_path, "后勤立绘")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
    _path = r"Game\Content\UI\Pose\Ser"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            if i.endswith(".uexp"):
                png_convert(os.path.join(_p2, i), path_out)


def fashion():
    path_out = path.join(unpath_path, "角色静态立绘")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
    _path = r"Game\Content\UI\Pose\Fashion"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            if i.endswith(".uexp"):
                if "_144" in i:
                    continue
                png_convert(os.path.join(_p2, i), path_out)


def dialogue():
    path_out = path.join(unpath_path, "CGBG")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
    _path = r"Game\Content\UI\Picture\Dialogue"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            if i.endswith(".uexp"):
                png_convert(os.path.join(_p2, i), path_out)


def bgm():
    path_out = path.join(unpath_path, "BGM")
    if not path.exists(path_out):
        makedirs(path_out)
    else:
        shutil.rmtree(path_out)
        makedirs(path_out)
    _path = r"Game\Content\Wwise\Windows"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            if i.endswith(".wem"):
                shutil.copy(os.path.join(_p2, i), path.join(unpath_path, f"BGM\\{i}"))
                ...
    _list = []
    for filename in os.listdir(path_out):
        if ".wem" in filename:
            _list += [filename.removesuffix(".wem")]
    # print(_list)
    _path = path.join(cache_step1_path, r"Game\Content\Wwise\Windows\BGM.txt")
    _m3u = open(_path, 'r+', encoding='utf-8')
    _sheet = []
    for _line in _m3u:
        for i in _list:
            if i in _line:
                _l = _line.split("\t")
                _ = [_l[1], _l[2]]+_l[2].split("_")
                while len(_) <6:
                    _.append("")
                _sheet.append(_)

    # print(_sheet)
    dlcstr = ""
    for i in _sheet:
        if "DLC" in i[3]:
            dlcstr = "BGM_" + i[3] + "_name"
            break
    if dlcstr:
        _path = path.join(cache_step1_path, r"Game\Content\Settings\riki\Riki.txt")
        _txt = open(_path, 'r+', encoding='utf-8')
        _lines1 = []
        for _line in _txt:
            if dlcstr in _line:
                __ = _line.split("\t")
                __ = __[9].split("|")[-1], __[10].split(".")[-1]
                _lines1.append(__)
                # print(__)
        _path = path.join(cache_step1_path, r"Game\Content\Settings\language\riki.txt")
        _txt = open(_path, 'r+', encoding='utf-8')
        _lines2 = []
        for _line in _txt:
            if dlcstr in _line:
                _lines2.append(_line.strip().split("\t"))
                # print(_line.strip().split("\t"))
        lines = []
        linesnum = 0
        for i in _lines2:
            for u in _lines1:
                if i[0] == u[1]:
                    if "DLC" not in u[0]:
                        linesnum += 1
                    lines.append(i+[u[0]])
                    break
        # print(lines)
        _sheetsnum = 0
        for i in _sheet:
            if "Story" == i[3]:
                _sheetsnum += 1
        flag = True if _sheetsnum == linesnum else False
        # print("flag", flag, _sheetsnum, linesnum)
        _n1 = 0
        for n, i in enumerate(_sheet):
            for u in lines:
                if i[3]+"_"+i[4] == u[2]:
                    _sheet[n].extend(["", u[1]])
                    break
            else:
                if flag and i[3] == 'Story':
                    # print(i)
                    _n = int(_n1)
                    for u in lines:
                        if "DLC" not in u[2]:
                            # print(u[2])
                            if not _n:
                                _n1 += 1
                                _sheet[n].extend(["", u[1]])
                                break
                            else:
                                _n -= 1
    with open(path.join(unpath_path, f"BGM\\sheet.txt"), 'w', encoding='utf-8') as f:
        for i in _sheet:
            f.write("\t".join(i) + "\n")
        # print(_sheet)
        cnnali = [i[7] if len(i) == 8 else "" for i in _sheet]
        # print(cnnali)
        for name in _list:

            try:
                # 1. 用 vgmstream 解码为 WAV
                wav_path = path.join(path_out, f"{name}.wav")
                wem_path = path.join(path_out, f"{name}.wem")
                subprocess.run(
                    [r"D:\Kin-project\PythonProjects\GamesUnpack\vgmstream-win64\vgmstream-cli.exe", "-o", wav_path,
                     wem_path], check=True)
                for i in _sheet:
                    if name == i[0]:
                        cnna = i[7] if len(i) == 8 else ""
                        if cnna and cnnali.count(cnna) == 1:
                            name = f"{cnna} - 尘白禁区"
                            print(name)
                            break
                # 2. 用 FFmpeg 转 WAV 为 FLAC
                subprocess.run([
                    r"D:\Program Files\ffmpeg\ffmpeg.exe",
                    "-i", wav_path,
                    "-c:a", "flac",
                    path.join(path_out, f"{name}.flac")
                ])

            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                if os.path.exists(wem_path):
                    os.remove(wem_path)


def chara():
    path_out = path.join(unpath_path, "角色立绘spine")
    if not path.exists(path_out):
        makedirs(path_out)
    _path = r"Game\Content\Spine\Hero"
    _p1 = path.join(step1_path, _path)
    _p2 = path.join(cache_step1_path, _path)
    _list = compare_folders_by_name(_p1, _p2)
    if _list[0]:
        print(f"删除：{_list[0]}")
    if _list[1]:
        for i in _list[1]:
            pdp = path.join(_p2, i)
            path_out = path.join(unpath_path, f"角色立绘spine\\{i}")
            convert_spine(pdp, path_out)


def compare_folders_by_name(dir1, dir2):
    """对比两个文件夹中的文件名差异"""
    # 获取两个文件夹中的文件列表
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))

    # 找出差异
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    common_files = files1 & files2
    return [only_in_dir1, only_in_dir2, common_files]


def SnowUnpack():
    subprocess.run(".\\quickbms_4gb_files.exe "
                   "-o -F \"{}.pak\" "
                   ".\\unreal_tournament_4_0.4.27e_snowbreak.bms "
                   f"\"{cbcz_paks_path}\" "
                   f"\"{quickbms_outpath}\"")


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    quickbms_path = r"D:\Program Files (Green)\quickbms"
    work_path = os.getcwd()
    chdir(quickbms_path)
    cbcz_paks_path = r"D:\Program Files\Snow\data\game\Game\Content\Paks"
    unpath_path = r"E:\Unpack\尘白禁区"
    cache_step1_path = path.join(unpath_path, "cache\\step1")
    step1_path = path.join(unpath_path, "step1")
    if not path.exists(cache_step1_path):
        makedirs(cache_step1_path)
    if len(os.listdir(path.join(unpath_path, "step1"))) == 0:
        quickbms_outpath = step1_path
        _first_flag = True
    else:
        quickbms_outpath = cache_step1_path
        _first_flag = False
    # SnowUnpack()
    asset_path_list = [r"Game\Content\Plot\CgPlot",
                       r"Game\Content\Plot\CgPlot\Login_Plots\PoltAsset",
                       r"Game\Content\Spine\Hero",
                       r"Game\Content\UI\Picture\Dialogue",
                       r"Game\Content\UI\Pose\Fashion",
                       r"Game\Content\UI\Pose\Ser",
                       r"Game\Content\Wwise\Windows"]

    if not _first_flag:
        #  活动界面spine
        activity_ui()
        # login_ui()
        # fashion()
        # dialogue()
        # ser()
        # bgm()
        # chara()

