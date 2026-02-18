#!/usr/bin/env python
# coding=utf-8
import requests
import sys
import os
import pyperclip  # 引入剪切板库

# ============================================
# --- 配置区 (请在此处修改为你的信息) ---
# 1. 你的图床 API 地址，必须以 /api/v1/upload 结尾
API_URL = "https://your-domain.com/api/v1/upload"

# 2. 你的 API Token (在个人中心 -> 令牌管理中获取)
# 注意：Token 通常是一长串字符，有时包含开头的数字和竖线，请完整复制。
TOKEN = "your_auth_token_here"
# ============================================

def upload_to_lsky(file_path):
    # 1. 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"❌ 错误: 找不到文件 '{file_path}'")
        return

    print(f"正在上传: {os.path.basename(file_path)} ...")

    # 2. 构造请求头 (使用 Bearer Token 鉴权)
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/json',
        # 伪装 User-Agent 防止部分防火墙拦截
        'User-Agent': 'Mozilla/5.0 (Python Lsky Uploader)'
    }

    try:
        # 3. 读取文件并准备上传
        # 使用 'rb' 模式读取二进制流
        with open(file_path, 'rb') as f:
            # 构造 multipart/form-data 表单，字段名为 'file'
            files = {
                'file': (os.path.basename(file_path), f)
            }

            # 4. 发送 POST 请求
            # 设置 timeout 防止网络卡死
            response = requests.post(API_URL, headers=headers, files=files, timeout=30)

            # 5. 处理响应
            if response.status_code == 200:
                res_data = response.json()
                # 再次确认 API 返回的状态也是 true
                if res_data.get('status'):
                    # 提取 URL
                    img_url = res_data['data']['links']['url']

                    # ---> 核心步骤：复制到剪切板 <---
                    pyperclip.copy(img_url)

                    print(f"✅ 上传成功！")
                    print(f"🔗 URL: {img_url}")
                    print("📋 状态: 链接已自动复制到剪切板，直接粘贴即可！")
                else:
                    print(f"❌ 上传失败 (API拒绝): {res_data.get('message')}")
            elif response.status_code == 401:
                 print("❌ 认证失败：Token 无效或已过期，请检查配置。")
            else:
                print(f"❌ 网络请求失败 | HTTP 状态码: {response.status_code}")
                # 调试时可取消下面注释查看详细信息
                # print(f"响应内容: {response.text}")

    except Exception as e:
        print(f"❌ 程序运行异常: {str(e)}")

# 主程序入口
if __name__ == "__main__":
    # 检查命令行参数是否足够
    if len(sys.argv) < 2:
        print("使用方法错误。")
        print("正确用法: python upload.py <本地图片路径>")
        print("示例: python upload.py screenshot.png")
    else:
        # 获取命令行传入的第一个参数作为文件路径
        target_file = sys.argv[1]
        upload_to_lsky(target_file)
