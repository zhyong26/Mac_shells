#!/usr/bin/env python
# coding=utf-8
import requests
import sys
import os

# --- 核心配置 ---
API_URL = "https://your-domain.com/api/v1/upload"  # 替换为你的 API 地址
TOKEN = "your_auth_token_here"                      # 替换为你的 API Token
# ----------------

def upload_for_typora(file_paths):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/json',
        'User-Agent': 'Typora-Uploader'
    }

    urls = []
    
    for path in file_paths:
        if not os.path.isfile(path):
            continue
            
        try:
            with open(path, 'rb') as f:
                files = {'file': (os.path.basename(path), f)}
                response = requests.post(API_URL, headers=headers, files=files, timeout=30)
                
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get('status'):
                        urls.append(res_json['data']['links']['url'])
        except Exception:
            pass

    # 符合 Typora 输出规范
    if urls:
        print("Upload Success:")
        for url in urls:
            print(url)
    else:
        print("Upload Failed")
        sys.exit(1)

if __name__ == "__main__":
    # Typora 会一次性传入一个或多个图片路径作为参数
    image_paths = sys.argv[1:]
    upload_for_typora(image_paths)
