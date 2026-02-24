#!/usr/bin/env python
# coding=utf-8
import os
import argparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# 阈值常量：200KB
SIZE_THRESHOLD = 200 * 1024

def get_args():
    parser = argparse.ArgumentParser(description="指定 URL 下载页面大图 (自动过滤 <200KB 文件)")
    parser.add_argument("url", help="目标网页的完整 URL")
    default_folder = datetime.now().strftime("%Y%m%d_%H%M%S")
    parser.add_argument("-o", "--output", default=default_folder, help="下载文件夹名称")
    return parser.parse_args()

def download_images(target_url, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": target_url
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"访问页面失败: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    img_urls = list(set([urljoin(target_url, img.get('src') or img.get('data-src'))
                         for img in img_tags if img.get('src') or img.get('data-src')]))

    print(f"目标: {target_url} | 发现链接: {len(img_urls)}")

    with ThreadPoolExecutor(max_workers=8) as executor:
        for i, url in enumerate(img_urls, 1):
            executor.submit(save_and_filter, url, save_folder, headers, i, len(img_urls))

def save_and_filter(url, folder, headers, index, total):
    """下载并过滤小文件"""
    try:
        if url.startswith('data:'): return

        filename = url.split('/')[-1].split('?')[0]
        if not filename: filename = f"img_{index}.jpg"
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            filename += ".jpg"

        path = os.path.join(folder, filename)

        res = requests.get(url, headers=headers, timeout=15, stream=True)
        if res.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)

            # --- 新增：检查文件大小逻辑 ---
            file_size = os.path.getsize(path)
            if file_size < SIZE_THRESHOLD:
                os.remove(path)
                print(f"[{index}/{total}] 跳过/已删除 (过小: {file_size/1024:.1f}KB): {filename}")
            else:
                print(f"[{index}/{total}] 下载成功 ({file_size/1024:.1f}KB): {filename}")
            # ---------------------------

    except Exception as e:
        print(f"下载异常 {url}: {e}")

if __name__ == "__main__":
    args = get_args()
    download_images(args.url, args.output)
