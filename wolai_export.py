import os
import requests
import json
import re
from util import *

session = requests.session()
session.headers.update({
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://www.wolai.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "wolai-app-version": "1.1.1-19",
    "wolai-client-platform": "web",
    "wolai-client-version": "",
    "wolai-os-platform": "mac",
    "x-client-timeoffset": "-480",
    "x-client-timezone": "Asia/Shanghai"
})
session.cookies.update({
    "token": ""
})


def get_pages():
    result = session.post('https://api.wolai.com/v1/workspace/getWorkspaceData', data={}).json()
    spaceId = result.get('data').get('workspaces')[0].get('id')
    url = "https://api.wolai.com/v1/workspace/getWorkspacePages"
    data = {
        "spaceId": spaceId
    }
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, data=data).json()
    return response


def export_md(page_id, page_title, recover_tree=True, generate_toc="auto", include_subpage=True):
    url = "https://api.wolai.com/v1/exportMarkdown"
    data = {
        "pageId": page_id,
        "pageTitle": page_title,
        "options": {
            "recoverTree": recover_tree,
            "generateToc": generate_toc,
            "includeSubPage": include_subpage
        }
    }
    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, data=data).json()
    print(response)
    url = response.get('data')
    filename = download(url, 'markdown')
    if filename.endswith(".zip"):
        unzip_file(filename)
        os.remove(filename)


def export_pdf(page_id, page_title):
    url = "https://api.wolai.com/v1/puppeteer/export"
    data = {
        "pageId": page_id,
        "exportType": "pdf",
        "theme": "light",
        "os": "mac",
        "options": {
            "scale": 1
        }
    }
    data = json.dumps(data, separators=(',', ':'))
    print(f'正在请求生成pdf:{page_title}')
    response = session.post(url, data=data).json()
    print(response.get('data'))
    url = response.get('data').get('singedUrl')
    download(url, 'pdf')


if __name__ == '__main__':
    result = get_pages()
    blocks = result.get('data').get('blocks')
    for key in blocks:
        block = blocks[key]
        title = block.get('value').get('attributes').get('title')[0][0]
        export_md(key, title)
        export_pdf(key, title)

    replace_wolai_url_to_inner_link('markdown')
