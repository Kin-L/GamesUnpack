import subprocess
from os import path, remove, walk
import json
from concurrent.futures import ThreadPoolExecutor
from config_manager import ConfigManager
from pathlib import Path

cfg = ConfigManager()
SPINE_EXE = cfg.get("spine_path")
ffm_path = str(cfg.get("ffm_path"))
with open("res/template.export.json", 'r', encoding='utf-8') as f:
    ejtdata = json.load(f)


def exportSpineJson(input_json_path, out_path=None):
    _INPUT_JSON = input_json_path
    Export_JSON = path.splitext(input_json_path)[0] + ".export.json"
    OUTPUT_SPINE = path.splitext(input_json_path)[0] + ".spine"

    cmd = [
        SPINE_EXE,
        "-i", _INPUT_JSON,
        "-o", OUTPUT_SPINE,
        "-r", "cache"
    ]
    try:
        print(f"正在导入 {_INPUT_JSON} 到 Spine 项目...")
        subprocess.run(cmd, check=True)
        print(f"成功创建 Spine 项目: {OUTPUT_SPINE}")
    except subprocess.CalledProcessError as e:
        print(f"导入失败: {e}")
        return
    except Exception as e:
        print(f"发生错误: {e}")
        return

        # 读取JSON文件
    with open(_INPUT_JSON, 'r', encoding='utf-8') as file:
        ijdata = json.load(file)
    ejdata = dict(ejtdata)
    if len(ijdata["animations"]) == 1:
        if out_path:
            _path = path.join(out_path, Path(_INPUT_JSON).name)
        else:
            _path = _INPUT_JSON
        ejdata["output"] = _path.replace(".json", ".mov")
    else:
        if out_path:
            ejdata["output"] = out_path
        else:
            ejdata["output"] = Path(_INPUT_JSON).parent
    ejdata["project"] = OUTPUT_SPINE
    with open(Export_JSON, 'w', encoding='utf-8') as file:
        json.dump(ejdata, file, ensure_ascii=False, indent=4)
    cmd = [
        SPINE_EXE,
        "-e", Export_JSON
    ]
    try:
        print(f"正在渲染导出 {_INPUT_JSON} ...")
        subprocess.run(cmd, check=True)
        print(f"成功导出: {_INPUT_JSON}")
    except subprocess.CalledProcessError as e:
        print(f"导入失败: {e}")
        return
    except Exception as e:
        print(f"发生错误: {e}")
        return
    remove(Export_JSON)
    remove(OUTPUT_SPINE)


def sjemain():
    max_workers = cfg.get("max_workers")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:  # type: ignore
        # 提交所有任务到线程池，并传入索引 i
        futures = [
            executor.submit(exportSpineJson, json_file, None)
            for json_file in cfg.Json_list
        ]

        # 可选：等待所有任务完成（with 语句会自动等待）
        for future in futures:
            future.result()  # 检查是否有异常


# 使用示例
if __name__ == "__main__":
    INPUT_JSON = r"H:\SnowbreakContainmentZone\V3.0.0.130-20250710\UNPAK\out\CgPlot\Dlc18_plots\sp_pic_dlc18_bg001\sp_pic_dlc18_bg001.json"
    exportSpineJson(INPUT_JSON)
    # convert_mov_to_mp4(r"E:\Unpack\尘白禁区\登录界面spine\sp_login_bg019\sp_login_bg019.mov")
