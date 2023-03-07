import os
import urllib
from urllib.parse import unquote

import requests
import json
import re


def download(url, save_path='files'):
    # 匹配文件名的正则表达式
    pattern = r"(?<=/)[^/]+?(?=\?)"
    match = re.search(pattern, url)
    if not match:
        raise BaseException('未匹配到文件名')
    filename = match.group(0)  # 输出：%E5%A4%87%E5%BF%98.pdf

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 使用 unquote() 函数对文件名进行解码
    filename = os.path.join(save_path + '/' + unquote(filename))

    if os.path.exists(filename):
        return filename

    print('下载文件:{}'.format(filename))
    # 发送 GET 请求并下载文件
    response = requests.get(url)
    # 写入文件
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename


def unzip_file(zip_filename: str, extract_dir="."):
    import zipfile

    if not zip_filename.endswith(".zip"):
        return

    # 创建一个 ZipFile 对象，并打开 ZIP 文件
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        # 解压缩所有文件到当前目录
        zip_ref.extractall(extract_dir + "/" + zip_filename[:zip_filename.rfind(".")])

    print(f"文件 {zip_filename} 解压完成")


def replace_wolai_url_to_inner_link(folder_path):
    # 遍历文件夹内的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历所有文件
        for file in files:
            # 如果文件名以 .md 结尾，说明是 Markdown 文件
            if file.endswith(".md"):
                # 读取 Markdown 文件内容
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 匹配包含 https://www.wolai.com/ 的链接格式
                pattern = r"\[([^\]]+)\]\((https://www\.wolai\.com/[^\)]+)\)"

                # 将链接格式替换为指定格式
                new_content = re.sub(pattern, r"[[\1]]", content)

                # 写入修改后的内容
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
