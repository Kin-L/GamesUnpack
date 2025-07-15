import subprocess
import os
from PIL import Image
import binascii
from demo.atlas_unpack import split_atlas


def png_convert(file_path, out_path):
    root, name = os.path.split(file_path)
    file_name = os.path.splitext(name)[0]
    subprocess.run([
        r"D:\Program Files (Green)\umodel_win32\umodel_64.exe",
        f"-path={root}",
        "-game=ue4.26",
        "-export",
        f"-out={out_path}",
        file_name
    ])
    try:
        tga = f"{out_path}\\{file_name}.tga"
        png = f"{out_path}\\{file_name}.png"
        img = Image.open(tga)
        img.save(png, "PNG")
        print(f"转换成功: {png}")
        os.remove(tga)
    except Exception as e:
        print(f"转换失败: {e}")


def convert_to_png(input_path, output_path):
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".uexp"):
                out_dir = os.path.join(output_path, root.replace(input_path, "").strip("\\"))
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                png_convert(os.path.join(root, file), out_dir)


def split_and_save(text_data, clean_filename):
    try:
        # 找到文件名.png到最后一个index: -1
        start_png = text_data.find(f'{clean_filename}.png')
        end_atlas = text_data.rfind('index: -1') + len('index: -1')
        atlas_content = text_data[start_png:end_atlas] if start_png != -1 and end_atlas != -1 else ''

        # 找到"{"skeleton":{"hash": 或者带换行的"{\n\"skeleton\": {" 到最后一个 }
        start_json = text_data.find('{\n"skeleton": {')
        if start_json == -1:
            start_json = text_data.find('{"skeleton":{"hash":')  # 修改匹配条件
        end_json = text_data.rfind('}')
        json_content = text_data[start_json:end_json + 1] if start_json != -1 and end_json != -1 else ''
        return atlas_content, json_content
    except Exception as e:
        return False, False  # 表示失败


def convert_spine(input_path, output_path):
    for root, dirs, files in os.walk(input_path):
        for filename in files:
            if filename.endswith(".uexp"):
                if "_a" in filename:
                    continue
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'rb') as file:
                        # 读取文件内容并转换为16进制
                        hex_data = binascii.hexlify(file.read())
                        # 将16进制转换为文本（UTF-8解码，忽略错误）
                        text_data = bytes.fromhex(hex_data.decode('utf-8')).decode('utf-8', errors='ignore')
                except Exception as e:
                    continue
                # 尝试拆分文本并生成atlas和json文件
                original_filename = os.path.splitext(filename)[0]
                clean_filename = original_filename.replace('-atlas', '').replace('-data', '')
                atlas_content, json_content = split_and_save(text_data, clean_filename)
                out_dir = os.path.join(output_path, root.replace(input_path, "").strip("\\"))
                # print(output_path, root, input_path, out_dir)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                # 如果有atlas内容，保存为.atlas文件
                if atlas_content:
                    atlas_filename = f"{clean_filename}.atlas"
                    atlas_path = os.path.join(out_dir, atlas_filename)
                    with open(atlas_path, 'w', encoding='utf-8') as atlas_file:
                        atlas_file.write(atlas_content)

                # 如果有json内容，保存为.json文件
                if json_content:
                    json_filename = f"{clean_filename}.json"
                    json_path = os.path.join(out_dir, json_filename)
                    with open(json_path, 'w', encoding='utf-8') as json_file:
                        json_file.write(json_content)
    convert_to_png(input_path, output_path)
    for root, dirs, files in os.walk(output_path):
        for filename in files:
            if filename.endswith(".atlas"):
                atlas_path = os.path.join(root, filename)
                unitName = os.path.split(filename)[1]
                outputPath = os.path.join(root, 'images')  # sub
                # outputPath = root
                if not os.path.exists(outputPath):
                    os.makedirs(outputPath)
                split_atlas(unitName, output_path=outputPath, atlas_path=atlas_path)

if __name__ == '__main__':
    convert_to_png(r"E:\Unpack\尘白禁区\cache\step1\Game\Content\UI\Picture\DLC28",
                   r"E:\Unpack\尘白禁区\DLC28")
    # convert_spine(r"E:\Unpack\尘白禁区\step1\Game\Content\Plot\CgPlot\Dlc17_plots\PoltAsset\spine",
    #               r"E:\Unpack\尘白禁区\活动界面spine")