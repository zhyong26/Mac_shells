#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import shutil
from pathlib import Path

# --- 中文分类映射配置 ---
FILE_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic", ".webp", ".raw", ".tiff"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv", ".pptx", ".pages", ".numbers", ".key", ".md"],
    "安装包": [".dmg", ".pkg", ".iso", ".app"],
    "压缩包": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "视频": [".mp4", ".mov", ".webm",".avi", ".mkv", ".wmv", ".flv"],
    "音频": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "电子书": [".epub", ".mobi", ".azw3"],
    "脚本与代码": [".py", ".sh", ".js", ".html", ".css", ".cpp", ".json", ".yaml", ".go", ".rs"],
    "设计工程": [".psd", ".ai", ".sketch", ".fig", ".dwg"]
}

def get_unique_path(path):
    """处理同名文件冲突：若文件已存在，则添加数字后缀"""
    counter = 1
    original_path = path
    while path.exists():
        path = original_path.with_name(f"{original_path.stem}_{counter}{original_path.suffix}")
        counter += 1
    return path

def clean_empty_folders(target_dir, category_names):
    """递归删除空文件夹（自底向上遍历）"""
    print("\n--- 正在清理空文件夹 ---")
    for root, dirs, files in os.walk(target_dir, topdown=False):
        current_path = Path(root)

        # 跳过根目录及预设的分类文件夹
        if current_path == target_dir or current_path.name in category_names:
            continue

        # 检查是否为空目录（排除 macOS 的隐藏文件 .DS_Store）
        items = [i for i in os.listdir(current_path) if i != '.DS_Store']

        if not items:
            try:
                # 删除可能存在的 .DS_Store 随后删除文件夹
                ds_store = current_path / '.DS_Store'
                if ds_store.exists():
                    ds_store.unlink()
                current_path.rmdir()
                print(f"[Deleted] 空文件夹: {current_path.relative_to(target_dir)}")
            except Exception as e:
                print(f"[Error] 无法删除文件夹 {current_path}: {e}")

def organize_folder(target_path_str):
    target_dir = Path(target_path_str).expanduser().resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"错误: 路径 '{target_path_str}' 不存在或不是有效的目录。")
        sys.exit(1)

    # 预设分类文件夹名称集合
    category_names = set(FILE_CATEGORIES.keys())
    category_names.add("其他")

    print(f"开始整理目录: {target_dir}")

    # 第一阶段：移动文件
    for root, dirs, files in os.walk(target_dir):
        current_path = Path(root)

        # 避免进入已经生成的分类文件夹进行扫描
        try:
            relative_parts = current_path.relative_to(target_dir).parts
            if relative_parts and relative_parts[0] in category_names:
                continue
        except ValueError:
            pass

        for file_name in files:
            if file_name.startswith('.'):
                continue

            file_path = current_path / file_name
            file_ext = file_path.suffix.lower()

            target_category = "其他"
            for category, exts in FILE_CATEGORIES.items():
                if file_ext in exts:
                    target_category = category
                    break

            dest_folder = target_dir / target_category
            dest_folder.mkdir(exist_ok=True)

            dest_path = get_unique_path(dest_folder / file_name)
            try:
                shutil.move(str(file_path), str(dest_path))
            except Exception as e:
                print(f"[Error] 移动失败 {file_name}: {e}")

    # 第二阶段：清理空目录
    clean_empty_folders(target_dir, category_names)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 脚本名.py <目标文件夹路径>")
        sys.exit(1)

    organize_folder(sys.argv[1])
    print("\n--- 整理及清理任务执行完毕 ---")
